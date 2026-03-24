def check_content(text: str) -> dict:
    """
    Minimal deterministic safety check used for scaffold/testing.

    - If text is empty -> safe=False with issue 'empty_text'
    - Otherwise -> safe=True, no issues
    """
    if not text or not text.strip():
        return {"safe": False, "issues": ["empty_text"]}
    return {"safe": True, "issues": []}
