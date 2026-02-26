# PostgreSQL DB設計書（要件起点）

## 1. 目的
本設計書は、以下の要件を中心に PostgreSQL の論理/物理設計を定義する。

- LINEチャット経由で麻雀の成績を登録できる
- 半荘/対戦単位で結果を集計できる
- 期間指定や複数プレイヤー比較の統計・グラフ描画に耐える
- 将来的な仕様拡張時も整合性を維持できる

## 2. 設計方針
- 業務上の主キーは `line_user_id` / `line_group_id` を採用
- 集計元データは正規化し、派生値は再計算可能に保つ
- 入力途中データ（draft）と確定データ（final）を分離
- 更新競合や多重登録を DB制約で防ぐ
- 監査可能性のためイベントログを保持

## 3. ER概要
- `players`: ユーザー
- `groups`: LINEグループ
- `group_memberships`: グループ参加履歴
- `group_settings`: グループ設定
- `matches`: 対戦
- `hanchans`: 半荘
- `hanchan_score_drafts`: 入力途中の点数
- `hanchan_scores`: 確定点数
- `match_settlements`: 対戦精算結果（スナップショット）
- `match_participants`: 対戦参加者
- `user_hanchan_stats`: 半荘ごとの順位などの統計明細
- `events_audit_log`: 操作監査ログ

## 4. テーブル定義（DDL案）
```sql
create table players (
  line_user_id text primary key,
  line_user_name text,
  jantama_name text,
  mode text not null default 'wait',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table groups (
  line_group_id text primary key,
  mode text not null default 'wait',
  active_match_id uuid,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table group_memberships (
  line_group_id text not null references groups(line_group_id),
  line_user_id text not null references players(line_user_id),
  joined_at timestamptz not null default now(),
  left_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (line_group_id, line_user_id, joined_at)
);

create table group_settings (
  line_group_id text primary key references groups(line_group_id),
  rate integer not null default 0 check (rate >= 0),
  ranking_prize jsonb not null default '[20,10,-10,-20]'::jsonb,
  chip_rate integer not null default 0,
  tobi_prize integer not null default 10,
  num_of_players integer not null default 4 check (num_of_players in (3, 4)),
  rounding_method integer not null default 1,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table matches (
  match_id uuid primary key,
  line_group_id text not null references groups(line_group_id),
  status text not null check (status in ('active', 'archived', 'disabled')),
  started_at timestamptz not null default now(),
  finished_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index idx_matches_group_started_at on matches (line_group_id, started_at desc);
create index idx_matches_status on matches (status);

create table hanchans (
  hanchan_id uuid primary key,
  match_id uuid not null references matches(match_id),
  line_group_id text not null references groups(line_group_id),
  sequence_no integer not null check (sequence_no > 0),
  status text not null check (status in ('draft', 'final', 'disabled')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (match_id, sequence_no)
);

create index idx_hanchans_match_sequence on hanchans (match_id, sequence_no);
create index idx_hanchans_status on hanchans (status);

create table hanchan_score_drafts (
  hanchan_id uuid not null references hanchans(hanchan_id) on delete cascade,
  line_user_id text not null references players(line_user_id),
  raw_score integer not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (hanchan_id, line_user_id)
);

create table hanchan_scores (
  hanchan_id uuid not null references hanchans(hanchan_id) on delete cascade,
  line_user_id text not null references players(line_user_id),
  raw_score integer not null,
  converted_score integer not null,
  rank integer not null check (rank between 1 and 4),
  yakuman_count integer not null default 0 check (yakuman_count >= 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (hanchan_id, line_user_id)
);

create index idx_hanchan_scores_user_created_at on hanchan_scores (line_user_id, created_at);
create index idx_hanchan_scores_hanchan on hanchan_scores (hanchan_id);

create table match_participants (
  match_id uuid not null references matches(match_id) on delete cascade,
  line_user_id text not null references players(line_user_id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (match_id, line_user_id)
);

create table match_settlements (
  match_id uuid not null references matches(match_id) on delete cascade,
  line_user_id text not null references players(line_user_id),
  sum_score integer not null default 0,
  chip_score integer not null default 0,
  chip_price integer not null default 0,
  sum_price integer not null default 0,
  total_price integer not null default 0,
  settled_at timestamptz not null default now(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (match_id, line_user_id)
);

create index idx_match_settlements_user_settled_at on match_settlements (line_user_id, settled_at);

create table events_audit_log (
  event_id uuid primary key,
  aggregate_type text not null,
  aggregate_id text not null,
  event_type text not null,
  actor_line_user_id text,
  line_group_id text,
  payload jsonb not null,
  occurred_at timestamptz not null default now(),
  created_at timestamptz not null default now()
);

create index idx_events_aggregate on events_audit_log (aggregate_type, aggregate_id, occurred_at);
create index idx_events_group_time on events_audit_log (line_group_id, occurred_at);
```

## 5. 主要制約
- `hanchan_scores`: 1半荘1ユーザー1行（PK）
- `match_participants`: 1対戦1ユーザー1行（PK）
- `group_settings`: 1グループ1設定（PK）
- `hanchans (match_id, sequence_no)`: 同一対戦内の半荘番号重複禁止
- status 列は CHECK で enum 代替

## 6. 集計・統計の基本クエリ方針
- ランキング: `hanchan_scores` と `match_settlements` を集計
- 期間指定: `created_at` / `settled_at` による条件絞り
- ヒストグラム: `rank`, `raw_score`, `converted_score` 集計
- 推移グラフ: `hanchan.sequence_no` または `created_at` で時系列集計

## 7. 現行実装との差分（改修観点）
1. `matches` / `hanchans` の可変Mapフィールドを行明細に分解する必要がある
2. `user_match` / `user_hanchan` は `match_participants` / `hanchan_scores` へ統合可能
3. `group.mode` と `active_match_id` 依存の制御を state管理テーブル中心へ再設計する
4. Web管理画面の直接更新はトランザクション境界を強制する
5. `line_user_id` と内部ID混在のキーを統一する

## 8. 実装フェーズ（提案）
1. スキーマ作成 + マイグレーション基盤導入
2. Repository層を PostgreSQL 実装へ差し替え
3. 入力系ユースケースを `draft` / `final` 分離へ改修
4. 統計系ユースケースをSQL集計へ段階移行
5. 監査ログ導入
6. 旧Mongo依存コードの撤去

## 9. 初回マイグレーション運用
- Alembic設定: `alembic.ini`, `alembic/env.py`
- 初回revision: `alembic/versions/20260226_0001_initial_schema.py`
- 実行:
```bash
POSTGRES_DATABASE_URL='postgresql://<user>:<pass>@<host>:5432/<db>' alembic upgrade head
```
