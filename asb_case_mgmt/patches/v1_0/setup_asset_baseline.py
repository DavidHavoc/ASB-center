# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


ASSET_CATEGORY_MAP = {
	"ASB Assistive Devices": "Office Equipments - ASB",
	"ASB IT Equipment": "Electronic Equipments - ASB",
	"ASB Facility Assets": "Furnitures and Fixtures - ASB",
}



def execute():
	_setup_custom_fields()
	_setup_center_locations()
	_setup_asset_categories()



def _setup_custom_fields():
	custom_fields = {
		"Location": [
			{
				"fieldname": "asb_center",
				"fieldtype": "Link",
				"label": "ASB Center",
				"options": "Center",
				"insert_after": "location_name",
				"in_standard_filter": 1,
			},
		],
		"Asset": [
			{
				"fieldname": "asb_center",
				"fieldtype": "Link",
				"label": "ASB Center",
				"options": "Center",
				"insert_after": "location",
				"in_standard_filter": 1,
			},
			{
				"fieldname": "asb_beneficiary",
				"fieldtype": "Link",
				"label": "Beneficiary",
				"options": "Beneficiary",
				"insert_after": "asb_center",
			},
			{
				"fieldname": "asb_maintenance_frequency_months",
				"fieldtype": "Int",
				"label": "Maintenance Frequency (Months)",
				"insert_after": "maintenance_required",
			},
			{
				"fieldname": "asb_next_maintenance_date",
				"fieldtype": "Date",
				"label": "Next Maintenance Date",
				"insert_after": "asb_maintenance_frequency_months",
			},
		],
	}
	create_custom_fields(custom_fields, update=True)



def _setup_center_locations():
	centers = frappe.get_all("Center", fields=["name", "center_name"], filters={"is_active": 1})
	for center in centers:
		location_name = f"{center.center_name} Location"
		existing = frappe.db.get_value("Location", {"location_name": location_name}, "name")
		if existing:
			frappe.db.set_value("Location", existing, "asb_center", center.name, update_modified=False)
			continue

		location = frappe.get_doc(
			{
				"doctype": "Location",
				"location_name": location_name,
			}
		).insert(ignore_permissions=True)
		frappe.db.set_value("Location", location.name, "asb_center", center.name, update_modified=False)



def _company_name():
	return (
		frappe.db.get_value("Company", {"company_name": "ASB Foundation"}, "name")
		or frappe.db.get_value("Company", {}, "name")
	)



def _pick_account(company, preferred_name=None, account_type=None, root_type=None):
	if preferred_name and frappe.db.exists("Account", preferred_name):
		return preferred_name

	filters = {"company": company, "is_group": 0}
	if account_type:
		filters["account_type"] = account_type
	if root_type:
		filters["root_type"] = root_type
	return frappe.db.get_value("Account", filters, "name")



def _setup_asset_categories():
	company = _company_name()
	if not company:
		return

	accumulated_depreciation = _pick_account(company, account_type="Accumulated Depreciation")
	depreciation_expense = _pick_account(company, account_type="Depreciation") or _pick_account(
		company, root_type="Expense"
	)

	for category_name, preferred_fixed_asset_account in ASSET_CATEGORY_MAP.items():
		fixed_asset_account = _pick_account(
			company,
			preferred_name=preferred_fixed_asset_account,
			account_type="Fixed Asset",
		)
		if not fixed_asset_account:
			continue

		existing = frappe.db.get_value("Asset Category", {"asset_category_name": category_name}, "name")
		if existing:
			doc = frappe.get_doc("Asset Category", existing)
		else:
			doc = frappe.get_doc({"doctype": "Asset Category", "asset_category_name": category_name})

		account_row = None
		for row in doc.accounts:
			if row.company_name == company:
				account_row = row
				break

		if not account_row:
			doc.append("accounts", {"company_name": company, "fixed_asset_account": fixed_asset_account})
			account_row = doc.accounts[-1]

		account_row.fixed_asset_account = fixed_asset_account
		if accumulated_depreciation:
			account_row.accumulated_depreciation_account = accumulated_depreciation
		if depreciation_expense:
			account_row.depreciation_expense_account = depreciation_expense

		if existing:
			doc.save(ignore_permissions=True)
		else:
			doc.insert(ignore_permissions=True)
