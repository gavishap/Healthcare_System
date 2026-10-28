You are a fresh blind council reviewer, not a seat. No tools, file access, writes or delegation. The opinions below are shuffled and stripped of author/model identity. Use the neutral context and then answer exactly three questions in 300-450 words total: 1. Strongest opinion and why (pick one letter). 2. Biggest blind spot in any single opinion. 3. What all available opinions missed. Do not infer absent perspectives or invent medical evidence.

# Neutral Council Context

Decision: What architecture, evidence policy, LLM/tool responsibilities, and implementation sequence best satisfy this healthcare briefing challenge while retaining a sensible path to a full-stack application?

Source facts: The supplied PDF asks for a demonstrable prototype (~120 minutes), a single business pitch slide (~10 minutes), and a live interview (~20 minutes). The transcript describes 2 hours plus 30 minutes Q&A/slide, so exact timing differs slightly. Cloud deployment is optional bonus; local working slice sufficient. Data must be sourced by builder. Provided infrastructure is optional n8n and Portkey gateway configured with Claude Sonnet 4.5 through Bedrock; credentials are not supplied to this session. No application code exists. Only an initialized Obsidian/Omnia knowledge vault exists. The owner currently asks for planning and notes, not implementation or publication.

User and workflow: A HEALTH SYSTEM STRATEGY TEAM enters a medical condition. It receives a structured briefing on current standard of care, emerging treatments in development, and companies/institutions involved. It has no patient data or clinical treatment recommendation workflow. Gabriel proposed fuzzy condition resolution with user confirmation, live evidence retrieval, relevance/trust pruning, visualizations, evidence comparison, sponsor mapping, and research provenance. The interviewer corrected doctor/patient framing, advised primary regulatory/trial/publication evidence over news, rejected reputation/awards/reviews as a trust basis, cautioned against circular citation and duplicate evidence, and asked for deterministic source-type/study-stage/metadata policy rather than an LLM council deciding source authority. Expert review should validate the policy. Current accepted direction compares evidence strength and development stage, not patient treatment suitability. A 30/60-day news window was suggested for discovery, not a requirement to discard older current guidelines. No supported condition, budget, jurisdiction, production auth, or expert-approved policy is chosen. Assume a US-focused prototype explicitly marked as an assumption; other geographies must be labeled.

Options to compare fairly: (A) typed Python FastAPI service with thin React/TypeScript UI and explicit bounded research workflow; (B) one TypeScript full-stack service with typed schemas; (C) fastest Streamlit or n8n-based prototype with an upgrade path; (D) autonomous multi-agent research/council runtime. You may propose another design. Distinguish development-time council (this process) from any application runtime council. Avoid treating model agreement as clinical truth.

Verified source capabilities: PubMed has public NCBI E-utilities and abstract/index metadata (not always full text); ClinicalTrials.gov API v2 supplies study records, with sponsor/investigator responsible for accuracy, and registry presence is not efficacy/approval; FDA Drugs@FDA supplies approval history and labeling for covered products, while an arbitrary label listing alone is not proof of approval; current authoritative guidelines are needed for standard-of-care claims and must match jurisdiction/subtype. MeSH can help biomedical term resolution. Guideline access/coverage for arbitrary conditions is unverified. Public Portkey docs describe Bedrock tool/structured-output support; the actual provided enterprise gateway's behavior must be tested. FastAPI validates response models; in-process background tasks are not a durable job system. These are source capabilities, not proof any integration already works.

Constraints: Optimize first for a truthful live vertical slice with visible evidence, bounded cost/time, partial failures, replay labeled with timestamps, no invented results. Show unknowns instead of claiming complete search. Preserve source IDs, snapshots/locators, claim-to-source links, publication/update/retrieval dates, evidence family deduplication, conflicts and exclusions. Ranking weights are provisional until domain expert review; policy must not imply calibrated certainty. LLM tool requests execute only through typed allowlisted server functions. Client never gets model keys. Avoid schema-only validation being described as proof of factual correctness. Address prompt injection/SSRF safely and proportionately. Favor concrete contracts, manageable scope, and a buildable day-one sequence over architectural theater.

