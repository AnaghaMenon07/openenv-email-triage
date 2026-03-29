# env/grader.py

def grade(action, expected):
    score = 0.0

    # 🎯 Category check
    if action.get("category") == expected.get("category"):
        score += 0.4

    # ⚡ Priority check
    if action.get("priority") == expected.get("priority"):
        score += 0.2

    # 💬 Response quality (simple heuristic)
    response = action.get("response", "")
    if response:
        response_lower = response.lower()

        # polite tone
        if "sorry" in response_lower or "apologize" in response_lower:
            score += 0.1

        # helpful intent
        if "help" in response_lower or "assist" in response_lower:
            score += 0.1

        # mentions issue keywords
        if "refund" in response_lower or "issue" in response_lower:
            score += 0.1

    # ❌ penalty for wrong category
    if action.get("category") != expected.get("category"):
        score -= 0.2

    # clamp score between 0 and 1
    score = max(0.0, min(score, 1.0))

    return score