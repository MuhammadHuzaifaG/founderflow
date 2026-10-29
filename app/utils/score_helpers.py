def calculate_score(urgency: int, fit: int, access: int) -> int:
    weighted = (urgency * 0.45) + (fit * 0.35) + (access * 0.20)
    return max(1, min(100, round(weighted)))

def format_score(score: int) -> str:
    return f"{score}/100"