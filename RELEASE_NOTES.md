# Release Notes - SSK Case Management 1.0.0

Date: 2026-05-04

## Highlights

- Core case management DocTypes: Center, Beneficiary, Service Visit, Assessment, Individual Plan.
- Specialist monthly service summary with center-scoped permissions.
- Stock and asset center-scope validation with baseline masters.
- Georgian language registration and translation coverage for the app layer.
- Migration patch set hardened for idempotency and safe reruns.

## Upgrade Notes

- Run `bench --site <site-name> migrate` after pulling changes.
- Ensure a Company named "SSK Foundation" exists (or only one company is present) before migrate.
- For newly added centers, re-run the stock and asset baseline patches if you need auto-created warehouses/locations.

## Known Limitations

- Warehouses and locations are created by baseline patches for existing centers only; new centers require manual setup or re-running the patches.
- Payroll integration is limited to monthly summary aggregation and is not wired into Salary Slip logic yet.
