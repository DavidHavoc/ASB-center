import frappe
from frappe import _


def _location_center(location):
	if not location or not frappe.db.has_column("Location", "asb_center"):
		return None
	return frappe.db.get_value("Location", location, "asb_center")


def validate_asset_center_scope(doc, method=None):
	location_center = _location_center(doc.location)
	if location_center and not doc.asb_center:
		doc.asb_center = location_center
	elif location_center and doc.asb_center and location_center != doc.asb_center:
		frappe.throw(_("Asset Center must match the selected Location Center."))

	if doc.asb_beneficiary:
		beneficiary_center = frappe.db.get_value("Beneficiary", doc.asb_beneficiary, "center")
		if beneficiary_center and not doc.asb_center:
			doc.asb_center = beneficiary_center
		elif beneficiary_center and doc.asb_center != beneficiary_center:
			frappe.throw(_("Asset Beneficiary must belong to the same Center as the Asset."))
