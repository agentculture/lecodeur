# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

`lecodeur` ("le codeur" — the coder) is the **local coding agent** of the Culture
mesh: a long-lived resident agent that implements, edits, and tests code.

### The matched pair: thinker + coder

lecodeur is the **doer** of a matched pair, and these are its closest siblings:

- **[`lepenseur`](https://github.com/agentculture/lepenseur)** ("le penseur" — the
  thinker) is the **closest sibling**. It reasons, plans, and analyzes, but acts
  only through writing (chat + files) — no execution. lepenseur plans; lecodeur
  executes. The two are scaffolded in parallel and share this exact runtime shape
  (acp / local vLLM), differing in model and mandate.
- **[`daria`](https://github.com/agentculture/daria)** (awareness) is the
  **next-closest sibling**. It observes the mesh and surfaces drift.

The division of labor: **daria notices, lepenseur reasons, lecodeur builds.** It is
also an AgentCulture sibling to [`culture`](https://github.com/agentculture/culture)
(the IRC agent mesh) and [`steward`](https://github.com/agentculture/steward) (the
alignment agent, which owns the sibling-pattern contract and the vendored skills).
See the workspace-level `CLAUDE.md` one directory up for the Organic Development
framework overview.

`AGENTS.md` vs this file — they coexist and serve different readers:

- **`AGENTS.md`** is the **runtime system prompt** the `acp` backend reads when the
  agent runs. It is the source of truth, mirrored into `culture.yaml`'s
  `system_prompt:`. `daria/AGENTS.md` is the worked example.
- **`CLAUDE.md`** (this file) is **dev guidance for a Claude that resides here to
  help build and maintain lecodeur** — project shape, build/test/publish commands,
  conventions. Editing code is a CLAUDE.md task; editing the agent's behavior is an
  `AGENTS.md` task.

## Runtime: locally-hosted vLLM over `acp`, NOT Claude-backed

lecodeur is **not** a Claude-backed agent. At runtime it is served by a
**local vLLM code model** over the `acp` backend, exactly like `daria`. The repo
root's `culture.yaml` declares this:

```yaml
agents:
- suffix: lecodeur
  backend: acp
  model: vllm-local/Qwen/Qwen3-Coder-Next    # 80B total / 3B active MoE — see fit note
  system_prompt: |                            # mirror of AGENTS.md
    You are lecodeur, the local coding agent of the Culture mesh. ...
  acp_command: [opencode, acp]
```

**Served model:** `Qwen/Qwen3-Coder-Next` (80B total, 3B active MoE). The official
weights are **BF16 (~160GB)**, which does **not** fit this host (DGX Spark, 128GB
unified memory) — the local vLLM deployment must use a **quantized variant**
(FP8 ≈ ~80GB, or one of the community quants). Pin the exact quantized repo in the
`model:` string at serve time; the line above names the family, not necessarily the
weights that get loaded.

Do not add a Claude/`CLAUDE.md`-driven runtime path. The agent's intelligence
comes from the served model; this file only guides contributors working in the repo.

## Current state — scaffolded

The AgentCulture sibling scaffold landed via **GitHub issue #1** ("Scaffold
lecodeur as a full CLI/PyPI AgentCulture sibling"). The structure and commands
below describe what is **present** in the repo today: the `lecodeur` package with
the `whoami`/`learn`/`explain` verbs, the test suite, CI, the vendored skills, and
the `acp`/vLLM `culture.yaml`. The agent itself (the served vLLM model doing coding
work) is the next phase — the CLI scaffold is its host, not yet its hands.

steward owns the sibling-pattern contract and is the canonical upstream for the
vendored skills; when extending the scaffold, copy from `../steward` and rename
`steward`→`lecodeur` / `steward-cli`→`lecodeur` (dist name).

## Project shape (afi-cli pattern, no `src/`)

Distributed as **`lecodeur`** on PyPI (dist name, import name, and binary all
`lecodeur` — no `-cli` suffix). Hatchling backend, Python ≥3.12.

```text
lecodeur/                    # Python package (pip install lecodeur)
├── __init__.py             # __version__ via importlib.metadata("lecodeur")
├── __main__.py             # python -m lecodeur
└── cli/
    ├── __init__.py         # argparse main(); _LecodeurArgumentParser (routes .error() through emit_error)
    ├── _errors.py          # LecodeurError + EXIT_USER_ERROR / EXIT_ENV_ERROR
    ├── _output.py          # emit_result / emit_error / emit_diagnostic — strict stdout/stderr split
    └── _commands/          # one module per verb; each exposes register(sub) + a handler
        ├── whoami.py       # smallest identity probe — reads culture.yaml (supports --json)
        ├── learn.py        # orientation verb
        └── explain.py      # affordance verb (e.g. `lecodeur explain backend`)
tests/                       # pytest suite (tests/test_cli.py)
.claude/skills/              # vendored skills — see Skills convention
.github/workflows/           # tests.yml + publish.yml
pyproject.toml               # version source-of-truth
CHANGELOG.md                 # Keep-a-Changelog
AGENTS.md                    # runtime system prompt (acp backend)
culture.yaml                 # agent declaration (backend: acp, vllm-local model)
.flake8 / .markdownlint-cli2.yaml   # repo-local lint config — no per-user home configs
```

**Mutation safety:** any verb that writes defaults to **dry-run**; require an
explicit `--apply` flag to commit changes. The initial verbs (`whoami`/`learn`/
`explain`) are read-only. This is the load-bearing convention for a coding agent —
honor it for every new write verb.

## Build / test / publish

- **Install for dev:** `uv sync`.
- **Run CLI from source:** `uv run lecodeur --version` / `uv run python -m lecodeur whoami`.
- **Tests:** `uv run pytest -n auto -v`. Run a single test:
  `uv run pytest tests/test_cli.py::test_whoami_text -v`. Coverage in CI:
  `uv run pytest -n auto --cov=lecodeur --cov-report=xml`.
- **Lint:** `uv run black --check lecodeur tests`, `uv run isort --check-only .`,
  `uv run flake8`, `uv run bandit -r lecodeur`, `markdownlint-cli2 "**/*.md"`.
  Line length is **100** (black/isort/flake8 all agree).
- **Version bump — required on every PR:**
  `python3 .claude/skills/version-bump/scripts/bump.py {patch|minor|major}` updates
  `pyproject.toml` and prepends a CHANGELOG entry. The `version-check` CI job fails
  the run if the PR version equals main's — **no exception for docs/config-only PRs**
  (AgentCulture rule). `lecodeur.__version__` reads from package metadata; there is
  no separate literal to keep in sync.
- **Publish:** push to `main` triggers `publish.yml` → `uv build` → publishes
  `lecodeur` to PyPI via **Trusted Publishing** (OIDC, no API tokens). PRs
  publish a `.dev<run_number>` to TestPyPI; fork PRs are skipped (no OIDC context).

## Skills convention (cite-don't-import)

Six skills are **vendored from steward** (the canonical upstream) by copying each
`../steward/.claude/skills/<name>/` verbatim into `.claude/skills/<name>/`. Once
copied, this repo **owns** its copy and may diverge:

`cicd` (PR lifecycle on `agex pr`, plus Sonar gating), `communicate` (cross-repo
issues and mesh messages via `agtag`), `version-bump`, `run-tests`, `sonarclaude`,
`doc-test-alignment`.

Every skill ships `SKILL.md` (why/when) + `scripts/<entry-point>` (the automation —
following a skill should be "run this script," not ten manual steps). **No external
path dependencies**: scripts must not reach outside this repo; vendor what they need
into their own `scripts/`. This is what makes skills portable across the mesh.

Per-machine paths live in **`.claude/skills.local.yaml`** (git-ignored); a committed
**`.claude/skills.local.yaml.example`** documents every key. Skills read the local
file, falling back to the example.

## Lane discipline

- **lecodeur scaffolds and maintains its own repo.** The scaffold work in issue #1
  is lecodeur's to do — that is why steward filed the issue here rather than editing
  this repo (steward never writes into siblings).
- **Do not edit `../steward` from here.** The acceptance criterion to add lecodeur to
  steward's `docs/skill-sources.md` downstream column is a **separate PR against the
  steward repo**, not an edit made from this checkout.
- Sibling paths (`../steward`, `../daria`, `../culture`) assume the shared-workspace
  layout. If the checkout differs, treat them as descriptive project names.

## Conventions and workflow

**Memory discipline — recall before, remember after.** This repo keeps its
eidetic memory **in-repo and public**: records resolve to
`<repo-root>/.eidetic/memory` — committed, and shared with the team and mesh
peers (the `claude` and `colleague` backends both read the same
`lecodeur` scope), so memory travels with the repo, not a private
home-dir store. Make it a per-task habit:

- **`/recall` before you start.** Search the store for the area you're about
  to touch — prior decisions, gotchas, "have we done this before?" — so you
  build on what's already known instead of re-deriving it. Do this before
  non-trivial tasks, not just when asked.
- **`/remember` when something worth keeping surfaces.** A non-obvious
  decision and its rationale, a constraint, a fix and *why* it was needed, a
  gotcha that cost time, a fact the next session would otherwise re-learn.
  Capture it as it happens, not at the end when it's faded.

A plain `/remember` lands the note in `./.eidetic/memory` in this repo — no
flag needed (the wrappers here default to `--visibility public`; in-repo
routing needs `eidetic >= 0.10.0`, older CLIs keep records in `$HOME`). Keep
something out of the committed store only by passing `--visibility private`
(routes to `$HOME/.eidetic/memory`, never committed); `/recall` reads both
stores and merges. Don't store what the repo already records (code structure,
git history, what's already in this file or `CHANGELOG.md`) — store what you'd
have to re-derive. These are the `recall`/`remember` skills (`.claude/skills/`),
backed by the `eidetic` store.
