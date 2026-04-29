# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe


def execute():
	home_page = "/app/asb-center-home"
	for role_name in ("ASB Specialist", "ASB Center Coordinator"):
		if frappe.db.exists("Role", role_name):
			frappe.db.set_value("Role", role_name, "home_page", home_page, update_modified=False)
