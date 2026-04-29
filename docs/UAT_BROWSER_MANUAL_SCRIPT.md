# Manual Browser UAT Script for asb.localhost

Date: 2026-04-16
Target URL: http://asb.localhost
Scope: Role-based browser testing for Admin, Center Coordinator, and Specialist with positive and negative cases.

UAT run identifier to use in this script: BROWSER-UAT-20260416

Exact test records used by this script:
- UAT Center: UAT Browser Center 20260416
- UAT Coordinator User: uat.coordinator.20260416@asb.localhost
- UAT Specialist Vake User: uat.specialist.vake.20260416@asb.localhost
- UAT Specialist Saburtalo User: uat.specialist.saburtalo.20260416@asb.localhost
- UAT Password for created users: Uat@2026!
- UAT Employee Coordinator: UAT Coordinator Vake 20260416
- UAT Employee Specialist Vake: UAT Specialist Vake 20260416
- UAT Employee Specialist Saburtalo: UAT Specialist Saburtalo 20260416
- UAT Beneficiary Vake Code: BEN-UAT-BROWSER-0001
- UAT Beneficiary Saburtalo Code: BEN-UAT-BROWSER-0002
- UAT Beneficiary Coordinator Code: BEN-UAT-BROWSER-COORD-01
- UAT Stock Item: UAT-STOCK-BROWSER-20260416
- UAT Batch: BATCH-UAT-BROWSER-20260416
- UAT Asset Item: UAT-ASSET-ITEM-BROWSER-20260416
- UAT Asset Name: UAT Asset Browser 20260416

Existing records referenced:
- Center A: ASB Tbilisi Vake Center
- Center B: ASB Tbilisi Saburtalo Center
- Center A Warehouse: ASB Tbilisi Vake Center Stock - ASB
- Center B Warehouse: ASB Tbilisi Saburtalo Center Stock - ASB
- Center A Location: ASB Tbilisi Vake Center Location
- Center B Location: ASB Tbilisi Saburtalo Center Location
- Existing Beneficiary in Center B: BEN-DEMO-0004

## 1) Admin Test Steps

