# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate



def execute():
	company = (
		frappe.db.get_value("Company", {"company_name": "ASB Foundation"}, "name")
		or frappe.db.get_value("Company", {}, "name")
	)
	if not company:
		return

	current_year = int(nowdate().split("-")[0])
	for year in (current_year, current_year + 1):
		_ensure_fiscal_year(year, company)

	if frappe.db.has_column("Company", "default_fiscal_year"):
		frappe.db.set_value(
			"Company",
			company,
			"default_fiscal_year",
			str(current_year),
			update_modified=False,
		)



def _ensure_fiscal_year(year, company):
	year_name = str(year)
	start_date = f"{year}-01-01"
	end_date = f"{year}-12-31"

	if frappe.db.exists("Fiscal Year", year_name):
		doc = frappe.get_doc("Fiscal Year", year_name)
		doc.year_start_date = start_date
		doc.year_end_date = end_date
		doc.disabled = 0
	else:
		doc = frappe.get_doc(
			{
				"doctype": "Fiscal Year",
				"year": year_name,
				"year_start_date": start_date,
				"year_end_date": end_date,
				"disabled": 0,
			}
		)

	if not any((row.company == company) for row in doc.companies):
		doc.append("companies", {"company": company})

	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)
