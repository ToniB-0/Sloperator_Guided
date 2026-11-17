# AGENTS.md

Sloperator is a tree-walking interpreter for SlopLang, written in Python 3.13+ with no
runtime dependencies.

## Project layout

| Path | Contents |
| --- | --- |
| `sloperator.py` | CLI entrypoint; `--check` parses without executing |
| `sloperator/lexer/` | Source text to tokens |
| `sloperator/parser/` | Tokens to AST; parser-specific rules live in `sloperator/parser/AGENTS.md` |
| `sloperator/evaluator/` | AST execution, values, environments |
| `sloperator/runner.py` | `check_program`, `run_program`, and `run_source` |
| `tests/` | Pytest suite |
| `examples/` | Runnable `.slop` programs |
| `docs/spec.md` | The language specification |
| `playground/` | Web playground server and page |

## Validation

Run these from the project root; all four must pass:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

Run the comparison tests specifically with `uv run pytest tests/test_comparisons.py -q`.

After any code change, run `uv run ruff format` to apply formatting before validating.

## When to add regression tests

Add a regression test whenever you fix a bug or change language-visible behavior:

- Write the failing case first and assert the corrected output or diagnostic, so the test
  fails without the fix.
- Put parser or lexer tests next to the affected stage (`tests/test_parser.py`,
  `tests/test_lexer.py`). Use `run_source` for evaluator and end-to-end cases, asserting
  on `stdout`, `stderr`, and `exit_code`.
- Cover changed operators, error messages, scoping rules, and built-ins; these are all
  language-visible behavior.
- Add or update an `examples/*.slop` program for a new feature. `tests/test_examples.py`
  runs every example and requires a clean exit with non-empty output.
- A behavior-preserving refactor needs no new test, but the full suite must still pass.

## Language behavior

Do not restate the language here or in the README. Link to
[`docs/spec.md`](docs/spec.md) for syntax, values, operators, built-ins, and errors, and
update the spec whenever behavior changes.
