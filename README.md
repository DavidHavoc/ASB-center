# SSK Case Management (asb_case_mgmt)

SSK Case Management is a custom Frappe app for nonprofit and social-services operations, built to run with ERPNext version-15.
The internal app name remains `asb_case_mgmt` for historical reasons, but all user-facing labels are SSK.

This app is designed to keep nonprofit-specific workflows in app-level code (instead of forking ERPNext core), while still using ERPNext standard modules for HR, payroll-adjacent metrics, stock, and assets.

## Contents

1. Purpose and Scope
2. Current Phase Coverage
3. Functional Architecture
4. DocTypes Implemented
5. Role and Permission Model
6. Workspace and Home Page
7. Employee Linkage and Contracts
8. Visit and Assessment Logic
9. Installation and Setup
10. Running the Site Locally
11. Migrations and Patches
12. End-to-End Testing Guide
13. Troubleshooting
14. File and Code Map
15. Roadmap
16. Contributing
17. License

## 1) Purpose and Scope

This app supports social-services case management with the following priorities:

1. Centers
2. Employees and HR structure
3. Beneficiaries and personal case card
4. Visits, assessments, and permissions
5. Inventory and assets (next phase)

## 2) Current Phase Coverage

Implemented in this phase:

1. Center registry
2. Beneficiary registry
3. Service visits with monthly counting
4. Assessments with repeated/final timeline support
5. Individual plan as personal card layer
6. Specialist assignment model
7. Center and specialist permission filters
8. SSK workspace home page with core shortcuts
9. Employee custom fields for center and contract tracking
10. Stock baseline data and center-scope validation
11. Asset baseline data and center linkage validation
12. Georgian language registration and translations for the app layer

## 3) Functional Architecture

The app follows a hybrid architecture:

1. ERPNext standard models are used where sensible:
	- Employee (extended via Custom Fields)
	- Role and Desk routing
2. Nonprofit-specific models are implemented as standard app DocTypes:
	- Center
	- Beneficiary
	- Service Visit
	- Assessment
	- Individual Plan
3. Permission and scoping logic is implemented in app-level hook functions:
	- Center-based visibility
	- Specialist-assignment visibility

## 4) DocTypes Implemented

### 4.1 Center

Purpose:

1. Master registry for service centers.

Key fields:

1. Center Name
2. Description
3. Address
4. Phone
5. Email
6. Is Active

Behavior:

1. Naming series-based identifier
2. Phone and email validation

### 4.2 Beneficiary

Purpose:

1. Master profile for service beneficiaries.

Key fields include:

1. Service Type
2. Beneficiary Code
3. Service Status
4. Full Name
5. Personal ID
6. Address
7. Region
8. Municipality
9. Guardian or Parent
10. Phone
11. Email
12. Sex
13. Birth Date
14. Age (computed)
15. Age Category (computed)
16. Diagnosis or Status
17. First Assessment Date
18. Responsible Specialists (child table)
19. Family Status
20. Enrollment Date
21. First Service Date
22. Application or Contract Number
23. Exit Date
24. Exit Reason
25. Attachment
26. Notes

Behavior:

1. Age and age category computed from birth date
2. Date consistency validation
3. Specialist assignment duplicate prevention
4. Specialist-center consistency check

### 4.3 Beneficiary Specialist (Child Table)

Purpose:

1. Maps one beneficiary to one or more specialists.

Key fields:

1. Specialist (Employee)
2. Assignment Role (Primary, Secondary)
3. From Date
4. To Date

### 4.4 Service Visit

Purpose:

1. Records service delivery events linked to beneficiary and specialist.

Key fields:

1. Beneficiary
2. Center
3. Specialist
4. Visit Date
5. Visit Month (computed)
6. Visit Type
7. Status
8. Service Units
9. Duration Minutes
10. Notes

Behavior:

1. Auto-sets visit month as YYYY-MM
2. Enforces center match with beneficiary
3. Enforces specialist assignment to beneficiary
4. Supports payroll-ready aggregation via whitelisted methods

### 4.5 Assessment

Purpose:

1. Tracks initial, repeated, and final assessments over time.

