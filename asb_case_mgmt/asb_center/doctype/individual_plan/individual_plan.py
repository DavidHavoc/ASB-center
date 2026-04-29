# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate

from asb_case_mgmt.asb_center.utils import get_beneficiary_center, is_specialist_assigned_to_beneficiary


class IndividualPlan(Document):
	def validate(self):
		self._normalize_fields()
		self._set_center_from_beneficiary()
		self._validate_specialist_assignment()
		self._validate_dates()
		self._validate_goals()

	def _normalize_fields(self):
		self.notes = (self.notes or "").strip()

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
				_("Individual Plan center must match Beneficiary center: {0}.").format(
					frappe.bold(beneficiary_center)
				)
			)

	def _validate_specialist_assignment(self):
		if not self.beneficiary or not self.specialist:
			return

		if not is_specialist_assigned_to_beneficiary(self.beneficiary, self.specialist):
			frappe.throw(
				_("Specialist {0} is not assigned to Beneficiary {1}.").format(
					frappe.bold(self.specialist), frappe.bold(self.beneficiary)
				)
			)

	def _validate_dates(self):
		if self.plan_end_date and self.plan_start_date:
			if getdate(self.plan_end_date) < getdate(self.plan_start_date):
				frappe.throw(_("Plan End Date cannot be before Plan Start Date."))

	def _validate_goals(self):
		if self.status in ("Active", "Completed") and not self.goals:
			frappe.throw(_("At least one goal is required when the plan is Active or Completed."))
