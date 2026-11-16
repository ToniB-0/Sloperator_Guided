from sloperator.lexer import tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal
from sloperator.runner import run_source


def only_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


def test_multiplication_binds_tighter_than_addition_in_the_ast():
    # `2 + 3 * 4` must parse as `2 + (3 * 4)`, so the '+' node's right side is the product.
    expression = only_expression("2 + 3 * 4✨")
    assert isinstance(expression, Binary)
    assert expression.operator.lexeme == "+"
    assert isinstance(expression.left, Literal) and expression.left.value == 2

    product = expression.right
    assert isinstance(product, Binary)
    assert product.operator.lexeme == "*"
    assert isinstance(product.left, Literal) and product.left.value == 3
    assert isinstance(product.right, Literal) and product.right.value == 4


def test_multiplication_is_evaluated_before_addition():
    result = run_source("hallucinate(2 + 3 * 4)✨")
    assert result.stderr == ""
    assert result.stdout == "14\n"


def test_grouping_overrides_multiplication_before_addition():
    result = run_source("hallucinate((2 + 3) * 4)✨")
    assert result.stderr == ""
    assert result.stdout == "20\n"
