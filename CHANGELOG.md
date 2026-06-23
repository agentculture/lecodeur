# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-23

### Added

- **Vendored the `remember` + `recall` memory skills from eidetic-cli**
  (cite-don't-import) — the write/read halves of eidetic's shared
  `~/.eidetic/memory` surface, so this agent (Claude and its colleague backend)
  can persist facts across sessions and recall them later, sharing one store.
  `remember` drives `eidetic remember` (idempotent upsert of one JSON record or
  an NDJSON batch on stdin, dedup by id + content hash); `recall` drives
  `eidetic recall` with four search modes — exact / approximate / keyword /
  hybrid — each hit carrying text, full provenance metadata, a relevance score,
  and a freshness signal. The `.sh` wrappers are byte-verbatim from eidetic-cli
  (their first-party origin); each `SKILL.md` is localized only in the
  illustrative `--scope <nick>` examples (Provenance keeps "First-party to
  eidetic-cli"). Both default to this agent's PRIVATE scope, reading the suffix
  from `culture.yaml`. Runtime dep: the `eidetic` CLI on PATH (else a local
  eidetic-cli checkout with `uv`). Propagated by rollout-cli's `eidetic-memory`
  recipe.

## [0.1.0] - 2026-05-22

### Added

- Initial scaffold to the AgentCulture sibling pattern (issue #1).
- `lecodeur` package (dist + import name) with the afi-cli CLI chassis:
  `cli/__init__.py` (argparse, `_LecodeurArgumentParser`), `_errors.py`
  (`LecodeurError` + exit-code policy), `_output.py` (strict stdout/stderr
  split).
- Agent-first verbs: `whoami` (identity probe reading `culture.yaml`),
  `learn` (self-teaching prompt), `explain` (markdown topic catalog, including
  `explain backend`). All read-only and `--json`-aware.
- `culture.yaml` declaring the `acp` backend and the
  `vllm-local/Qwen/Qwen3-Coder-Next` served model; `AGENTS.md` runtime prompt.
- pytest suite (`tests/test_cli.py`).
- CI: `tests.yml` (test + lint + version-check) and `publish.yml`
  (PyPI/TestPyPI via Trusted Publishing).
- Six skills vendored from steward (`cicd`, `communicate`, `version-bump`,
  `run-tests`, `sonarclaude`, `doc-test-alignment`) and
  `.claude/skills.local.yaml.example`.
- Repo-local lint configs (`.flake8`, `.markdownlint-cli2.yaml`) and
  `CHANGELOG.md`.
