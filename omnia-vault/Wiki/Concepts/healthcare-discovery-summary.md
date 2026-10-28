---
tags:
  - "concept"
topics:
  - "healthcare-system"
status: growing
created: 2026-10-27
updated: 2026-10-27
sources:
  - Raw/Sources/2026-10-27-architecture-analysis.md
  - Raw/Sources/2026-10-27-discovery-transcript.md
  - Raw/Sources/2026-10-27-prototype-challenge.md
  - Raw/Sources/2026-10-27-architecture-research.md
  - Raw/Sources/2026-10-27-sourcing-discovery-transcript.md
  - Raw/Sources/2026-10-27-sourcing-request.md
source_count: 6
aliases: []
---

# Healthcare Discovery Summary

> [!info] Source and decision status
> The interview and PDF establish requirements; the authored design and researched documentation support the proposals. Technical choices remain proposed until adopted.

## What The Sources Establish

The challenge is to turn a medical condition into a structured briefing for a health system strategy team. The three required output areas are current standard of care, emerging treatments in development, and key companies/institutions. Data must be sourced by the builder. A live local slice is sufficient; cloud deployment is optional. The PDF recommends 120 minutes for the prototype, 10 for a single business slide, and 20 for the interview. The conversation describes two hours plus 30 minutes for Q&A/slide; confirm the exact remaining time before implementation.

Gabriel chose healthcare because of related client experience. His earlier real-estate risk/onboarding example demonstrates experience with full-stack automation, document intake, business rules and feedback; those financial workflows are background, not requirements for this product. The interviewer introduces himself as Dinesh, an AI architect at Insight Global, interviewing for Perficient; these identities are transcript statements, not independently verified facts. Role questions are deferred to Alex in the conversation.

## Ideas Raised And How They Evolved

| Direction | Conversation outcome | Design consequence |
|---|---|---|
| Who uses it | Doctor/patient framing was corrected repeatedly to strategy team | Organizational research workflow; no patient intake or treatment selection |
| Input | Condition name, with fuzzy matching proposed by Gabriel | Resolve term/subtype, then confirm before retrieval |
| Retrieval | Public medical evidence required; synthetic-only cannot demonstrate freshness | Live primary-source queries plus transparently labeled replay |
| Current care | Established treatment landscape | Use current applicable guidelines; an approval alone does not establish care standard |
| Emerging treatments | Trials/publications/regulatory changes | Separate development stage, results availability and approval |
| News | Gabriel proposed 30/60-day discovery | News can surface leads; claims need underlying evidence |
| Pruning/scoring | Interviewer liked the idea, demanded concrete rules | Versioned deterministic eligibility and transparent evidence facets |
| Citation chains | Interviewer warned against treating every layer equally | Resolve underlying evidence; deduplicate families and flag loops |
| Reputation/awards | Proposed initially as trust signals, challenged by interviewer | Exclude popularity, awards and years-in-business from evidence authority |
| LLM council | Proposed to adjudicate contradictory sources | Use here for design; runtime models cannot vote source authority into existence |
| Visualizations/ranking | Accepted only with corrected framing | Compare evidence/development stages, not best treatment for a person |
| Companies | Sponsors/backers and institutions requested | Role-specific, dated evidence links; trial sponsor is not necessarily manufacturer |
| Expert feedback | Interviewer endorsed validating policy with experts | Reviewed policy revisions and evaluation cases; no silent model self-training |
| Omnia/Obsidian | Gabriel explained project memory, transcripts, business/code links and long projects | This vault stores project knowledge; application evidence storage is separate |

The original 247-line transcript stopped during vault setup. The later supplied 374-line capture continues the sourcing discussion: the interviewer fixes U.S. scope, asks for a small explicit source policy, permits assuming client validation for the prototype exercise, and proposes PubMed plus clinical-trials records for the required sections. FDA/CDC are discussed with narrower regulatory/public-health roles. The runtime agent should operate within configured sources rather than choose authority or recursively chase citations. The extended transcript still contains no completed application, chosen stack, actual clinically validated policy, measured result or agreed deployment. Meeting recording/transcription use is permitted in the transcript. Do not infer delivery from this.

## Authorization Boundary

The earlier architecture request and council record remain historical. The owner's current request asks for a first sourcing-layer action plan, with whole-system architecture assigned to another agent and LLM credentials to follow. This authorizes the sourcing plan and integration preparation. The PDF's slide/repository-sharing directions remain interview criteria, not current instructions to publish or message anyone. See [[Wiki/Concepts/healthcare-sourcing-plan|First sourcing draft]].

See [[Wiki/Concepts/healthcare-product-scope|Product scope]], [[Wiki/Concepts/healthcare-evidence-policy|Evidence policy]], and [[Wiki/Concepts/healthcare-delivery-roadmap|Delivery roadmap]].
