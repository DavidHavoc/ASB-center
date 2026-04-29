# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import getdate, today, validate_email_address, validate_phone_number


class Beneficiary(Document):
	def autoname(self):
		if not self.beneficiary_code:
			self.beneficiary_code = make_autoname("BEN-.YYYY.-.#####")

	def validate(self):
		self._normalize_text_fields()
		self._set_age_fields()
		self._validate_contact_fields()
		self._validate_dates()
		self._validate_specialist_rows()

	def _normalize_text_fields(self):
		self.full_name = (self.full_name or "").strip()
		self.beneficiary_code = (self.beneficiary_code or "").strip().upper()
		self.personal_id = (self.personal_id or "").strip()
		self.region = (self.region or "").strip()
		self.municipality = (self.municipality or "").strip()
		self.guardian_parent = (self.guardian_parent or "").strip()
		self.phone = (self.phone or "").strip()
		self.email = (self.email or "").strip().lower()
		self.application_contract_number = (self.application_contract_number or "").strip()

	def _set_age_fields(self):
		if not self.birth_date:
			self.age = None
			self.age_category = None
			return

		birth_date = getdate(self.birth_date)
		current_date = getdate(today())
		age = current_date.year - birth_date.year - (
			(current_date.month, current_date.day) < (birth_date.month, birth_date.day)
		)
		self.age = max(age, 0)

		if self.age < 6:
			self.age_category = "Early Childhood"
		elif self.age < 18:
			self.age_category = "Child/Adolescent"
		elif self.age < 60:
			self.age_category = "Adult"
		else:
			self.age_category = "Senior"

	def _validate_contact_fields(self):
		if self.email:
			validate_email_address(self.email, throw=True)

		if self.phone and not validate_phone_number(self.phone):
			frappe.throw(_("Phone number is invalid: {0}").format(frappe.bold(self.phone)))

	def _validate_dates(self):
		if self.birth_date and getdate(self.birth_date) > getdate(today()):
			frappe.throw(_("Birth Date cannot be in the future."))

		if self.exit_date and self.enrollment_date and getdate(self.exit_date) < getdate(self.enrollment_date):
			frappe.throw(_("Exit Date cannot be before Enrollment Date."))

		if (
			self.first_service_date
			and self.enrollment_date
			and getdate(self.first_service_date) < getdate(self.enrollment_date)
		):
			frappe.throw(_("First Service Date cannot be before Enrollment Date."))

	def _validate_specialist_rows(self):
		seen = set()

		for row in self.responsible_specialists or []:
			if row.specialist in seen:
				frappe.throw(
					_("Specialist {0} is assigned more than once.").format(frappe.bold(row.specialist))
				)
			seen.add(row.specialist)

			employee_center = frappe.db.get_value("Employee", row.specialist, "asb_center")
			if self.center and employee_center and employee_center != self.center:
				frappe.throw(
					_("Specialist {0} is linked to Center {1}, not {2}.").format(
						frappe.bold(row.specialist),
						frappe.bold(employee_center),
						frappe.bold(self.center),
					)
				)
