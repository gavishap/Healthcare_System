from app.fixtures import fixture_documents
from app.policy import rank_documents, validate_claim, find_conflicts, identity_ok
from app.schemas import ResearchRequest
from app.workflow import fixture_claims
from pydantic import ValidationError
import pytest


def bundle():
    return rank_documents(fixture_documents("type 2 diabetes"), "type 2 diabetes", "test-run")


def test_retracted_citation_cannot_support_any_claim():
    docs = fixture_documents("type 2 diabetes")
    docs[0].retracted = True
    ranked = rank_documents(docs, "type 2 diabetes", "test")
    rejected = next(c for c in ranked if c["canonical_id"] == docs[0].canonical_id)
    assert rejected["decision"] == "excluded"
    assert rejected["allowed_claim_types"] == []
    assert "RETRACTED_PUBLICATION" in rejected["reason_codes"]


def test_quote_and_id_must_resolve_to_exact_saved_passage():
    citations = bundle()
    claim = fixture_claims(citations)[0]
    assert validate_claim(claim, citations)[0]
    claim["references"][0]["quote"] = "Fabricated quotation not in the snapshot"
    assert "QUOTE_NOT_IN_SNAPSHOT" in validate_claim(claim, citations)[1]
    claim["references"][0]["evidence_id"] = "invented"
    assert "UNKNOWN_EVIDENCE_ID" in validate_claim(claim, citations)[1]


def test_metadata_is_not_approval_or_current_care():
    citations = bundle()
    for kind in ["approval", "current_care"]:
        claim = fixture_claims(citations)[0]
        claim["claim_type"] = kind
        assert not validate_claim(claim, citations)[0]


def test_cannot_relabel_approval_claim_as_a_published_finding():
    citations = bundle()
    claim = fixture_claims(citations)[0]
    claim["text"] = "Example intervention is FDA-approved and standard of care."
    assert "UNVERIFIED_REGULATORY_OR_CARE_LANGUAGE" in validate_claim(claim, citations)[1]


def test_source_domain_lookalike_userinfo_and_bad_port_are_rejected():
    doc = fixture_documents("diabetes")[0]
    for url in [
        "https://pubmed.ncbi.nlm.nih.gov.evil.test/99000001/",
        "https://pubmed.ncbi.nlm.nih.gov@evil.test/99000001/",
        "https://pubmed.ncbi.nlm.nih.gov:bad/99000001/",
        "http://pubmed.ncbi.nlm.nih.gov/99000001/",
        "https://pubmed.ncbi.nlm.nih.gov/1111/",
    ]:
        doc.url = url
        assert not identity_ok(doc)


def test_locators_must_match_content_before_evidence_is_admitted():
    docs = fixture_documents("diabetes")
    docs[0].passages[0]["text"] = "Changed text not in saved record"
    matching = next(
        c for c in rank_documents(docs, "diabetes", "test") if c["canonical_id"] == docs[0].canonical_id
    )
    assert matching["evidence"] == []
    assert matching["allowed_claim_types"] == []


def test_same_nct_reports_share_a_family_but_not_an_extra_independent_vote():
    docs = fixture_documents("diabetes")
    for d in docs:
        d.nct_ids = ["NCT01234567"]
    ranked = rank_documents(docs + docs, "diabetes", "test")
    assert len(ranked) == 2
    assert len({c["family_id"] for c in ranked}) == 1
    assert ranked[1]["duplicate_of"] == ranked[0]["id"]


def test_opposite_findings_preserve_both_claims_without_picking_a_winner():
    citations = bundle()
    claims = fixture_claims(citations)
    for i, c in enumerate(claims):
        c["id"] = f"claim-{i}"
        c["references"] = validate_claim(c, citations)[2]
    conflicts = find_conflicts(claims, citations)
    assert len(conflicts) == 1
    assert conflicts[0]["claim_ids"] == ["claim-0", "claim-1"]
    assert conflicts[0]["status"] == "unresolved"
    claims[1]["population"] = "children"
    assert find_conflicts(claims, citations) == []


def test_patient_or_search_expression_input_is_not_accepted():
    for term in ["diabetes; DROP TABLE citations", "DOB 1990 patient name Jane", "diabetes[Title] OR asthma"]:
        with pytest.raises(ValidationError):
            ResearchRequest(condition=term, scope_confirmed=True)
    with pytest.raises(ValidationError):
        ResearchRequest(condition="diabetes", scope_confirmed=False)
