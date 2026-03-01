from pathlib import Path


def test_repo_has_readme() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    assert (repo_root / "README.md").exists()
