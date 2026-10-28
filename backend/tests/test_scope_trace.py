"""Replay the reported public record and adversarial scope variants, without network calls."""

import copy
import json
from datetime import date
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.sources import parse_trial, parse_pubmed, Sources
from app.scope import resolve_scope, ScopeAmbiguity, condition_matches
from app.policy import rank_documents, validate_claim
from app.workflow import structured_claims
from app.llm import evidence_packet

AS_OF = date(2026, 10, 27)
STUDY = json.loads((Path(__file__).parent / "fixtures/nct01954147.json").read_text(encoding="utf-8"))


def citation(study, condition="Type 2 diabetes", population="general"):
    doc = parse_trial(study, "2026-10-27T23:36:40Z")
    return rank_documents([doc], condition, "trace-test", population, as_of=AS_OF)[0]


def active_study():
    study = copy.deepcopy(STUDY)
    status = study["protocolSection"]["statusModule"]
    status["overallStatus"] = "RECRUITING"
    status["lastUpdatePostDateStruct"]["date"] = "2026-10-20"
    return study


def test_reported_record_is_not_a_pregnancy_study_and_cannot_be_current_emerging_activity():
    c = citation(STUDY)
    assert c["canonical_id"] == "NCT01954147"
    assert c["population"]["minimum_age"] == "35 Years"
    assert c["population"]["maximum_age"] == "65 Years"
    assert c["population"]["countries"] == ["China"]
    assert "pregnancy" not in c["population_tags"]  # Cord tissue and pregnancy exclusions are not inclusion.
    assert c["display_bucket"] == "historical_or_unverified"
    assert "TRIAL_NOT_CURRENT_ACTIVE" in c["reason_codes"]
    assert "TRIAL_UPDATE_OUTSIDE_CURRENCY_WINDOW" in c["reason_codes"]
    assert c["allowed_claim_types"] == [] and c["eligible_sections"] == []
    assert structured_claims([c]) == []  # Includes sponsor: no separate path into key organizations.
    assert evidence_packet([c]) == []  # The model cannot bring it back into the summary.
    assert any(e["locator"].endswith("eligibilityCriteria") for e in c["evidence"])


@pytest.mark.parametrize(
    "name,extra",
    [
        ("pregnancy", "pregnant adults"),
        ("obesity", "adults with obesity"),
        ("pediatric", "children and adolescents"),
    ],
)
def test_specific_populations_are_separate_from_the_general_condition(name, extra):
    study = active_study()
    study["protocolSection"]["identificationModule"]["briefTitle"] = "Type 2 diabetes in " + extra
    c = citation(study)
    assert name in c["population_tags"]
    assert c["eligible_sections"] == ["specific_populations"]
    claims = structured_claims([c])
    assert claims and all(x["section"] == "specific_populations" for x in claims)
    assert all(validate_claim(x, [c])[0] for x in claims)
    tampered = copy.deepcopy(claims[0])
    tampered["section"] = "emerging"
    assert "SECTION_SCOPE_NOT_PERMITTED" in validate_claim(tampered, [c])[1]


def test_requested_population_must_be_established_and_is_not_inferred_from_exclusions():
    assert citation(active_study(), population="pregnancy")["decision"] == "excluded"
    study = active_study()
    study["protocolSection"]["identificationModule"]["briefTitle"] = "Type 2 diabetes in pregnant adults"
    c = citation(study, population="pregnancy")
    assert c["display_bucket"] == "general"  # General within the explicitly requested population.
    assert "emerging" in c["eligible_sections"]


def test_parenthesized_exclusion_heading_does_not_turn_excluded_pregnancy_into_population():
    study = active_study()
    study["protocolSection"]["eligibilityModule"]["eligibilityCriteria"] = (
        "Adults with Type 2 diabetes.\nExclusion Criteria (all participants):\nPregnancy or breastfeeding."
    )
    assert "pregnancy" not in citation(study)["population_tags"]


def test_background_condition_mention_does_not_admit_an_unfocused_paper():
    scope = resolve_scope("Type 2 diabetes")
    assert not condition_matches(scope, "GLP-1 therapy in cancer", [], "Type 2 diabetes is common worldwide.")
    assert condition_matches(scope, "Type 2 diabetes in pregnancy and gestational diabetes", [], "")


