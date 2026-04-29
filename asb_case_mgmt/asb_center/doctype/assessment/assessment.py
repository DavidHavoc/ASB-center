# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate

from asb_case_mgmt.asb_center.utils import get_beneficiary_center, is_specialist_assigned_to_beneficiary


class Assessment(Document):
	def validate(self):
		self._normalize_fields()
		self._set_center_from_beneficiary()
		self._validate_specialist_assignment()
		self._validate_assessment_timeline()
		self._set_assessment_cycle_number()
		self._validate_domain_tracking()
		self._validate_scores()

	def _normalize_fields(self):
		self.progress_summary = (self.progress_summary or "").strip()
		self.recommendations = (self.recommendations or "").strip()
		self.notes = (self.notes or "").strip()
		if self.assessment_type == "Initial":
			self.previous_assessment = None

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
				_("Assessment center must match Beneficiary center: {0}.").format(
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

	def _validate_assessment_timeline(self):
		if self.next_review_date and self.assessment_date:
			if getdate(self.next_review_date) < getdate(self.assessment_date):
				frappe.throw(_("Next Review Date cannot be before Assessment Date."))

		if self.assessment_type in ("Repeated", "Final"):
			if not self.previous_assessment:
				frappe.throw(
					_("Previous Assessment is required for {0} assessments.").format(
						frappe.bold(self.assessment_type)
					)
				)

			if self.previous_assessment == self.name:
				frappe.throw(_("Previous Assessment cannot reference the current Assessment."))

			existing_count = frappe.db.count(
				"Assessment",
				filters={
					"beneficiary": self.beneficiary,
					"name": ["!=", self.name or ""],
				},
			)
			if existing_count < 1:
				frappe.throw(
					_("A {0} assessment requires at least one previous assessment.").format(
						frappe.bold(self.assessment_type)
					)
				)

			previous = frappe.db.get_value(
				"Assessment",
				self.previous_assessment,
				["beneficiary", "assessment_date"],
				as_dict=True,
			)
			if not previous:
				frappe.throw(_("Previous Assessment {0} does not exist.").format(frappe.bold(self.previous_assessment)))

			if previous.beneficiary != self.beneficiary:
				frappe.throw(_("Previous Assessment must belong to the same Beneficiary."))

			if self.assessment_date and previous.assessment_date and getdate(previous.assessment_date) > getdate(
				self.assessment_date
			):
				frappe.throw(_("Previous Assessment date cannot be after the current Assessment date."))

	def _set_assessment_cycle_number(self):
		if not self.beneficiary or not self.assessment_date:
			self.assessment_cycle_number = None
			return

		previous_count = frappe.db.count(
			"Assessment",
			filters={
				"beneficiary": self.beneficiary,
				"name": ["!=", self.name or ""],
				"assessment_date": ["<=", self.assessment_date],
			},
		)
		self.assessment_cycle_number = previous_count + 1

	def _validate_domain_tracking(self):
		if not self.domain_scores:
			frappe.throw(_("At least one Domain Score row is required."))

	def _validate_scores(self):
		if (self.total_score or 0) < 0:
			frappe.throw(_("Total Score cannot be negative."))

		if (self.service_schedule_count or 0) < 0:
			frappe.throw(_("Service Delivery Schedule Count cannot be negative."))