1. Menu path: Login page at /login | Record: Administrator account | Action: Sign in with Administrator credentials. | Expected result: Desk opens without errors. | Failure: Login fails or Desk does not load.
2. Menu path: Desk > ASB Center Home at /app/asb-center-home | Record: ASB Center Home workspace | Action: Open workspace and verify shortcuts for Center, Beneficiary, Service Visit, Assessment, Individual Plan. | Expected result: All shortcuts are visible and clickable. | Failure: Any shortcut missing or broken.
3. Menu path: Desk > Search > Center at /app/center | Record: UAT Browser Center 20260416 | Action: Create a new Center with address, phone, email, active flag. | Expected result: Center saves and appears in list. | Failure: Save blocked unexpectedly or center missing from list.
4. Menu path: Desk > User and Permissions > User at /app/user | Record: uat.coordinator.20260416@asb.localhost | Action: Create user, assign role ASB Center Coordinator, set password Uat@2026!. | Expected result: User enabled with role assigned. | Failure: User not created, role missing, or password cannot be set.
5. Menu path: Desk > User and Permissions > User at /app/user | Record: uat.specialist.vake.20260416@asb.localhost and uat.specialist.saburtalo.20260416@asb.localhost | Action: Create both users, assign role ASB Specialist, set password Uat@2026!. | Expected result: Both users created and enabled. | Failure: Either user missing role or cannot log in.
6. Menu path: Desk > Human Resources > Employee at /app/employee | Record: UAT Coordinator Vake 20260416 | Action: Create Employee linked to uat.coordinator.20260416@asb.localhost with Center A and contract fields filled. | Expected result: Employee saves with ASB Center and contract data. | Failure: Employee does not save or ASB fields not persisted.
7. Menu path: Desk > Human Resources > Employee at /app/employee | Record: UAT Specialist Vake 20260416 | Action: Create Employee linked to uat.specialist.vake.20260416@asb.localhost with Center A and contract fields filled. | Expected result: Employee saves with Center A. | Failure: Save fails or center field empty.
8. Menu path: Desk > Human Resources > Employee at /app/employee | Record: UAT Specialist Saburtalo 20260416 | Action: Create Employee linked to uat.specialist.saburtalo.20260416@asb.localhost with Center B and contract fields filled. | Expected result: Employee saves with Center B. | Failure: Save fails or wrong center saved.
9. Menu path: Desk > ASB Center Home > Beneficiary at /app/beneficiary | Record: BEN-UAT-BROWSER-0001 | Action: Create Beneficiary in Center A, assign UAT Specialist Vake in Responsible Specialists table. | Expected result: Beneficiary saves, age and age category auto-fill. | Failure: Save fails, specialist not retained, or age fields not computed.
10. Menu path: Desk > ASB Center Home > Beneficiary at /app/beneficiary | Record: BEN-UAT-BROWSER-0002 | Action: Create Beneficiary in Center B, assign UAT Specialist Saburtalo. | Expected result: Beneficiary saves in Center B with specialist assignment. | Failure: Save fails or center/specialist mismatch is accepted incorrectly.
11. Menu path: Desk > ASB Center Home > Individual Plan at /app/individual-plan | Record: Plan for BEN-UAT-BROWSER-0001 | Action: Create Active plan with at least one goal. | Expected result: Plan saves successfully. | Failure: Active plan with valid goal cannot be saved.
12. Menu path: Desk > ASB Center Home > Individual Plan at /app/individual-plan | Record: Plan for BEN-UAT-BROWSER-0001 | Action: Try to create Active plan without goals. | Expected result: Validation blocks save. | Failure: Active plan saves without goals.
13. Menu path: Desk > ASB Center Home > Service Visit at /app/service-visit | Record: Visit for BEN-UAT-BROWSER-0001 | Action: Create Completed visit with Visit Type Community Outreach and Service Units 1. | Expected result: Center auto-fills from beneficiary and visit month auto-generates as YYYY-MM. | Failure: Center not auto-filled, wrong center, or visit month missing.
14. Menu path: Desk > ASB Center Home > Assessment at /app/assessment | Record: Initial assessment for BEN-UAT-BROWSER-0001 | Action: Create Initial assessment with Scoring Tool AEPS (Old) and one Domain Score row. | Expected result: Assessment saves with cycle number 1. | Failure: Initial assessment fails despite valid data.
15. Menu path: Desk > ASB Center Home > Assessment at /app/assessment | Record: Repeated assessment for BEN-UAT-BROWSER-0001 | Action: Create Repeated assessment, set Previous Assessment to the initial one, use Scoring Tool AEPS (New), add domain row. | Expected result: Saves with cycle number 2 and previous assessment reference. | Failure: Save blocked incorrectly or cycle/previous link missing.
16. Menu path: Desk > ASB Center Home > Assessment at /app/assessment | Record: Repeated assessment for BEN-UAT-BROWSER-0002 | Action: Try to create Repeated assessment without Previous Assessment. | Expected result: Validation blocks save with previous assessment required message. | Failure: Repeated assessment saves without previous link.
17. Menu path: Desk > Search > Specialist Monthly Service Summary at /app/specialist-monthly-service-summary | Record: Summary row for UAT Specialist Vake for current month | Action: Open list and filter Specialist = UAT Specialist Vake employee and Summary Month = current month. | Expected result: Row exists and totals reflect completed visits created in UAT. | Failure: No row generated or totals do not change after new visits.
18. Menu path: Desk > Stock > Item at /app/item | Record: UAT-STOCK-BROWSER-20260416 | Action: Create Item with Has Batch No enabled, Has Expiry Date enabled, Shelf Life set, Item Group ASB Medical Supplies, UOM Nos. | Expected result: Item saves and is usable in stock transactions. | Failure: Item cannot save with required stock settings.
19. Menu path: Desk > Stock > Batch at /app/batch | Record: BATCH-UAT-BROWSER-20260416 | Action: Create Batch for UAT stock item, set expiry date in future, set ASB Center to Center A. | Expected result: Batch saves with expiry and center. | Failure: Batch not created or center/expiry not saved.
20. Menu path: Desk > Stock > Stock Entry at /app/stock-entry | Record: Material Receipt for UAT stock item | Action: Create Material Receipt to Center A Warehouse with batch and qty 5, submit. | Expected result: Document submits with docstatus 1. | Failure: Submission fails for valid same-center transaction.
21. Menu path: Desk > Stock > Stock Entry at /app/stock-entry | Record: Material Issue for UAT stock item | Action: Create Material Issue from Center A Warehouse with same batch and qty 2, submit. | Expected result: Document submits with docstatus 1. | Failure: Submission fails for valid same-center transaction.
22. Menu path: Desk > Stock > Stock Entry at /app/stock-entry | Record: Material Transfer cross-center test | Action: Try transfer from Center A Warehouse to Center B Warehouse for UAT item. | Expected result: Validation blocks save due to cross-center scope mismatch. | Failure: Cross-center transfer is accepted.
23. Menu path: Desk > Assets > Asset at /app/asset | Record: UAT-ASSET-ITEM-BROWSER-20260416 | Action: Create fixed asset Item with Asset Category ASB IT Equipment. | Expected result: Item saves and can be used in Asset document. | Failure: Fixed asset item cannot be created.
24. Menu path: Desk > Assets > Asset at /app/asset | Record: UAT Asset Browser 20260416 | Action: Create Asset with Company ASB Foundation, Item Code UAT-ASSET-ITEM-BROWSER-20260416, Location Center A Location, Purchase Date today, Gross Purchase Amount, ASB Center Center A, maintenance fields filled. | Expected result: Asset saves and center link persists. | Failure: Asset not saved or ASB Center not retained.
25. Menu path: Desk > Assets > Asset at /app/asset | Record: Invalid cross-center asset | Action: Create Asset in Center A and set Beneficiary BEN-DEMO-0004 (Center B). | Expected result: Validation blocks save with center mismatch message. | Failure: Asset saves with beneficiary from another center.

