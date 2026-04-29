# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe


BASE_ROLES = (
	{"role_name": "ASB Center Coordinator", "desk_access": 1},
	{"role_name": "ASB Specialist", "desk_access": 1},
)


def execute():
	for role in BASE_ROLES:
		if frappe.db.exists("Role", role["role_name"]):
			continue

		frappe.get_doc(
			{
				"doctype": "Role",
				"role_name": role["role_name"],
				"desk_access": role["desk_access"],
			}
		).insert(ignore_permissions=True)
