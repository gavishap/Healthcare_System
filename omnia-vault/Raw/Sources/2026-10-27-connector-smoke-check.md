---
Title: "Public biomedical endpoint smoke checks"
Reference: "Local public_probe.py output captured in Raw/Files/prototype-challenge/probe-results.json"
ContentType:
  - "markdown"
Created: 2026-10-27
Processed: true
tags:
  - "source"
---

# Public Endpoint Smoke Checks

Two read-only public requests made on 2026-10-27 returned JSON successfully:

1. ClinicalTrials.gov API v2 `/api/v2/studies`, condition query `type 2 diabetes`, page size 1. Top-level response keys: `studies`, `nextPageToken`.
2. PubMed ESearch `/entrez/eutils/esearch.fcgi`, database `pubmed`, term `type 2 diabetes`, result cap 1, JSON output. Top-level response keys: `header`, `esearchresult`.

Responses are saved locally as `Raw/Files/prototype-challenge/clinicaltrials-sample.json` and `pubmed-sample.json`. No patient records, authentication or enterprise gateway were involved. The test term is an engineering connectivity example, not the selected supported demo condition. These results establish endpoint reachability and a small response shape only; they do not validate a medical claim, application adapter, literature search, source freshness, or clinical policy.

An initial inline probe command failed locally from shell quoting before any network request. The file-based probe above replaced it and succeeded. No failure was counted as a successful integration.
