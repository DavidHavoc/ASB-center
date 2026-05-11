# Final Handover - SSK Case Management Phase 1

## Scope

Phase 1 delivers core SSK case-management workflows on top of ERPNext v15 without forking core ERPNext.

## Included

- DocTypes: Center, Beneficiary, Service Visit, Assessment, Individual Plan, Specialist Monthly Service Summary.
- Custom fields on Employee, Warehouse, Stock Entry, Batch, Location, and Asset.
- Permission logic for center and specialist scoping.
- Baseline masters and setup patches (see docs/BASELINE_DATA.md).
- Georgian language registration and translations for the app layer.
- Production deployment steps (PROD_DEPLOY.md).

## Not Included

- Demo/UAT data on production sites.
- Automatic payroll Salary Slip integration.
- Automatic warehouse/location creation on new Center creation (manual or patch rerun required).

## Operational Notes

- Roles required: SSK Center Coordinator, SSK Specialist, System Manager.
- Ensure Company "SSK Foundation" exists before running baseline patches.
- The demo seed script is restricted to developer mode and should never be used in production.

## Key Docs

- README.md
- PROD_DEPLOY.md
- docs/BASELINE_DATA.md
- UAT_STATUS.md
