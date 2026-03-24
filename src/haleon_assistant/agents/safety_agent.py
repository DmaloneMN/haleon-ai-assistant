from typing import Dict, List

from haleon_assistant.tools.content_safety_tool import check_content


class SafetyAgent:
    """Safety agent for scaffold that defers to content_safety_tool.check_content."""

    def check(self, query: str, docs: List[Dict]) -> dict:
        """
        Build a single text blob from query + document snippets and run the safety check.
        Returns dict with keys 'ok' (bool) and 'issues' (list).
        """
        parts = []
        if query:
            parts.append(query)
        for d in docs or []:
            if isinstance(d, dict):
                s = d.get("snippet") or d.get("text") or ""
                if s:
                    parts.append(s)
        text = " ".join(parts).strip()
        res = check_content(text)
        ok = bool(res.get("safe", True))
        return {"ok": ok, "issues": res.get("issues", [])}
