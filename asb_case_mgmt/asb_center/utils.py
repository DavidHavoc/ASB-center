import frappe


def get_employee_for_user(user):
	if not user or user == "Guest":
		return None

	employee = frappe.db.get_value("Employee", {"user_id": user, "status": "Active"}, "name")
	if employee:
		return employee

	return frappe.db.get_value("Employee", {"user_id": user}, "name")


def get_employee_center(employee):
	if not employee:
		return None

	return frappe.db.get_value("Employee", employee, "asb_center")


def get_user_center(user):
	employee = get_employee_for_user(user)
	return get_employee_center(employee)


def get_beneficiary_center(beneficiary):
	if not beneficiary:
		return None

	return frappe.db.get_value("Beneficiary", beneficiary, "center")


def is_specialist_assigned_to_beneficiary(beneficiary, specialist):
	if not beneficiary or not specialist:
		return False

	return bool(
		frappe.db.exists(
			"Beneficiary Specialist",
			{
				"parent": beneficiary,
				"parenttype": "Beneficiary",
				"parentfield": "responsible_specialists",
				"specialist": specialist,
			},
		)
	)
