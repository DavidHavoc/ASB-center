# Demo Seed Commands (Non-Production)

Use this only with a clean bench or a non-production test site. The seed script is blocked unless developer mode is enabled.

## Run the seed script

From bench root:

```bash
bench --site <site-name> execute asb_case_mgmt.scripts.seed_demo_data.execute
```

## What it creates

1. 2 Centers
2. 3 Employees
3. 5 Beneficiaries

## Demo identity layout

1. Tbilisi Vake Center: Nino and Giorgi
2. Tbilisi Saburtalo Center: Ana
3. Beneficiaries are distributed across both centers for permission testing
4. On an existing test site, the script updates matching demo records in place instead of creating duplicates.
