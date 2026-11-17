from sloperator.runner import run_source


def test_loop_with_a_false_condition_never_runs():
    result = run_source("ralph ❌ {\n    hallucinate(“never”)✨\n}")
    assert result.stdout == ""
    assert result.stderr == ""
    assert result.exit_code == 0
