from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.exit_code == 0
    return result.stdout


def fails(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 1
    return result.stderr.rstrip("\n")


def test_not_flips_booleans_and_double_not_flips_back():
    assert run("hallucinate(!✅, !❌, !!✅)✨") == "❌ ✅ ✅\n"


def test_not_of_a_number_is_a_runtime_error():
    assert fails("hallucinate(!1)✨") == (
        "SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got number"
    )


def test_not_of_a_string_is_a_runtime_error():
    assert fails("hallucinate(!“slop”)✨") == (
        "SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got string"
    )
