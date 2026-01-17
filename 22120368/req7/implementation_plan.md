# Implementation Plan - Enhance API Test Assertions

## Goal
Improve the quality of the API test suite by adding deep assertions that verify:
1.  **Sorting Logic**: Verify `sortOrder` and `sortField` actually affect the response order.
2.  **Data Integrity**: Verify that created resources (Candidates) return the correct data fields.

## Proposed Changes

### 1. `req7/generate_postman_collection.py`

#### Recruitment API (Create Candidate)
- **`REC.API.01_Valid_Full` & `REC.API.02_Valid_Minimal`**:
    - Add assertions to check if `jsonData.data.firstName`, `lastName`, and `email` match the request payload.

#### Performance API (List Reviews)
- **`PERF.API.08_Sort_DESC`**:
    - **Current**: Just checks status 200.
    - **Change**: Set `sortField=id` & `sortOrder=DESC`.
    - **Assertion**: Extract `id` from all items in `data` and verify they are in descending order (`ids[i] >= ids[i+1]`).

- **`PERF.API.28_SortField_Valid_Date`**:
    - **Current**: Checks status 422 (Strict) or 200.
    - **Change**: Ensure we use a valid field `reviewPeriodStart`, set `sortOrder=ASC`.
    - **Assertion**: Extract `reviewPeriodStart`, parse as Date, and verify ascending order.

## Verification Plan

### Automated Tests
1.  **Regenerate Collection**: Run `python3 req7/generate_postman_collection.py`.
2.  **Run Newman**: Execute the collection `npx newman run ...`.
3.  **Expectation**: All tests pass (Green), including the new logic assertions.

### Manual Verification
- Review the `newman_report.json` or CLI output to see specific assertion names like "Sorted by ID DESC" passing.
