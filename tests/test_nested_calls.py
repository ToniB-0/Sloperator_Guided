from sloperator.lexer import tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Call, ExprStmt, FunctionDecl, Literal, Variable

SOURCE = """clanker add(left, right) {
    ship left + right✨
}
hallucinate(add(1, 2))✨"""


def test_call_is_direct_argument_of_another_call():
    declaration, statement = parse(tokenize(SOURCE))
    assert isinstance(declaration, FunctionDecl)
    assert isinstance(statement, ExprStmt)

    outer = statement.expression
    assert isinstance(outer, Call)
    assert isinstance(outer.callee, Variable) and outer.callee.name.lexeme == "hallucinate"
    assert len(outer.arguments) == 1

    inner = outer.arguments[0]
    assert isinstance(inner, Call)
    assert isinstance(inner.callee, Variable) and inner.callee.name.lexeme == "add"
    assert len(inner.arguments) == 2

    left, right = inner.arguments
    assert isinstance(left, Literal) and left.value == 1
    assert isinstance(right, Literal) and right.value == 2
