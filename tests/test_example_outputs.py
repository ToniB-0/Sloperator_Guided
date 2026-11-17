from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


@pytest.mark.parametrize(
    ("example", "expected"),
    [
        ("equality.slop", "✅\n❌\n❌\n"),
        ("short-circuit.slop", "❌\n✅\n"),
    ],
)
def test_example_output(example: str, expected: str):
    result = run_source((EXAMPLES / example).read_text(encoding="utf-8"))
    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == expected
