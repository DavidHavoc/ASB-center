# Copyright (c) 2026, Dvd and contributors
# For license information, please see license.txt

import frappe


def execute():
	_migrate_scoring_tool_values()
	_link_previous_assessments()



def _migrate_scoring_tool_values():
	if not frappe.db.has_column("Assessment", "scoring_tool"):
		return

	frappe.db.sql(
		"""
		update `tabAssessment`
		set scoring_tool = 'AEPS (New)'
		where scoring_tool = 'AEPS'
		"""
	)



def _link_previous_assessments():
	if not frappe.db.has_column("Assessment", "previous_assessment"):
		return

	rows = frappe.get_all(
		"Assessment",
		fields=["name", "beneficiary", "assessment_date", "assessment_type", "previous_assessment", "creation"],
		order_by="beneficiary asc, assessment_date asc, creation asc",
	)

	last_assessment_by_beneficiary = {}
	for row in rows:
		beneficiary = row.beneficiary
		previous_name = last_assessment_by_beneficiary.get(beneficiary)

		if row.assessment_type in ("Repeated", "Final") and not row.previous_assessment and previous_name:
			frappe.db.set_value(
				"Assessment",
				row.name,
				"previous_assessment",
				previous_name,
				update_modified=False,
			)

		last_assessment_by_beneficiary[beneficiary] = row.name