Key fields:

1. Beneficiary
2. Center
3. Specialist
4. Assessment Date
5. Assessment Type (Initial, Repeated, Final)
6. Scoring Tool (Barthel, AEPS, Other)
7. Total Score
8. Service Delivery Schedule Count
9. Domain Scores (child table)
10. Progress Summary
11. Recommendations
12. Next Review Date
13. Notes

Behavior:

1. Repeated and final assessments require at least one previous assessment
2. Enforces center and specialist assignment consistency
3. Validates score and schedule count as non-negative

### 4.6 Assessment Domain Score (Child Table)

Purpose:

1. Stores per-domain progress metrics.

Key fields:

1. Domain
2. Baseline Score
3. Current Score
4. Progress Notes

### 4.7 Individual Plan

Purpose:

1. Personal card layer for case planning.

Key fields:

1. Beneficiary
2. Center
3. Responsible Specialist
4. Status (Draft, Active, Completed)
5. Plan Start Date
6. Plan End Date
7. Review Frequency
8. Goals (child table)
9. Notes

Behavior:

1. Active and completed plans require at least one goal
2. Enforces center and specialist assignment consistency

### 4.8 Individual Plan Goal (Child Table)

Purpose:

1. Goal-level tracking for individual plans.

Key fields:

1. Goal
2. Target Date
3. Status
4. Progress Notes

## 5) Role and Permission Model

### Roles

1. SSK Center Coordinator
2. SSK Specialist
3. System Manager (full access)

### Access Rules

1. Every user is expected to map to an Employee record.
2. Employee carries center linkage via custom field asb_center.
3. Center coordinators can view and manage records for their center.
4. Specialists can see records in their center where they are the assigned specialist (directly or via beneficiary specialist mapping).

Permission query and has-permission hooks are implemented in app code and attached in hooks.py.

## 6) Workspace and Home Page

A public workspace is created:

1. Label: SSK Center Home
2. Route: /app/ssk-center-home

Workspace shortcuts include:

1. Center
2. Individual Plan
3. Beneficiary
4. Service Visit
5. Assessment

Role home pages for SSK Specialist and SSK Center Coordinator are set to:

1. /app/ssk-center-home

## 7) Employee Linkage and Contracts

Employee is extended with custom fields:

1. asb_center (Link to Center)
2. asb_contract_number
3. asb_contract_start_date
4. asb_contract_end_date
5. asb_contract_attachment

This supports center assignment, contract administration, and scanned document attachment.

## 8) Visit and Assessment Logic

### Payroll-adjacent metrics

Whitelisted methods in Service Visit:

1. get_monthly_visit_count(beneficiary, month)
2. get_specialist_monthly_service_units(specialist, month)

These methods provide a clean integration point for future payroll calculations based on service delivery counts.

## 9) Installation and Setup

### Prerequisites

1. Frappe Bench with ERPNext version-15
2. Site created (example: <site-name>)
3. App installed on site

### Install App

Run from bench root:

```bash
bench get-app <REPO_URL> --branch main
bench --site <site-name> install-app asb_case_mgmt
bench --site <site-name> migrate
```

### Required baseline masters for HR flows

For Employee creation to work, ensure these masters exist:

1. Company
2. Gender records
3. Warehouse Type Transit (needed by ERPNext company setup side-effects)

## 10) Running the Site Locally

Start services:

```bash
cd /path/to/frappe-bench
bench start
```

Open:

1. Login: http://127.0.0.1:8000/login
2. Workspace: http://127.0.0.1:8000/app/ssk-center-home

## 11) Migrations and Patches

Patches currently registered:

1. asb_case_mgmt.patches.v1_0.create_base_roles
2. asb_case_mgmt.patches.v1_0.setup_employee_linkage
3. asb_case_mgmt.patches.v1_0.set_home_workspace
4. asb_case_mgmt.patches.v1_0.setup_visit_assessment_alignment
5. asb_case_mgmt.patches.v1_0.setup_payroll_monthly_summary
6. asb_case_mgmt.patches.v1_0.setup_fiscal_year_baseline
7. asb_case_mgmt.patches.v1_0.setup_stock_baseline
8. asb_case_mgmt.patches.v1_0.setup_asset_baseline
9. asb_case_mgmt.patches.v1_0.rename_asb_to_ssk
10. asb_case_mgmt.patches.v1_0.register_georgian_language

