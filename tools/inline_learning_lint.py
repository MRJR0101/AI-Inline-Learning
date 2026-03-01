#!/usr/bin/env python3
"""Lint inline-learning comment blocks for required fields."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

DEFAULT_EXTENSIONS = {
    ".py",
    ".ps1",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".sql",
    ".sh",
    ".md",
}
REQUIRED_LABELS = {"HEY", "MISTAKE", "LESSON", "RULE"}
LABEL_PATTERN = re.compile(
    r"^\s*(?:#|//|--|;|\*|/\*|rem\s+)?\s*(HEY|MISTAKE|LESSON|RULE)\b[^:]*:",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    code: str
    message: str


def parse_labels(lines: Sequence[str]) -> list[tuple[int, str]]:
    labels: list[tuple[int, str]] = []
    for line_no, line in enumerate(lines, start=1):
        match = LABEL_PATTERN.match(line)
        if match:
            labels.append((line_no, match.group(1).upper()))
    return labels


def validate_labels(path: Path, labels: Sequence[tuple[int, str]], max_gap: int) -> list[Finding]:
    findings: list[Finding] = []
    current_start: int | None = None
    current_labels: set[str] = set()
    last_line = -1

    def flush_block() -> None:
        nonlocal current_start, current_labels
        if current_start is None:
            return
        missing = REQUIRED_LABELS - current_labels
        if missing:
            findings.append(
                Finding(
                    path=str(path),
                    line=current_start,
                    code="IL001",
                    message=f"Missing labels in HEY block: {', '.join(sorted(missing))}",
                )
            )
        current_start = None
        current_labels = set()

    for line_no, label in labels:
        if label == "HEY":
            flush_block()
            current_start = line_no
            current_labels = {"HEY"}
            last_line = line_no
            continue

        if current_start is None or (line_no - last_line) > max_gap:
            findings.append(
                Finding(
                    path=str(path),
                    line=line_no,
                    code="IL002",
                    message=f"{label} label found without a nearby HEY label",
                )
            )
            continue

        current_labels.add(label)
        last_line = line_no

    flush_block()
    return findings


def lint_text(path: Path, text: str, max_gap: int) -> list[Finding]:
    labels = parse_labels(text.splitlines())
    return validate_labels(path=path, labels=labels, max_gap=max_gap)


def lint_file(path: Path, max_gap: int) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="ignore")
    return lint_text(path=path, text=text, max_gap=max_gap)


def iter_source_files(paths: Sequence[Path], extensions: set[str]) -> Iterable[Path]:
    seen: set[Path] = set()
    for raw_path in paths:
        path = raw_path.resolve()
        if path.is_file():
            if path.suffix.lower() in extensions and path not in seen:
                seen.add(path)
                yield path
            continue

        if not path.is_dir():
            continue

        for child in path.rglob("*"):
            if not child.is_file():
                continue
            if child.suffix.lower() not in extensions:
                continue
            if any(part.startswith(".git") for part in child.parts):
                continue
            resolved = child.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            yield resolved


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lint inline-learning comment blocks.")
    parser.add_argument(
        "paths",
        nargs="*",
        default=["patterns", "examples"],
        help="Files or directories to scan (default: patterns examples).",
    )
    parser.add_argument(
        "--max-gap",
        type=int,
        default=8,
        help="Maximum allowed line gap between labels within a single block.",
    )
    parser.add_argument(
        "--extensions",
        default=",".join(sorted(DEFAULT_EXTENSIONS)),
        help="Comma-separated file extensions to scan.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON findings.",
    )
    return parser


def parse_extensions(value: str) -> set[str]:
    parsed: set[str] = set()
    for raw in value.split(","):
        ext = raw.strip().lower()
        if not ext:
            continue
        if not ext.startswith("."):
            ext = f".{ext}"
        parsed.add(ext)
    return parsed or DEFAULT_EXTENSIONS


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    extensions = parse_extensions(args.extensions)
    paths = [Path(p) for p in args.paths]

    findings: list[Finding] = []
    for file_path in iter_source_files(paths=paths, extensions=extensions):
        findings.extend(lint_file(path=file_path, max_gap=args.max_gap))

    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        for finding in findings:
            print(f"{finding.path}:{finding.line}: {finding.code} {finding.message}")
        if findings:
            print(f"\n{len(findings)} inline-learning issue(s) found.")
        else:
            print("No inline-learning issues found.")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
