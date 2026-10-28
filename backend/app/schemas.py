from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator
import re


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ResearchRequest(StrictModel):
    condition: str = Field(min_length=3, max_length=120)
    jurisdiction: Literal["US"] = "US"
    population: Literal[
        "general", "pregnancy", "pediatric", "obesity", "kidney_disease", "cardiovascular_disease"
    ] = "general"
    scope_confirmed: Literal[True]
    mode: Literal["live", "fixture"] = "live"
    use_llm: bool = True
    max_records: int = Field(default=12, ge=4, le=20)

    @field_validator("condition")
    @classmethod
    def condition_only(cls, value: str) -> str:
        value = " ".join(value.split())
        if not re.fullmatch(r"[\w\s(),/'’\-–]+", value) or len(value) < 3:
            raise ValueError("Enter a condition name using words, not a search expression or patient record.")
        if "@" in value or re.search(r"\b(?:DOB|MRN|patient name)\b", value, re.I):
            raise ValueError("Use a condition name only. Remove personal information.")
        return value


class ProcessRequest(ResearchRequest):
    pmids: list[str] = Field(default_factory=list, max_length=16)
    nct_ids: list[str] = Field(default_factory=list, max_length=8)

    @field_validator("pmids")
    @classmethod
    def check_pmids(cls, values: list[str]) -> list[str]:
        if any(not re.fullmatch(r"\d{1,10}", x) for x in values):
            raise ValueError("PMIDs must be numeric NCBI identifiers.")
        return list(dict.fromkeys(values))

    @field_validator("nct_ids")
    @classmethod
    def check_ncts(cls, values: list[str]) -> list[str]:
        if any(not re.fullmatch(r"NCT\d{8}", x) for x in values):
            raise ValueError("Use NCT followed by eight digits.")
        return list(dict.fromkeys(values))


class SourceDocument(StrictModel):
    source: Literal["pubmed", "clinicaltrials"]
    canonical_id: str
    url: str
    title: str
    published_date: str | None = None
    updated_date: str | None = None
    retrieved_at: str
    publication_types: list[str] = Field(default_factory=list)
    doi: str | None = None
    nct_ids: list[str] = Field(default_factory=list)
    journal: str | None = None
    authors: list[str] = Field(default_factory=list)
    phase: str | None = None
    status: str | None = None
    has_results: bool = False
    retracted: bool = False
    corrected: bool = False
    verified: bool = True
    jurisdiction: str = "unknown"
    access_level: str = "abstract_only"
    snapshot: dict
    passages: list[dict]
    organization_roles: list[dict] = Field(default_factory=list)
    population: dict = Field(default_factory=dict)
    study_type: str | None = None
    primary_purpose: str | None = None
    interventions: list[dict] = Field(default_factory=list)


class EvidenceReference(StrictModel):
    evidence_id: str
    quote: str = Field(min_length=12, max_length=1600)


class CandidateClaim(StrictModel):
    section: Literal["care_landscape", "emerging", "organizations", "specific_populations"]
    claim_type: Literal[
        "published_finding", "development", "organization", "current_care", "approval", "efficacy"
    ]
    text: str = Field(min_length=15, max_length=900)
    intervention: str
    population: str
    outcome: str
    direction: Literal["positive", "negative", "mixed", "neutral"]
    references: list[EvidenceReference] = Field(min_length=1, max_length=3)


class Extraction(StrictModel):
    claims: list[CandidateClaim] = Field(max_length=10)
    limitations: list[str] = Field(max_length=8)


class SupportDecision(StrictModel):
    index: int
    supported: bool
    explanation: str


class SupportReview(StrictModel):
    decisions: list[SupportDecision]


class ToolArguments(StrictModel):
    citation_ids: list[str] = Field(min_length=1, max_length=12)
