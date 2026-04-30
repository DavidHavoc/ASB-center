import re

import frappe
from frappe import _
from frappe.utils import now_datetime


MONTH_PATTERN = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


def _validate_month(summary_month):
	if not summary_month or not MONTH_PATTERN.match(summary_month):
		frappe.throw(_("Month must be in YYYY-MM format."))


def _summary_name(specialist, summary_month):
	return frappe.db.get_value(
		"Specialist Monthly Service Summary",
		{"specialist": specialist, "summary_month": summary_month},
		"name",
	)


def rebuild_specialist_monthly_summary(specialist, summary_month):
	if not specialist or not summary_month:
		return {}

	if not frappe.db.exists("DocType", "Specialist Monthly Service Summary"):
		return {}

	_validate_month(summary_month)

	aggregate = frappe.db.sql(
		"""
		select
			count(*) as total_rows,
			coalesce(sum(case when status = 'Completed' then 1 else 0 end), 0) as completed_visits,
			coalesce(sum(case when status = 'Completed' then service_units else 0 end), 0) as total_service_units,
			coalesce(sum(case when status = 'Completed' then duration_minutes else 0 end), 0) as total_duration_minutes,
			count(distinct case when status = 'Completed' then beneficiary end) as unique_beneficiaries,
			coalesce(sum(case when status = 'No Show' then 1 else 0 end), 0) as no_show_count,
			coalesce(sum(case when status = 'Cancelled' then 1 else 0 end), 0) as cancelled_count
		from `tabService Visit`
		where specialist = %s and visit_month = %s
		""",
		(specialist, summary_month),
		as_dict=True,
	)[0]

	existing_name = _summary_name(specialist, summary_month)
	if not aggregate.total_rows:
		if existing_name:
			frappe.delete_doc(
				"Specialist Monthly Service Summary",
				existing_name,
				force=1,
				ignore_permissions=True,
			)
		return {}

	center = frappe.db.get_value("Employee", specialist, "asb_center")
	payload = {
		"specialist": specialist,
		"center": center,
		"summary_month": summary_month,
		"completed_visits": int(aggregate.completed_visits or 0),
		"total_service_units": float(aggregate.total_service_units or 0),
		"total_duration_minutes": int(aggregate.total_duration_minutes or 0),
		"unique_beneficiaries": int(aggregate.unique_beneficiaries or 0),
		"no_show_count": int(aggregate.no_show_count or 0),
		"cancelled_count": int(aggregate.cancelled_count or 0),
		"last_rebuilt_on": now_datetime(),
	}

	if existing_name:
		doc = frappe.get_doc("Specialist Monthly Service Summary", existing_name)
		doc.update(payload)
		doc.save(ignore_permissions=True)
	else:
		doc = frappe.get_doc(
			{
				"doctype": "Specialist Monthly Service Summary",
				**payload,
			}
		)
		doc.insert(ignore_permissions=True)

	return payload


def on_service_visit_change(doc, method=None):
	affected_pairs = {(doc.specialist, doc.visit_month)}

	if method == "on_update":
		previous_doc = doc.get_doc_before_save()
		if previous_doc:
			affected_pairs.add((previous_doc.specialist, previous_doc.visit_month))

	for specialist, summary_month in affected_pairs:
		if specialist and summary_month:
			rebuild_specialist_monthly_summary(specialist, summary_month)


@frappe.whitelist()
def get_specialist_monthly_totals(specialist=None, summary_month=None, center=None):
	filters = {}
	if specialist:
		filters["specialist"] = specialist
	if summary_month:
		_validate_month(summary_month)
		filters["summary_month"] = summary_month
	if center:
		filters["center"] = center

	return frappe.get_list(
		"Specialist Monthly Service Summary",
		filters=filters,
		fields=[
			"name",
			"specialist",
			"center",
			"summary_month",
			"completed_visits",
			"total_service_units",
			"total_duration_minutes",
			"unique_beneficiaries",
			"no_show_count",
			"cancelled_count",
			"last_rebuilt_on",
		],
		order_by="summary_month desc, specialist asc",
	)


def rebuild_all_specialist_monthly_summaries():
	if not frappe.db.exists("DocType", "Specialist Monthly Service Summary"):
		return

	pairs = frappe.db.sql(
		"""
		select distinct specialist, visit_month
		from `tabService Visit`
		where ifnull(specialist, '') != '' and ifnull(visit_month, '') != ''
		""",
		as_dict=True,
	)
	valid_pairs = {(row.specialist, row.visit_month) for row in pairs}

	for specialist, summary_month in valid_pairs:
		rebuild_specialist_monthly_summary(specialist, summary_month)

	existing = frappe.get_all(
		"Specialist Monthly Service Summary",
		fields=["name", "specialist", "summary_month"],
	)
	for row in existing:
		if (row.specialist, row.summary_month) not in valid_pairs:
			frappe.delete_doc(
				"Specialist Monthly Service Summary",
				row.name,
				force=1,
				ignore_permissions=True,
			)
