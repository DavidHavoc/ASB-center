import frappe
from frappe.modules.import_file import import_file_by_path

def run():
    frappe.delete_doc("Workspace", "SSK Center Home", ignore_missing=True, force=True)
    frappe.db.commit()
    import_file_by_path("/home/dvd/projects/frappe/frappe-bench/apps/asb_case_mgmt/asb_case_mgmt/asb_center/workspace/asb_center_home/asb_center_home.json", force=True)
    frappe.db.commit()
    print("Successfully deleted and re-imported workspace using absolute path")
