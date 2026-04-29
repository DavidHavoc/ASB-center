# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import re

import frappe
from frappe import _
from frappe.model.document import Document


MONTH_PATTERN = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


class SpecialistMonthlyServiceSummary(Document):
	def validate(self):
		self._validate_month()
		self._set_center_from_specialist()
		self._validate_unique_summary()
		self._validate_non_negative_totals()

	def _validate_month(self):
		if not self.summary_month or not MONTH_PATTERN.match(self.summary_month):
			frappe.throw(_("Summary Month must be in YYYY-MM format."))

	def _set_center_from_specialist(self):
		if not self.specialist:
			return

		employee_center = frappe.db.get_value("Employee", self.specialist, "asb_center")
		if employee_center and not self.center:
			self.center = employee_center

		if employee_center and self.center and self.center != employee_center:
			frappe.throw(_("Summary Center must match the Specialist's Center."))

	def _validate_unique_summary(self):
		duplicate = frappe.db.exists(
			"Specialist Monthly Service Summary",
			{
				"specialist": self.specialist,
				"summary_month": self.summary_month,
				"name": ["!=", self.name or ""],
			},
		)
		if duplicate:
			frappe.throw(_("A monthly summary already exists for this Specialist and Month."))

	def _validate_non_negative_totals(self):
		for fieldname in (
			"completed_visits",
			"total_service_units",
			"total_duration_minutes",
			"unique_beneficiaries",
			"no_show_count",
			"cancelled_count",
		):
			if (self.get(fieldname) or 0) < 0:
				frappe.throw(_("{0} cannot be negative.").format(frappe.bold(self.meta.get_label(fieldname))))
