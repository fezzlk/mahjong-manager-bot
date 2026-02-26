#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import os
from typing import Any
import uuid

from pymongo import MongoClient
import psycopg2
from psycopg2.extras import execute_batch, Json


DEFAULT_BATCH_SIZE = 1000


def oid_to_uuid(value: Any) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_URL, str(value))


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def as_dt(value: Any) -> datetime:
    return value if isinstance(value, datetime) else now_utc()


def map_match_status(status: Any) -> str:
    return {0: "disabled", 1: "active", 2: "archived"}.get(status, "archived")


def map_hanchan_status(status: Any) -> str:
    return {0: "disabled", 1: "draft", 2: "final"}.get(status, "final")


def chunked(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


class EtlRunner:
    def __init__(self, mongo_uri: str, mongo_db: str, pg_dsn: str, dry_run: bool) -> None:
        self.mongo = MongoClient(mongo_uri)[mongo_db]
        self.pg = psycopg2.connect(pg_dsn)
        self.pg.autocommit = False
        self.dry_run = dry_run
        self.match_sequence_counter: defaultdict[str, int] = defaultdict(int)

    def run(self, batch_size: int = DEFAULT_BATCH_SIZE) -> None:
        try:
            with self.pg.cursor() as cur:
                self._load_players(cur, batch_size)
                self._load_groups(cur, batch_size)
                self._load_group_settings(cur, batch_size)
                self._load_group_memberships(cur, batch_size)
                self._load_matches(cur, batch_size)
                self._load_hanchans_and_scores(cur, batch_size)
                self._load_match_participants(cur, batch_size)
                self._load_match_settlements(cur, batch_size)
                self._load_web_users(cur, batch_size)
                self._load_command_aliases(cur, batch_size)
                self._load_yakuman_stats(cur, batch_size)

            if self.dry_run:
                self.pg.rollback()
                print("[DRY RUN] rollback completed")
            else:
                self.pg.commit()
                print("[DONE] migration committed")
        finally:
            self.pg.close()

    def _insert_batch(
        self,
        cur: psycopg2.extensions.cursor,
        query: str,
        rows: list[dict[str, Any]],
        batch_size: int,
    ) -> None:
        if not rows:
            return
        for chunk in chunked(rows, batch_size):
            execute_batch(cur, query, chunk)

    def _load_players(self, cur: psycopg2.extensions.cursor, batch_size: int) -> None:
        docs = list(self.mongo.line_users.find({}))
        rows = []
        for d in docs:
            rows.append(
                {
                    "line_user_id": d.get("line_user_id"),
                    "line_user_name": d.get("line_user_name"),
                    "jantama_name": d.get("jantama_name"),
                    "mode": d.get("mode") or "wait",
                    "created_at": as_dt(d.get("created_at")),
                    "updated_at": as_dt(d.get("updated_at")),
                }
            )
        self._insert_batch(
            cur,
            """
            INSERT INTO players (line_user_id, line_user_name, jantama_name, mode, created_at, updated_at)
            VALUES (%(line_user_id)s, %(line_user_name)s, %(jantama_name)s, %(mode)s, %(created_at)s, %(updated_at)s)
            ON CONFLICT (line_user_id) DO NOTHING
            """,
            rows,
            batch_size,
        )
        print(f"[players] {len(rows)}")

    def _load_groups(self, cur: psycopg2.extensions.cursor, batch_size: int) -> None:
        docs = list(self.mongo.groups.find({}))
        rows = []
        for d in docs:
            active_match = d.get("active_match_id")
            rows.append(
                {
                    "line_group_id": d.get("line_group_id"),
                    "mode": d.get("mode") or "wait",
                    "active_match_id": oid_to_uuid(active_match) if active_match else None,
                    "created_at": as_dt(d.get("created_at")),
                    "updated_at": as_dt(d.get("updated_at")),
                }
            )
        self._insert_batch(
            cur,
            """
            INSERT INTO groups (line_group_id, mode, active_match_id, created_at, updated_at)
            VALUES (%(line_group_id)s, %(mode)s, %(active_match_id)s, %(created_at)s, %(updated_at)s)
            ON CONFLICT (line_group_id) DO NOTHING
            """,
            rows,
            batch_size,
        )
        print(f"[groups] {len(rows)}")

    def _load_group_settings(self, cur: psycopg2.extensions.cursor, batch_size: int) -> None:
        docs = list(self.mongo.group_settings.find({}))
        rows = []
        for d in docs:
            rows.append(
                {
                    "line_group_id": d.get("line_group_id"),
                    "rate": d.get("rate", 0),
                    "ranking_prize": Json(d.get("ranking_prize", [20, 10, -10, -20])),
                    "chip_rate": d.get("chip_rate", 0),
                    "tobi_prize": d.get("tobi_prize", 10),
                    "num_of_players": d.get("num_of_players", 4),
                    "rounding_method": d.get("rounding_method", 1),
                    "created_at": as_dt(d.get("created_at")),
                    "updated_at": as_dt(d.get("updated_at")),
                }
            )
        self._insert_batch(
            cur,
            """
            INSERT INTO group_settings (
              line_group_id, rate, ranking_prize, chip_rate, tobi_prize,
              num_of_players, rounding_method, created_at, updated_at
            )
            VALUES (
              %(line_group_id)s, %(rate)s, %(ranking_prize)s, %(chip_rate)s, %(tobi_prize)s,
              %(num_of_players)s, %(rounding_method)s, %(created_at)s, %(updated_at)s
            )
            ON CONFLICT (line_group_id) DO NOTHING
            """,
            rows,
            batch_size,
        )
        print(f"[group_settings] {len(rows)}")

    def _load_group_memberships(self, cur: psycopg2.extensions.cursor, batch_size: int) -> None:
        docs = list(self.mongo.user_groups.find({}))
        rows = []
        for d in docs:
            rows.append(
                {
                    "line_group_id": d.get("line_group_id"),
                    "line_user_id": d.get("line_user_id"),
                    "joined_at": as_dt(d.get("created_at")),
                    "left_at": None,
                    "created_at": as_dt(d.get("created_at")),
                    "updated_at": as_dt(d.get("updated_at")),
                }
            )
        self._insert_batch(
            cur,
            """
            INSERT INTO group_memberships (
              line_group_id, line_user_id, joined_at, left_at, created_at, updated_at
            )
            VALUES (
              %(line_group_id)s, %(line_user_id)s, %(joined_at)s, %(left_at)s, %(created_at)s, %(updated_at)s
            )
            ON CONFLICT DO NOTHING
            """,
            rows,
            batch_size,
        )
        print(f"[group_memberships] {len(rows)}")

    def _load_matches(self, cur: psycopg2.extensions.cursor, batch_size: int) -> None:
        docs = list(self.mongo.matches.find({}))
        rows = []
        for d in docs:
            match_uuid = oid_to_uuid(d.get("_id"))
            line_group_id = d.get("line_group_id")
            self.match_sequence_counter[line_group_id] += 1
            rows.append(
                {
                    "match_id": match_uuid,
                    "line_group_id": line_group_id,
                    "status": map_match_status(d.get("status")),
                    "started_at": as_dt(d.get("created_at")),
                    "finished_at": as_dt(d.get("updated_at"))
                    if d.get("sum_prices_with_chip")
                    else None,
                    "created_at": as_dt(d.get("created_at")),
                    "updated_at": as_dt(d.get("updated_at")),
                }
            )
        self._insert_batch(
            cur,
            """
            INSERT INTO matches (
              match_id, line_group_id, status, started_at, finished_at, created_at, updated_at
            )
            VALUES (
              %(match_id)s, %(line_group_id)s, %(status)s, %(started_at)s, %(finished_at)s, %(created_at)s, %(updated_at)s
            )
            ON CONFLICT (match_id) DO NOTHING
            """,
            rows,
            batch_size,
        )
        print(f"[matches] {len(rows)}")

    def _load_hanchans_and_scores(
        self, cur: psycopg2.extensions.cursor, batch_size: int
    ) -> None:
        hanchan_docs = list(self.mongo.hanchans.find({}))
        hanchan_rows = []
        draft_rows = []
        score_rows = []

        sequence_by_match: defaultdict[str, int] = defaultdict(int)

        for d in hanchan_docs:
            hanchan_uuid = oid_to_uuid(d.get("_id"))
            match_uuid = oid_to_uuid(d.get("match_id"))
            match_key = str(match_uuid)
            sequence_by_match[match_key] += 1
            sequence_no = sequence_by_match[match_key]

            status = map_hanchan_status(d.get("status"))

            hanchan_rows.append(
                {
                    "hanchan_id": hanchan_uuid,
                    "match_id": match_uuid,
                    "line_group_id": d.get("line_group_id"),
                    "sequence_no": sequence_no,
                    "status": status,
                    "created_at": as_dt(d.get("created_at")),
                    "updated_at": as_dt(d.get("updated_at")),
                }
            )

            raw_scores = d.get("raw_scores", {}) or {}
            converted_scores = d.get("converted_scores", {}) or {}

            if status == "draft":
                for line_user_id, raw_score in raw_scores.items():
                    draft_rows.append(
                        {
                            "hanchan_id": hanchan_uuid,
                            "line_user_id": line_user_id,
                            "raw_score": int(raw_score),
                            "created_at": as_dt(d.get("created_at")),
                            "updated_at": as_dt(d.get("updated_at")),
                        }
                    )
            else:
                sorted_raw = sorted(raw_scores.items(), key=lambda x: x[1], reverse=True)
                rank_map: dict[str, int] = {}
                for idx, (line_user_id, _) in enumerate(sorted_raw, start=1):
                    rank_map[line_user_id] = idx

                for line_user_id, raw_score in raw_scores.items():
                    score_rows.append(
                        {
                            "hanchan_id": hanchan_uuid,
                            "line_user_id": line_user_id,
                            "raw_score": int(raw_score),
                            "converted_score": int(converted_scores.get(line_user_id, 0)),
                            "rank": rank_map.get(line_user_id, 4),
                            "yakuman_count": 0,
                            "created_at": as_dt(d.get("created_at")),
                            "updated_at": as_dt(d.get("updated_at")),
                        }
                    )

        self._insert_batch(
            cur,
            """
            INSERT INTO hanchans (
              hanchan_id, match_id, line_group_id, sequence_no, status, created_at, updated_at
            )
            VALUES (
              %(hanchan_id)s, %(match_id)s, %(line_group_id)s, %(sequence_no)s, %(status)s, %(created_at)s, %(updated_at)s
            )
            ON CONFLICT (hanchan_id) DO NOTHING
            """,
            hanchan_rows,
            batch_size,
        )

        self._insert_batch(
            cur,
            """
            INSERT INTO hanchan_score_drafts (
              hanchan_id, line_user_id, raw_score, created_at, updated_at
            )
            VALUES (
              %(hanchan_id)s, %(line_user_id)s, %(raw_score)s, %(created_at)s, %(updated_at)s
            )
            ON CONFLICT (hanchan_id, line_user_id) DO NOTHING
            """,
            draft_rows,
            batch_size,
        )

        self._insert_batch(
            cur,
            """
            INSERT INTO hanchan_scores (
              hanchan_id, line_user_id, raw_score, converted_score, rank,
              yakuman_count, created_at, updated_at
            )
            VALUES (
              %(hanchan_id)s, %(line_user_id)s, %(raw_score)s, %(converted_score)s, %(rank)s,
              %(yakuman_count)s, %(created_at)s, %(updated_at)s
            )
            ON CONFLICT (hanchan_id, line_user_id) DO NOTHING
            """,
            score_rows,
            batch_size,
        )
        print(
            f"[hanchans] {len(hanchan_rows)} [hanchan_score_drafts] {len(draft_rows)} [hanchan_scores] {len(score_rows)}"
        )

    def _load_match_participants(
        self, cur: psycopg2.extensions.cursor, batch_size: int
    ) -> None:
        docs = list(self.mongo.user_matches.find({}))
        rows = []
        for d in docs:
            rows.append(
                {
                    "match_id": oid_to_uuid(d.get("match_id")),
                    "line_user_id": self._resolve_line_user_id(d.get("user_id")),
                    "created_at": as_dt(d.get("created_at")),
                    "updated_at": as_dt(d.get("updated_at")),
                }
            )
        self._insert_batch(
            cur,
            """
            INSERT INTO match_participants (match_id, line_user_id, created_at, updated_at)
            VALUES (%(match_id)s, %(line_user_id)s, %(created_at)s, %(updated_at)s)
            ON CONFLICT (match_id, line_user_id) DO NOTHING
            """,
            [r for r in rows if r["line_user_id"]],
            batch_size,
        )
        print(f"[match_participants] {len(rows)}")

    def _load_match_settlements(
        self, cur: psycopg2.extensions.cursor, batch_size: int
    ) -> None:
        docs = list(self.mongo.matches.find({}))
        rows = []
        for d in docs:
            match_uuid = oid_to_uuid(d.get("_id"))
            sum_scores = d.get("sum_scores", {}) or {}
            chip_scores = d.get("chip_scores", {}) or {}
            chip_prices = d.get("chip_prices", {}) or {}
            sum_prices = d.get("sum_prices", {}) or {}
            total_prices = d.get("sum_prices_with_chip", {}) or {}

            keys = set(sum_scores) | set(chip_scores) | set(chip_prices) | set(sum_prices) | set(total_prices)
            for line_user_id in keys:
                rows.append(
                    {
                        "match_id": match_uuid,
                        "line_user_id": line_user_id,
                        "sum_score": int(sum_scores.get(line_user_id, 0)),
                        "chip_score": int(chip_scores.get(line_user_id, 0)),
                        "chip_price": int(chip_prices.get(line_user_id, 0)),
                        "sum_price": int(sum_prices.get(line_user_id, 0)),
                        "total_price": int(total_prices.get(line_user_id, 0)),
                        "settled_at": as_dt(d.get("updated_at")),
                        "created_at": as_dt(d.get("created_at")),
                        "updated_at": as_dt(d.get("updated_at")),
                    }
                )
        self._insert_batch(
            cur,
            """
            INSERT INTO match_settlements (
              match_id, line_user_id, sum_score, chip_score, chip_price, sum_price, total_price,
              settled_at, created_at, updated_at
            )
            VALUES (
              %(match_id)s, %(line_user_id)s, %(sum_score)s, %(chip_score)s, %(chip_price)s, %(sum_price)s, %(total_price)s,
              %(settled_at)s, %(created_at)s, %(updated_at)s
            )
            ON CONFLICT (match_id, line_user_id) DO NOTHING
            """,
            rows,
            batch_size,
        )
        print(f"[match_settlements] {len(rows)}")

    def _load_web_users(self, cur: psycopg2.extensions.cursor, batch_size: int) -> None:
        docs = list(self.mongo.web_users.find({}))
        rows = []
        for d in docs:
            rows.append(
                {
                    "web_user_id": oid_to_uuid(d.get("_id")),
                    "user_code": d.get("user_code"),
                    "name": d.get("name"),
                    "email": d.get("email"),
                    "linked_line_user_id": d.get("linked_line_user_id"),
                    "is_approved_line_user": bool(d.get("is_approved_line_user", False)),
                    "created_at": as_dt(d.get("created_at")),
                    "updated_at": as_dt(d.get("updated_at")),
                }
            )
        self._insert_batch(
            cur,
            """
            INSERT INTO web_users (
              web_user_id, user_code, name, email, linked_line_user_id, is_approved_line_user, created_at, updated_at
            )
            VALUES (
              %(web_user_id)s, %(user_code)s, %(name)s, %(email)s, %(linked_line_user_id)s, %(is_approved_line_user)s, %(created_at)s, %(updated_at)s
            )
            ON CONFLICT (web_user_id) DO NOTHING
            """,
            rows,
            batch_size,
        )
        print(f"[web_users] {len(rows)}")

    def _load_command_aliases(
        self, cur: psycopg2.extensions.cursor, batch_size: int
    ) -> None:
        docs = list(self.mongo.command_aliases.find({}))
        rows = []
        for d in docs:
            rows.append(
                {
                    "command_alias_id": oid_to_uuid(d.get("_id")),
                    "line_user_id": d.get("line_user_id"),
                    "line_group_id": d.get("line_group_id"),
                    "alias": d.get("alias"),
                    "command": d.get("command"),
                    "mentionees": Json(d.get("mentionees", [])),
                    "created_at": as_dt(d.get("created_at")),
                    "updated_at": as_dt(d.get("updated_at")),
                }
            )
        self._insert_batch(
            cur,
            """
            INSERT INTO command_aliases (
              command_alias_id, line_user_id, line_group_id, alias, command, mentionees, created_at, updated_at
            )
            VALUES (
              %(command_alias_id)s, %(line_user_id)s, %(line_group_id)s, %(alias)s, %(command)s, %(mentionees)s, %(created_at)s, %(updated_at)s
            )
            ON CONFLICT (command_alias_id) DO NOTHING
            """,
            rows,
            batch_size,
        )
        print(f"[command_aliases] {len(rows)}")

    def _load_yakuman_stats(self, cur: psycopg2.extensions.cursor, batch_size: int) -> None:
        docs = list(self.mongo.yakuman_users.find({}))
        rows = []
        for d in docs:
            rows.append(
                {
                    "yakuman_user_stat_id": oid_to_uuid(d.get("_id")),
                    "line_user_id": d.get("line_user_id"),
                    "yakuman_name": d.get("yakuman_name") or "unknown",
                    "count": int(d.get("count", 0)),
                    "created_at": as_dt(d.get("created_at")),
                    "updated_at": as_dt(d.get("updated_at")),
                }
            )
        self._insert_batch(
            cur,
            """
            INSERT INTO yakuman_user_stats (
              yakuman_user_stat_id, line_user_id, yakuman_name, count, created_at, updated_at
            )
            VALUES (
              %(yakuman_user_stat_id)s, %(line_user_id)s, %(yakuman_name)s, %(count)s, %(created_at)s, %(updated_at)s
            )
            ON CONFLICT (yakuman_user_stat_id) DO NOTHING
            """,
            [r for r in rows if r["line_user_id"]],
            batch_size,
        )
        print(f"[yakuman_user_stats] {len(rows)}")

    def _resolve_line_user_id(self, mongo_user_id: Any) -> str | None:
        if mongo_user_id is None:
            return None
        user_doc = self.mongo.line_users.find_one({"_id": mongo_user_id})
        if not user_doc:
            return None
        return user_doc.get("line_user_id")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MongoDB to PostgreSQL ETL")
    parser.add_argument("--mongo-uri", default=os.getenv("EXTERNAL_DATABASE_URL"))
    parser.add_argument("--mongo-db", default=os.getenv("DATABASE_NAME"))
    parser.add_argument("--pg-dsn", default=os.getenv("POSTGRES_DATABASE_URL"))
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.mongo_uri:
        raise RuntimeError("--mongo-uri or EXTERNAL_DATABASE_URL is required")
    if not args.mongo_db:
        raise RuntimeError("--mongo-db or DATABASE_NAME is required")
    if not args.pg_dsn:
        raise RuntimeError("--pg-dsn or POSTGRES_DATABASE_URL is required")

    runner = EtlRunner(
        mongo_uri=args.mongo_uri,
        mongo_db=args.mongo_db,
        pg_dsn=args.pg_dsn,
        dry_run=args.dry_run,
    )
    runner.run(batch_size=args.batch_size)


if __name__ == "__main__":
    main()