Each seat must independently argue its assigned angle in 150-300 words, identify a preferred option, decisive tradeoffs and the biggest failure mode. No tools, writes, further delegation, or other seats' opinions; use this supplied pack. End with exactly POSITION: <one sentence>. Do not present unverified medical claims as facts.


Opinion A
As an outsider, I would choose **one TypeScript full-stack service** for both the two-hour prototype and the initial product. One language, shared schemas, and one deployment keep the prototype achievable without creating a separate architecture to replace later. A typed Python API plus React becomes attractive when substantial Python-specific analysis justifies the extra boundary.

For two hours, build one complete path: condition input, retrieval from a small approved source set, an evidence table, and a cited briefing covering care landscape, emerging therapies, and organizations. Keep the source documents and retrieval dates. Streamlit/n8n can demonstrate the flow quickly, but offers a weaker starting point for the intended product experience. Autonomous multi-agent orchestration adds coordination and debugging costs before its benefit is established.

**Deterministic code should own the evidence contract:** source permissions, retrieval, document identifiers, provenance, citation resolution, structured validation, retries, and execution budgets. Keep trial phase, regulatory status, evidence strength, geography, and observation date as separate fields. Every substantive claim must reference a stored evidence passage; unsupported fields remain unknown. Citation checks establish traceability; semantic support still needs evaluation and selective human review.

The LLM should interpret the condition, propose searches, request allowlisted tools through validated schemas, extract candidate facts, reconcile conflicting findings, and synthesize the briefing. It must preserve uncertainty and distinguish reported results from strategic interpretation. Tool permissions and publication checks remain outside the model.

For the product, add durable storage, background jobs, access controls, and evaluation datasets while retaining this division.

POSITION: Build a single TypeScript service with deterministic evidence controls and a bounded LLM research loop, expanding the architecture only when measured needs justify it.

Opinion B
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

Opinion C
I prefer **C: a single Streamlit application with typed Python contracts and separate retrieval, evidence-policy, and presentation modules**. With no application code or credentials available, this offers the strongest chance of a truthful demonstration within 120 minutes. A and B offer cleaner full-stack foundations but consume time on service and UI integration. n8n is useful if already configured; its optional availability provides little scheduling certainty. D adds coordination, latency, and verification work without improving evidence authority.

Scope the demonstration to **one explicitly supported condition and a US jurisdiction assumption**, with alias confirmation. Use a small, builder-curated baseline from accessible authoritative guidelines and relevant regulatory/publication records, plus one bounded live ClinicalTrials.gov integration for emerging treatments and sponsor mapping. Display missing coverage openly.

Apply deterministic source-type, study-stage, jurisdiction, and metadata rules. Preserve source identifiers, locators, snapshots, dates, claim links, evidence-family duplicates, conflicts, and exclusions. Any ordering remains provisional pending expert review. Registry entries describe development activity; they cannot establish efficacy or approval.

The LLM may draft a structured summary from admitted evidence if gateway access works. Keep a deterministic briefing template available. Allow at most one bounded synthesis call; server functions own retrieval and validation. Use fixed upstream hosts, typed parameters, server-held keys, and source text treated as untrusted data.

Allocate 15 minutes to access checks and scope, 25 to evidence and contracts, 35 to live retrieval, 25 to briefing and provenance views, and 20 to failure handling and rehearsal. Replay carries original retrieval timestamps and a prominent label. Keep the pitch slide outside this build budget.

The biggest failure mode is unsupported standard-of-care coverage disguised by polished synthesis. Reusable modules provide the later migration path to FastAPI and React.

POSITION: Ship a narrow Streamlit evidence briefing with one live integration, explicit coverage limits, and an optional bounded LLM summary.