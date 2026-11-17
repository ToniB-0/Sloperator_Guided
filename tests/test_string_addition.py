from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.exit_code == 0
    return result.stdout


def test_adding_an_empty_string_on_the_left_keeps_the_original():
    assert run("hallucinate(“” + “slop”)✨") == "slop\n"


def test_adding_an_empty_string_on_the_right_keeps_the_original():
    assert run("hallucinate(“slop” + “”)✨") == "slop\n"


def test_adding_a_string_with_an_emoji_works():
    assert run("hallucinate(“café” + “✨”)✨") == "café✨\n"
