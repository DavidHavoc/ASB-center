# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


UOMS = (
	("Nos", 1),
	("Box", 0),
	("Kg", 0),
	("Litre", 0),
	("Set", 1),
)

STOCK_ENTRY_TYPES = (
	"Material Issue",
	"Material Receipt",
	"Material Transfer",
	"Material Transfer for Manufacture",
	"Material Consumption for Manufacture",
	"Manufacture",
	"Repack",
	"Send to Subcontractor",
	"Disassemble",
)



def execute():
	_setup_custom_fields()
	_setup_uoms()
	_setup_item_groups()
	_setup_stock_entry_types()
	_setup_center_warehouses()
	_enable_auto_batch_creation()



def _setup_custom_fields():
	custom_fields = {
		"Warehouse": [
			{
				"fieldname": "asb_center",
				"fieldtype": "Link",
				"label": "ASB Center",
				"options": "Center",
				"insert_after": "company",
				"in_standard_filter": 1,
			},
		],
		"Stock Entry": [
			{
				"fieldname": "asb_center",
				"fieldtype": "Link",
				"label": "ASB Center",
				"options": "Center",
				"insert_after": "cost_center",
				"in_standard_filter": 1,
			},
		],
		"Batch": [
			{
				"fieldname": "asb_center",
				"fieldtype": "Link",
				"label": "ASB Center",
				"options": "Center",
				"insert_after": "item",
				"in_standard_filter": 1,
			},
		],
	}
	create_custom_fields(custom_fields, update=True)



def _setup_uoms():
	for uom_name, must_be_whole_number in UOMS:
		if frappe.db.exists("UOM", uom_name):
			continue
		frappe.get_doc(
			{
				"doctype": "UOM",
				"uom_name": uom_name,
				"must_be_whole_number": must_be_whole_number,
			}
		).insert(ignore_permissions=True)



def _ensure_item_group(item_group_name, parent_item_group=None, is_group=0):
	existing = frappe.db.get_value("Item Group", {"item_group_name": item_group_name}, "name")
	if existing:
		doc = frappe.get_doc("Item Group", existing)
		changed = False
		if doc.is_group != is_group:
			doc.is_group = is_group
			changed = True
		if parent_item_group and doc.parent_item_group != parent_item_group:
			doc.parent_item_group = parent_item_group
			changed = True
		if changed:
			doc.save(ignore_permissions=True)
		return doc.name

	doc = frappe.get_doc(
		{
			"doctype": "Item Group",
			"item_group_name": item_group_name,
			"parent_item_group": parent_item_group,
			"is_group": is_group,
		}
	)
	return doc.insert(ignore_permissions=True).name



def _setup_item_groups():
	root = _ensure_item_group("All Item Groups", is_group=1)
	asb_supplies = _ensure_item_group("ASB Supplies", parent_item_group=root, is_group=1)
	_ensure_item_group("ASB Consumables", parent_item_group=asb_supplies, is_group=0)
	_ensure_item_group("ASB Medical Supplies", parent_item_group=asb_supplies, is_group=0)
	_ensure_item_group("ASB Assistive Devices", parent_item_group=asb_supplies, is_group=0)



def _setup_stock_entry_types():
	for purpose in STOCK_ENTRY_TYPES:
		if frappe.db.exists("Stock Entry Type", purpose) or frappe.db.exists(
			"Stock Entry Type", {"purpose": purpose}
		):
			continue
		frappe.get_doc(
			{
				"doctype": "Stock Entry Type",
				"name": purpose,
				"purpose": purpose,
			}
		).insert(ignore_permissions=True)



def _company_name_and_abbr():
	company = (
		frappe.db.get_value("Company", {"company_name": "ASB Foundation"}, "name")
		or frappe.db.get_value("Company", {}, "name")
	)
	if not company:
		return None, None
	return company, frappe.db.get_value("Company", company, "abbr")



def _resolve_parent_warehouse(company, company_abbr):
	preferred_names = [f"Stores - {company_abbr}", f"All Warehouses - {company_abbr}"]
	for warehouse_name in preferred_names:
		if frappe.db.exists("Warehouse", warehouse_name):
			return warehouse_name

	return frappe.db.get_value("Warehouse", {"company": company, "is_group": 1}, "name")



def _setup_center_warehouses():
	company, company_abbr = _company_name_and_abbr()
	if not company or not company_abbr:
		return

	parent_warehouse = _resolve_parent_warehouse(company, company_abbr)
	if not parent_warehouse:
		return

	centers = frappe.get_all("Center", fields=["name", "center_name"], filters={"is_active": 1})
	for center in centers:
		warehouse_name = f"{center.center_name} Stock"
		existing = frappe.db.get_value(
			"Warehouse",
			{"warehouse_name": warehouse_name, "company": company},
			"name",
		)
		if existing:
			frappe.db.set_value("Warehouse", existing, "asb_center", center.name, update_modified=False)
			continue

		warehouse = frappe.get_doc(
			{
				"doctype": "Warehouse",
				"warehouse_name": warehouse_name,
				"company": company,
				"parent_warehouse": parent_warehouse,
				"is_group": 0,
			}
		).insert(ignore_permissions=True)
		frappe.db.set_value("Warehouse", warehouse.name, "asb_center", center.name, update_modified=False)



def _enable_auto_batch_creation():
	if frappe.db.exists("DocType", "Stock Settings") and frappe.get_meta("Stock Settings").has_field(
		"auto_create_new_batch"
	):
		frappe.db.set_single_value("Stock Settings", "auto_create_new_batch", 1)
