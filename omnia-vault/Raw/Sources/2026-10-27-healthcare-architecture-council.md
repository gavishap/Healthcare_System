---
Title: "Healthcare briefing architecture council record"
Reference: "_relay/council/2026-10-27-healthcare-briefing-architecture.md"
ContentType:
  - "markdown"
Created: 2026-10-27
Processed: true
tags:
  - "source"
---

# Council Capture

This source captures the original council record, including unavailable seats. It is model-generated engineering analysis, not clinical evidence or a five-seat cross-model consensus.

# Healthcare Briefing Architecture Council

Date: 2026-10-27. Chair: Codex. Invocation: owner explicitly requests the cloned vault council skill and Claude Code perspective.

## Method And Execution Status

Five independent seats were attempted in groups of at most three to respect concurrency limits. Each Codex seat used a fresh read-only CLI invocation; the Outsider ran from an empty temporary directory and received only a stripped decision. Claude seats each used a fresh headless plan-mode invocation, disabled tools and a supplied neutral pack; no prior session was resumed. Claude failures were retried once.

Codex CLI: 0.163.0-alpha.11.1; configured model gpt-6.1-sol with xhigh reasoning, not overridden. Claude Code: 2.1.234; no inference succeeded, so no active model identity is claimed. The Skeptic final output file was present and complete, but its wrapper retained inherited output handles after CLI exit; the wrapper was stopped after all three Codex final outputs had been verified. Subsequent review uses direct output files to avoid that process-handling issue. No model result was ghost-written.

The mixed available opinions were shuffled before blind review; the reviewer saw only letter labels. Missing Claude seats/reviewer are explicit limitations.

## Framed Question And Shared Context

# Neutral Council Context

Decision: What architecture, evidence policy, LLM/tool responsibilities, and implementation sequence best satisfy this healthcare briefing challenge while retaining a sensible path to a full-stack application?

Source facts: The supplied PDF asks for a demonstrable prototype (~120 minutes), a single business pitch slide (~10 minutes), and a live interview (~20 minutes). The transcript describes 2 hours plus 30 minutes Q&A/slide, so exact timing differs slightly. Cloud deployment is optional bonus; local working slice sufficient. Data must be sourced by builder. Provided infrastructure is optional n8n and Portkey gateway configured with Claude Sonnet 4.5 through Bedrock; credentials are not supplied to this session. No application code exists. Only an initialized Obsidian/Omnia knowledge vault exists. The owner currently asks for planning and notes, not implementation or publication.

User and workflow: A HEALTH SYSTEM STRATEGY TEAM enters a medical condition. It receives a structured briefing on current standard of care, emerging treatments in development, and companies/institutions involved. It has no patient data or clinical treatment recommendation workflow. Gabriel proposed fuzzy condition resolution with user confirmation, live evidence retrieval, relevance/trust pruning, visualizations, evidence comparison, sponsor mapping, and research provenance. The interviewer corrected doctor/patient framing, advised primary regulatory/trial/publication evidence over news, rejected reputation/awards/reviews as a trust basis, cautioned against circular citation and duplicate evidence, and asked for deterministic source-type/study-stage/metadata policy rather than an LLM council deciding source authority. Expert review should validate the policy. Current accepted direction compares evidence strength and development stage, not patient treatment suitability. A 30/60-day news window was suggested for discovery, not a requirement to discard older current guidelines. No supported condition, budget, jurisdiction, production auth, or expert-approved policy is chosen. Assume a US-focused prototype explicitly marked as an assumption; other geographies must be labeled.

Options to compare fairly: (A) typed Python FastAPI service with thin React/TypeScript UI and explicit bounded research workflow; (B) one TypeScript full-stack service with typed schemas; (C) fastest Streamlit or n8n-based prototype with an upgrade path; (D) autonomous multi-agent research/council runtime. You may propose another design. Distinguish development-time council (this process) from any application runtime council. Avoid treating model agreement as clinical truth.

Verified source capabilities: PubMed has public NCBI E-utilities and abstract/index metadata (not always full text); ClinicalTrials.gov API v2 supplies study records, with sponsor/investigator responsible for accuracy, and registry presence is not efficacy/approval; FDA Drugs@FDA supplies approval history and labeling for covered products, while an arbitrary label listing alone is not proof of approval; current authoritative guidelines are needed for standard-of-care claims and must match jurisdiction/subtype. MeSH can help biomedical term resolution. Guideline access/coverage for arbitrary conditions is unverified. Public Portkey docs describe Bedrock tool/structured-output support; the actual provided enterprise gateway's behavior must be tested. FastAPI validates response models; in-process background tasks are not a durable job system. These are source capabilities, not proof any integration already works.

