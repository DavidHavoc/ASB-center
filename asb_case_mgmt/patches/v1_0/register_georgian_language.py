# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.rename_doc import rename_doc


LANGUAGE_CODE = "ka"
LANGUAGE_NAME = "ქართული"
LEGACY_NAMES = ("Georgian",)


def _find_existing_language_name():
	if frappe.db.exists("Language", LANGUAGE_CODE):
		return LANGUAGE_CODE

	for filters in (
		{"language_code": LANGUAGE_CODE},
		{"language_name": LANGUAGE_NAME},
	):
		name = frappe.db.get_value("Language", filters, "name")
		if name:
			return name

	for legacy_name in LEGACY_NAMES:
		name = frappe.db.get_value("Language", {"language_name": legacy_name}, "name")
		if name:
			return name

	return None


def execute():
	existing_name = _find_existing_language_name()
	if existing_name and existing_name != LANGUAGE_CODE and not frappe.db.exists("Language", LANGUAGE_CODE):
		rename_doc(
			"Language",
			existing_name,
			LANGUAGE_CODE,
			force=True,
			merge=False,
			ignore_permissions=True,
		)

	if not frappe.db.exists("Language", LANGUAGE_CODE):
		frappe.get_doc(
			{
				"doctype": "Language",
				"name": LANGUAGE_CODE,
				"language_code": LANGUAGE_CODE,
				"language_name": LANGUAGE_NAME,
				"enabled": 1,
			}
		).insert(ignore_permissions=True)
		return

	doc = frappe.get_doc("Language", LANGUAGE_CODE)
	changed = False

	if doc.language_code != LANGUAGE_CODE:
		doc.language_code = LANGUAGE_CODE
		changed = True

	if doc.language_name != LANGUAGE_NAME:
		doc.language_name = LANGUAGE_NAME
		changed = True

	if not doc.enabled:
		doc.enabled = 1
		changed = True

	if changed:
		doc.save(ignore_permissions=True)
