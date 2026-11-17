from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.exit_code == 0
    return result.stdout


def test_comparison_binds_tighter_than_equality():
    # `1 < 2 == ✅` must parse as `(1 < 2) == ✅`, not `1 < (2 == ✅)`.
    assert run("hallucinate(1 < 2 == ✅)✨") == "✅\n"


def test_equality_compares_a_comparison_result():
    assert run("hallucinate(1 == 2 < 3)✨") == "❌\n"
