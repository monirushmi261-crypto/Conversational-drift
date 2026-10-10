drift_history = []


def calculate_drift(missed_facts, wrong_facts):

    total = len(missed_facts) + len(wrong_facts)

    if total == 0:
        return 0

    drift = (total / (total + 1)) * 100

    return round(drift,2)


def save_drift(turn, score):
    drift_history.append(
        {
            "turn": turn,
            "score": score
        }
    )


def get_drift_history():
    return drift_history
