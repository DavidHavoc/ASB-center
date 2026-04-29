import frappe
from frappe import _


def _warehouse_center(warehouse):
	if not warehouse or not frappe.db.has_column("Warehouse", "asb_center"):
		return None
	return frappe.db.get_value("Warehouse", warehouse, "asb_center")


def _iter_stock_entry_warehouses(doc):
	for warehouse in (doc.from_warehouse, doc.to_warehouse):
		if warehouse:
			yield warehouse

	for row in doc.items or []:
		for warehouse in (row.s_warehouse, row.t_warehouse):
			if warehouse:
				yield warehouse


def validate_stock_entry_center_scope(doc, method=None):
	if not frappe.db.has_column("Stock Entry", "asb_center"):
		return

	centers = {center for center in (_warehouse_center(wh) for wh in _iter_stock_entry_warehouses(doc)) if center}
	if len(centers) > 1:
		frappe.throw(_("Stock Entry warehouses must belong to the same Center scope."))

	inferred_center = next(iter(centers), None)
	if inferred_center and not doc.asb_center:
		doc.asb_center = inferred_center

	if doc.asb_center and inferred_center and doc.asb_center != inferred_center:
		frappe.throw(_("Stock Entry Center must match the selected warehouse Center scope."))