After pulling updates:

```bash
cd /path/to/frappe-bench
bench --site <site-name> migrate
```

### Deployment and Handover Docs

- [PROD_DEPLOY.md](PROD_DEPLOY.md)
- [RELEASE_NOTES.md](RELEASE_NOTES.md)
- [FINAL_HANDOVER.md](FINAL_HANDOVER.md)
- [docs/BASELINE_DATA.md](docs/BASELINE_DATA.md)
- [UAT_STATUS.md](UAT_STATUS.md)

## 12) End-to-End Testing Guide

Recommended UAT sequence:

1. Create a Center
2. Create an Employee and set asb_center
3. Create Beneficiary and assign specialist in child table
4. Create Service Visit for beneficiary and specialist
5. Create Initial Assessment with domain scores
6. Create Individual Plan with one or more goals
7. Login as specialist user and verify scoped visibility

### Functional checks

1. Beneficiary age is auto-computed
2. Specialist cannot create visit for unassigned beneficiary
3. Assessment repeated or final requires prior assessment
4. Specialist and coordinator land on SSK Center Home
5. Center and specialist data filters are enforced in lists

### API checks

```bash
bench --site <site-name> execute asb_case_mgmt.asb_center.doctype.service_visit.service_visit.get_monthly_visit_count --kwargs "{'beneficiary':'<BENEFICIARY_ID>','month':'2026-04'}"
bench --site <site-name> execute asb_case_mgmt.asb_center.doctype.service_visit.service_visit.get_specialist_monthly_service_units --kwargs "{'specialist':'<EMPLOYEE_ID>','month':'2026-04'}"
```

## 13) Troubleshooting

### bench start fails with Redis port already in use

Symptom:

1. Address already in use on port 11000 or 13000

Fix:

```bash
pkill -f "redis-server 127.0.0.1:11000"
pkill -f "redis-server 127.0.0.1:13000"
cd /path/to/frappe-bench
bench start
```

### migrate fails saying redis_cache is not running

1. Ensure bench services are running before migrate.
2. Run bench start in one terminal, then run migrate in another terminal.

### Employee creation fails on missing links

Likely missing baseline ERPNext records (Company, Gender, Warehouse Type Transit).

## 14) File and Code Map

Core app files:

1. App hooks
	- asb_case_mgmt/hooks.py
2. Permission logic
	- asb_case_mgmt/permissions.py
3. Shared utility functions
	- asb_case_mgmt/asb_center/utils.py
4. Workspace
	- asb_case_mgmt/asb_center/workspace/asb_center_home/asb_center_home.json
5. Patches
	- asb_case_mgmt/patches/v1_0 (see patches.txt for the ordered list)

DocTypes:

1. Center
2. Beneficiary
3. Beneficiary Specialist
4. Service Visit
5. Assessment
6. Assessment Domain Score
7. Individual Plan
8. Individual Plan Goal

All DocType definitions live under:

1. asb_case_mgmt/asb_center/doctype/<doctype_name>

## 15) Roadmap

Next planned scope:

1. Advanced inventory flows (consumables, expiry tracking, distribution reporting)
2. Extended asset lifecycle workflows (maintenance scheduling, depreciation automation)
3. Payroll mapping from monthly service units to Salary Slip logic
4. Additional dashboards and reports

## 16) Contributing

### Local development workflow

```bash
cd /path/to/frappe-bench/apps/asb_case_mgmt
pre-commit install
```

Tooling configured:

1. ruff
2. eslint
3. prettier
4. pyupgrade

### Best-practice guidelines for this app

1. Keep nonprofit logic inside this app.
2. Prefer ERPNext extension patterns over core forks.
3. Keep migrations idempotent and patch-safe.
4. Preserve compatibility with Frappe and ERPNext version-15.

## 17) License

MIT
