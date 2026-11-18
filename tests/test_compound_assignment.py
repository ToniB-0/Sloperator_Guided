from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.exit_code == 0
    return result.stdout


def test_compound_assignment_adds_numbers():
    source = "slop n = 2✨\nn += 3 * 4✨\nhallucinate(n)✨"
    assert run(source) == "14\n"


def test_compound_assignment_joins_strings():
    source = "slop greeting = “hello”✨\ngreeting += “, slop”✨\nhallucinate(greeting)✨"
    assert run(source) == "hello, slop\n"


def test_compound_assignment_updates_the_nearest_shadowed_variable():
    source = (
        "slop greeting = “outer”✨\n"
        "{\n"
        "    slop greeting = “inner”✨\n"
        "    {\n"
        "        greeting += “!”✨\n"
        "    }\n"
        "    hallucinate(greeting)✨\n"
        "}\n"
        "hallucinate(greeting)✨"
    )
    assert run(source) == "inner!\nouter\n"


def test_compound_assignment_evaluates_the_right_hand_side_first():
    source = (
        "slop n = 2✨\n"
        "clanker change() {\n"
        "    n = 10✨\n"
        "    ship 1✨\n"
        "}\n"
        "n += change()✨\n"
        "hallucinate(n)✨"
    )
    assert run(source) == "11\n"


def test_compound_assignment_to_an_undefined_name_is_a_runtime_error():
    result = run_source("missing += 1✨")

    assert result.stdout == ""
    assert result.exit_code == 1
    assert result.stderr == "SlopLang runtime error at line 1: undefined variable 'missing'\n"


def test_compound_assignment_to_loadbearing_is_a_runtime_error():
    result = run_source("loadbearing LIMIT = 1✨\nLIMIT += 2✨")

    assert result.stdout == ""
    assert result.exit_code == 1
    assert (
        result.stderr == "SlopLang runtime error at line 2: cannot assign to loadbearing 'LIMIT'\n"
    )


def test_compound_assignment_rejects_incompatible_operand_types():
    result = run_source("slop x = 1✨\nx += “a”✨")

    assert result.stdout == ""
    assert result.exit_code == 1
    assert result.stderr == (
        "SlopLang runtime error at line 2: operands of '+=' must both be numbers "
        "or both be strings, got number and string\n"
    )
