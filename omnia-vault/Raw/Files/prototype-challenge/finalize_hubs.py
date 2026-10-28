from pathlib import Path

root=Path.cwd()
src=['Raw/Sources/2026-10-27-architecture-request.md','Raw/Sources/2026-10-27-prototype-challenge.md','Raw/Sources/2026-10-27-discovery-transcript.md','Raw/Sources/2026-10-27-architecture-analysis.md','Raw/Sources/2026-10-27-architecture-research.md']
def fm(tag, sources):
    return '---\ntags:\n  - "'+tag+'"\ntopics:\n  - "healthcare-system"\nstatus: growing\ncreated: 2026-10-27\nupdated: 2026-10-27\nsources:\n'+''.join('  - '+s+'\n' for s in sources)+f'source_count: {len(sources)}\naliases: []\n---\n\n'
hub='''# Healthcare System

## Goal

Design a condition intelligence application for a health system strategy team: an auditable briefing covering current care, emerging treatments and involved companies/institutions. Preserve the corrected strategy-team scope, live-source requirements and deterministic evidence policy from the interview.

## Status

The challenge PDF and supplied transcript are captured, along with the owner's planning request, primary-source documentation checks and an original architecture proposal. The application is not built. Credentials, supported condition, applicable guideline and expert-reviewed policy remain unresolved. The current request authorizes architecture strategy and notes; interview deliverables are planned rather than executed.

Recommended full-stack direction: a modular FastAPI/Pydantic backend with thin React/TypeScript UI, bounded LLM/tool workflow, source snapshots and claim-level provenance. A strict two-hour demo may use a Streamlit shell around reusable typed Python modules when no working frontend scaffold exists. The stack remains proposed; read the council's disagreement before locking it.

## Start Here

- [[Wiki/Concepts/healthcare-discovery-summary|Conversation summary and corrections]]
- [[Wiki/Concepts/healthcare-application-architecture|Full application architecture and diagram]]
- [[Wiki/Concepts/healthcare-council-verdict|Council verdict and dissent]]
- [[Wiki/Concepts/healthcare-architecture-decisions|Proposed architecture decisions]]
- [[Wiki/Concepts/healthcare-delivery-roadmap|Prototype plan and growth path]]
- [[Wiki/Concepts/healthcare-open-questions|Open decisions and assumptions]]

## Work Directions

| Direction | Note |
|---|---|
| User/problem and acceptance | [[Wiki/Concepts/healthcare-product-scope]] |
| Condition resolution and source coverage | [[Wiki/Concepts/healthcare-condition-and-source-strategy]] |
| Deterministic evidence policy | [[Wiki/Concepts/healthcare-evidence-policy]] |
| LLMs and server tool calling | [[Wiki/Concepts/healthcare-llm-and-tools]] |
| Data, citations and source versions | [[Wiki/Concepts/healthcare-data-and-provenance]] |
| API and research state machine | [[Wiki/Concepts/healthcare-api-and-job-flow]] |
| Evidence tables and analyst interface | [[Wiki/Concepts/healthcare-briefing-interface]] |
| Security and policy governance | [[Wiki/Concepts/healthcare-security-and-governance]] |
| Evaluation and failure cases | [[Wiki/Concepts/healthcare-evaluation-plan]] |
| Deployment and operations | [[Wiki/Concepts/healthcare-deployment-and-operations]] |

## Next Steps

- [ ] Select one condition, subtype, jurisdiction and accessible current guideline.
- [ ] Validate the evidence policy with a domain reviewer.
- [ ] Test provided gateway auth, a real tool-call round trip and typed output when credentials are available.
- [ ] Choose the initial interface against actual remaining build time, then implement one cited live slice.

## Related

- [[Wiki/Topics/healthcare-system|Knowledge hub]]
- [[Wiki/Concepts/source-ingestion-workflow|Vault ingestion workflow]]
'''
(root/'Wiki/Projects/healthcare-system.md').write_text(fm('project',src)+hub,encoding='utf-8')
topic='''# Healthcare System

Knowledge hub for the health system strategy briefing application. The supplied interview establishes the user and evidence boundaries; the linked design notes propose implementation rather than claiming an application exists.

## Project And Decisions

- [[Wiki/Projects/healthcare-system|Project overview and work-direction map]]
- [[Wiki/Concepts/healthcare-discovery-summary|Interview summary]]
- [[Wiki/Concepts/healthcare-application-architecture|Architecture]]
- [[Wiki/Concepts/healthcare-council-verdict|Council verdict]]
- [[Wiki/Concepts/healthcare-architecture-decisions|Architecture decisions]]

## Evidence And Execution

- [[Wiki/Concepts/healthcare-condition-and-source-strategy|Sources and condition scope]]
- [[Wiki/Concepts/healthcare-evidence-policy|Evidence policy]]
- [[Wiki/Concepts/healthcare-llm-and-tools|LLM and tool responsibilities]]
- [[Wiki/Concepts/healthcare-data-and-provenance|Provenance]]
- [[Wiki/Concepts/healthcare-evaluation-plan|Evaluation]]
- [[Wiki/Concepts/healthcare-delivery-roadmap|Delivery plan]]
- [[Wiki/Concepts/healthcare-open-questions|Open questions]]

## Vault Workflow

- [[Wiki/Concepts/source-ingestion-workflow|Source ingestion workflow]]
- [[Wiki/Concepts/raw-vs-compiled-knowledge|Raw versus compiled knowledge]]
'''
(root/'Wiki/Topics/healthcare-system.md').write_text(fm('topic',src)+topic,encoding='utf-8')
# Attach the concrete probe evidence only to the note that cites its results.
p=root/'Wiki/Concepts/healthcare-condition-and-source-strategy.md'
t=p.read_text(encoding='utf-8').replace('source_count: 4','  - Raw/Sources/2026-10-27-connector-smoke-check.md\nsource_count: 5')
p.write_text(t,encoding='utf-8')
print('Updated project and topic hubs; linked concrete endpoint check.')
