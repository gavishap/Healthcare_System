---
Title: "Owner-requested trace and correction of the diabetes briefing mismatch"
Reference: "Owner request, attached Evidence Desk screenshot, saved PostgreSQL source versions, local code and verification, 2026-10-27"
ContentType:
  - "markdown"
Created: 2026-10-27
Processed: true
tags:
  - "source"
---

# Request And Observed Evidence

The owner supplied ClinicalTrials.gov record NCT01954147 and an Evidence Desk screenshot, asking to trace how the result reached the briefing, identify whether search, retrieval, extraction or synthesis caused the mismatch, correct the pipeline, distinguish general conditions from specific populations, and rerun the same condition. The accompanying conversation described pregnancy-specific evidence for a type 2 diabetes input, a standard-care gap, and emerging-treatment/company relevance. The conversation is evidence of the requested behavior, not an instruction to trust its clinical interpretation.

## Original Run

- Run: `d9e18095-7c51-4688-9e2f-96d682c52f98`, policy v1, condition `Type 2 diabetes`, US, eight-record cap, live mode, model enabled. Four PubMed and four trial records were saved.
- Target citation: `cit_5816b118ee11720571114886`, rank 5, 3/3 condition words matched, trial status `UNKNOWN`, last update posted `2014-02-20`, no posted registry results. Snapshot SHA-256: `58913d03511e3b77a42090f38486317e36d2e3828d444aeb5948fc44449387a0`.
- Actual trial eligibility: type 2 diabetes, men and women aged 35–65, China. Positive pregnancy test and breastfeeding are exclusions. Umbilical cord describes the cell source; this is not a pregnancy cohort. The source also links a publication, so absence of posted registry results must not be described as absence of all published research.
- Original source: [ClinicalTrials.gov record](https://clinicaltrials.gov/study/NCT01954147); structured source: [official API record](https://clinicaltrials.gov/api/v2/studies/NCT01954147).
- Actual pregnancy-specific paper: [PMID 39084811](https://pubmed.ncbi.nlm.nih.gov/39084811/), “Diagnosis and Treatment of Hyperglycemia in Pregnancy: Type 2 Diabetes Mellitus and Gestational Diabetes.” Pediatric paper: [PMID 27974926](https://pubmed.ncbi.nlm.nih.gov/27974926/). Their findings appeared under general published care evidence. A cognitive-impairment paper also needed a separate population label.

## Causal Trace

1. The request confirmed a condition and US scope but did not resolve a separate population.
2. The saved PubMed query was `"Type 2 diabetes"[Title/Abstract] AND humans[MeSH Terms]`. The saved trial attempt recorded the condition, four-record cap and retrieval date, without a complete raw HTTP parameter log. Initially inspected connector code had no trial currency/status filter. Do not invent the original upstream order beyond the recorded rank/cap.
3. `parse_trial` retained full source JSON but exposed only title, summary, registry status and sponsor/collaborator passages to downstream processing. Eligibility, conditions, interventions, age and geography were not exposed as structured screening inputs.
4. `rank_documents` admitted sources based on identity, retraction and word overlap. Three condition-word matches sufficed for ordering; population, unknown recruitment status and the 2014 update did not gate emerging activity.
5. `structured_claims` copied every admitted registry title into emerging treatments and every sponsor into organizations. It recorded population as unknown and bypassed model semantic review as a field copy. This target produced one development statement and one sponsor statement.
6. The stored model tool-call IDs contain only the four PubMed citations, not the target trial. The two target claims therefore did not originate from model extraction. The model did preserve pregnancy/childhood wording in the literature statements, but synthesis displayed them under the general section because no population lane was enforced.
7. Current-care coverage was set to unavailable for every run because no registered guideline connector exists. The UI's “not established” headline conflated missing system coverage with the state of clinical care. The source date also displayed a day early because a date-only UTC value was formatted in US local time.

## Implemented Correction

Policy `us-evidence-2026-10-27.v3` resolves diabetes subtype aliases, rejects ambiguous live `diabetes` input with a clarification, and retains raw/canonical condition plus population in the run and query attempts. Trial parsing exposes eligibility, positive inclusion criteria, conditions, ages, sex, countries, interventions and organization class. Pregnancy exclusions, including parenthesized exclusion headings, and cord tissue do not become pregnancy inclusion labels.

The type 2 diabetes PubMed query now requires primary title focus using fixed aliases, publication classes and publication-date ordering. Background-only abstract mentions cannot establish focus. Trial discovery requests active interventional treatment studies ordered by last update. Source screening independently rechecks subtype, positive eligibility, status, currency, study type and purpose; explicit-ID processing cannot bypass these gates.

Emerging activity requires a treatment trial with an active registry status and an update within a versioned three-year research-screening window. This is an engineering cutoff, not a medical evidence-validity threshold. Historical/unverified records remain in the citation register with no permitted current section. Population-specific evidence receives only the separate section. Claim validation enforces section eligibility outside the model. Organization claims require a documented role passage and inherit their study's eligibility; industry and institutional roles are labeled separately.

The UI/export show specific-population evidence separately, explain the guideline coverage gap, mark legacy policies, display eligibility metadata, and preserve date-only precision without timezone shifts. Existing historical reports/snapshots are not rewritten.

## Verification

- Read-only replay command: `python -m scripts.trace_citation --run-id d9e18095-7c51-4688-9e2f-96d682c52f98 --nct-id NCT01954147`, from the backend repository. Output is ignored `data/trace-nct01954147.json`. No model/source calls and no historical-report mutation. Target statements: 2 before, 0 after. Original pregnancy/pediatric/cognitive statements fail the general-section gate. The replay preserves original model wording and is not a new semantic review.
- Final running-Docker/API run: `71402689-3f21-48b2-977a-56e7cce27885`, same condition, US, eight-record budget, live/model enabled. Eight citations; six accepted structured statements for three population-specific trials and their industry sponsors; six model candidates withheld by claim/section checks. All accepted statements are in the separate population section. No NCT01954147 citation or claim is rediscovered. Main general/emerging/company coverage remains unavailable in this bounded sample; no missing conclusion is fabricated.
- The final three trial records are NCT07271186 (diabetic kidney disease / Regeneron), NCT07896109 (obesity-related eligibility / Novo Nordisk) and NCT07639684 (obesity with type 2 diabetes / Boston Scientific). These are recorded sponsor roles, not a ranking of market leaders or proof of ownership/efficacy. NCT07472907 is excluded for condition mismatch.
- Thirty-six backend tests pass with real PostgreSQL. Ruff checks, production frontend/Docker build, standard UI smoke and scope-specific browser assertions pass. Scope checks cover literature and trial pregnancy/pediatric separation, obesity, exclusions, wrong subtype, aliases/clarification, stale/unknown/observational trials, role propagation, date-only display, exports and legacy notices. No browser runtime errors observed. The existing dependency deprecation warning is unrelated.
- No guideline/FDA connector, clinical domain validation or production deployment is added. The subtype/focus parser and population labels are bounded rules; false exclusions and unrecognized cohorts remain possible. Small result caps are disclosed and can leave general coverage empty.
