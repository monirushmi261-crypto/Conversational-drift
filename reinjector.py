def build_memory_summary(all_facts):
    """
    Converts stored facts into a clean prompt format
    so the LLM can reuse them.
    """

    if not all_facts:
        return ""

    summary = "Important facts (must follow):\n"

    seen = set()  # avoid duplicates

    for fact in all_facts:
        # fact format: (id, entity, value)
        entity = fact[1]
        value = fact[2]

        key = (entity, value)

        if key not in seen:
            summary += f"- {entity} = {value}\n"
            seen.add(key)

    return summary
