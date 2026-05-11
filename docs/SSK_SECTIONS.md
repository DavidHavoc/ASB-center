# SSK Sections Guide

This guide explains the main workflow sections in SSK Case Management and how they are used together.

## Center
- Purpose: A service hub that scopes users, beneficiaries, stock, and assets.
- Used when: Setting up operations for a new location.
- Key fields: Center name, contact info, active status.
- Dependencies: Employees and beneficiaries link to a center.

## Beneficiary
- Purpose: The person receiving services. Core record for all service workflows.
- Used when: Enrolling someone to receive support from a specific center.
- Key fields: Beneficiary code, center, service type/status, responsible specialists.
- Dependencies: Requires a center; specialist assignments drive permissions.

## Individual Plan
- Purpose: The care plan and goals for a beneficiary.
- Used when: Defining active goals and planned services.
- Key fields: Beneficiary, specialist, plan start date, goals.
- Dependencies: Requires a beneficiary and specialist; active plans require at least one goal.

## Service Visit
- Purpose: A recorded service interaction delivered to a beneficiary.
- Used when: Logging completed visits and service units.
- Key fields: Beneficiary, specialist, visit date, visit type, service units.
- Behavior: Center and visit month auto-populate from beneficiary and date.

## Assessment
- Purpose: Track baseline and follow-up evaluations for progress.
- Used when: Recording initial and repeated assessments over time.
- Key fields: Beneficiary, specialist, assessment type, scoring tool, domain scores.
- Behavior: Repeated assessments must reference the previous assessment to increment cycle.
