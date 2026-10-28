> Last handoff: 2026-10-28T00:42Z · by codex · at 14ff004 (main)

# Relay State - the baton

## Now

- Evidence Desk runs locally with FastAPI/Pydantic, React/TypeScript/Vite,
  PostgreSQL 17 and Docker Compose. UI: loopback 5173; API: 8000;
  PostgreSQL named-volume storage: 55432.
- Policy `us-evidence-2026-10-27.v3` is deployed and verified. Backend commit
  `286103f`; frontend commit `88cb877`. No external application deployment.
- The client presentation is consolidated to three landscape slides with an
  editable workflow/decision diagram, an actual screen and source-backed notes.
  Entry point: `Wiki/Concepts/healthcare-client-presentation.md`. Native Page:
  `page_6776fb97e91c8191aa54596235d43dfc`; reconnect that Page to edit it.
- The deck is now named Evidence Desk_deck. A validated three-slide independent
  PowerPoint export is prepared as `Presentation/Evidence_Desk_deck.pptx`.
- The private GitHub repository `https://github.com/gavishap/Healthcare_System`
  is created. The prepared consolidated checkout has backend, frontend, vault,
  source attachments, deck/previews and thirteen sanitized sessions in AI History.
  Its first push is pending; original local repositories remain independent.
- The original-result trace and runtime limits remain in
  `Wiki/Concepts/healthcare-evidence-scope-trace.md` and
  `Wiki/Concepts/healthcare-evidence-runtime.md`. General evidence, specific
  populations and historical/unverified trials have distinct eligibility.
  A study's eligibility controls its sponsors as well.
- Current standard-care content remains unavailable because no registered,
  applicable guideline connector exists. FDA evidence and domain review also
  remain open. The presentation states these limits and proposes a reviewed pilot.

## Just landed

- Consolidated the existing 22-slide deck into exactly three pages at the
  owner's request. They cover client value/output, the evidence workflow and
  decision path, and the working prototype with reviewed-pilot dependencies.
  Supporting provenance, correction and evaluation context stay in notes.
- All three slides are rendered and visually reviewed; a wrapped branch label
  is shortened. The same native Page, teal style and 1280-by-720 format remain.
  There is no additional cover or appendix. The earlier 22-slide delivery record
  is historical. This is native artifact review, not PowerPoint application testing.
- Saved delivery context and a linked project entry in the Wiki. A separate
  PowerPoint export now passes package/layout/font/import checks. Native
  PowerPoint is not tested; no PDF or stakeholder message is sent.
- Application state is unchanged by the presentation task. Latest live run
  `71402689-3f21-48b2-977a-56e7cce27885` retrieves eight citations and accepts
  six statements, all for specific populations. Six model candidates are
  withheld; general sections stay unavailable in that sample.
- Existing verification records report 36 backend tests, Ruff, frontend/Docker
  builds and browser checks passing. Application tests are not rerun for this
  presentation. Original saved-evidence replay removes both NCT01954147
  statements without network/model calls or historical-report mutation.

## Next

- [ ] Push and verify the consolidated private repository; record publication
  completion and the active-chat archive cutoff.
- [ ] Register an accessible, applicable current US guideline and validate its
  recommendations before claiming standard-care coverage. Add FDA evidence for
  approval statements when needed.
- [ ] Review population/focus rules with a domain reviewer; evaluate false
  exclusions, unknown cohorts and better coverage within explicit budgets.
- [ ] Improve literature extraction/retrieval without bypassing section gates.
  The final bounded run accepts no general literature statement.
- [ ] Define pilot identity/tenants, durable jobs, migrations, backups, retention
  and evaluated condition scope before operational use.

## Open questions

- Guideline access and permitted use, domain reviewer, supported conditions and
  population vocabulary, acceptable trial-update window, operating budget,
  pilot sharing. Repository destination is now the owner's private GitHub
  Healthcare_System repository. No pilot dates or ROI are agreed.
- The original council's Claude perspectives remain pending by the owner's
  choice to finish that planning run without them. Do not restart automatically.

## Watch out

- Presentation artifact reference:
  `artifact_external_e6729f95-ef72-4c9b-8716-6566d25b5f25`. Reconnect the saved
  Page if the reference expires; preserve the deck rather than duplicating it.
  Source references live in notes; the displayed example is partial.
- The three-year trial-update window is an engineering filter, not a clinical
  evidence-validity cutoff. Scope parsing and cohort detection are bounded;
  small caps and probabilistic extraction can leave general sections empty.
- Registration is not benefit or approval. A sponsor role does not establish
  product ownership or market leadership. Missing posted results do not imply
  no related publication. Automated checks are not domain validation; no
  detected conflict does not establish consensus.
- Historical reports retain original source/policy versions. Replay applies
  current gates to old model text; it is not a fresh semantic review.
- No guideline/FDA connector or production deployment is delivered. Jobs remain
  single-process and restart interrupts unfinished work. Credentials and runtime
  evidence databases stay outside commits and client bundles. The owner explicitly
  authorizes sanitized AI History in the private publication; raw sessions stay local.
- Preserve unrelated existing edits to council verdict, raw-vs-compiled note
  and relay protocol. Vault origin is the Omnia template: commit locally, never
  push project material there.
