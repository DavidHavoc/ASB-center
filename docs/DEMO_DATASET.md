# SSK Case Management Demo Dataset (Non-Production)

This dataset is for UAT/demo environments only. Do not load it on production sites.

This dataset is designed for a client demo and UAT walkthrough.

It creates:

- 2 Centers
- 3 Employees
- 5 Beneficiaries

Location theme:

- Tbilisi, Georgia
- Georgian names used for the demo records

## 1) Centers

### Center A
- Name: SSK Tbilisi Vake Center
- Description: Main urban service center in Tbilisi
- Address: Tbilisi - Vake
- Phone: +995599000001
- Email: tbilisi.vake.center@example.invalid

### Center B
- Name: SSK Tbilisi Saburtalo Center
- Description: Secondary service center in Tbilisi
- Address: Tbilisi - Saburtalo
- Phone: +995599000002
- Email: tbilisi.saburtalo.center@example.invalid

## 2) Employees

### Employee 1
- First Name: Nino
- Last Name: Beridze
- Gender: Female
- Date of Birth: 1990-05-14
- Date of Joining: 2026-04-01
- Company: SSK Foundation
- User ID: nino.specialist@example.invalid
- Center: SSK Tbilisi Vake Center
- Contract Number: SSK-TBS-EMP-001

### Employee 2
- First Name: Giorgi
- Last Name: Kapanadze
- Gender: Male
- Date of Birth: 1992-11-03
- Date of Joining: 2026-04-01
- Company: SSK Foundation
- User ID: giorgi.specialist@example.invalid
- Center: SSK Tbilisi Vake Center
- Contract Number: SSK-TBS-EMP-002

### Employee 3
- First Name: Ana
- Last Name: Mchedlidze
- Gender: Female
- Date of Birth: 1988-08-22
- Date of Joining: 2026-04-01
- Company: SSK Foundation
- User ID: ana.specialist@example.invalid
- Center: SSK Tbilisi Saburtalo Center
- Contract Number: SSK-TBS-EMP-003

## 3) Beneficiaries

### Beneficiary 1
- Beneficiary Code: BEN-DEMO-0001
- Full Name: Nino Gelashvili
- Service Type: Disability Support
- Service Status: Active
- Center: SSK Tbilisi Vake Center
- Responsible Specialist: Nino
- Birth Date: 2011-06-20

### Beneficiary 2
- Beneficiary Code: BEN-DEMO-0002
- Full Name: Luka Chikovani
- Service Type: Child Protection
- Service Status: Active
- Center: SSK Tbilisi Vake Center
- Responsible Specialist: Giorgi
- Birth Date: 2016-02-12

### Beneficiary 3
- Beneficiary Code: BEN-DEMO-0003
- Full Name: Elene Qavlashvili
- Service Type: Rehabilitation
- Service Status: Active
- Center: SSK Tbilisi Vake Center
- Responsible Specialist: Nino
- Birth Date: 2008-09-30

### Beneficiary 4
- Beneficiary Code: BEN-DEMO-0004
- Full Name: Saba Tsertsvadze
- Service Type: Social Protection
- Service Status: Active
- Center: SSK Tbilisi Saburtalo Center
- Responsible Specialist: Ana
- Birth Date: 2014-01-18

### Beneficiary 5
- Beneficiary Code: BEN-DEMO-0005
- Full Name: Mariam Dvalishvili
- Service Type: Disability Support
- Service Status: Active
- Center: SSK Tbilisi Saburtalo Center
- Responsible Specialist: Ana
- Birth Date: 2012-12-05

## 4) Recommended Demo Flow

1. Open SSK Center Home
2. Show Center list
3. Open Employee records and point out center and contract fields
4. Open Beneficiary records and show specialist assignment
5. Create or show Service Visit records
6. Create or show Assessment records
7. Create or show Individual Plan records
8. Log in as specialist and show limited visibility

## 5) Suggested Seed Values for Visits and Assessments

- Visit Date: 2026-04-09
- Assessment Date: 2026-04-09
- Assessment Type: Initial
- Scoring Tool: Barthel
- Service Units: 1

## 6) Notes

1. This dataset is intentionally simple for demo clarity.
2. It is safe to reuse in a fresh site after migrate.
3. Names can be changed without affecting the structure.
4. On an existing test site, the seed script updates matching demo records in place.
