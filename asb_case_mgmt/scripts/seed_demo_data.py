import frappe
from frappe.utils import today


DEMO_CENTERS = [
	{
		"center_name": "SSK Tbilisi Vake Center",
		"description": "Main urban service center in Tbilisi",
		"address": "Tbilisi - Vake",
		"phone": "+995599000001",
		"email": "tbilisi.vake.center@ssk.localhost",
		"legacy_names": ["ASB Baghdad Center"],
	},
	{
		"center_name": "SSK Tbilisi Saburtalo Center",
		"description": "Secondary service center in Tbilisi",
		"address": "Tbilisi - Saburtalo",
		"phone": "+995599000002",
		"email": "tbilisi.saburtalo.center@ssk.localhost",
		"legacy_names": ["ASB Basra Center"],
	},
]

DEMO_EMPLOYEES = [
	{
		"first_name": "Nino",
		"last_name": "Beridze",
		"gender": "Female",
		"date_of_birth": "1990-05-14",
		"user_id": "nino.specialist@ssk.localhost",
		"center": "SSK Tbilisi Vake Center",
		"contract_number": "SSK-TBS-EMP-001",
		"legacy_user_ids": ["ali.specialist@asb.localhost"],
	},
	{
		"first_name": "Giorgi",
		"last_name": "Kapanadze",
		"gender": "Male",
		"date_of_birth": "1992-11-03",
		"user_id": "giorgi.specialist@ssk.localhost",
		"center": "SSK Tbilisi Vake Center",
		"contract_number": "SSK-TBS-EMP-002",
		"legacy_user_ids": ["sara.specialist@asb.localhost"],
	},
	{
		"first_name": "Ana",
		"last_name": "Mchedlidze",
		"gender": "Female",
		"date_of_birth": "1988-08-22",
		"user_id": "ana.specialist@ssk.localhost",
		"center": "SSK Tbilisi Saburtalo Center",
		"contract_number": "SSK-TBS-EMP-003",
		"legacy_user_ids": ["omar.specialist@asb.localhost"],
	},
]

DEMO_BENEFICIARIES = [
	{
		"beneficiary_code": "BEN-DEMO-0001",
		"full_name": "Nino Gelashvili",
		"service_type": "Disability Support",
		"center": "SSK Tbilisi Vake Center",
		"specialist": "nino.specialist@ssk.localhost",
		"birth_date": "2011-06-20",
	},
	{
		"beneficiary_code": "BEN-DEMO-0002",
		"full_name": "Luka Chikovani",
		"service_type": "Child Protection",
		"center": "SSK Tbilisi Vake Center",
		"specialist": "giorgi.specialist@ssk.localhost",
		"birth_date": "2016-02-12",
	},
	{
		"beneficiary_code": "BEN-DEMO-0003",
		"full_name": "Elene Qavlashvili",
		"service_type": "Rehabilitation",
		"center": "SSK Tbilisi Vake Center",
		"specialist": "nino.specialist@ssk.localhost",
		"birth_date": "2008-09-30",
	},
	{
		"beneficiary_code": "BEN-DEMO-0004",
		"full_name": "Saba Tsertsvadze",
		"service_type": "Social Protection",
		"center": "SSK Tbilisi Saburtalo Center",
		"specialist": "ana.specialist@ssk.localhost",
		"birth_date": "2014-01-18",
	},
	{
		"beneficiary_code": "BEN-DEMO-0005",
		"full_name": "Mariam Dvalishvili",
		"service_type": "Disability Support",
		"center": "SSK Tbilisi Saburtalo Center",
		"specialist": "ana.specialist@ssk.localhost",
		"birth_date": "2012-12-05",
	},
]


def _ensure_gender_values():
	for gender in ("Male", "Female", "Other"):
		if not frappe.db.exists("Gender", gender):
			frappe.get_doc({"doctype": "Gender", "gender": gender}).insert(ignore_permissions=True)


def _ensure_company():
	if not frappe.db.exists("Company", "SSK Foundation"):
		frappe.get_doc(
			{
				"doctype": "Company",
				"company_name": "SSK Foundation",
				"abbr": "SSK",
				"default_currency": "USD",
				"country": "Iraq",
			}
		).insert(ignore_permissions=True)


def _ensure_user(email, first_name):
	if not frappe.db.exists("User", email):
		frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": first_name,
				"enabled": 1,
				"send_welcome_email": 0,
				"roles": [{"role": "SSK Specialist"}],
			}
		).insert(ignore_permissions=True)


