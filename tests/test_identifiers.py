from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.exit_code == 0
    return result.stdout


def test_digits_are_allowed_in_variable_names():
    source = "slop score2 = 40✨\nscore2 = score2 + 2✨\nhallucinate(score2)✨"
    assert run(source) == "42\n"


def test_digits_are_allowed_in_function_and_parameter_names():
    source = "clanker add2(a1, b2) {\n    ship a1 + b2✨\n}\nhallucinate(add2(40, 2))✨"
    assert run(source) == "42\n"


def test_identifier_cannot_start_with_a_digit():
    result = run_source("slop 2score = 40✨\nhallucinate(2score)✨")
    assert result.stdout == ""
    assert result.exit_code == 1
    assert result.stderr == (
        "SlopLang syntax error at line 1: expected a variable name after 'slop', found '2'\n"
    )
