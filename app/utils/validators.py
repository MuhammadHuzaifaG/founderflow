def sanitize_text(value: str, max_length: int = 4000) -> str:
    if value is None:
        return ""
    cleaned = value.strip().replace("\r\n", "\n")
    if len(cleaned) > max_length:
        return cleaned[:max_length]
    return cleaned