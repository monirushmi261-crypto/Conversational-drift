from memory_store import get_all_facts

def check_contradiction(entity, new_value):
    facts = get_all_facts()

    old_values = []

    for f in facts:
        if f[1] == entity:  # entity match
            old_values.append(f[2])

    if old_values and new_value not in old_values:
        return True, old_values
    
    return False, old_values

