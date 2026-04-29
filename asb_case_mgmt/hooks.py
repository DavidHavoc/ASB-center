app_name = "asb_case_mgmt"
app_title = "ASB center"
app_publisher = "Dvd"
app_description = "Center app for ASB "
app_email = "godhvc@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "asb_case_mgmt",
# 		"logo": "/assets/asb_case_mgmt/logo.png",
# 		"title": "ASB center",
# 		"route": "/asb_case_mgmt",
# 		"has_permission": "asb_case_mgmt.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/asb_case_mgmt/css/asb_case_mgmt.css"
# app_include_js = "/assets/asb_case_mgmt/js/asb_case_mgmt.js"

# include js, css files in header of web template
# web_include_css = "/assets/asb_case_mgmt/css/asb_case_mgmt.css"
# web_include_js = "/assets/asb_case_mgmt/js/asb_case_mgmt.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "asb_case_mgmt/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "asb_case_mgmt/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "asb_case_mgmt.utils.jinja_methods",
# 	"filters": "asb_case_mgmt.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "asb_case_mgmt.install.before_install"
# after_install = "asb_case_mgmt.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "asb_case_mgmt.uninstall.before_uninstall"
# after_uninstall = "asb_case_mgmt.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "asb_case_mgmt.utils.before_app_install"
# after_app_install = "asb_case_mgmt.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "asb_case_mgmt.utils.before_app_uninstall"
# after_app_uninstall = "asb_case_mgmt.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "asb_case_mgmt.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Center": "asb_case_mgmt.permissions.center_query_conditions",
	"Beneficiary": "asb_case_mgmt.permissions.beneficiary_query_conditions",
	"Service Visit": "asb_case_mgmt.permissions.service_visit_query_conditions",
	"Assessment": "asb_case_mgmt.permissions.assessment_query_conditions",
	"Individual Plan": "asb_case_mgmt.permissions.individual_plan_query_conditions",
	"Specialist Monthly Service Summary": "asb_case_mgmt.permissions.specialist_monthly_service_summary_query_conditions",
}

has_permission = {
	"Center": "asb_case_mgmt.permissions.center_has_permission",
	"Beneficiary": "asb_case_mgmt.permissions.beneficiary_has_permission",
	"Service Visit": "asb_case_mgmt.permissions.service_visit_has_permission",
	"Assessment": "asb_case_mgmt.permissions.assessment_has_permission",
	"Individual Plan": "asb_case_mgmt.permissions.individual_plan_has_permission",
	"Specialist Monthly Service Summary": "asb_case_mgmt.permissions.specialist_monthly_service_summary_has_permission",
}

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Service Visit": {
		"after_insert": "asb_case_mgmt.payroll.on_service_visit_change",
		"on_update": "asb_case_mgmt.payroll.on_service_visit_change",
		"on_trash": "asb_case_mgmt.payroll.on_service_visit_change",
	},
	"Stock Entry": {
		"validate": "asb_case_mgmt.stock.validate_stock_entry_center_scope",
	},
	"Asset": {
		"validate": "asb_case_mgmt.assets.validate_asset_center_scope",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"asb_case_mgmt.tasks.all"
# 	],
# 	"daily": [
# 		"asb_case_mgmt.tasks.daily"
# 	],
# 	"hourly": [
# 		"asb_case_mgmt.tasks.hourly"
# 	],
# 	"weekly": [
# 		"asb_case_mgmt.tasks.weekly"
# 	],
# 	"monthly": [
# 		"asb_case_mgmt.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "asb_case_mgmt.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "asb_case_mgmt.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "asb_case_mgmt.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["asb_case_mgmt.utils.before_request"]
# after_request = ["asb_case_mgmt.utils.after_request"]

# Job Events
# ----------
# before_job = ["asb_case_mgmt.utils.before_job"]
# after_job = ["asb_case_mgmt.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"asb_case_mgmt.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

role_home_page = {
	"ASB Specialist": "/app/asb-center-home",
	"ASB Center Coordinator": "/app/asb-center-home",
}

