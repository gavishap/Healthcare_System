---
tags:
  - "concept"
topics:
  - "healthcare-system"
status: growing
created: 2026-10-27
updated: 2026-10-27
sources:
  - Raw/Sources/2026-10-27-sourcing-request.md
  - Raw/Sources/2026-10-27-sourcing-discovery-transcript.md
  - Raw/Sources/2026-10-27-sourcing-research.md
  - Raw/Sources/2026-10-27-sourcing-design.md
  - Raw/Sources/2026-10-27-openai-sourcing-selection.md
source_count: 5
aliases:
  - "Sourcing layer first draft"
---

# Healthcare Sourcing Layer — First Draft Plan

Build a bounded research workflow that turns a confirmed medical condition into an inspectable evidence package for a U.S. health system strategy team. Every item must show its origin, what it can support, its limitations and its connection to a study, intervention or organization. The broader application's architecture belongs to the separate architecture workstream; this plan defines its sourcing component.

**Status:** draft v0.1, prepared 2026-10-27. This is an implementation plan; no sourcing service or LLM integration has been built in this chat. Source-role documentation was checked, but no condition-specific clinical conclusion is established.

## 1. Carry Forward The Interview Decisions

The newly supplied transcript extends the earlier capture from 247 to 374 lines. Its later discussion explicitly fixes the prototype to the **United States**, asks for a small concrete source set, and suggests **PubMed for current-care literature** and **clinical-trials records for emerging treatments and companies**. FDA and CDC were discussed as examples; the interviewer narrows their roles to regulatory and public-health information.

The runtime agent operates inside a fixed, reviewable source policy. It cannot decide which institutions are authoritative on each run. The interview permits assuming client validation for the prototype exercise. That assumption allows development to proceed; it does not establish that an actual domain reviewer has approved this draft for operational use.

The output serves organizational research. Compare evidence, development stages and documented organizations; do not recommend a treatment for an individual or rank therapies as clinically best. Awards, company reputation, article popularity and model agreement are excluded from evidence authority.

## 2. Start With Four Source Families

| Source | Section it supports | What to retrieve and why | Boundary |
|---|---|---|---|
| **PubMed, NLM/NCBI** | Current-care literature; supporting published research for emerging treatments | PMID/DOI, title, authors, publication type/date, abstract and permitted full-text links. Provides reproducible literature discovery. | Indexing is not endorsement. Label metadata-only, abstract-only and full-text access. A paper match alone does not establish current care. |
| **ClinicalTrials.gov, NLM** | Emerging treatments; key companies and institutions | NCT ID, condition, interventions, design/phase, study status, results availability, dates, sponsor/collaborator roles and locations. One structured record supports both pipeline and organization views. | Information is submitted by study organizations/investigators. Registration is not proven benefit, U.S. approval or government endorsement. |
| **FDA, initially Drugs@FDA and associated approval documents** | U.S. regulatory context across sections | Covered product, ingredient, application, applicant, approval action, exact indication/population and relevant approved labeling. | Generic label listings are insufficient. No match means unknown within searched coverage, not proof of nonapproval. Devices and uncovered biologics require separate adapters. |
| **A registered U.S. guideline issuer for the selected condition** | Current standard of care | Checked guideline version, relevant population, recommendation section, publication/update date and accessible supporting passage. | This fourth source is a design addition. It closes the gap between finding literature and substantiating a current recommendation. |