Constraints: Optimize first for a truthful live vertical slice with visible evidence, bounded cost/time, partial failures, replay labeled with timestamps, no invented results. Show unknowns instead of claiming complete search. Preserve source IDs, snapshots/locators, claim-to-source links, publication/update/retrieval dates, evidence family deduplication, conflicts and exclusions. Ranking weights are provisional until domain expert review; policy must not imply calibrated certainty. LLM tool requests execute only through typed allowlisted server functions. Client never gets model keys. Avoid schema-only validation being described as proof of factual correctness. Address prompt injection/SSRF safely and proportionately. Favor concrete contracts, manageable scope, and a buildable day-one sequence over architectural theater.

Each seat must independently argue its assigned angle in 150-300 words, identify a preferred option, decisive tradeoffs and the biggest failure mode. No tools, writes, further delegation, or other seats' opinions; use this supplied pack. End with exactly POSITION: <one sentence>. Do not present unverified medical claims as facts.


## Outsider Context

Decision only: Choose an architecture for a two-hour prototype and later full-stack product that turns a medical condition into a cited research briefing for a health system strategy team: current care landscape, emerging therapies, and involved organizations. Options: typed Python API plus React, one TypeScript full-stack service, Streamlit/n8n, or an autonomous multi-agent workflow. How should deterministic evidence controls and LLM reasoning/tool calls divide responsibilities? The tool compares evidence/development stages rather than advising individual patients. Argue as an OUTSIDER who has no project history, in 150-300 words. No tools, file access, writes, or delegation. End POSITION: <one-sentence stance>.

## Skeptic — Codex

The fatal flaw is promising an arbitrary-condition briefing before proving access to current, applicable guidelines. PubMed, trial registries, and approval records cannot collectively substitute for that missing coverage. A polished synthesis could therefore mislabel emerging research as standard care while displaying impeccable citations. Schema validation and model agreement would not catch this category error.

I prefer **C: a Streamlit prototype with typed Python contracts and a bounded workflow**, with A as the expansion path. A and B are credible application architectures, but their additional setup earns little until the evidence workflow works. D adds unpredictable retrieval, cost, and coordination without resolving authority or completeness.

Try to kill the approach before building its presentation:

1. Select one condition and verify accessible US guideline coverage, including subtype and currency. If coverage fails, change the supported scope or explicitly leave standard care unresolved.
2. Produce one inspectable claim-to-source record manually. Require source identifiers, supporting passages or locators, relevant dates, jurisdiction, and evidence-family links.
3. Implement bounded retrieval and deterministic source classification. Preserve contradictions and exclusions; avoid an aggregate confidence score that suggests calibration.
4. Let the LLM propose condition matches and draft supported summaries. Server functions enforce tool allowlists and retrieval limits; retrieved text never authorizes tool execution.
5. Demonstrate partial failure and clearly timestamped replay before adding visualizations. Keep domain logic outside Streamlit so a later FastAPI/React application can reuse it.

The biggest failure mode is a convincing briefing whose apparent completeness exceeds its evidence coverage. Live retrieval does not establish currentness, and a replay must never masquerade as a fresh search.

POSITION: Build a narrowly supported Streamlit evidence slice first, and expand toward FastAPI/React only after its provenance and coverage limits survive inspection.

## Rebuilder — Claude

UNAVAILABLE: Authentication failed twice before inference. No opinion produced.

## Maximalist — Claude

UNAVAILABLE: Authentication failed twice before inference. No opinion produced.

## Outsider — Codex

As an outsider, I would choose **one TypeScript full-stack service** for both the two-hour prototype and the initial product. One language, shared schemas, and one deployment keep the prototype achievable without creating a separate architecture to replace later. A typed Python API plus React becomes attractive when substantial Python-specific analysis justifies the extra boundary.

For two hours, build one complete path: condition input, retrieval from a small approved source set, an evidence table, and a cited briefing covering care landscape, emerging therapies, and organizations. Keep the source documents and retrieval dates. Streamlit/n8n can demonstrate the flow quickly, but offers a weaker starting point for the intended product experience. Autonomous multi-agent orchestration adds coordination and debugging costs before its benefit is established.

