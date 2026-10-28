from app.reporting import safe_markdown, source_link
from app.llm import evidence_packet
from app.fixtures import fixture_documents
from app.policy import rank_documents


def test_export_does_not_turn_external_text_into_html_images_or_links():
    escaped = safe_markdown("<script>alert(1)</script> ![image](https://outside.example)")
    assert "<script>" not in escaped
    assert "!\\[image\\]" in escaped
    assert (
        source_link({"url": "https://pubmed.ncbi.nlm.nih.gov/99000001/"}, "fabricated", synthetic=True)
        == "fabricated (synthetic fixture; no original publication)"
    )


def test_model_input_is_bounded_even_when_source_passages_are_long():
    documents = fixture_documents("diabetes")
    for d in documents:
        d.snapshot["abstract"][0]["text"] = "diabetes " * 10000
        d.passages[0]["text"] = d.snapshot["abstract"][0]["text"]
    docs = rank_documents(documents, "diabetes", "cap-test")
    packet = evidence_packet(docs)
    assert sum(len(e["text"]) for c in packet for e in c["evidence"]) <= 32000
    assert all(len(e["text"]) <= 2500 for c in packet for e in c["evidence"])
