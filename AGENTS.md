# AI Agent Repo Guide

## Quick Summary
- This is a Frappe/ERPNext bench with a custom app named asb_case_mgmt.
- Branding is SSK, but the Python package name remains asb_case_mgmt.
- Primary local site for validation is asb.localhost.

## Key Paths
- App code: apps/asb_case_mgmt/asb_case_mgmt
- Module folder: apps/asb_case_mgmt/asb_case_mgmt/asb_center
- Module alias for migrations: apps/asb_case_mgmt/asb_case_mgmt/ssk_center
- Docs: apps/asb_case_mgmt/docs
- Patches: apps/asb_case_mgmt/asb_case_mgmt/patches
- Tests: apps/asb_case_mgmt/asb_case_mgmt/tests
- Scripts: apps/asb_case_mgmt/asb_case_mgmt/scripts

## Core Domain Objects
- Center: service hub that scopes users, beneficiaries, stock, and assets.
- Beneficiary: person receiving services; linked to a center and specialists.
- Individual Plan: active goals and plan for a beneficiary.
- Service Visit: logged service interactions with units and visit month.
- Assessment: baseline and repeated evaluations with cycle tracking.

## Roles and Workspace
- Roles: SSK Center Coordinator, SSK Specialist, System Manager.
- Workspace: SSK Center Home at /app/ssk-center-home.

## Common Commands

```
bench --site asb.localhost migrate
bench --site asb.localhost clear-cache
bench --site asb.localhost clear-website-cache
bench build
bench --site asb.localhost backup
bench --site asb.localhost console
```

## Key Docs
- App overview: apps/asb_case_mgmt/README.md
- Deployment: apps/asb_case_mgmt/PROD_DEPLOY.md
- Handover: apps/asb_case_mgmt/FINAL_HANDOVER.md
- Baseline data: apps/asb_case_mgmt/docs/BASELINE_DATA.md
- UAT checklist: apps/asb_case_mgmt/docs/UAT_CHECKLIST.md
- UAT steps: apps/asb_case_mgmt/docs/UAT_BROWSER_MANUAL_SCRIPT.md
- Demo dataset: apps/asb_case_mgmt/docs/DEMO_DATASET.md
- Demo commands: apps/asb_case_mgmt/docs/DEMO_SEED_COMMANDS.md

## Known Pitfalls
- Migrations expect a module named ssk_center; the alias path exists to satisfy imports.
- The rename patch is in apps/asb_case_mgmt/asb_case_mgmt/patches/v1_0/rename_asb_to_ssk.py.
- Demo seeding is gated to developer mode in apps/asb_case_mgmt/asb_case_mgmt/scripts/seed_demo_data.py.