**Deterministic code should own the evidence contract:** source permissions, retrieval, document identifiers, provenance, citation resolution, structured validation, retries, and execution budgets. Keep trial phase, regulatory status, evidence strength, geography, and observation date as separate fields. Every substantive claim must reference a stored evidence passage; unsupported fields remain unknown. Citation checks establish traceability; semantic support still needs evaluation and selective human review.

The LLM should interpret the condition, propose searches, request allowlisted tools through validated schemas, extract candidate facts, reconcile conflicting findings, and synthesize the briefing. It must preserve uncertainty and distinguish reported results from strategic interpretation. Tool permissions and publication checks remain outside the model.

For the product, add durable storage, background jobs, access controls, and evaluation datasets while retaining this division.

POSITION: Build a single TypeScript service with deterministic evidence controls and a bounded LLM research loop, expanding the architecture only when measured needs justify it.

## Operator — Codex

I prefer **C: a single Streamlit application with typed Python contracts and separate retrieval, evidence-policy, and presentation modules**. With no application code or credentials available, this offers the strongest chance of a truthful demonstration within 120 minutes. A and B offer cleaner full-stack foundations but consume time on service and UI integration. n8n is useful if already configured; its optional availability provides little scheduling certainty. D adds coordination, latency, and verification work without improving evidence authority.

Scope the demonstration to **one explicitly supported condition and a US jurisdiction assumption**, with alias confirmation. Use a small, builder-curated baseline from accessible authoritative guidelines and relevant regulatory/publication records, plus one bounded live ClinicalTrials.gov integration for emerging treatments and sponsor mapping. Display missing coverage openly.

Apply deterministic source-type, study-stage, jurisdiction, and metadata rules. Preserve source identifiers, locators, snapshots, dates, claim links, evidence-family duplicates, conflicts, and exclusions. Any ordering remains provisional pending expert review. Registry entries describe development activity; they cannot establish efficacy or approval.

The LLM may draft a structured summary from admitted evidence if gateway access works. Keep a deterministic briefing template available. Allow at most one bounded synthesis call; server functions own retrieval and validation. Use fixed upstream hosts, typed parameters, server-held keys, and source text treated as untrusted data.

Allocate 15 minutes to access checks and scope, 25 to evidence and contracts, 35 to live retrieval, 25 to briefing and provenance views, and 20 to failure handling and rehearsal. Replay carries original retrieval timestamps and a prominent label. Keep the pitch slide outside this build budget.

The biggest failure mode is unsupported standard-of-care coverage disguised by polished synthesis. Reusable modules provide the later migration path to FastAPI and React.

POSITION: Ship a narrow Streamlit evidence briefing with one live integration, explicit coverage limits, and an optional bounded LLM summary.

## Anonymization Mapping (Disclosed After Review)

- Opinion A: outsider
- Opinion B: skeptic
- Opinion C: operator

## Codex Blind Review

1. **Opinion C is strongest** because it translates the constraints into an executable demonstration: one supported condition, a stated US assumption, a curated evidence baseline, one live integration, and a bounded synthesis step that depends on gateway availability. Its time allocation makes the tradeoffs inspectable. Separating retrieval, evidence policy, and presentation also provides a credible migration path without requiring two application layers immediately. It addresses operational failures through labeled replay, visible coverage gaps, and a deterministic briefing fallback. B states the guideline-access prerequisite more forcefully, and that prerequisite should become an explicit gate within C’s initial access checks. C wins on overall implementation discipline, not because Streamlit establishes evidence quality.

2. **Opinion A’s biggest blind spot is its insufficiently gated day-one scope.** Its proposed complete path combines condition interpretation, search planning, multiple evidence sources, extraction, conflict reconciliation, and cited synthesis within two hours, despite having neither application code nor supplied credentials. Shared TypeScript schemas reduce integration overhead, but they do not resolve guideline accessibility, enterprise gateway compatibility, or evidence coverage. A correctly separates traceability from semantic support; however, it places evaluation datasets in the later product phase without defining a minimum factual acceptance check for the demonstration. The corrective step is to prove one accessible, applicable guideline source and one inspectable briefing record before committing to the broader research loop. Its architecture remains credible; its initial scope needs sharper admission and stopping rules.

