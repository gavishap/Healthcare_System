"""Clearly synthetic edge cases. Never substituted for a live failed retrieval."""

from .schemas import SourceDocument


def fixture_documents(condition: str):
    result = []
    for i, verdict in enumerate(["improved", "did not improve"]):
        body = f"SYNTHETIC POLICY TEST: In adults with {condition}, Example intervention {verdict} the example endpoint compared with placebo. This is fabricated evidence for guardrail testing, not medical research."
        snap = {"abstract": [{"text": body}], "synthetic": True}
        result.append(
            SourceDocument(
                source="pubmed",
                canonical_id=str(99000001 + i),
                url=f"https://pubmed.ncbi.nlm.nih.gov/{99000001 + i}/",
                title=f"Synthetic {condition} opposing-finding fixture {i + 1} — not a real publication",
                published_date="2026-01-01",
                retrieved_at="2026-10-27T00:00:00Z",
                publication_types=["Randomized Controlled Trial"],
                has_results=True,
                snapshot=snap,
                passages=[{"locator": "/abstract/0/text", "text": body}],
            )
        )
    return result
