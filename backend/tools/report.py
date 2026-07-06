"""
Offline report generator for the Phase 7 Garmin data inventory.

Reads only snapshots/_manifest.json and the snapshot files it references - no
garminconnect or AccountManager import anywhere in this file - so docs/api-report.md
can always be regenerated without hitting Garmin again.

Run with:
    uv run --directory backend python -m tools.report
"""

import json
from pathlib import Path
from typing import Any

from tools import router_map

SNAPSHOTS_DIR = Path(__file__).parent / "snapshots"
MANIFEST_PATH = SNAPSHOTS_DIR / "_manifest.json"
REPORT_PATH = Path(__file__).resolve().parents[2] / "docs" / "api-report.md"

MAX_ITEMS = 5
SAMPLE_LIMIT = 400


def sketch(value: Any, depth: int = 0) -> str:
    """
    One-line-per-level shape sketch: top-level keys with value types, recursing
    two levels into dicts and peeking at a list's first element's shape.

    :param value: parsed JSON value
    :param depth: current recursion depth, stops at 2
    :return: indented multi-line shape description
    """
    indent = "  " * depth

    if depth > 2:
        return f"{indent}..."

    if isinstance(value, dict):
        lines = []

        for key in list(value.keys())[:MAX_ITEMS]:
            lines.append(f"{indent}- {key}: {type(value[key]).__name__}")

            if isinstance(value[key], dict | list) and value[key]:
                lines.append(sketch(value[key], depth + 1))

        if len(value) > MAX_ITEMS:
            lines.append(f"{indent}  ... (+{len(value) - MAX_ITEMS} more keys)")

        return "\n".join(lines)

    if isinstance(value, list):
        if not value:
            return f"{indent}[] (empty list)"

        return f"{indent}list[{len(value)}] of:\n" + sketch(value[0], depth + 1)

    return f"{indent}{type(value).__name__} = {value!r}"


def truncated_sample(value: Any) -> str:
    """
    Render value as indented JSON, truncated to SAMPLE_LIMIT characters.

    :param value: parsed JSON value
    :return: JSON text, possibly truncated with a trailing marker
    """
    text = json.dumps(value, indent=2, default=str)

    if len(text) <= SAMPLE_LIMIT:
        return text

    return text[:SAMPLE_LIMIT].rstrip(" ") + "\n... (truncated)"


def render_method(record: dict[str, Any]) -> str:
    """
    Render one method's Markdown section from its manifest record.

    :param record: one entry from snapshots/_manifest.json
    :return: Markdown text for this method's section
    """
    lines = [f"### {record['method']}", "", f"- **Status:** {record['status']}"]

    if record["args"]:
        lines.append(f"- **Args:** `{json.dumps(record['args'], default=str)}`")

    if record["status"] == "data":
        data = json.loads((SNAPSHOTS_DIR / record["snapshot"]).read_text(encoding="utf-8"))
        lines.append("- **Shape:**")
        lines.append("")
        lines.append("```")
        lines.append(sketch(data))
        lines.append("```")
        lines.append("- **Sample:**")
        lines.append("")
        lines.append("```json")
        lines.append(truncated_sample(data))
        lines.append("```")
    elif record["status"] in ("404", "error", "skipped"):
        lines.append(f"- **Reason:** {record['error']}")

    return "\n".join(lines)


def build_report(records: list[dict[str, Any]]) -> str:
    """
    Group manifest records by router (in router_map.ROUTER_ORDER) and render the full report.

    :param records: parsed snapshots/_manifest.json contents
    :return: full Markdown document
    """
    by_router: dict[str, list[dict[str, Any]]] = {router: [] for router in router_map.ROUTER_ORDER}

    for record in records:
        by_router.setdefault(record["router"], []).append(record)

    sections = ["# Garmin API Inventory", "", "Generated offline from `backend/tools/snapshots/`.", ""]

    for router in router_map.ROUTER_ORDER:
        methods = sorted(by_router.get(router, []), key=lambda r: r["method"])

        if not methods:
            continue

        sections.append(f"## {router}")
        sections.append("")

        for record in methods:
            sections.append(render_method(record))
            sections.append("")

    return "\n".join(sections)


def main() -> None:
    """Read the manifest, build the report, and write docs/api-report.md."""
    records = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(records), encoding="utf-8")
    print(f"Wrote {REPORT_PATH} from {len(records)} manifest entries.")


if __name__ == "__main__":
    main()
