# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	custom_fields = {
		"Employee": [
			{
				"fieldname": "asb_section",
				"fieldtype": "Section Break",
				"label": "ASB Case Management",
				"insert_after": "date_of_joining",
				"collapsible": 1,
			},
			{
				"fieldname": "asb_center",
				"fieldtype": "Link",
				"label": "Center",
				"options": "Center",
				"insert_after": "asb_section",
				"in_standard_filter": 1,
			},
			{
				"fieldname": "asb_contract_number",
				"fieldtype": "Data",
				"label": "Contract Number",
				"insert_after": "asb_center",
			},
			{
				"fieldname": "asb_contract_start_date",
				"fieldtype": "Date",
				"label": "Contract Start Date",
				"insert_after": "asb_contract_number",
			},
			{
				"fieldname": "asb_contract_end_date",
				"fieldtype": "Date",
				"label": "Contract End Date",
				"insert_after": "asb_contract_start_date",
			},
			{
				"fieldname": "asb_contract_attachment",
				"fieldtype": "Attach",
				"label": "Contract Attachment",
				"insert_after": "asb_contract_end_date",
			},
		]
	}

	create_custom_fields(custom_fields, update=True)

	role_home_pages = {
		"ASB Specialist": "/app/asb-center-home",
		"ASB Center Coordinator": "/app/asb-center-home",
	}

	for role_name, home_page in role_home_pages.items():
		if frappe.db.exists("Role", role_name):
			frappe.db.set_value("Role", role_name, "home_page", home_page, update_modified=False)
