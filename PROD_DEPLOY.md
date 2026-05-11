# SSK Case Management Production Deployment

This guide covers clean production rollout and upgrades for the asb_case_mgmt app.

## Prerequisites

- ERPNext v15 bench with required services (redis, queue, scheduler) running.
- A site created for production (example: <site-name>).
- A Company record named "SSK Foundation" exists, or the site has exactly one Company.
  - If multiple companies exist and "SSK Foundation" is missing, baseline patches skip company-scoped setup.

## Clean Install (new site)

From the bench root:

```bash
bench get-app <REPO_URL> --branch main
bench --site <site-name> install-app asb_case_mgmt
bench --site <site-name> migrate
bench --site <site-name> clear-cache
```

Restart services (choose your process manager):

```bash
bench restart
```

## Upgrade (existing site)

```bash
git pull
bench --site <site-name> migrate
bench --site <site-name> clear-cache
bench restart
```

## Post-Deploy Checks

1. Log in as Administrator and open /app/ssk-center-home.
2. Confirm roles exist: SSK Center Coordinator, SSK Specialist.
3. Confirm Georgian language is available (Language list includes code "ka").
4. Confirm custom fields exist on Employee, Warehouse, Stock Entry, Batch, Location, and Asset.
5. Confirm baseline masters:
   - UOMs: Nos, Box, Kg, Litre, Set
   - Item Groups: SSK Supplies, SSK Consumables, SSK Medical Supplies, SSK Assistive Devices
   - Stock Entry Types listed in BASELINE_DATA.md
   - Asset Categories: SSK Assistive Devices, SSK IT Equipment, SSK Facility Assets
6. Create a Center, Beneficiary, Service Visit, Assessment, and Individual Plan to validate workflows.

## Optional: Re-run Baseline Patches

If you add new centers and need warehouses/locations, re-run:

```bash
bench --site <site-name> execute asb_case_mgmt.patches.v1_0.setup_stock_baseline.execute
bench --site <site-name> execute asb_case_mgmt.patches.v1_0.setup_asset_baseline.execute
```

If migrating from legacy ASB naming, ensure migrate completes so rename_asb_to_ssk runs.
