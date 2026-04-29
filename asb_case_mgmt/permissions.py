import frappe

from asb_case_mgmt.asb_center.utils import (
	get_employee_for_user,
	get_user_center,
	is_specialist_assigned_to_beneficiary,
)


def _has_role(user, role):
	return role in frappe.get_roles(user)


def _is_system_manager(user):
	return _has_role(user, "System Manager")


def _is_center_coordinator(user):
	return _has_role(user, "ASB Center Coordinator")


def _is_specialist(user):
	return _has_role(user, "ASB Specialist")


def _center_condition(doctype, center):
	if not center:
		return "1=0"
	return f"`tab{doctype}`.`center` = {frappe.db.escape(center)}"


def center_query_conditions(user=None):
	user = user or frappe.session.user
	if _is_system_manager(user):
		return ""

	center = get_user_center(user)
	if _is_center_coordinator(user) or _is_specialist(user):
		if not center:
			return "1=0"
		return f"`tabCenter`.`name` = {frappe.db.escape(center)}"

	return "1=0"


def beneficiary_query_conditions(user=None):
	user = user or frappe.session.user
	if _is_system_manager(user):
		return ""

	center = get_user_center(user)
	if _is_center_coordinator(user):
		return _center_condition("Beneficiary", center)

	if _is_specialist(user):
		employee = get_employee_for_user(user)
		if not center or not employee:
			return "1=0"

		return (
			f"({_center_condition('Beneficiary', center)})"
			" and exists ("
			"select 1 from `tabBeneficiary Specialist` bs "
			"where bs.parent = `tabBeneficiary`.`name` "
			"and bs.parenttype = 'Beneficiary' "
			"and bs.parentfield = 'responsible_specialists' "
			f"and bs.specialist = {frappe.db.escape(employee)})"
		)

	return "1=0"


def service_visit_query_conditions(user=None):
	user = user or frappe.session.user
	if _is_system_manager(user):
		return ""

	center = get_user_center(user)
	if _is_center_coordinator(user):
		return _center_condition("Service Visit", center)

	if _is_specialist(user):
		employee = get_employee_for_user(user)
		if not center or not employee:
			return "1=0"

		employee_escaped = frappe.db.escape(employee)
		return (
			f"({_center_condition('Service Visit', center)}) and ("
			f"`tabService Visit`.`specialist` = {employee_escaped} "
			"or exists ("
			"select 1 from `tabBeneficiary Specialist` bs "
			"where bs.parent = `tabService Visit`.`beneficiary` "
			"and bs.parenttype = 'Beneficiary' "
			"and bs.parentfield = 'responsible_specialists' "
			f"and bs.specialist = {employee_escaped}))"
		)

	return "1=0"


def assessment_query_conditions(user=None):
	user = user or frappe.session.user
	if _is_system_manager(user):
		return ""

	center = get_user_center(user)
	if _is_center_coordinator(user):
		return _center_condition("Assessment", center)

	if _is_specialist(user):
		employee = get_employee_for_user(user)
		if not center or not employee:
			return "1=0"

		employee_escaped = frappe.db.escape(employee)
		return (
			f"({_center_condition('Assessment', center)}) and ("
			f"`tabAssessment`.`specialist` = {employee_escaped} "
			"or exists ("
			"select 1 from `tabBeneficiary Specialist` bs "
			"where bs.parent = `tabAssessment`.`beneficiary` "
			"and bs.parenttype = 'Beneficiary' "
			"and bs.parentfield = 'responsible_specialists' "
			f"and bs.specialist = {employee_escaped}))"
		)

	return "1=0"


