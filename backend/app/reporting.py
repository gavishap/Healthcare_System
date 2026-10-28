import html
import re


def safe_markdown(value: str) -> str:
    """External content remains text in the exported Markdown, never active HTML/images/links."""
    return re.sub(r"([\\`*_\[\]{}])", r"\\\1", html.escape(value, quote=False))


def source_link(citation: dict, label: str, *, synthetic=False) -> str:
    if synthetic or citation.get("is_synthetic"):
        return safe_markdown(label) + " (synthetic fixture; no original publication)"
    return f"[{safe_markdown(label)}]({citation['url']})"