@pytest.mark.parametrize(
    "title",
    [
        "Diagnosis and Treatment of Hyperglycemia in Pregnancy: Type 2 Diabetes Mellitus and Gestational Diabetes.",
        "Type 2 diabetes mellitus in children and adolescents: a relatively new clinical problem within pediatric practice.",
    ],
)
def test_original_literature_population_mismatches_are_separated_before_model_extraction(title):
    xml = f"""<PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>12345</PMID><Article>
    <ArticleTitle>{title}</ArticleTitle><Abstract><AbstractText>Type 2 diabetes research in this specific population.</AbstractText></Abstract>
    </Article></MedlineCitation></PubmedArticle></PubmedArticleSet>"""
    doc = parse_pubmed(xml, "2026-10-27T00:00:00Z")[0]
    c = rank_documents([doc], "Type 2 diabetes", "literature-population-test")[0]
    assert c["decision"] != "excluded"
    assert c["display_bucket"] == "specific_population"
    assert c["eligible_sections"] == ["specific_populations"]
    assert evidence_packet([c])[0]["eligible_sections"] == ["specific_populations"]


def test_diabetic_complication_requires_subtype_in_positive_eligibility():
    scope = resolve_scope("Type 2 diabetes")
    assert condition_matches(
        scope, "Kidney trial", ["Diabetic kidney disease"], "Diagnosis of Type 2 diabetes"
    )
    assert not condition_matches(scope, "Kidney trial", ["Type 1 diabetes"], "Type 2 diabetes in background")


@pytest.mark.parametrize("other", ["Type 1 diabetes", "Gestational diabetes"])
def test_other_diabetes_types_do_not_pass_on_shared_words_or_summary_mentions(other):
    study = active_study()
    study["protocolSection"]["conditionsModule"]["conditions"] = [other]
    c = citation(study)
    assert c["decision"] == "excluded"
    assert "CONDITION_MISMATCH" in c["reason_codes"]


def test_current_general_trial_and_institutional_role_are_preserved():
    c = citation(active_study())
    claims = structured_claims([c])
    assert {x["section"] for x in claims} == {"emerging", "organizations"}
    assert all(validate_claim(x, [c])[0] for x in claims)
    assert "company status not established" in claims[1]["text"]
    assert all(x["population"] != "unknown" for x in claims)
    assert c["population"]["sex"] == "ALL"
    study = active_study()
    del study["protocolSection"]["eligibilityModule"]["maximumAge"]
    assert "minimum age 35 Years" in structured_claims([citation(study)])[0]["text"]


def test_observational_study_cannot_be_an_emerging_treatment_even_if_recent_and_active():
    study = active_study()
    study["protocolSection"]["designModule"]["studyType"] = "OBSERVATIONAL"
    c = citation(study)
    assert c["eligible_sections"] == []
    assert structured_claims([c]) == []


def test_aliases_normalize_without_silently_picking_a_diabetes_subtype():
    for condition in ["T2DM", "type II diabetes", "diabetes mellitus type 2"]:
        assert resolve_scope(condition)["condition"] == "Type 2 diabetes"
        assert citation(active_study(), condition)["decision"] != "excluded"
    with pytest.raises(ScopeAmbiguity):
        resolve_scope("diabetes")
    response = TestClient(app).post(
        "/api/research-runs", json={"condition": "diabetes", "scope_confirmed": True}
    )
    assert response.status_code == 422 and "Specify type" in response.json()["detail"]


async def test_discovery_uses_normalized_condition_and_separate_population(monkeypatch):
    calls = []

    async def fake(self, condition, count, ids=None, populations=None):
        calls.append((condition, populations))
        return [], {"source": "test", "status": "no_matches"}

    monkeypatch.setattr(Sources, "pubmed", fake)
    monkeypatch.setattr(Sources, "trials", fake)
    sources = Sources()
    try:
        _, attempts = await sources.collect("T2DM", 8, population="pregnancy")
        assert calls == [("Type 2 diabetes", ["pregnancy"])] * 2
        assert all(a["scope"]["population"] == ["pregnancy"] for a in attempts)
    finally:
        await sources.close()