## 2) Center Coordinator Test Steps

1. Menu path: Login page at /login | Record: uat.coordinator.20260416@asb.localhost | Action: Log in with Uat@2026!. | Expected result: Lands on ASB Center Home workspace. | Failure: Login fails or wrong home page.
2. Menu path: Desk > ASB Center Home > Beneficiary at /app/beneficiary | Record: BEN-DEMO-0001, BEN-DEMO-0002, BEN-DEMO-0003 | Action: Verify these Center A records are visible in list. | Expected result: Center A records visible. | Failure: Center A records missing.
3. Menu path: Desk > ASB Center Home > Beneficiary at /app/beneficiary | Record: BEN-DEMO-0004 | Action: Search for BEN-DEMO-0004 and attempt to open direct URL /app/beneficiary/BEN-DEMO-0004. | Expected result: Access denied or record hidden. | Failure: Coordinator can open Center B beneficiary.
4. Menu path: Desk > ASB Center Home > Beneficiary at /app/beneficiary | Record: BEN-UAT-BROWSER-COORD-01 | Action: Create beneficiary in Center A with UAT Specialist Vake assigned. | Expected result: Beneficiary saves and appears in list. | Failure: Cannot save valid Center A beneficiary.
5. Menu path: Desk > ASB Center Home > Beneficiary at /app/beneficiary | Record: BEN-UAT-BROWSER-COORD-01 | Action: Edit Responsible Specialists and try to add UAT Specialist Saburtalo (Center B). | Expected result: Validation blocks save due to specialist center mismatch. | Failure: Cross-center specialist assignment is accepted.
6. Menu path: Desk > ASB Center Home > Individual Plan at /app/individual-plan | Record: Plan for BEN-UAT-BROWSER-COORD-01 | Action: Create Active plan with one goal. | Expected result: Plan saves. | Failure: Valid plan cannot be saved.
7. Menu path: Desk > ASB Center Home > Service Visit at /app/service-visit | Record: Visit for BEN-UAT-BROWSER-COORD-01 | Action: Create Completed visit and save. | Expected result: Visit saves with center in Coordinator scope. | Failure: Save fails for valid center-scoped visit.
8. Menu path: Desk > ASB Center Home > Assessment at /app/assessment | Record: Initial assessment for BEN-UAT-BROWSER-COORD-01 | Action: Create Initial assessment with one domain row and scoring tool Barthel. | Expected result: Assessment saves. | Failure: Valid initial assessment fails.
9. Menu path: Desk > Search > Specialist Monthly Service Summary at /app/specialist-monthly-service-summary | Record: UAT Specialist Vake monthly row | Action: Filter by Center A and current month. | Expected result: Center A summary rows are visible. | Failure: No center row visible after completed visits.
10. Menu path: Desk > Search > Specialist Monthly Service Summary at /app/specialist-monthly-service-summary | Record: SMS-2026-00001 or any non-Center-A row | Action: Open direct URL of row from another center. | Expected result: Access denied. | Failure: Coordinator can open summary row from another center.

## 3) Specialist Test Steps