3. **All three miss the immediate deliverable boundary and a concrete demonstration acceptance contract.** The owner currently authorizes planning and notes. Their implementation recommendations should therefore become a reviewable plan with assumptions, unresolved access questions, evidence contracts, and a timed runbook; implementation should remain a subsequent step.

   None specifies a small, predeclared set of expected behaviors against inspectable evidence. That set should test whether supporting passages actually justify claims, missing guideline coverage leaves standard care unresolved, registry activity remains distinct from approval or efficacy, duplicate evidence stays linked, and partial retrieval remains visible. These checks would demonstrate behavior without implying expert approval or calibrated certainty.

   They also leave the business pitch largely undeveloped. The slide should connect the briefing to the strategy team’s task: comparing documented care landscapes, development activity, and participating organizations while inspecting provenance and gaps. Any promised time savings or decision improvement should be presented as a hypothesis to evaluate.

## Claude Blind Review

UNAVAILABLE: No authenticated Claude session. No review is attributed.

## Council Verdict: Healthcare Briefing Architecture

**The bench:** Skeptic — Codex; Rebuilder — Claude unavailable; Maximalist — Claude unavailable; Outsider — Codex (isolated); Operator — Codex. This is an incomplete three-seat council with one Codex blind review, not a completed cross-model council. Claude Code authentication failed twice per seat with “OAuth session expired and could not be refreshed.” A later read-only auth check still reports logged out. The owner says they will sign in; no Claude opinion is attributed until a successful invocation exists.

### Consensus

All three available seats independently favor a narrow supported-condition slice, explicit provenance, deterministic evidence controls, bounded LLM work and visible uncertainty. All reject an autonomous runtime council as a substitute for evidence authority. Current applicable guideline coverage is the critical dependency; live retrieval and citation presence do not establish medical correctness.

### Dissent

Skeptic and Operator choose Streamlit for the strict two-hour prototype because no application scaffold exists. Outsider chooses one TypeScript full-stack service to avoid a later migration and reduce language boundaries. The Chair proposes FastAPI/Pydantic plus React as the target application architecture, agreeing with the majority that a Streamlit shell is the safer initial demo when setup time is unproven. No seat establishes the team's actual framework speed, so the target stack recommendation has moderate confidence and remains proposed.

Operator allows an optional LLM summary/deterministic fallback. The owner's requested LLM/tool-calling architecture still requires a real tool-call round trip in the intended demo; a source-only fallback must be labeled as degraded and cannot be represented as satisfying that capability. This preserves the useful failure path without silently changing the requirement.

### Caught In Review

The Codex reviewer selects the Operator opinion as the strongest executable plan, identifies overbroad day-one scope in the Outsider proposal, and adds an explicit demonstration acceptance contract: check semantic support, missing guidelines, registry versus efficacy/approval, evidence deduplication and partial-source visibility. The reviewer also restores the current authorization boundary (planning/notes only) and the business pitch as a separate planned deliverable. The second bench's review is absent because Claude is unavailable.

### The Chair's Ruling

Recommend a condition intelligence workbench for strategy analysts, with separate current-care, emerging-pipeline and organization views. Use explicit workflow stages, fixed source adapters, versioned claim-specific evidence rules, bounded tool calls, and cited synthesis. Show source/update/retrieval dates, eligibility reasons, conflicts and evidence-family links. No treatment leaderboard or opaque scalar trust score.

Target the full-stack product as a modular FastAPI/Pydantic service and thin React/TypeScript UI. Use SQLite/local immutable snapshots for a local single-user demonstration and PostgreSQL/object storage/durable workers for a shared pilot. With an unproven scaffold and a hard two-hour build window, begin with reusable Python domain modules in a Streamlit interface, then expose the same domain contracts through FastAPI/React. A one-language TypeScript service is a credible alternative if it is demonstrably the fastest proven team scaffold. Do not claim that this condition has already been established.

This is engineering advice with moderate confidence, limited by missing Claude perspectives, unknown team scaffold speed, unchosen guideline/condition and untested enterprise credentials. Domain experts must validate clinical evidence rules. Reopen the stack if setup exceeds the demo budget; reopen coverage if no applicable current guideline is available; reconsider an advisory critic only if labeled evaluations show measurable benefit at acceptable cost/latency.

### First Move

Select one condition and jurisdiction, then verify an accessible current guideline and one inspectable claim-to-source example before implementation.

