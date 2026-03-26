# Codex MCP Auto-Recovery Setup

PC再起動後も、CodexがMCP接続時に `cloud-run-logging-mcp` を自動起動・復旧するための手順です。  
他プロジェクトへ横展開できるように、共通化前提でまとめています。

## 前提

- Codexは `~/.codex/config.toml` の `mcp_servers` を参照してMCPを起動する
- 再起動後に接続が切れる主な原因は以下
  - Docker daemon 未起動
  - MCPイメージ未build
  - 鍵ファイルパス不整合

## 1. ラッパースクリプトを作成

各プロジェクトに `scripts/start_cloud_run_logging_mcp.sh` を作成します。

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_REPO_DIR="${MCP_REPO_DIR:-${SCRIPT_DIR}/../../cloud-run-logging-mcp}"
MCP_IMAGE="${MCP_IMAGE:-cloud-run-logging-mcp:local}"
MCP_KEY_PATH="${MCP_KEY_PATH:-/absolute/path/to/sa.json}"

docker info >/dev/null 2>&1 || { [[ "$(uname)" == "Darwin" ]] && open -ga Docker || true; }
for i in {1..90}; do docker info >/dev/null 2>&1 && break; sleep 2; done
docker info >/dev/null 2>&1

docker image inspect "${MCP_IMAGE}" >/dev/null 2>&1 || docker build -t "${MCP_IMAGE}" "${MCP_REPO_DIR}"
[[ -f "${MCP_KEY_PATH}" ]]

exec docker run --rm -i \
  -e GCP_SA_JSON_PATH=/secrets/key.json \
  -v "${MCP_KEY_PATH}:/secrets/key.json:ro" \
  "${MCP_IMAGE}"
```

## 2. 実行権限を付与

```bash
chmod +x scripts/start_cloud_run_logging_mcp.sh
```

## 3. `~/.codex/config.toml` を設定

`mcp_servers.cloud-run-logging-mcp` をラッパー呼び出しに変更します。

```toml
personality = "pragmatic"

[mcp_servers.cloud-run-logging-mcp]
command = "/bin/zsh"
args = ["-lc", "/ABSOLUTE/PATH/TO/PROJECT/scripts/start_cloud_run_logging_mcp.sh"]
enabled = true
```

## 4. プロジェクト差分を環境変数で吸収

必要に応じて以下を上書きします。

- `MCP_KEY_PATH`
- `MCP_REPO_DIR`
- `MCP_IMAGE`

## 5. 動作確認

1. Dockerを停止した状態でCodexを起動
2. MCPツール（Cloud Runログ取得）を実行
3. 自動でDocker起動待ち・MCP起動され、ログ取得できることを確認

## 運用メモ

- 複数プロジェクトで同一MCPを使う場合:
  - スクリプトを `~/.codex/bin/` などに1本化し、各プロジェクトは同じスクリプトを参照
- `config.toml` は相対パスより絶対パス運用が安定
