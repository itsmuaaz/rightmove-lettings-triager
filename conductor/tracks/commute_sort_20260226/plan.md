# Implementation Plan: Commute Sort CLI Flag

## Phase 1: CLI Argument Parsing
- [ ] Task: Implement `--sort-by` flag parsing
    - [ ] Sub-task: Write Tests (argparse logic)
    - [ ] Sub-task: Implement Feature (Add `--sort-by` with choices `['min', 'transport', 'cycling']` and default `min`)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: CLI Argument Parsing' (Protocol in workflow.md)

## Phase 2: Sorting Logic Update
- [ ] Task: Pass `--sort-by` value to sorting function
    - [ ] Sub-task: Write Tests (pass config to sorting mechanism)
    - [ ] Sub-task: Implement Feature (Update main logic to propagate `sort_by` state)
- [ ] Task: Update property sorting based on the selected mode
    - [ ] Sub-task: Write Tests (assert different sorting orders based on `sort_by` parameter)
    - [ ] Sub-task: Implement Feature (Modify the sorting key to use `min`, `transport`, or `cycling` time)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Sorting Logic Update' (Protocol in workflow.md)

## Phase 3: Integration and Error Handling
- [ ] Task: Validate overall CLI behavior
    - [ ] Sub-task: Write Tests (Integration test to verify full execution with `--sort-by` flag)
    - [ ] Sub-task: Implement Feature (Ensure invalid inputs trigger error via argparse)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Integration and Error Handling' (Protocol in workflow.md)