1. Menu path: Login page at /login | Record: uat.specialist.vake.20260416@asb.localhost | Action: Log in with Uat@2026!. | Expected result: Lands on ASB Center Home workspace. | Failure: Login fails or wrong home page.
2. Menu path: Desk > ASB Center Home > Beneficiary at /app/beneficiary | Record: BEN-UAT-BROWSER-0001 and BEN-UAT-BROWSER-COORD-01 | Action: Verify assigned beneficiaries are visible. | Expected result: Assigned records visible. | Failure: Assigned records missing.
3. Menu path: Desk > ASB Center Home > Beneficiary at /app/beneficiary | Record: BEN-DEMO-0004 | Action: Search BEN-DEMO-0004 and attempt direct URL /app/beneficiary/BEN-DEMO-0004. | Expected result: Record is not visible or access denied. | Failure: Specialist can open unassigned cross-center record.
4. Menu path: Desk > ASB Center Home > Service Visit at /app/service-visit | Record: Visit for BEN-UAT-BROWSER-0001 | Action: Create Completed visit with Visit Type Case Conference and Service Units 1. | Expected result: Visit saves. | Failure: Valid assigned visit cannot be created.
5. Menu path: Desk > ASB Center Home > Assessment at /app/assessment | Record: Initial and Repeated for BEN-UAT-BROWSER-0001 | Action: Create Initial assessment with domain row, then create Repeated linked to Previous Assessment. | Expected result: Both save and repeated links correctly. | Failure: Valid repeated assessment flow fails.
6. Menu path: Desk > ASB Center Home > Assessment at /app/assessment | Record: Repeated without previous | Action: Attempt Repeated assessment without Previous Assessment. | Expected result: Validation blocks save. | Failure: Repeated saves without previous assessment.
7. Menu path: Desk > ASB Center Home > Service Visit at /app/service-visit | Record: Visit for BEN-DEMO-0004 | Action: Attempt to create visit for BEN-DEMO-0004. | Expected result: Save blocked by permission or assignment validation. | Failure: Specialist can create cross-center unassigned visit.
8. Menu path: Desk > Search > Specialist Monthly Service Summary at /app/specialist-monthly-service-summary | Record: Current month row for UAT Specialist Vake employee | Action: Filter by current month and specialist. | Expected result: Summary row visible with updated service units and visit count. | Failure: Summary not visible or not updated.

## 4) Cleanup Plan (Keep Baseline Masters and Production Setup)

Objective: Remove only temporary UAT verification records created by this script and keep all baseline masters and production-required setup.

Records to delete (only names/codes from this script):
- Center: UAT Browser Center 20260416
- Users: uat.coordinator.20260416@asb.localhost, uat.specialist.vake.20260416@asb.localhost, uat.specialist.saburtalo.20260416@asb.localhost
- Employees: UAT Coordinator Vake 20260416, UAT Specialist Vake 20260416, UAT Specialist Saburtalo 20260416
- Beneficiaries: BEN-UAT-BROWSER-0001, BEN-UAT-BROWSER-0002, BEN-UAT-BROWSER-COORD-01
- Individual Plans created for these beneficiaries
- Service Visits created for these beneficiaries
- Assessments created for these beneficiaries
- Specialist Monthly Service Summary rows tied only to deleted specialist employees and month if orphaned
- Stock Item: UAT-STOCK-BROWSER-20260416
- Batch: BATCH-UAT-BROWSER-20260416
- Stock Entries containing UAT-STOCK-BROWSER-20260416 (cancel submitted docs first, then delete)
- Asset Item: UAT-ASSET-ITEM-BROWSER-20260416
- Asset: UAT Asset Browser 20260416 and other UAT assets created in this run

Safe deletion order:
1. Delete Repeated and Initial Assessments for UAT beneficiaries.
2. Delete Service Visits for UAT beneficiaries.
3. Delete Individual Plans for UAT beneficiaries.
4. Delete UAT Beneficiaries.
5. Cancel and delete UAT Stock Entries, then delete UAT Batch, then delete UAT Stock Item.
6. Delete UAT Assets, then delete UAT fixed asset item.
7. Delete UAT Employees.
8. Delete UAT Users.
9. Delete UAT Center.
10. Delete orphan Specialist Monthly Service Summary rows for removed specialist employees if present.

Do not delete these baseline and production-required records:
- Centers: ASB Main Center, ASB Tbilisi Vake Center, ASB Tbilisi Saburtalo Center
- Demo beneficiaries and employees with BEN-DEMO and ASB-TBS-EMP identifiers
- UOM baseline set (Nos, Box, Kg, Litre, Set)
- ASB item groups under ASB Supplies
- Stock Entry Type baseline set
- Fiscal Years 2026 and 2027
- Center-linked warehouses and center-linked locations
- Asset categories: ASB Assistive Devices, ASB IT Equipment, ASB Facility Assets
- All ASB custom fields on Employee, Warehouse, Stock Entry, Batch, Location, Asset
- Specialist Monthly Service Summary DocType and permissions/hooks setup
