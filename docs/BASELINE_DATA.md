# Baseline Data and Patches

This document lists the baseline data created or updated by migration patches.

## Roles and Home Pages

- Roles: SSK Center Coordinator, SSK Specialist
- Role home pages: /app/ssk-center-home

## Workspace

- Workspace: SSK Center Home
- Route: /app/ssk-center-home

## Employee Linkage

Custom fields added to Employee:

- asb_center (Link to Center)
- asb_contract_number
- asb_contract_start_date
- asb_contract_end_date
- asb_contract_attachment

## Visit and Assessment Alignment

- Updates legacy scoring tool values from "AEPS" to "AEPS (New)" when present.
- Backfills previous assessment links for repeated/final assessments when missing.

## Monthly Specialist Summary

- Builds or updates Specialist Monthly Service Summary rows from Service Visit data.

## Fiscal Years

- Ensures fiscal years for the current year and next year exist.
- Sets the default fiscal year on the selected company when possible.

## Stock Baseline

- Custom fields: Warehouse.asb_center, Stock Entry.asb_center, Batch.asb_center
- UOMs: Nos, Box, Kg, Litre, Set
- Item Groups: SSK Supplies, SSK Consumables, SSK Medical Supplies, SSK Assistive Devices
- Stock Entry Types: Material Issue, Material Receipt, Material Transfer, Material Transfer for Manufacture,
  Material Consumption for Manufacture, Manufacture, Repack, Send to Subcontractor, Disassemble
- Center warehouses created under the company root warehouse for each active Center
- Stock Settings: auto_create_new_batch enabled

## Asset Baseline

- Custom fields: Location.asb_center, Asset.asb_center, Asset.asb_beneficiary,
  Asset.asb_maintenance_frequency_months, Asset.asb_next_maintenance_date
- Center locations created for each active Center
- Asset Categories: SSK Assistive Devices, SSK IT Equipment, SSK Facility Assets

## Localization

- Language registration: ka (Georgian)
- Translation file: asb_case_mgmt/translations/ka.csv

## Legacy Rename (ASB to SSK)

- Renames roles, module, workspace, company, item groups, and asset categories from ASB to SSK where present.
