from career_data import DOMAIN_WEIGHTS, DOMAINS, TRAIT_LABELS, get_question_traits


def calculate_trait_scores(answers: list[int], question_set_id: str) -> dict[str, float]:
    question_traits = get_question_traits(question_set_id)
    if not question_traits:
        raise ValueError("Unknown question set")

    totals = {trait: 0.0 for trait in TRAIT_LABELS}
    maximums = {trait: 0.0 for trait in TRAIT_LABELS}

    for answer, mapping in zip(answers, question_traits):
        for trait, weight in mapping.items():
            totals[trait] += answer * weight
            maximums[trait] += 5 * weight

    return {
        trait: round((totals[trait] / maximums[trait]) * 100, 2)
        if maximums[trait]
        else 0.0
        for trait in totals
    }


def calculate_domain_scores(traits: dict[str, float]) -> list[dict]:
    domain_lookup = {domain["name"]: domain for domain in DOMAINS}
    scored = []

    for name, weights in DOMAIN_WEIGHTS.items():
        total_weight = sum(weights.values())
        weighted_score = sum(traits[trait] * weight for trait, weight in weights.items())
        score = weighted_score / total_weight
        domain = domain_lookup[name]
        scored.append(
            {
                "name": name,
                "slug": domain["slug"],
                "category": domain["category"],
                "summary": domain["summary"],
                "icon": domain["icon"],
                "score": round(score, 1),
            }
        )

    return sorted(scored, key=lambda item: item["score"], reverse=True)


def score_assessment(answers: list[int], question_set_id: str) -> dict:
    traits = calculate_trait_scores(answers, question_set_id)
    ranked_domains = calculate_domain_scores(traits)
    top_traits = sorted(traits.items(), key=lambda item: item[1], reverse=True)[:5]

    return {
        "recommendations": ranked_domains[:5],
        "top_traits": [
            {"code": code, "name": TRAIT_LABELS[code], "score": round(score, 1)}
            for code, score in top_traits
        ],
        "methodology": (
            "Responses are normalized across 20 career traits and compared with "
            "weighted profiles for 25 IT domains."
        ),
        "question_set_id": question_set_id,
    }
