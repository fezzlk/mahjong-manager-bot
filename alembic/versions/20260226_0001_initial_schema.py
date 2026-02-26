"""initial postgresql schema

Revision ID: 20260226_0001
Revises:
Create Date: 2026-02-26 09:55:00
"""

from __future__ import annotations

from alembic import op

revision = "20260226_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE players (
          line_user_id TEXT PRIMARY KEY,
          line_user_name TEXT,
          jantama_name TEXT,
          mode TEXT NOT NULL DEFAULT 'wait',
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )

    op.execute(
        """
        CREATE TABLE groups (
          line_group_id TEXT PRIMARY KEY,
          mode TEXT NOT NULL DEFAULT 'wait',
          active_match_id UUID,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )

    op.execute(
        """
        CREATE TABLE group_memberships (
          line_group_id TEXT NOT NULL REFERENCES groups(line_group_id),
          line_user_id TEXT NOT NULL REFERENCES players(line_user_id),
          joined_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          left_at TIMESTAMPTZ,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          PRIMARY KEY (line_group_id, line_user_id, joined_at)
        );
        """
    )

    op.execute(
        """
        CREATE TABLE group_settings (
          line_group_id TEXT PRIMARY KEY REFERENCES groups(line_group_id),
          rate INTEGER NOT NULL DEFAULT 0 CHECK (rate >= 0),
          ranking_prize JSONB NOT NULL DEFAULT '[20,10,-10,-20]'::jsonb,
          chip_rate INTEGER NOT NULL DEFAULT 0,
          tobi_prize INTEGER NOT NULL DEFAULT 10,
          num_of_players INTEGER NOT NULL DEFAULT 4 CHECK (num_of_players IN (3, 4)),
          rounding_method INTEGER NOT NULL DEFAULT 1,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )

    op.execute(
        """
        CREATE TABLE matches (
          match_id UUID PRIMARY KEY,
          line_group_id TEXT NOT NULL REFERENCES groups(line_group_id),
          status TEXT NOT NULL CHECK (status IN ('active', 'archived', 'disabled')),
          started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          finished_at TIMESTAMPTZ,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        """
        CREATE INDEX idx_matches_group_started_at ON matches (line_group_id, started_at DESC);
        CREATE INDEX idx_matches_status ON matches (status);
        """
    )

    op.execute(
        """
        CREATE TABLE hanchans (
          hanchan_id UUID PRIMARY KEY,
          match_id UUID NOT NULL REFERENCES matches(match_id),
          line_group_id TEXT NOT NULL REFERENCES groups(line_group_id),
          sequence_no INTEGER NOT NULL CHECK (sequence_no > 0),
          status TEXT NOT NULL CHECK (status IN ('draft', 'final', 'disabled')),
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          UNIQUE (match_id, sequence_no)
        );
        """
    )
    op.execute(
        """
        CREATE INDEX idx_hanchans_match_sequence ON hanchans (match_id, sequence_no);
        CREATE INDEX idx_hanchans_status ON hanchans (status);
        """
    )

    op.execute(
        """
        CREATE TABLE hanchan_score_drafts (
          hanchan_id UUID NOT NULL REFERENCES hanchans(hanchan_id) ON DELETE CASCADE,
          line_user_id TEXT NOT NULL REFERENCES players(line_user_id),
          raw_score INTEGER NOT NULL,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          PRIMARY KEY (hanchan_id, line_user_id)
        );
        """
    )

    op.execute(
        """
        CREATE TABLE hanchan_scores (
          hanchan_id UUID NOT NULL REFERENCES hanchans(hanchan_id) ON DELETE CASCADE,
          line_user_id TEXT NOT NULL REFERENCES players(line_user_id),
          raw_score INTEGER NOT NULL,
          converted_score INTEGER NOT NULL,
          rank INTEGER NOT NULL CHECK (rank BETWEEN 1 AND 4),
          yakuman_count INTEGER NOT NULL DEFAULT 0 CHECK (yakuman_count >= 0),
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          PRIMARY KEY (hanchan_id, line_user_id)
        );
        """
    )
    op.execute(
        """
        CREATE INDEX idx_hanchan_scores_user_created_at ON hanchan_scores (line_user_id, created_at);
        CREATE INDEX idx_hanchan_scores_hanchan ON hanchan_scores (hanchan_id);
        """
    )

    op.execute(
        """
        CREATE TABLE match_participants (
          match_id UUID NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
          line_user_id TEXT NOT NULL REFERENCES players(line_user_id),
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          PRIMARY KEY (match_id, line_user_id)
        );
        """
    )

    op.execute(
        """
        CREATE TABLE match_settlements (
          match_id UUID NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
          line_user_id TEXT NOT NULL REFERENCES players(line_user_id),
          sum_score INTEGER NOT NULL DEFAULT 0,
          chip_score INTEGER NOT NULL DEFAULT 0,
          chip_price INTEGER NOT NULL DEFAULT 0,
          sum_price INTEGER NOT NULL DEFAULT 0,
          total_price INTEGER NOT NULL DEFAULT 0,
          settled_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          PRIMARY KEY (match_id, line_user_id)
        );
        """
    )
    op.execute(
        """
        CREATE INDEX idx_match_settlements_user_settled_at ON match_settlements (line_user_id, settled_at);
        """
    )

    op.execute(
        """
        CREATE TABLE web_users (
          web_user_id UUID PRIMARY KEY,
          user_code TEXT NOT NULL UNIQUE,
          name TEXT,
          email TEXT,
          linked_line_user_id TEXT,
          is_approved_line_user BOOLEAN NOT NULL DEFAULT FALSE,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )

    op.execute(
        """
        CREATE TABLE command_aliases (
          command_alias_id UUID PRIMARY KEY,
          line_user_id TEXT NOT NULL REFERENCES players(line_user_id),
          line_group_id TEXT REFERENCES groups(line_group_id),
          alias TEXT NOT NULL,
          command TEXT NOT NULL,
          mentionees JSONB NOT NULL DEFAULT '[]'::jsonb,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          UNIQUE (line_user_id, line_group_id, alias)
        );
        """
    )

    op.execute(
        """
        CREATE TABLE yakuman_user_stats (
          yakuman_user_stat_id UUID PRIMARY KEY,
          line_user_id TEXT NOT NULL REFERENCES players(line_user_id),
          yakuman_name TEXT NOT NULL,
          count INTEGER NOT NULL DEFAULT 0 CHECK (count >= 0),
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          UNIQUE (line_user_id, yakuman_name)
        );
        """
    )

    op.execute(
        """
        CREATE TABLE events_audit_log (
          event_id UUID PRIMARY KEY,
          aggregate_type TEXT NOT NULL,
          aggregate_id TEXT NOT NULL,
          event_type TEXT NOT NULL,
          actor_line_user_id TEXT,
          line_group_id TEXT,
          payload JSONB NOT NULL,
          occurred_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        CREATE INDEX idx_events_aggregate ON events_audit_log (aggregate_type, aggregate_id, occurred_at);
        CREATE INDEX idx_events_group_time ON events_audit_log (line_group_id, occurred_at);
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS events_audit_log;")
    op.execute("DROP TABLE IF EXISTS yakuman_user_stats;")
    op.execute("DROP TABLE IF EXISTS command_aliases;")
    op.execute("DROP TABLE IF EXISTS web_users;")
    op.execute("DROP TABLE IF EXISTS match_settlements;")
    op.execute("DROP TABLE IF EXISTS match_participants;")
    op.execute("DROP TABLE IF EXISTS hanchan_scores;")
    op.execute("DROP TABLE IF EXISTS hanchan_score_drafts;")
    op.execute("DROP TABLE IF EXISTS hanchans;")
    op.execute("DROP TABLE IF EXISTS matches;")
    op.execute("DROP TABLE IF EXISTS group_settings;")
    op.execute("DROP TABLE IF EXISTS group_memberships;")
    op.execute("DROP TABLE IF EXISTS groups;")
    op.execute("DROP TABLE IF EXISTS players;")

