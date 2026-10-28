from pathlib import Path
import re

root=Path.cwd()
source='Raw/Sources/2026-10-27-evidence-runtime-handoff.md'
for rel in ['Wiki/Projects/healthcare-system.md','Wiki/Concepts/healthcare-evidence-runtime.md','Wiki/Concepts/healthcare-application-architecture.md','Wiki/Concepts/healthcare-sourcing-contract.md','Wiki/Concepts/healthcare-evidence-policy.md','Wiki/Logs/2026-10-27-evidence-runtime.md']:
    p=root/rel
    t=p.read_text(encoding='utf-8')
    if source not in t:
        t=re.sub(r'source_count: (\d+)',lambda m:'  - '+source+'\nsource_count: '+str(int(m.group(1))+1),t,count=1)
    if rel.endswith('healthcare-evidence-runtime.md'):
        marker='''
> [!info] Baseline and concurrent correction
> Backend `5e62673` and frontend `862f36f` save the implemented application. The baseline test command passes 31 tests including early shared scope checks; the v2 live result below is historical evidence. The separate active chat **Trace trial result mismatch** is continuing policy-v3 condition/population and trial-currency corrections. Its uncommitted edits are preserved; verify its later handoff before claiming the newest policy is fully deployed or tested. See the handoff source for the boundary.
'''
        t=t.replace('# Healthcare Evidence Runtime\n','# Healthcare Evidence Runtime\n'+marker,1)
    p.write_text(t,encoding='utf-8')

state='''# Relay State — the baton

## Now

- Evidence Desk is implemented in the sibling application repositories, with
  FastAPI/Pydantic, React/TypeScript/Vite, PostgreSQL 17 and Docker Compose.
  Baseline commits: backend `5e62673`, frontend `862f36f`. No remote push.
- Runtime guide: `Wiki/Concepts/healthcare-evidence-runtime.md`; integration
  boundary: `POST /api/evidence/process` takes canonical PMID/NCT identifiers
  and re-fetches fixed APIs before evidence processing. A research-run endpoint
  also performs its own bounded discovery.
- Supplied NCBI/OpenAI keys work and remain only in ignored backend settings.
  `OPENAI_MODEL` was blank; configurable default `gpt-4.1-mini` is tested.
  Postgres uses a named volume on loopback port 55432; UI 5173 and API 8000.
- IMPORTANT: the separate active chat **Trace trial result mismatch** is editing
  the same backend to tighten subtype/population, currency and section eligibility
  under policy v3. Preserve its in-progress edits. Do not race a rebuild or
  overwrite its modules. Its later trace/handoff should supersede this notice.

## Just landed

- Fixed-source API adapters, identity/retraction screening, deterministic citation
  ordering, immutable source snapshots, exact evidence locators, claim links,
  bounded model evidence-tool/extraction/review, potential conflicts, citation
  drawer, policy view and cited Markdown/JSON exports are implemented.
- The policy-v2 live API run `546eeb36-85e5-4293-821c-8ad79bdcb224` retrieves four
  PubMed and four ClinicalTrials.gov records, saves ten accepted/structured claims,
  withholds three candidates, and executes one evidence tool across three model
  calls. It is partial: no checked applicable US guideline is connected.
- Original 20 core backend tests pass; the baseline checkpoint additionally
  observes 31 passing tests with early shared scope regressions. Frontend/Docker
  builds and isolated browser checks pass. Later v3 edits require the trace
  workstream's final verification rather than reusing v2 results as proof.
- Actual key-value and tracked-environment scans pass. API keys never enter the
  browser. The optional application bearer token is distinct from upstream keys.
- New source/request/implementation/handoff captures and a runtime note/log
  update the project hub, architecture, policy and sourcing integration notes.

## Next

- [ ] Let **Trace trial result mismatch** finish the ongoing v3 correction,
  regression/trace, UI/report integration and local deployment; review its handoff.
- [ ] Register an accessible current US guideline and validate claim applicability;
  add an FDA adapter for applicable approval claims if needed.
- [ ] Obtain real domain-policy review beyond the interview's prototype assumption.
- [ ] Define pilot identity/tenants, durable jobs, versioned migrations, backups,
  retention and broader condition coverage before operational use.

## Open questions

- Current guideline coverage/domain reviewer; expanded conditions/populations;
  pilot access/retention/budgets and external repository sharing destination.
- The original council's Claude perspectives remain pending by the owner's
  choice to finish that planning run without them. Do not restart automatically.

## Watch out

- Do not call PubMed indexing a standard-of-care endorsement, registry listing
  proven benefit, automated semantic checking clinical validation, or no detected
  conflict consensus. Current-care/approval claims are deliberately withheld.
- Model limitation prose without evidence references is withheld in policy v2;
  historical reports keep their original policy/version and source snapshots.
- Exact condition/population and emerging-activity fixes are concurrently changing
  in another chat. Baseline captures do not certify unfinished v3 changes.
- Jobs are single-process local tasks; restart marks unfinished work interrupted.
  The application is not a production identity/tenant or distributed worker system.
- Keep code and actual runtime evidence in application repos/Postgres; keep source
  knowledge in this vault. Do not commit keys, `.env`, local data or screenshots.
- Vault origin remains the Omnia template. Commit locally only; do not push there.
'''
(root/'_relay/STATE.md').write_text(state,encoding='utf-8')
print('Recorded baseline verification and preserved the separate active scope correction.')
