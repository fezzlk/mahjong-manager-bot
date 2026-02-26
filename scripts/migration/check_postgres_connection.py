#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys

import psycopg2


def resolve_dsn() -> str:
    dsn = os.getenv("POSTGRES_DATABASE_URL")
    if dsn:
        return dsn

    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT", "5432")
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    sslmode = os.getenv("POSTGRES_SSLMODE")

    required = {
        "POSTGRES_HOST": host,
        "POSTGRES_DB": dbname,
        "POSTGRES_USER": user,
        "POSTGRES_PASSWORD": password,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        raise RuntimeError(
            "POSTGRES_DATABASE_URL is not set, and required env vars are missing: "
            + ", ".join(missing)
        )

    parts = [
        f"host={host}",
        f"port={port}",
        f"dbname={dbname}",
        f"user={user}",
        f"password={password}",
    ]
    if sslmode:
        parts.append(f"sslmode={sslmode}")
    return " ".join(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cloud SQL PostgreSQL connection check")
    parser.add_argument(
        "--query",
        default="SELECT current_database(), current_user, version();",
        help="SQL query to run after connecting",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dsn = resolve_dsn()
    conn = None
    try:
        conn = psycopg2.connect(dsn)
        with conn.cursor() as cur:
            cur.execute(args.query)
            rows = cur.fetchall()
            for i, row in enumerate(rows, start=1):
                print(f"row_{i}: {row}")
        print("postgres connection check: OK")
        return 0
    except Exception as exc:
        print(f"postgres connection check: NG ({exc})", file=sys.stderr)
        return 1
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    raise SystemExit(main())

