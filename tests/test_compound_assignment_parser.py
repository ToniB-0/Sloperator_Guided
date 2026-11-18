from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Assign, Binary, Literal


def parse_source(source: str):
    return parse(tokenize(source))


def test_plus_equal_is_tokenized():
    assert tokenize("+=")[0].type is TokenType.PLUS_EQUAL
    assert tokenize("+=")[0].lexeme == "+="


def test_compound_assignment_parses_as_an_assignment_statement():
    (statement,) = parse_source("n += 3 * 4✨")

    assert isinstance(statement, Assign)
    assert statement.name.lexeme == "n"
    assert statement.operator.type is TokenType.PLUS_EQUAL
    assert isinstance(statement.value, Binary)
    assert statement.value.operator.type is TokenType.STAR
    assert isinstance(statement.value.left, Literal) and statement.value.left.value == 3
    assert isinstance(statement.value.right, Literal) and statement.value.right.value == 4


def test_plain_assignment_still_parses():
    (statement,) = parse_source("n = 1✨")

    assert isinstance(statement, Assign)
    assert statement.operator.type is TokenType.EQUAL