def execute():
	_ensure_gender_values()
	_ensure_company()

	center_lookup = {}
	for center in DEMO_CENTERS:
		doc = None
		for legacy_name in center.get("legacy_names", []):
			existing_legacy = frappe.db.get_value("Center", {"center_name": legacy_name}, "name")
			if existing_legacy:
				doc = frappe.get_doc("Center", existing_legacy)
				break

		if not doc:
			existing_center = frappe.db.get_value("Center", {"center_name": center["center_name"]}, "name")
			if existing_center:
				doc = frappe.get_doc("Center", existing_center)

		if doc:
			doc.update(center)
			doc.save(ignore_permissions=True)
			center_lookup[center["center_name"]] = doc.name
		else:
			doc = frappe.get_doc({"doctype": "Center", **center})
			center_lookup[center["center_name"]] = doc.insert(ignore_permissions=True).name

	employee_lookup = {}
	for employee in DEMO_EMPLOYEES:
		for legacy_user_id in employee.get("legacy_user_ids", []):
			_ensure_user(legacy_user_id, employee["first_name"])
		_ensure_user(employee["user_id"], employee["first_name"])
		existing_employee = None
		for lookup_user_id in [*employee.get("legacy_user_ids", []), employee["user_id"]]:
			existing_employee = frappe.db.get_value("Employee", {"user_id": lookup_user_id}, "name")
			if existing_employee:
				break
		if existing_employee:
			doc = frappe.get_doc("Employee", existing_employee)
			doc.first_name = employee["first_name"]
			doc.last_name = employee.get("last_name")
			doc.gender = employee["gender"]
			doc.date_of_birth = employee["date_of_birth"]
			doc.company = "SSK Foundation"
			doc.asb_center = center_lookup[employee["center"]]
			doc.asb_contract_number = employee["contract_number"]
			doc.asb_contract_start_date = today()
			doc.save(ignore_permissions=True)
			employee_lookup[employee["user_id"]] = existing_employee
			continue

		doc = frappe.get_doc(
			{
				"doctype": "Employee",
				"first_name": employee["first_name"],
				"last_name": employee.get("last_name"),
				"gender": employee["gender"],
				"date_of_birth": employee["date_of_birth"],
				"date_of_joining": today(),
				"status": "Active",
				"company": "SSK Foundation",
				"user_id": employee["user_id"],
				"asb_center": center_lookup[employee["center"]],
				"asb_contract_number": employee["contract_number"],
				"asb_contract_start_date": today(),
			}
		)
		employee_lookup[employee["user_id"]] = doc.insert(ignore_permissions=True).name

	for beneficiary in DEMO_BENEFICIARIES:
		specialist_employee = employee_lookup[beneficiary["specialist"]]
		existing_beneficiary = frappe.db.get_value(
			"Beneficiary", {"beneficiary_code": beneficiary["beneficiary_code"]}, "name"
		)
		if existing_beneficiary:
			doc = frappe.get_doc("Beneficiary", existing_beneficiary)
			doc.service_type = beneficiary["service_type"]
			doc.service_status = "Active"
			doc.center = center_lookup[beneficiary["center"]]
			doc.full_name = beneficiary["full_name"]
			doc.personal_id = f"PID-{beneficiary['beneficiary_code']}"
			doc.address = beneficiary["center"]
			doc.region = beneficiary["center"].split()[1]
			doc.municipality = "Demo Municipality"
			doc.guardian_parent = "Demo Guardian"
			doc.phone = "+995599111111"
			doc.email = f"{beneficiary['beneficiary_code'].lower()}@ssk.localhost"
			doc.sex = "Female"
			doc.birth_date = beneficiary["birth_date"]
			doc.diagnosis_status = "Demo case for UAT"
			doc.first_assessment_date = today()
			doc.family_status = "Single"
			doc.enrollment_date = today()
			doc.first_service_date = today()
			doc.application_contract_number = f"APP-{beneficiary['beneficiary_code']}"
			doc.notes = "Seeded demo beneficiary"
			doc.set("responsible_specialists", [])
			doc.append(
				"responsible_specialists",
				{
					"specialist": specialist_employee,
					"assignment_role": "Primary",
					"from_date": today(),
				},
			)
			doc.save(ignore_permissions=True)
			continue

		beneficiary_doc = frappe.get_doc(
			{
				"doctype": "Beneficiary",
				"beneficiary_code": beneficiary["beneficiary_code"],
				"service_type": beneficiary["service_type"],
				"service_status": "Active",
				"center": center_lookup[beneficiary["center"]],
				"full_name": beneficiary["full_name"],
				"personal_id": f"PID-{beneficiary['beneficiary_code']}",
				"address": beneficiary["center"],
				"region": beneficiary["center"].split()[1],
				"municipality": "Demo Municipality",
				"guardian_parent": "Demo Guardian",
				"phone": "+9647711111111",
				"email": f"{beneficiary['beneficiary_code'].lower()}@ssk.localhost",
				"sex": "Female",
				"birth_date": beneficiary["birth_date"],
				"diagnosis_status": "Demo case for UAT",
				"first_assessment_date": today(),
				"family_status": "Single",
				"enrollment_date": today(),
				"first_service_date": today(),
				"application_contract_number": f"APP-{beneficiary['beneficiary_code']}",
				"notes": "Seeded demo beneficiary",
				"responsible_specialists": [
					{
						"specialist": specialist_employee,
						"assignment_role": "Primary",
						"from_date": today(),
					}
				],
			}
		)
		beneficiary_doc.insert(ignore_permissions=True)

	frappe.db.commit()
	print(
		{
			"centers": list(center_lookup.values()),
			"employees": list(employee_lookup.values()),
			"beneficiaries": [item["beneficiary_code"] for item in DEMO_BENEFICIARIES],
		}
	)
