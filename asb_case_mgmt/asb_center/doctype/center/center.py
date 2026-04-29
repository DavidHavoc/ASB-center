# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import validate_email_address, validate_phone_number


class Center(Document):
	def validate(self):
		self.center_name = (self.center_name or "").strip()
		self.address = (self.address or "").strip()
		self.description = (self.description or "").strip()
		self.phone = (self.phone or "").strip()
		self.email = (self.email or "").strip().lower()

		if not self.naming_series:
			self.naming_series = "CTR-.YYYY.-.#####"

		if self.email:
			validate_email_address(self.email, throw=True)

		if self.phone and not validate_phone_number(self.phone):
			frappe.throw(_("Phone number is invalid: {0}").format(frappe.bold(self.phone)))
