---
tags:
  - "concept"
topics:
  - "healthcare-system"
status: growing
created: 2026-10-27
updated: 2026-10-27
sources:
  - Raw/Sources/2026-10-27-evidence-scope-trace.md
source_count: 1
aliases: []
---

# Diabetes Briefing — Evidence Trace And Correction

The mismatch came from missing population and trial-activity gates, followed by section routing. It was not a fabricated citation. The linked stem-cell trial is **not pregnancy-specific**: it studies type 2 diabetes in adults aged 35–65 and excludes pregnancy. The actual pregnancy-specific literature was [PMID 39084811](https://pubmed.ncbi.nlm.nih.gov/39084811/); pediatric evidence also reached the general care section.

## Where The Pipeline Failed

| Stage | Original behavior | Correction |
|---|---|---|
| Request/search | Condition-only scope; broad title/abstract discovery | Resolve subtype and population; title-focused type 2 diabetes literature and explicit trial-purpose/status filters |
| Extraction | Full trial JSON stored, but eligibility and population absent from screening fields | Retain conditions, positive inclusion, exclusions, ages, sex, countries and interventions with inspectable locators |
| Admission/ranking | 3/3 shared words admitted the target despite `UNKNOWN` status and a 2014 update | Condition/subtype and population gate before ranking; active treatment studies within a stated three-year update window |
| Structured synthesis | Every admitted trial and sponsor copied into emerging/organizations | Study eligibility controls both sections; historical records stay in the register; specific cohorts receive a separate section |
| Model/synthesis | Population-specific findings placed under general care | Server checks each claim's section against source eligibility, including after model extraction |
| Standard care | Hard-coded unavailable coverage headed “not established” | State that guideline retrieval is missing; do not imply the condition has no established care |
| Display | Date-only UTC parsing shifted February 20 to February 19 | Preserve date precision in US local display; mark saved reports using older policies |

The original run is `d9e18095-7c51-4688-9e2f-96d682c52f98`. Target NCT01954147 ranked fifth. Its two statements came from deterministic field copying; the original model selected only the four PubMed sources. The clinical registry's missing posted results do not establish that no related publication exists.

## Replay And Same-Condition Rerun

The read-only replay of the original saved source versions removes both target statements (**2 → 0**) and prevents the original pregnancy/pediatric findings from entering the general section. Run it from `backend/`:

```powershell
python -m scripts.trace_citation --run-id d9e18095-7c51-4688-9e2f-96d682c52f98 --nct-id NCT01954147
```

The replay writes ignored `backend/data/trace-nct01954147.json`; it makes no network/model calls, preserves original retrieval timestamps and does not change historical reports.

The final live run under policy v3 uses the same **Type 2 diabetes / US / eight records / model enabled** request: [open corrected briefing](http://localhost:5173/?run=71402689-3f21-48b2-977a-56e7cce27885). It retrieves eight citations and accepts six statements for three population-specific trials and their sponsors. All six stay in separate population evidence. Six model candidates are withheld. NCT01954147 is absent; a retrieved cochlear study is excluded. The main general-care/emerging/company sections stay unavailable in this bounded sample, with pointers to the specific-population section.

Thirty-six backend tests, Ruff checks, production frontend/Docker builds, the standard browser smoke and scope-specific UI/export/date regressions pass. Original snapshots remain inspectable.

## Limits And Next Work

The three-year window is a visible engineering rule, not a clinical cutoff. Title-based focus and a bounded population vocabulary can exclude relevant papers or miss other cohorts. Small caps and probabilistic model extraction can leave coverage empty. Expanding retrieval should preserve these gates and be evaluated with reviewed examples.

**Standard-care content still requires a registered, applicable current guideline connector.** FDA coverage and clinical domain review also remain open. Correcting a misleading label cannot supply missing guidance. See [[Wiki/Concepts/healthcare-evidence-runtime|Runtime]], [[Wiki/Concepts/healthcare-evidence-policy|Evidence policy]] and [[Wiki/Projects/healthcare-system|Project hub]].
