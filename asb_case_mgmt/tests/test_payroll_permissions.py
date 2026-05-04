import frappe
from frappe.core.doctype.user_permission.test_user_permission import create_user
from frappe.tests.utils import FrappeTestCase
from erpnext.setup.doctype.employee.test_employee import make_employee

from asb_case_mgmt.asb_center.utils import get_user_center
from asb_case_mgmt.payroll import get_specialist_monthly_totals
from asb_case_mgmt.patches.v1_0 import setup_employee_linkage


class TestPayrollPermissions(FrappeTestCase):
	def setUp(self):
		frappe.set_user("Administrator")

		self.summary_month = "2099-01"
		self._ensure_role("SSK Center Coordinator")
		self._ensure_role("SSK Specialist")
		self._ensure_employee_linkage()
		self.company = self._get_or_create_company()
		self.department = self._ensure_department(self.company)
		self._ensure_gender("Female")

		self.center_a = self._ensure_center("Test Center A")
		self.center_b = self._ensure_center("Test Center B")

		suffix = frappe.generate_hash(length=8)
		self.coordinator_user = create_user(
			f"test_asb_coord_{suffix}@example.com", "SSK Center Coordinator"
		)
		self.specialist_user_a = create_user(
			f"test_asb_spec_a_{suffix}@example.com", "SSK Specialist"
		)
		self.specialist_user_b = create_user(
			f"test_asb_spec_b_{suffix}@example.com", "SSK Specialist"
		)
		self._ensure_user_role(self.coordinator_user, "SSK Center Coordinator")
		self._ensure_user_role(self.specialist_user_a, "SSK Specialist")
		self._ensure_user_role(self.specialist_user_b, "SSK Specialist")

		self.employee_coord = make_employee(
			self.coordinator_user.name,
			company=self.company,
			department=self.department,
			asb_center=self.center_a,
		)
		self.employee_a = make_employee(
			self.specialist_user_a.name,
			company=self.company,
			department=self.department,
			asb_center=self.center_a,
		)
		self.employee_b = make_employee(
			self.specialist_user_b.name,
			company=self.company,
			department=self.department,
			asb_center=self.center_b,
		)
		self._link_employee_to_user(self.employee_coord, self.coordinator_user, self.center_a)
		self._link_employee_to_user(self.employee_a, self.specialist_user_a, self.center_a)
		self._link_employee_to_user(self.employee_b, self.specialist_user_b, self.center_b)

		self.summary_a = self._make_summary(self.employee_a, self.center_a, self.summary_month, 5)
		self.summary_b = self._make_summary(self.employee_b, self.center_b, self.summary_month, 3)

	def tearDown(self):
		frappe.set_user("Administrator")
		frappe.db.rollback()

	def test_specialist_monthly_totals_respects_permissions(self):
		frappe.set_user(self.coordinator_user.name)
		self._force_user_center(self.coordinator_user.name, self.employee_coord, self.center_a)
		results = get_specialist_monthly_totals(summary_month=self.summary_month)
		self.assertEqual({row["specialist"] for row in results}, {self.employee_a})

		results = get_specialist_monthly_totals(
			summary_month=self.summary_month, center=self.center_b
		)
		self.assertEqual(results, [])

		frappe.set_user(self.specialist_user_a.name)
		self._force_user_center(self.specialist_user_a.name, self.employee_a, self.center_a)
		results = get_specialist_monthly_totals(summary_month=self.summary_month)
		self.assertEqual({row["specialist"] for row in results}, {self.employee_a})

		results = get_specialist_monthly_totals(
			summary_month=self.summary_month, specialist=self.employee_b
		)
		self.assertEqual(results, [])

	def _ensure_role(self, role_name):
		if not frappe.db.exists("Role", role_name):
			frappe.get_doc(
				{"doctype": "Role", "role_name": role_name, "desk_access": 1}
			).insert(ignore_permissions=True)

	def _ensure_center(self, center_name):
		existing = frappe.db.get_value("Center", {"center_name": center_name}, "name")
		if existing:
			return existing

		center = frappe.get_doc(
			{"doctype": "Center", "center_name": center_name, "is_active": 1}
		).insert(ignore_permissions=True)
		return center.name

	def _ensure_department(self, company, department_name="Test Department"):
		existing = frappe.db.get_value(
			"Department", {"department_name": department_name, "company": company}, "name"
		)
		if existing:
			return existing

		department = frappe.get_doc(
			{
				"doctype": "Department",
				"department_name": department_name,
				"company": company,
				"is_group": 0,
			}
		).insert(ignore_permissions=True)
		return department.name

	def _ensure_gender(self, gender):
		if not frappe.db.exists("Gender", gender):
			frappe.get_doc({"doctype": "Gender", "gender": gender}).insert(
				ignore_permissions=True
			)

	def _ensure_user_role(self, user, role):
		if role not in frappe.get_roles(user.name):
			user.add_roles(role)
		frappe.clear_cache(user=user.name)

	def _ensure_employee_linkage(self):
		if not frappe.db.has_column("Employee", "asb_center"):
			setup_employee_linkage.execute()
			frappe.clear_cache(doctype="Employee")

	def _link_employee_to_user(self, employee, user, center):
		frappe.db.set_value("Employee", employee, "user_id", user.name, update_modified=False)
		frappe.db.set_value("Employee", employee, "status", "Active", update_modified=False)
		if frappe.db.has_column("Employee", "asb_center"):
			frappe.db.set_value(
				"Employee", employee, "asb_center", center, update_modified=False
			)
		frappe.clear_cache(user=user.name)

	def _force_user_center(self, user, employee, center):
		frappe.db.set_value("Employee", employee, "user_id", user, update_modified=False)
		frappe.db.set_value("Employee", employee, "status", "Active", update_modified=False)
		if frappe.db.has_column("Employee", "asb_center"):
			frappe.db.set_value(
				"Employee", employee, "asb_center", center, update_modified=False
			)
		frappe.clear_cache(user=user)
		self.assertEqual(
			get_user_center(user),
			center,
			msg=f"Expected center {center} for user {user}",
		)

	def _make_summary(self, specialist, center, summary_month, total_units):
		doc = frappe.get_doc(
			{
				"doctype": "Specialist Monthly Service Summary",
				"specialist": specialist,
				"center": center,
				"summary_month": summary_month,
				"completed_visits": 1,
				"total_service_units": total_units,
			}
		)
		doc.insert(ignore_permissions=True)
		return doc.name

	def _get_or_create_company(self):
		existing = frappe.db.get_value("Company", {}, "name")
		if existing:
			return existing

		flags = frappe.local.flags
		original_ignore = flags.get("ignore_chart_of_accounts", False)
		flags.ignore_chart_of_accounts = True
		try:
			company = frappe.get_doc(
				{
					"doctype": "Company",
					"company_name": "Test Company ASB",
					"country": "India",
					"default_currency": "INR",
				}
			)
			company.insert(ignore_permissions=True)
			return company.name
		finally:
			flags.ignore_chart_of_accounts = original_ignore
