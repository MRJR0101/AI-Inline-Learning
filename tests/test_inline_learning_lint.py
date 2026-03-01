from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

TOOL_PATH = Path(__file__).resolve().parents[1] / "tools" / "inline_learning_lint.py"


def run_lint(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL_PATH), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_valid_block_passes(tmp_path: Path) -> None:
    sample = tmp_path / "valid.py"
    sample.write_text(
        "\n".join(
            [
                "# HEY CLAUDE: Check this transform carefully.",
                "# MISTAKE: Previous refactor dropped null handling.",
                "# LESSON: Keep explicit null checks before cast.",
                "# RULE: Guard null and empty values before conversion.",
            ]
        ),
        encoding="utf-8",
    )

    result = run_lint(str(sample))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "No inline-learning issues found." in result.stdout


def test_missing_rule_is_reported(tmp_path: Path) -> None:
    sample = tmp_path / "missing_rule.py"
    sample.write_text(
        "\n".join(
            [
                "# HEY CLAUDE: Keep this parser stable.",
                "# MISTAKE: Broke column parsing for quoted values.",
                "# LESSON: Handle escaped delimiters before split.",
            ]
        ),
        encoding="utf-8",
    )

    result = run_lint("--json", str(sample))
    assert result.returncode == 1
    findings = json.loads(result.stdout)
    assert findings[0]["code"] == "IL001"
    assert "RULE" in findings[0]["message"]


def test_orphan_label_is_reported(tmp_path: Path) -> None:
    sample = tmp_path / "orphan.py"
    sample.write_text(
        "# MISTAKE: This marker exists without a HEY block.",
        encoding="utf-8",
    )

    result = run_lint("--json", str(sample))
    assert result.returncode == 1
    findings = json.loads(result.stdout)
    assert findings[0]["code"] == "IL002"
