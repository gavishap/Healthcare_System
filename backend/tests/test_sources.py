from app.sources import parse_pubmed, parse_trial
from app.policy import rank_documents

XML = """<PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>12345</PMID><Article><ArticleTitle>Type 2 diabetes trial</ArticleTitle><Journal><Title>Example Journal</Title><JournalIssue><PubDate><Year>2024</Year></PubDate></JournalIssue></Journal><Abstract><AbstractText Label="RESULTS">Type 2 diabetes endpoint improved in the measured population. NCT01234567.</AbstractText></Abstract><PublicationTypeList><PublicationType>Randomized Controlled Trial</PublicationType><PublicationType>Retracted Publication</PublicationType></PublicationTypeList></Article></MedlineCitation><PubmedData><ArticleIdList><ArticleId IdType="doi">10.example/test</ArticleId></ArticleIdList></PubmedData></PubmedArticle></PubmedArticleSet>"""


def test_pubmed_parser_preserves_results_retraction_and_study_identity():
    doc = parse_pubmed(XML, "2026-10-27T00:00:00Z")[0]
    assert doc.canonical_id == "12345"
    assert doc.has_results and doc.retracted
    assert doc.published_date == "2024"
    assert doc.nct_ids == ["NCT01234567"]
    assert doc.doi == "10.example/test"
    assert doc.passages[0]["locator"] == "/abstract/0/text"


def test_registry_without_results_cannot_support_efficacy_or_approval():
    doc = parse_trial(
        {
            "protocolSection": {
                "identificationModule": {"nctId": "NCT01234567", "briefTitle": "Type 2 diabetes study"},
                "descriptionModule": {
                    "briefSummary": "Registered type 2 diabetes study. No results available."
                },
                "statusModule": {
                    "overallStatus": "RECRUITING",
                    "lastUpdatePostDateStruct": {"date": "2026-10-20"},
                },
                "conditionsModule": {"conditions": ["Type 2 diabetes"]},
                "eligibilityModule": {
                    "eligibilityCriteria": "Inclusion Criteria: Adults with type 2 diabetes."
                },
                "designModule": {
                    "studyType": "INTERVENTIONAL",
                    "designInfo": {"primaryPurpose": "TREATMENT"},
                },
                "sponsorCollaboratorsModule": {"leadSponsor": {"name": "Example sponsor"}},
            }
        },
        "2026-10-27T00:00:00Z",
    )
    citation = rank_documents([doc], "type 2 diabetes", "test")[0]
    assert not doc.has_results
    assert citation["allowed_claim_types"] == ["development", "organization"]
    assert doc.organization_roles[0]["role"] == "lead_sponsor"
