# Sloperator

A tree-walking interpreter for [SlopLang](docs/spec.md), written in Python.

## Quick Start

Run a program:

```bash
uv run sloperator.py examples/fib.slop
```

Validate the project:

```bash
uv run pytest              # tests
uv run ruff format --check # formatting
uv run ruff check          # linting
uv run ty check            # type checking
```

## Layout

| Path                    | What it is                                           |
| ----------------------- | ---------------------------------------------------- |
| `sloperator.py`         | Command-line entrypoint                              |
| `sloperator/lexer/`     | Source text to tokens                                |
| `sloperator/parser/`    | Tokens to AST (`ast.py` holds the node definitions)  |
| `sloperator/evaluator/` | Walks the AST: values, environments, the interpreter |
| `sloperator/runner.py`  | Runs source through all three stages                 |
| `docs/spec.md`          | The language specification                           |
| `examples/`             | Example programs                                     |
| `tests/`                | Pytest suite                                         |
| `playground/`           | A web playground for running programs                |

## Playground

```bash
uv run playground/server.py
```

Then open <http://localhost:8080>.

See [docs/spec.md](docs/spec.md) for the full language specification.
