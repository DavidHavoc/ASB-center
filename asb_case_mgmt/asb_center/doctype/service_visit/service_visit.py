# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate

from asb_case_mgmt.asb_center.utils import get_beneficiary_center, is_specialist_assigned_to_beneficiary


class ServiceVisit(Document):
	def validate(self):
		self._normalize_fields()
		self._set_center_from_beneficiary()
		self._set_visit_month()
		self._validate_service_units()
		self._validate_specialist_assignment()

	def _normalize_fields(self):
		self.notes = (self.notes or "").strip()
		if self.service_units is None:
			self.service_units = 1

	def _set_center_from_beneficiary(self):
		if not self.beneficiary:
			return

		beneficiary_center = get_beneficiary_center(self.beneficiary)
		if not beneficiary_center:
			frappe.throw(
				_("Beneficiary {0} does not have a linked Center.").format(frappe.bold(self.beneficiary))
			)

		if not self.center:
			self.center = beneficiary_center
		elif self.center != beneficiary_center:
			frappe.throw(
				_("Service Visit center must match Beneficiary center: {0}.").format(
					frappe.bold(beneficiary_center)
				)
			)

	def _set_visit_month(self):
		if not self.visit_date:
			self.visit_month = None
			return

		visit_date = getdate(self.visit_date)
		self.visit_month = f"{visit_date.year:04d}-{visit_date.month:02d}"

	def _validate_service_units(self):
		if self.status == "Cancelled":
			self.service_units = 0

		if (self.service_units or 0) < 0:
			frappe.throw(_("Service Units cannot be negative."))

	def _validate_specialist_assignment(self):
		if not self.beneficiary or not self.specialist:
			return

		if not is_specialist_assigned_to_beneficiary(self.beneficiary, self.specialist):
			frappe.throw(
				_("Specialist {0} is not assigned to Beneficiary {1}.").format(
					frappe.bold(self.specialist), frappe.bold(self.beneficiary)
				)
			)


@frappe.whitelist()
def get_monthly_visit_count(beneficiary, month=None):
	if not beneficiary:
		return 0

	filters = {
		"beneficiary": beneficiary,
		"status": "Completed",
	}
	if month:
		filters["visit_month"] = month

	return frappe.db.count("Service Visit", filters=filters)


@frappe.whitelist()
def get_specialist_monthly_service_units(specialist, month):
	if not specialist or not month:
		frappe.throw(_("Both Specialist and Month are required."))

	from asb_case_mgmt.payroll import rebuild_specialist_monthly_summary

	summary = rebuild_specialist_monthly_summary(specialist, month)
	if not summary:
		return 0

	return summary.get("total_service_units") or 0
