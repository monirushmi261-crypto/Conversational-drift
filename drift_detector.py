def detect_forgetting(response, all_facts, user_input):

    missed = []

    response_lower = response.lower()

    # 🔥 Only track important entities
    important_entities = [
        "budget",
        "preference",
        "requirement",
        "usage"
    ]

    # Filter facts
    filtered_facts = [
        f for f in all_facts
        if f[1] in important_entities
    ]

    for fact in filtered_facts:
        value = fact[2].lower()

        if value not in response_lower:
            missed.append(fact)

    return missed
