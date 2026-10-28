"""Explicit condition/population scope. Titles and eligibility have different roles."""

import re


class ScopeAmbiguity(ValueError):
    pass


def normalized(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def diabetes_types(value: str) -> set[str]:
    value = normalized(value)
    matches = set()
    if re.search(r"\b(?:gestational diabetes|gdm)\b", value):
        matches.add("gestational_diabetes")
    if re.search(r"\b(?:type (?:2|ii) diabetes|diabetes (?:mellitus )?type (?:2|ii)|t2dm|t2d)\b", value):
        matches.add("type_2_diabetes")
    if re.search(r"\b(?:type (?:1|i) diabetes|diabetes (?:mellitus )?type (?:1|i)|t1dm|t1d)\b", value):
        matches.add("type_1_diabetes")
    return matches


def diabetes_type(value: str) -> str | None:
    matches = diabetes_types(value)
    return next(iter(matches)) if len(matches) == 1 else None


def population_tags(value: str) -> list[str]:
    """Only positive population wording; tissue provenance is never a population."""
    value = re.sub(r"\b(?:non[- ]?pregnant|not pregnant|without pregnancy)\b", "", value, flags=re.I)
    patterns = {
        "pregnancy": r"\b(?:pregnan\w*|gestational|maternal)\b",
        "pediatric": r"\b(?:children|childhood|pediatric|paediatric|adolescen\w*|youth)\b",
        "obesity": r"\b(?:obesity|obese|overweight)\b",
        "kidney_disease": r"\b(?:chronic kidney disease|ckd|renal impairment|dialysis)\b",
        "cardiovascular_disease": r"\b(?:heart failure|cardiovascular disease|atherosclerotic)\b",
        "liver_disease": r"\b(?:masld|mash|steatotic liver|steatohepatitis)\b",
        "cancer": r"\b(?:cancer|malignancy|oncology)\b",
        "cognitive_risk": r"\b(?:alzheimer\w*|cognitive impairment|dementia)\b",
    }
    return [key for key, pattern in patterns.items() if re.search(pattern, value, re.I)]


def resolve_scope(condition: str, population: str = "general", *, allow_ambiguous=False) -> dict:
    key = diabetes_type(condition)
    if not key and re.search(r"\bdiabet(?:es|ic)\b", condition, re.I) and not allow_ambiguous:
        raise ScopeAmbiguity(
            "Specify type 1, type 2, or gestational diabetes before researching this condition."
        )
    labels = {
        "type_2_diabetes": "Type 2 diabetes",
        "type_1_diabetes": "Type 1 diabetes",
        "gestational_diabetes": "Gestational diabetes",
    }
    requested = population_tags(condition)
    if population != "general" and population not in requested:
        requested.append(population)
    return {
        "raw_condition": condition,
        "condition": labels.get(key, condition),
        "condition_key": key or normalized(condition),
        "population": requested or ["general"],
        "jurisdiction": "US",
    }


def condition_matches(scope: dict, title: str, conditions: list[str], body: str) -> bool:
    # Structured registry conditions win over mentions in background or exclusions.
    corpus = " ".join(conditions) if conditions else title + " " + body
    if scope["condition_key"] in {"type_1_diabetes", "type_2_diabetes", "gestational_diabetes"}:
        if not conditions and diabetes_types(title):
            return scope["condition_key"] in diabetes_types(title)
        if conditions:
            if diabetes_types(corpus):
                return scope["condition_key"] in diabetes_types(corpus)
            # Generic diabetic complications may specify subtype in positive eligibility.
            return bool(re.search(r"diabet", corpus, re.I)) and scope["condition_key"] in diabetes_types(body)
        # A background abstract mention is insufficient to establish a paper's primary focus.
        return False
    words = set(normalized(scope["condition"]).split()) - {"of", "the", "and", "in"}
    return bool(words) and words <= set(normalized(corpus).split())


def trial_population(protocol: dict) -> dict:
    identity = protocol.get("identificationModule", {})
    conditions = protocol.get("conditionsModule", {}).get("conditions", [])
    eligibility = protocol.get("eligibilityModule", {})
    criteria = eligibility.get("eligibilityCriteria", "")
    inclusion = re.split(r"\b(?:key )?exclusion(?: criteria)?\b", criteria, maxsplit=1, flags=re.I)[0]
    # Ignore negative lines, including common pregnancy exclusion/contraception language.
    positive_lines = [
        line
        for line in inclusion.splitlines()
        if not re.search(r"\b(?:not|non|no|exclude\w*|negative|contracept\w*)\b", line, re.I)
    ]
    population_text = " ".join(
        [identity.get("officialTitle", ""), identity.get("briefTitle", ""), *conditions, *positive_lines]
    )
    tags = population_tags(population_text)
    ages = eligibility.get("stdAges", [])
    maximum_age = eligibility.get("maximumAge", "")
    child_age = re.fullmatch(r"(\d+) Years", maximum_age)
    if (ages == ["CHILD"] or (child_age and int(child_age[1]) < 18)) and "pediatric" not in tags:
        tags.append("pediatric")
    return {
        "conditions": conditions,
        "tags": tags,
        "minimum_age": eligibility.get("minimumAge"),
        "maximum_age": eligibility.get("maximumAge"),
        "sex": eligibility.get("sex"),
        "eligibility_criteria": criteria,
        "inclusion_criteria": inclusion,
        "countries": sorted(
            {
                x["country"]
                for x in protocol.get("contactsLocationsModule", {}).get("locations", [])
                if x.get("country")
            }
        ),
    }
