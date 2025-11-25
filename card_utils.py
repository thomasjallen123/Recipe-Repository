from pathlib import Path
from typing import Any, Dict, List

def _safe(scraper, method: str, default=None):
    fn = getattr(scraper, method, None)
    if callable(fn):
        try:
            return fn()
        except Exception:
            return default
    return default

def normalize(scraper) -> Dict[str, Any]:
    # Prefer a list of steps if available
    steps: List[str] = _safe(scraper, "instructions_list")
    if not steps:
        text = _safe(scraper, "instructions", "") or ""
        steps = [s.strip() for s in text.split("\n") if s.strip()]

    return {
        "title": _safe(scraper, "title", "Untitled Recipe"),
        "source_url": getattr(scraper, "url", ""),
        "host": _safe(scraper, "host", ""),
        "image": _safe(scraper, "image", None),
        "yields": _safe(scraper, "yields", None),
        "total_minutes": _safe(scraper, "total_time", None),
        "prep_minutes": _safe(scraper, "prep_time", None),
        "cook_minutes": _safe(scraper, "cook_time", None),
        "ingredients": _safe(scraper, "ingredients", []) or [],
        "steps": steps or [],
        "author": _safe(scraper, "author", None),
        "cuisine": _safe(scraper, "cuisine", None),
        "category": _safe(scraper, "category", None),
        "nutrients": _safe(scraper, "nutrients", None),
    }

def to_markdown(card: Dict[str, Any]) -> str:
    lines = [f"# {card['title']}", ""]
    if card.get("image"):
        lines += [f"![Recipe image]({card['image']})", ""]
    lines += [
        f"- **Source:** {card.get('host','')}",
        f"- **URL:** {card.get('source_url','')}",
    ]
    if card.get("yields"):        lines.append(f"- **Yields:** {card['yields']}")
    if card.get("total_minutes") is not None: lines.append(f"- **Total:** {card['total_minutes']} min")
    if card.get("prep_minutes")  is not None: lines.append(f"- **Prep:** {card['prep_minutes']} min")
    if card.get("cook_minutes")  is not None: lines.append(f"- **Cook:** {card['cook_minutes']} min")
    lines += ["", "## Ingredients", ""]
    for ing in card.get("ingredients", []):
        lines.append(f"- {ing}")
    lines += ["", "## Steps", ""]
    for i, step in enumerate(card.get("steps", []), 1):
        lines.append(f"{i}. {step}")
    lines += ["", "## Notes", "", "_Add your notes here…_"]
    return "\n".join(lines)

def safe_filename(title: str) -> str:
    keep = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    clean = "".join(c for c in title if c in keep).strip().replace(" ", "_")
    return clean or "recipe"

def write_outputs(card: Dict[str, Any], outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    base = safe_filename(card["title"])
    (outdir / f"{base}.json").write_text(__import__("json").dumps(card, indent=2, ensure_ascii=False), encoding="utf-8")
    (outdir / f"{base}.md").write_text(to_markdown(card), encoding="utf-8")