def individual_plan_query_conditions(user=None):
	user = user or frappe.session.user
	if _is_system_manager(user):
		return ""

	center = get_user_center(user)
	if _is_center_coordinator(user):
		return _center_condition("Individual Plan", center)

	if _is_specialist(user):
		employee = get_employee_for_user(user)
		if not center or not employee:
			return "1=0"

		employee_escaped = frappe.db.escape(employee)
		return (
			f"({_center_condition('Individual Plan', center)}) and ("
			f"`tabIndividual Plan`.`specialist` = {employee_escaped} "
			"or exists ("
			"select 1 from `tabBeneficiary Specialist` bs "
			"where bs.parent = `tabIndividual Plan`.`beneficiary` "
			"and bs.parenttype = 'Beneficiary' "
			"and bs.parentfield = 'responsible_specialists' "
			f"and bs.specialist = {employee_escaped}))"
		)

	return "1=0"


def center_has_permission(doc, user=None, permission_type=None):
	user = user or frappe.session.user
	if _is_system_manager(user):
		return True

	center = get_user_center(user)
	if _is_center_coordinator(user) or _is_specialist(user):
		return bool(center and doc.name == center)

	return False


def beneficiary_has_permission(doc, user=None, permission_type=None):
	user = user or frappe.session.user
	if _is_system_manager(user):
		return True

	center = get_user_center(user)
	if _is_center_coordinator(user):
		return bool(center and doc.center == center)

	if _is_specialist(user):
		employee = get_employee_for_user(user)
		return bool(
			center
			and employee
			and doc.center == center
			and is_specialist_assigned_to_beneficiary(doc.name, employee)
		)

	return False


def service_visit_has_permission(doc, user=None, permission_type=None):
	user = user or frappe.session.user
	if _is_system_manager(user):
		return True

	center = get_user_center(user)
	if _is_center_coordinator(user):
		return bool(center and doc.center == center)

	if _is_specialist(user):
		employee = get_employee_for_user(user)
		if not center or not employee or doc.center != center:
			return False
		return doc.specialist == employee or is_specialist_assigned_to_beneficiary(
			doc.beneficiary, employee
		)

	return False


def assessment_has_permission(doc, user=None, permission_type=None):
	user = user or frappe.session.user
	if _is_system_manager(user):
		return True

	center = get_user_center(user)
	if _is_center_coordinator(user):
		return bool(center and doc.center == center)

	if _is_specialist(user):
		employee = get_employee_for_user(user)
		if not center or not employee or doc.center != center:
			return False
		return doc.specialist == employee or is_specialist_assigned_to_beneficiary(
			doc.beneficiary, employee
		)

	return False


def individual_plan_has_permission(doc, user=None, permission_type=None):
	user = user or frappe.session.user
	if _is_system_manager(user):
		return True

	center = get_user_center(user)
	if _is_center_coordinator(user):
		return bool(center and doc.center == center)

	if _is_specialist(user):
		employee = get_employee_for_user(user)
		if not center or not employee or doc.center != center:
			return False
		return doc.specialist == employee or is_specialist_assigned_to_beneficiary(
			doc.beneficiary, employee
		)

	return False


def specialist_monthly_service_summary_query_conditions(user=None):
	user = user or frappe.session.user
	if _is_system_manager(user):
		return ""

	center = get_user_center(user)
	if _is_center_coordinator(user):
		return _center_condition("Specialist Monthly Service Summary", center)

	if _is_specialist(user):
		employee = get_employee_for_user(user)
		if not center or not employee:
			return "1=0"

		return (
			f"({_center_condition('Specialist Monthly Service Summary', center)}) and "
			f"`tabSpecialist Monthly Service Summary`.`specialist` = {frappe.db.escape(employee)}"
		)

	return "1=0"


def specialist_monthly_service_summary_has_permission(doc, user=None, permission_type=None):
	user = user or frappe.session.user
	if _is_system_manager(user):
		return True

	center = get_user_center(user)
	if _is_center_coordinator(user):
		return bool(center and doc.center == center)

	if _is_specialist(user):
		employee = get_employee_for_user(user)
		return bool(center and employee and doc.center == center and doc.specialist == employee)

	return False
