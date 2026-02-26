# Specification: Commute Sort CLI Flag

## Overview
Implement a new command-line interface (CLI) flag for the script that allows users to customize how property results are sorted based on commute times. By default, the script sorts by the minimum of transport and cycling times, but this feature will allow sorting explicitly by `transport` or `cycling`.

## Functional Requirements
- **CLI Flag:** Add a new CLI argument `--sort-by`.
- **Allowed Values:** The flag must accept the following values:
  - `min`: Sorts by the minimum of public transport or cycling time (default behavior).
  - `transport`: Sorts purely by public transport time.
  - `cycling`: Sorts purely by cycling time.
- **Default Behavior:** If the `--sort-by` flag is omitted, the script must default to the `min` sorting behavior.
- **Error Handling:** If an invalid value is passed to `--sort-by` (e.g., `--sort-by car`), the script must print a clear error message and immediately exit (non-zero exit code).
- **Integration:** The sorting logic in the main processing or reporting module must be updated to respect the selected sort method.

## Non-Functional Requirements
- **Documentation:** The CLI `--help` output must clearly describe the `--sort-by` flag and its valid options.

## Acceptance Criteria
- Running the script with `--sort-by transport` sorts the results by transport time.
- Running the script with `--sort-by cycling` sorts the results by cycling time.
- Running the script with `--sort-by min` or without the flag maintains the current sorting behavior.
- Running the script with `--sort-by invalid` prints an error message and terminates the execution.
- All new CLI parsing and sorting logic must be covered by unit tests.

## Out of Scope
- Adding support for other commute modes (e.g., walking, driving).
- Modifying how the commute times are actually calculated or fetched.