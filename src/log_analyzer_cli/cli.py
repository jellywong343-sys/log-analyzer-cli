from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

LEVEL_RE = re.compile(r"\b(TRACE|DEBUG|INFO|NOTICE|WARN(?:ING)?|ERROR|CRITICAL|FATAL)\b", re.I)
STATUS_RE = re.compile(r"(?<!\d)([1-5]\d{2})(?!\d)")
TIMESTAMP_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2}[T ][0-2]\d:[0-5]\d:[0-5]\d(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)")
NUMBER_RE = re.compile(r"\b\d+\b")
SPACE_RE = re.compile(r"\s+")

@dataclass
class FileSummary:
    file: str
    lines: int
    levels: dict[str, int]
    status_codes: dict[str, int]
    first_timestamp: str | None
    last_timestamp: str | None
    common_messages: list[tuple[str, int]]


def normalize_message(line: str) -> str:
    line = TIMESTAMP_RE.sub("<timestamp>", line.strip())
    line = NUMBER_RE.sub("<n>", line)
    return SPACE_RE.sub(" ", line)[:300]


def analyze_file(path: Path, top: int = 10, encoding: str = "utf-8") -> FileSummary:
    level_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    messages: Counter[str] = Counter()
    timestamps: list[str] = []
    line_count = 0
    with path.open("r", encoding=encoding, errors="replace") as handle:
        for raw in handle:
            line_count += 1
            level_match = LEVEL_RE.search(raw)
            if level_match:
                level = level_match.group(1).upper()
                if level == "WARNING":
                    level = "WARN"
                level_counts[level] += 1
            for status in STATUS_RE.findall(raw):
                status_counts[status] += 1
            if match := TIMESTAMP_RE.search(raw):
                timestamps.append(match.group(1))
            normalized = normalize_message(raw)
            if normalized:
                messages[normalized] += 1
    return FileSummary(
        file=str(path.resolve()),
        lines=line_count,
        levels=dict(sorted(level_counts.items())),
        status_codes=dict(sorted(status_counts.items())),
        first_timestamp=min(timestamps) if timestamps else None,
        last_timestamp=max(timestamps) if timestamps else None,
        common_messages=messages.most_common(top),
    )


def combine(summaries: list[FileSummary]) -> dict:
    levels: Counter[str] = Counter()
    statuses: Counter[str] = Counter()
    for item in summaries:
        levels.update(item.levels)
        statuses.update(item.status_codes)
    return {
        "files": len(summaries),
        "lines": sum(item.lines for item in summaries),
        "levels": dict(sorted(levels.items())),
        "status_codes": dict(sorted(statuses.items())),
    }


def write_csv(path: Path, summaries: list[FileSummary]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["file", "lines", "first_timestamp", "last_timestamp", "errors", "warnings"])
        for item in summaries:
            writer.writerow([
                item.file, item.lines, item.first_timestamp or "", item.last_timestamp or "",
                item.levels.get("ERROR", 0) + item.levels.get("CRITICAL", 0) + item.levels.get("FATAL", 0),
                item.levels.get("WARN", 0),
            ])


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze levels, status codes, and recurring log messages.")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--json", dest="json_path")
    parser.add_argument("--csv", dest="csv_path")
    args = parser.parse_args()
    summaries = [analyze_file(Path(name), args.top, args.encoding) for name in args.files]
    total = combine(summaries)
    print(f"Files: {total['files']}  Lines: {total['lines']}")
    print("Levels: " + (", ".join(f"{key}={value}" for key, value in total["levels"].items()) or "none"))
    print("HTTP statuses: " + (", ".join(f"{key}={value}" for key, value in total["status_codes"].items()) or "none"))
    for item in summaries:
        print(f"\n{item.file}")
        for message, count in item.common_messages:
            print(f"  {count:>4}  {message}")
    report = {"total": total, "files": [asdict(item) for item in summaries]}
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.csv_path:
        write_csv(Path(args.csv_path), summaries)

if __name__ == "__main__":
    main()
