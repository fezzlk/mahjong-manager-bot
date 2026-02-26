-- Migration verification SQL for MongoDB -> PostgreSQL
-- Usage:
--   1) Collect expected numbers from MongoDB before migration.
--   2) Replace values in expected_counts CTE.
--   3) Run against PostgreSQL after migration.

WITH expected_counts AS (
  SELECT
    0::bigint AS players_expected,
    0::bigint AS groups_expected,
    0::bigint AS hanchans_expected,
    0::bigint AS hanchan_score_rows_expected,
    0::bigint AS match_settlements_rows_expected
),
actual_counts AS (
  SELECT
    (SELECT count(*) FROM players) AS players_actual,
    (SELECT count(*) FROM groups) AS groups_actual,
    (SELECT count(*) FROM hanchans) AS hanchans_actual,
    (SELECT count(*) FROM hanchan_scores) + (SELECT count(*) FROM hanchan_score_drafts) AS hanchan_score_rows_actual,
    (SELECT count(*) FROM match_settlements) AS match_settlements_rows_actual
)
SELECT
  e.players_expected,
  a.players_actual,
  (e.players_expected = a.players_actual) AS players_ok,
  e.groups_expected,
  a.groups_actual,
  (e.groups_expected = a.groups_actual) AS groups_ok,
  e.hanchans_expected,
  a.hanchans_actual,
  (e.hanchans_expected = a.hanchans_actual) AS hanchans_ok,
  e.hanchan_score_rows_expected,
  a.hanchan_score_rows_actual,
  (e.hanchan_score_rows_expected = a.hanchan_score_rows_actual) AS hanchan_scores_ok,
  e.match_settlements_rows_expected,
  a.match_settlements_rows_actual,
  (e.match_settlements_rows_expected = a.match_settlements_rows_actual) AS match_settlements_ok
FROM expected_counts e
CROSS JOIN actual_counts a;

-- Per match settlement balance check
SELECT
  match_id,
  sum(sum_score) AS sum_score_total,
  sum(chip_score) AS chip_score_total,
  sum(sum_price) AS sum_price_total,
  sum(total_price) AS total_price_total
FROM match_settlements
GROUP BY match_id
ORDER BY match_id;

-- Detect missing referenced users in score tables
SELECT hs.hanchan_id, hs.line_user_id
FROM hanchan_scores hs
LEFT JOIN players p ON p.line_user_id = hs.line_user_id
WHERE p.line_user_id IS NULL
LIMIT 100;

SELECT ms.match_id, ms.line_user_id
FROM match_settlements ms
LEFT JOIN players p ON p.line_user_id = ms.line_user_id
WHERE p.line_user_id IS NULL
LIMIT 100;

-- Detect duplicate participants beyond PK expectation (should return 0 rows)
SELECT match_id, line_user_id, count(*)
FROM match_participants
GROUP BY match_id, line_user_id
HAVING count(*) > 1;