Source roles are supported by [PubMed Help](https://pubmed.ncbi.nlm.nih.gov/help/), [NLM's trial-record explanation](https://www.nlm.nih.gov/pubs/techbull/mj24/mj24_Clinical_Trials_Study_Record_Modernization.html), [ClinicalTrials.gov common questions](https://clinicaltrials.gov/find-studies/for-patients/common-questions) and [About Drugs@FDA](https://www.fda.gov/drugs/drug-approvals-and-databases/about-drugsfda). These sources serve different claim types; they do not form one universal trust ranking.

**Proposed first example: adult type 2 diabetes in the U.S.** Use the American Diabetes Association's [official Standards of Care](https://professional.diabetes.org/standards-of-care) as the candidate guideline anchor. Its page identifies the 2026 edition and possible interim updates. Verify relevant sections, currency, accessibility and retention permissions before using them. This condition and issuer are proposed here, rather than selected in the interview. If the guideline cannot be retrieved, report the gap and keep current-care claims unavailable.

**CDC remains optional:** use a relevant CDC document for public-health context or a specific applicable guideline when the condition warrants it. It is not a required connector for this first example. News and press releases are optional discovery leads in a later increment. The first slice uses the four sources above without a news feed or social search.

## 3. Make The Policy Explicit Before Retrieval

Define a versioned source registry with each connector's identity, permitted endpoints/hosts, document classes, allowed claim types, condition coverage, jurisdiction, required metadata and review status. Bind guideline entries to concrete documents/versions. New institutions require a reviewed configuration change; the runtime model cannot add them.

Apply claim-specific boundaries:

- **Current-care claim:** requires an applicable, current guideline passage and attribution to its issuer. Keep historical or uncertain guidance visibly limited.
- **Development claim:** a trial record can establish registered phase/status and intervention details. Preserve missing or non-applicable phase values; do not treat phase as efficacy.
- **Efficacy claim:** requires relevant results in an accessible study report or posted results. Preserve design, population, comparator and endpoint limitations; no-results registration cannot support benefit.
- **Approval claim:** requires the covered regulator's product/indication evidence. Keep regulatory, study and recruitment status separate.
- **Organization claim:** requires a documented role. Sponsor, collaborator, study site, applicant and author affiliation remain distinct; none automatically proves ownership or manufacturing rights.

Use the existing [[Wiki/Concepts/healthcare-evidence-policy|evidence policy]] for final claim eligibility. Sourcing supplies evidence and metadata-screening results; the downstream validator checks proposed claims against them. A source passing retrieval checks is not a medical truth certification.

## 4. Run The Workflow In A Bounded Sequence

1. **Resolve scope.** Preserve the input and confirm condition/subtype, population and U.S. jurisdiction. Suggest terminology matches; unresolved ambiguity returns clarification. Start with one supported profile.
2. **Build the required source plan.** Code selects the registered guideline, PubMed search, trial search and regulatory path. The model cannot omit required source attempts.
3. **Retrieve baseline evidence.** Fetch guideline/literature/trials independently where possible. Use normalized candidate interventions for targeted FDA lookups afterward. Log queries, filters, timestamps, source failures and result caps.
4. **Capture and normalize.** Retain permitted source text/JSON, stable IDs, source versions/hashes, access level and exact locators. Keep source publication/update dates separate from retrieval time.
5. **Screen metadata and identity.** Check source identity, relevance and applicability; identify missing metadata, retractions/corrections and superseded versions. Domain membership alone is insufficient. Record exclusions and reasons.
6. **Use the agent only for gaps.** It may propose a synonym, intervention alias or narrowly targeted follow-up against the approved tools. The server checks scope, source and remaining budget before execution.
7. **Link and deduplicate.** Connect documents to identifiable NCT/PMID/DOI study families and organization roles. Multiple reports of one study do not become multiple independent studies. Unknown overlap stays unknown.
8. **Return the evidence package.** Include candidate evidence, conflicts, limitations, rejected-item diagnostics and coverage. The application can then validate claims and assemble its briefing.

For the first version, follow only an explicitly approved document link, such as a PubMed record to its registered guideline publisher or permitted PMC article. Use one controlled hop and resolve canonical identifiers directly where available. Do not recursively chase news citations. Record loops or unavailable underlying evidence as unresolved.

Keep U.S. approval/care jurisdiction separate from study geography: ClinicalTrials.gov contains international research. Global studies may inform a U.S. strategy briefing, but their population and applicability must be visible. A recent 30/60-day view is an optional filter for activity, not a restriction on established guidelines. Explain which date each filter uses.

## 5. Separate LLM Access From Search Access

**Provider selected: OpenAI.** Use the Responses API for model access and its hosted `web_search` for supplemental discovery, with registry-derived domain filters and retained source URLs. This capability is documented in [official OpenAI documentation](https://developers.openai.com/api/docs/guides/tools-web-search); actual account/model access is untested. Keep the model configurable and `OPENAI_API_KEY` in the backend environment. A separate search vendor is not planned for this route. Direct biomedical connectors remain primary.

The LLM prepares constrained searches and extracts candidate passages. Server tools perform retrieval. An LLM API key enables web search only when the supplied provider/gateway exposes that capability; otherwise a separate search backend is needed. Public biomedical API access is configured independently. The first deterministic retrieval path can work before a model is connected.

Keep the provider adapter and model configurable, with OpenAI selected and no implicit third-party base-URL override. Once credentials are available in backend environment variables, test authentication, a real function-tool round trip, structured output and hosted search on that route. If it lacks a feature, report the limitation and use an explicitly configured alternative; do not silently change providers or describe ordinary API retrieval as model-driven web search.

Start with at most **20 candidate records across the run**, including supplemental retrieval, with provisional slots of one guideline, eight trial records, eight literature records and three regulatory records. Permit at most **two agent follow-up rounds and four supplemental tool calls** within that cap. Apply configured token, cost and wall-time limits, bounded retries and per-source rate controls. Show truncation and unmet coverage. These are engineering defaults to evaluate, not validated medical thresholds or a promise of comprehensive coverage.

## 6. Implement In This Order

| Step | Deliverable | Done when |
|---|---|---|
| 1. Freeze the first profile and policy | U.S. condition profile, source registry, claim-type rules and draft policy version | Required sources and scope are explicit; candidate guideline access is checked |
| 2. Wire ClinicalTrials.gov first | Typed trial records and sponsor/collaborator relationships | One live NCT record and one role can be traced to saved JSON fields; missing/results states remain accurate |
| 3. Add PubMed | Reproducible queries, PMID/DOI records and access labels | One relevant live publication has inspectable metadata and available evidence text |
| 4. Bind the guideline | Versioned, permitted recommendation excerpts | One current-care candidate resolves to the relevant guideline section; otherwise the section is unavailable |
| 5. Add targeted FDA checks | Product/indication lookup with matched/ambiguous/unknown states | One lookup is inspectable and generic labels cannot masquerade as approval proof |
| 6. Add bounded LLM discovery | Provider adapter, constrained search plan and tool execution | A real tool request/result is recorded; the model cannot expand source policy or exceed budgets |
| 7. Package and integrate | Stable sourcing result plus reproducible fixtures | The architecture workstream can consume it without needing scraping logic or provider prompts |

Steps 2–5 produce useful deterministic sourcing. Step 6 adds targeted discovery where gaps justify it. Keep the same output contract for both paths. No full-system framework, database or deployment decision is required to approve this sourcing plan.

## 7. Acceptance And Handoff

The first completed slice must provide an inspectable guideline-supported current-care candidate, a registered emerging-treatment candidate, and a documented organization role, with FDA context or an explicit coverage limitation. Every surfaced evidence ID must resolve to the stored version and exact passage/field. Every source attempt must distinguish success, no matches, blocked access, failure and unattempted work.

Evaluate fixtures for a no-results trial, duplicate study reports, circular citations, superseded/retracted material, different subtypes, incompatible findings, missing organization roles, misleading FDA labels, paywalls, malicious source text, throttling and budget exhaustion. These cases must not become unsupported affirmative care, benefit or approval claims. Preserve conflicting evidence instead of averaging it or taking a model vote. Record reviewer observations separately from automated reference checks.

The integration contract is [[Wiki/Concepts/healthcare-sourcing-contract|Sourcing runtime contract]]. The broader application receives evidence and coverage; final briefing language and final claim validation remain its responsibility.

**Still required for implementation:** model and credentials supplied through local backend configuration; verification of OpenAI hosted-search access; the first condition/guideline selection and document-access check; operating budget/deadline. OpenAI is selected and U.S. scope is decided. Real domain-policy approval remains a prerequisite for operational use beyond the prototype assumption.
