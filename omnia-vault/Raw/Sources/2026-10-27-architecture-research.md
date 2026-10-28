---
Title: "Primary-source checks for healthcare briefing architecture"
Reference: "Official documentation URLs listed in this capture"
ContentType:
  - "markdown"
Created: 2026-10-27
Processed: true
tags:
  - "source"
---

# Primary-Source Architecture Checks

Captured 2026-10-27 for architecture planning. These are documentation checks and design implications, not a clinical evidence review. Summaries below are original paraphrases; URLs identify the underlying primary sources. The enterprise gateway and end-to-end application have not been exercised.

## Biomedical Retrieval

- [NCBI developer APIs](https://www.ncbi.nlm.nih.gov/home/develop/api/) identifies E-utilities as an interface to Entrez databases including PubMed. Design implication: retrieve article identifiers and metadata through a fixed server adapter; indexing is not a quality endorsement or a guarantee of full-text access.
- [NCBI usage policy](https://support.nlm.nih.gov/kbArticle/?pn=KA-05510) gives the default 3 requests/second limit and up to 10 with an API key. Design implication: batch requests, share a limiter across workers, and handle throttling.
- [NLM API v2 announcement](https://www.nlm.nih.gov/pubs/techbull/ma24/ma24_clinicaltrials_api.html) documents a REST/OpenAPI interface to study records. [ClinicalTrials.gov](https://clinicaltrials.gov/) states that sponsors/investigators supply study information and that listing is not government approval of every study's science/safety. Design implication: trial registration, trial results, and demonstrated benefit are separate claim types.
- [NLM MeSH data](https://www.nlm.nih.gov/databases/download/mesh.html) describes controlled biomedical terminology and available data access. Design implication: propose MeSH-linked condition candidates; preserve the user's wording and require confirmation when subtype or term is ambiguous.

## Regulatory and Guideline Evidence

- [About Drugs@FDA](https://www.fda.gov/drugs/drug-approvals-and-databases/about-drugsfda) describes approval records, labels and review history for covered products. [FDA label repository](https://labels.fda.gov/) warns that submitted listing information is not necessarily the approved label. Design implication: approval claims require an applicable approval record and indication; do not infer approval from a generic label hit or a manufacturer name. Product coverage is not universal.
- [NICE evidence-review methods](https://www.nice.org.uk/process/pmg20/chapter/reviewing-evidence) describe matching evidence to a review question and documenting interpretation. Design implication: guidelines need population/jurisdiction/date context and expert interpretation. NICE is UK guidance; it must not silently establish US standard of care. The generic NICE guidance listing returned HTTP 403 in this research, so arbitrary live guideline access remains unproven.

## API and Model Infrastructure

- [FastAPI response models](https://fastapi.tiangolo.com/tutorial/response-model/) validate/filter response structure. [Background-task caveat](https://fastapi.tiangolo.com/tutorial/background-tasks/) distinguishes lightweight local tasks from work requiring separate queue/worker infrastructure. Design implication: typed output helps contracts; it does not verify medical facts. Persist job states and mark interrupted local prototype jobs honestly; introduce durable workers for pilot use.
- [Portkey library integrations](https://portkey.ai/docs/integrations/libraries) and [Bedrock structured outputs](https://portkey.ai/docs/integrations/llms/bedrock/structured-outputs) describe model access and schema-oriented generation. Design implication: isolate the gateway behind an adapter and test authentication, the supplied route/model, function-tool round trips, and supported structured-output behavior before depending on them. Current public docs do not prove the interview's enterprise gateway has identical features or configuration.

## Limits

No condition-specific guideline has been selected or validated. No therapeutic comparison, clinical recommendation, comprehensive search, calibrated evidence score, production security claim, or application latency/cost measurement is established here. The later architecture's thresholds and timings are provisional engineering proposals, not facts derived from these docs.
