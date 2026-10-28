# Supporting council session 01a17f86-eb1c-7492-8b9e-11c6f4afb22f

Chat ID: `01a17f86-eb1c-7492-8b9e-11c6f4afb22f`

Captured: 2026-10-28T00:43:31.586461+00:00

User-visible conversation. Full visible tool calls/results are in the accompanying JSONL. Credentials and local user/workspace paths are sanitized. Private model reasoning and system/developer scaffolding are excluded.

## 2026-10-27T22:41:55.860Z User

# AGENTS.md instructions for [PROJECT_ROOT]\omnia-vault

<INSTRUCTIONS>
# graphify
- **graphify** (`~/.Codex/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

--- project-doc ---

# AGENTS.md — Omnia Vault Rules

This folder is an **Omnia Vault**: an Obsidian **LLM Wiki** (captured sources
compiled into short, linked, source-traceable notes) + **Graphify code graphs**
of any tracked repos + a **relay** that lets different coding agents (Codex,
Claude Code, …) work the same project with zero copy-paste. The vault is the
project's memory; your chat history is not.

Every agent working in this folder follows these rules. The narrative guide is
[VAULT-GUIDE.md](VAULT-GUIDE.md); Claude-specific wiring is in
[CLAUDE.md](CLAUDE.md).

## The relay — FIRST and LAST thing in every session

- **Session start:** read `_relay/STATE.md` (the baton), run
  `python scripts/relay_tool.py status` and `git log --oneline -10`, then tell
  the user where things stand. Do not re-read raw sources or sweep code to
  resume. If the status tool warns the baton is stale, trust git + the newest
  `Wiki/Logs/` note, then repair STATE.md.
- **Session end (or when the user switches agents):** rewrite
  `_relay/STATE.md` (sections: Now / Just landed / Next / Open questions /
  Watch out — present-tense state, written for a stranger, brutally honest
  about what's unfinished), stamp it with
  `python scripts/relay_tool.py stamp --agent codex --summary "<paragraph>"`
  (use your own agent name), run the maintenance gate, and **commit**.
- Full protocol: `_relay/PROTOCOL.md`.

## Layers

| Layer | Path | Purpose |
|-------|------|---------|
| Raw sources | `Raw/Sources/` | Captured source material (transcripts, articles, notes). Never treat as compiled knowledge. |
| Raw files | `Raw/Files/` | Binary/attachment sources. Gitignored except `.gitkeep`. |
| Compiled Wiki | `Wiki/` | Short, linked, reusable notes compiled from Raw sources. The product. |
| Code graphs | `graphify/<repo>/` | Committed Graphify snapshots of tracked repos (generated — never hand-edit). |
| Relay | `_relay/` | The agent-to-agent baton (STATE.md), history, protocol. |
| Schema | `Schema/` | Frontmatter contracts, naming, lint rules, command reference. |
| Templates | `_templates/` | Note templates for every note type. |
| Tooling | `scripts/` | Deterministic build/lint/audit/relay tools (python stdlib only). |
| Chat archive | `chats/` | Both agents' transcripts as **local memory** (gitignored; secrets redacted on import). |

## Core rules

1. **Write reusable knowledge only under `Wiki/`** — topics in `Wiki/Topics/`,
   concepts in `Wiki/Concepts/`, entities in `Wiki/Entities/`, projects in
   `Wiki/Projects/`, logs in `Wiki/Logs/`.
2. **Never edit Raw sources to "improve" them**; compile them into `Wiki/`
   notes instead.
3. **Every compiled note links to its Raw sources**: `sources` lists real
   files under `Raw/Sources/`, and `source_count == len(sources)`. Never
   invent citations — no source, no claim (capture it as an Open Question).
4. **Search before reading broadly:**
   `python scripts/wiki_tool.py search-catalog --query "text"` first; open Raw
   sources only when compiled notes are insufficient. For code questions, the
   graph comes even earlier — see the 3-Layer Query Rule below.
5. **Maintenance gate before every commit** (use `python3` on macOS/Linux):

   ```bash
   python scripts/wiki_tool.py doctor
   python scripts/wiki_tool.py build
   python scripts/wiki_tool.py lint
   python scripts/wiki_tool.py source-lint
   python scripts/audit_public.py
   ```

   After source ingestion, also
   `python scripts/wiki_tool.py source-scan --update --accept-covered` then
   `source-lint`. All must pass.
6. **Never commit:** secrets, machine-local absolute paths, tracked work-repo
   code (gitignore repo folders; only `graphify/<repo>/` snapshots are
   committed), Obsidian plugin/cache state, or hand edits to generated files
   (`Wiki/catalog.jsonl`, `*/index.md`, `Schema/source-manifest.jsonl`,
   `graphify/`).

## 3-Layer Query Rule (questions about the project/code)

1. **Graph:** `graphify query "<question>" --graph graphify/<repo>/graph.json`
   (also `explain` / `path` / `affected`; overview in
   `graphify/<repo>/_GRAPH_REPORT.md` and `_COMMUNITY_*.md`).
2. **Wiki:** `python scripts/wiki_tool.py search-catalog --query "<topic>"` →
   top 1–3 notes.
3. **Raw:** the cited source file / the specific code files only.

## Workflows (readable by any agent — follow the file, not the folder name)

- Ingest a source: `.claude/skills/llm-wiki-ingest/SKILL.md`
- Ingest a recording or video URL: `.claude/skills/video-ingest/SKILL.md`
- Adopt an existing project: `.claude/skills/import-project/SKILL.md`
- The living plan + plan-aware intel triage ("is this video worth using?"):
  `.claude/skills/war-room/SKILL.md` — plan digest
  (`python scripts/plan_tool.py context`) BEFORE watching; the user gates
  every incorporation and every tool install.
- Answer questions: `.claude/skills/project-context-query/SKILL.md`
- Validate/fix notes: `.claude/skills/llm-wiki-lint/SKILL.md`
- Maintain/commit: `.claude/skills/llm-wiki-maintain/SKILL.md`
- Agent handoff (async baton): `.claude/skills/relay/SKILL.md`
- Cross-model plan/diff review (sync — before high-stakes builds):
  `.claude/skills/sparring/SKILL.md`. Works with Codex as the driver too:
  start with `--driver codex --reviewer claude` and use headless Claude
  (`claude -p ... --permission-mode plan --output-format json`) as the
  read-only critic; same `scripts/spar_tool.py` state, same rules.
- Cross-model decision panel (breadth, before locking a direction):
  `.claude/skills/council/SKILL.md` — five blind seats split across both
  models, anonymized cross-bench review, ruled verdict recorded in
  `_relay/council/`. The driving agent chairs; seats on the other model run
  headlessly (fresh thread/session per seat, never reused).
- GitHub PRs without gh CLI: `.claude/skills/github-pr-api/SKILL.md`
- Obsidian editing: `.claude/skills/obsidian-markdown/SKILL.md` (+ bases,
  canvas, cli, defuddle)
- Outward updates/reports: `.claude/skills/stakeholder-update-writing/SKILL.md`

## Reference

- Frontmatter contracts: `Schema/frontmatter-schema.md`
- Naming rules: `Schema/naming-conventions.md`
- Lint rules: `Schema/lint-checklist.md`
- Every command: `Schema/command-reference.md`
- Worked examples: `Schema/workflow-examples.md`

## Environment

- `python` on Windows, `python3` on macOS/Linux; scripts are stdlib-only.
- Optional tooling check: `python scripts/setup_vault.py --check`
  (git, graphify, crv, ffmpeg, node — all optional, each unlocks a feature).
- On Windows PowerShell set `$env:PYTHONUTF8=1` before `graphify`/`crv`.

</INSTRUCTIONS>
<environment_context>
  <cwd>[PROJECT_ROOT]\omnia-vault</cwd>
  <shell>powershell</shell>
  <current_date>2026-10-27</current_date>
  <timezone>America/New_York</timezone>
  <filesystem><workspace_roots><root>[PROJECT_ROOT]\omnia-vault</root></workspace_roots><permission_profile type="managed"><file_system type="restricted"><entry access="read"><special>:root</special></entry></file_system></permission_profile></filesystem>
</environment_context>

## 2026-10-27T22:41:56.070Z User

Operator: ground the decision in what can actually ship within the prototype budget.

# Neutral Council Context

Decision: What architecture, evidence policy, LLM/tool responsibilities, and implementation sequence best satisfy this healthcare briefing challenge while retaining a sensible path to a full-stack application?

Source facts: The supplied PDF asks for a demonstrable prototype (~120 minutes), a single business pitch slide (~10 minutes), and a live interview (~20 minutes). The transcript describes 2 hours plus 30 minutes Q&A/slide, so exact timing differs slightly. Cloud deployment is optional bonus; local working slice sufficient. Data must be sourced by builder. Provided infrastructure is optional n8n and Portkey gateway configured with Claude Sonnet 4.5 through Bedrock; credentials are not supplied to this session. No application code exists. Only an initialized Obsidian/Omnia knowledge vault exists. The owner currently asks for planning and notes, not implementation or publication.

User and workflow: A HEALTH SYSTEM STRATEGY TEAM enters a medical condition. It receives a structured briefing on current standard of care, emerging treatments in development, and companies/institutions involved. It has no patient data or clinical treatment recommendation workflow. Gabriel proposed fuzzy condition resolution with user confirmation, live evidence retrieval, relevance/trust pruning, visualizations, evidence comparison, sponsor mapping, and research provenance. The interviewer corrected doctor/patient framing, advised primary regulatory/trial/publication evidence over news, rejected reputation/awards/reviews as a trust basis, cautioned against circular citation and duplicate evidence, and asked for deterministic source-type/study-stage/metadata policy rather than an LLM council deciding source authority. Expert review should validate the policy. Current accepted direction compares evidence strength and development stage, not patient treatment suitability. A 30/60-day news window was suggested for discovery, not a requirement to discard older current guidelines. No supported condition, budget, jurisdiction, production auth, or expert-approved policy is chosen. Assume a US-focused prototype explicitly marked as an assumption; other geographies must be labeled.

Options to compare fairly: (A) typed Python FastAPI service with thin React/TypeScript UI and explicit bounded research workflow; (B) one TypeScript full-stack service with typed schemas; (C) fastest Streamlit or n8n-based prototype with an upgrade path; (D) autonomous multi-agent research/council runtime. You may propose another design. Distinguish development-time council (this process) from any application runtime council. Avoid treating model agreement as clinical truth.

Verified source capabilities: PubMed has public NCBI E-utilities and abstract/index metadata (not always full text); ClinicalTrials.gov API v2 supplies study records, with sponsor/investigator responsible for accuracy, and registry presence is not efficacy/approval; FDA Drugs@FDA supplies approval history and labeling for covered products, while an arbitrary label listing alone is not proof of approval; current authoritative guidelines are needed for standard-of-care claims and must match jurisdiction/subtype. MeSH can help biomedical term resolution. Guideline access/coverage for arbitrary conditions is unverified. Public Portkey docs describe Bedrock tool/structured-output support; the actual provided enterprise gateway's behavior must be tested. FastAPI validates response models; in-process background tasks are not a durable job system. These are source capabilities, not proof any integration already works.

Constraints: Optimize first for a truthful live vertical slice with visible evidence, bounded cost/time, partial failures, replay labeled with timestamps, no invented results. Show unknowns instead of claiming complete search. Preserve source IDs, snapshots/locators, claim-to-source links, publication/update/retrieval dates, evidence family deduplication, conflicts and exclusions. Ranking weights are provisional until domain expert review; policy must not imply calibrated certainty. LLM tool requests execute only through typed allowlisted server functions. Client never gets model keys. Avoid schema-only validation being described as proof of factual correctness. Address prompt injection/SSRF safely and proportionately. Favor concrete contracts, manageable scope, and a buildable day-one sequence over architectural theater.

Each seat must independently argue its assigned angle in 150-300 words, identify a preferred option, decisive tradeoffs and the biggest failure mode. No tools, writes, further delegation, or other seats' opinions; use this supplied pack. End with exactly POSITION: <one sentence>. Do not present unverified medical claims as facts.


## 2026-10-27T22:42:19.558Z Assistant

I prefer **C: a single Streamlit application with typed Python contracts and separate retrieval, evidence-policy, and presentation modules**. With no application code or credentials available, this offers the strongest chance of a truthful demonstration within 120 minutes. A and B offer cleaner full-stack foundations but consume time on service and UI integration. n8n is useful if already configured; its optional availability provides little scheduling certainty. D adds coordination, latency, and verification work without improving evidence authority.

Scope the demonstration to **one explicitly supported condition and a US jurisdiction assumption**, with alias confirmation. Use a small, builder-curated baseline from accessible authoritative guidelines and relevant regulatory/publication records, plus one bounded live ClinicalTrials.gov integration for emerging treatments and sponsor mapping. Display missing coverage openly.

Apply deterministic source-type, study-stage, jurisdiction, and metadata rules. Preserve source identifiers, locators, snapshots, dates, claim links, evidence-family duplicates, conflicts, and exclusions. Any ordering remains provisional pending expert review. Registry entries describe development activity; they cannot establish efficacy or approval.

The LLM may draft a structured summary from admitted evidence if gateway access works. Keep a deterministic briefing template available. Allow at most one bounded synthesis call; server functions own retrieval and validation. Use fixed upstream hosts, typed parameters, server-held keys, and source text treated as untrusted data.

Allocate 15 minutes to access checks and scope, 25 to evidence and contracts, 35 to live retrieval, 25 to briefing and provenance views, and 20 to failure handling and rehearsal. Replay carries original retrieval timestamps and a prominent label. Keep the pitch slide outside this build budget.

The biggest failure mode is unsupported standard-of-care coverage disguised by polished synthesis. Reusable modules provide the later migration path to FastAPI and React.

POSITION: Ship a narrow Streamlit evidence briefing with one live integration, explicit coverage limits, and an optional bounded LLM summary.
