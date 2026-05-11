# SSK Case Management UAT Checklist

This checklist is for client demonstrations and acceptance testing.

## 1) Environment Readiness

- [ ] Site opens at `/login`
- [ ] `SSK Center Home` workspace opens at `/app/ssk-center-home`
- [ ] `SSK Specialist` and `SSK Center Coordinator` roles exist
- [ ] `Center`, `Beneficiary`, `Service Visit`, `Assessment`, and `Individual Plan` DocTypes exist
- [ ] Redis and bench services are running

## 2) Master Data Setup

- [ ] Create 2 Centers
- [ ] Create 3 Employees
- [ ] Link each Employee to a Center
- [ ] Create 5 Beneficiaries
- [ ] Assign each Beneficiary to a responsible specialist

## 3) Center Workflow

- [ ] Create a center with name, description, address, phone, and email
- [ ] Verify center name appears in list view
- [ ] Verify center opens from the home page shortcut

## 4) Employee Workflow

- [ ] Create an Employee record
- [ ] Set `SSK Center`
- [ ] Add contract number
- [ ] Add contract start and end dates
- [ ] Upload contract attachment

## 5) Beneficiary Workflow

- [ ] Create a Beneficiary
- [ ] Set service type and service status
- [ ] Add personal details
- [ ] Assign at least one specialist in the child table
- [ ] Confirm age auto-calculates from birth date
- [ ] Confirm age category auto-fills

## 6) Visit Workflow

- [ ] Create a Service Visit
- [ ] Select beneficiary and specialist
- [ ] Confirm center auto-fills from beneficiary
- [ ] Save a completed visit
- [ ] Confirm visit month auto-generates as `YYYY-MM`

## 7) Assessment Workflow

- [ ] Create Initial Assessment
- [ ] Add one or more domain rows
- [ ] Confirm scoring tool selection works
- [ ] Create Repeated Assessment after the initial one exists
- [ ] Confirm repeated/final validation behaves correctly

## 8) Individual Plan Workflow

- [ ] Create Individual Plan
- [ ] Add at least one goal
- [ ] Confirm active plan cannot be saved without goals
- [ ] Confirm plan is visible on the home page shortcut

## 9) Permissions Checks

- [ ] Center Coordinator sees all records in their center
- [ ] Specialist sees only assigned beneficiaries
- [ ] Specialist can create allowed visit and assessment records
- [ ] Specialist does not see records from other centers

## 10) Payroll Readiness Checks

- [ ] Monthly visit count helper returns a number
- [ ] Specialist monthly service unit helper returns a number
- [ ] Values can be used for future payroll mapping

## 11) Suggested Demo Order

1. Center
2. Employee
3. Beneficiary
4. Service Visit
5. Assessment
6. Individual Plan

## 12) Pass Criteria

- [ ] User can navigate from home page to all core records
- [ ] Data is center-scoped
- [ ] Specialist access is limited correctly
- [ ] Demo dataset supports a complete client walkthrough
