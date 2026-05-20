# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe


ROLE_RENAMES = {
	"ASB Center Coordinator": "SSK Center Coordinator",
	"ASB Specialist": "SSK Specialist",
}

ITEM_GROUP_RENAMES = {
	"ASB Supplies": "SSK Supplies",
	"ASB Consumables": "SSK Consumables",
	"ASB Medical Supplies": "SSK Medical Supplies",
	"ASB Assistive Devices": "SSK Assistive Devices",
}

ASSET_CATEGORY_RENAMES = {
	"ASB Assistive Devices": "SSK Assistive Devices",
	"ASB IT Equipment": "SSK IT Equipment",
	"ASB Facility Assets": "SSK Facility Assets",
}

DOC_TYPES_WITH_MODULE = (
	"Center",
	"Beneficiary",
	"Assessment",
	"Service Visit",
	"Individual Plan",
	"Specialist Monthly Service Summary",
	"Assessment Domain Score",
	"Beneficiary Specialist",
	"Individual Plan Goal",
)

MODULE_OLD = "ASB center"
MODULE_NEW = "SSK center"
WORKSPACE_OLD = "ASB Center Home"
WORKSPACE_NEW = "SSK Center Home"
HOME_PAGE = "/app/ssk-center-home"
COMPANY_OLD = "ASB Foundation"
COMPANY_NEW = "SSK Foundation"
COMPANY_ABBR = "SSK"


def _safe_rename(doctype, old_name, new_name):
	if not frappe.db.exists(doctype, old_name):
		return
	if frappe.db.exists(doctype, new_name):
		frappe.rename_doc(
			doctype,
			old_name,
			new_name,
			merge=True,
			ignore_permissions=True,
		)
		return
	frappe.rename_doc(doctype, old_name, new_name, ignore_permissions=True)


def _rename_roles():
	for old_name, new_name in ROLE_RENAMES.items():
		_safe_rename("Role", old_name, new_name)
		if frappe.db.exists("Role", new_name):
			frappe.db.set_value(
				"Role", new_name, "home_page", HOME_PAGE, update_modified=False
			)


def _rename_module_def():
	_safe_rename("Module Def", MODULE_OLD, MODULE_NEW)


def _update_doctype_modules():
	for doctype_name in DOC_TYPES_WITH_MODULE:
		if not frappe.db.exists("DocType", doctype_name):
			continue
		current = frappe.db.get_value("DocType", doctype_name, "module")
		if current == MODULE_OLD:
			frappe.db.set_value(
				"DocType", doctype_name, "module", MODULE_NEW, update_modified=False
			)


def _rename_workspace():
	if frappe.db.exists("Workspace", WORKSPACE_OLD):
		_safe_rename("Workspace", WORKSPACE_OLD, WORKSPACE_NEW)

	if not frappe.db.exists("Workspace", WORKSPACE_NEW):
		return

	doc = frappe.get_doc("Workspace", WORKSPACE_NEW)
	doc.label = WORKSPACE_NEW
	doc.title = WORKSPACE_NEW
	doc.module = MODULE_NEW
	if doc.content:
		doc.content = doc.content.replace("ASB Case Management", "SSK Case Management")
	doc.save(ignore_permissions=True)


def _rename_company():
	_safe_rename("Company", COMPANY_OLD, COMPANY_NEW)
	if frappe.db.exists("Company", COMPANY_NEW):
		frappe.db.set_value(
			"Company", COMPANY_NEW, "abbr", COMPANY_ABBR, update_modified=False
		)


def _rename_item_groups():
	for old_name, new_name in ITEM_GROUP_RENAMES.items():
		_safe_rename("Item Group", old_name, new_name)


def _rename_asset_categories():
	for old_name, new_name in ASSET_CATEGORY_RENAMES.items():
		_safe_rename("Asset Category", old_name, new_name)


def execute():
	_rename_roles()
	_rename_module_def()
	_update_doctype_modules()
	_rename_workspace()
	_rename_company()
	_rename_item_groups()
	_rename_asset_categories()
