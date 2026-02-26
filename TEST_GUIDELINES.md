# Test Writing Guidelines

## Purpose
Use case tests should validate end-to-end behavior within the application boundary:
- Call actual services and repositories.
- Persist data in the test DB.
- Avoid mocking except for external APIs (e.g., LINE API, external HTTP).

## Required Test Metadata (Per Test)
Add a comment block at the top of each test with:
- Purpose
- Input
- Input rationale
- Expected output
- reply_service expected properties (e.g., texts/buttons/images)
- DB operations (records created/updated/deleted)

## General Principles
- Prefer real DB operations for domain correctness.
- Keep test fixtures explicit so setup intent is clear.
- Make assertions on both reply output and DB state.
- For external APIs, use stubs/mocks and keep behavior deterministic.

## Coverage Expectations
- Each use case should have 2–5 scenarios.
- Minimum: normal path + one edge case.
- Optional: validation errors, boundary values, and no-op paths.

## Example Comment Block
```
# Purpose: Verify ReplyGroupSettingsMenuUseCase returns formatted settings summary.
# Input: case1=\"メニュー2\"
# Input rationale: Validate alternative menu input still returns a menu response.
# Expected output: assert len(reply_service.buttons) == 1, assert isinstance(...)
# reply_service: texts, buttons
# DB ops: group_setting_repository.create(...)
```
