---
name: create-test-program
description: Create a runnable SlopLang example and an exact-output test for a language feature
---

# Create Test Program

Given a SlopLang language feature, add an example program and an exact-output regression test.

1. **Read the spec.** Consult `docs/spec.md` for the feature's syntax, semantics, value formatting, and error behavior. The spec is the source of truth.

2. **Write the example.** Create `examples/<feature>.slop` using real SlopLang syntax (smart
   quotes `“ ”`, `✨` terminators, `✅`/`❌`, `—` comments). Print one result per line with
   `hallucinate`, and cover the interesting cases (normal, boundary, and type-sensitive
   behavior). Keep it minimal and free of unrelated features.

3. **Write the exact-output test.** Add a case to `tests/test_example_outputs.py` that reads
   the example and asserts its exact `stdout`, empty `stderr`, and exit code 0. If the file
   does not exist, create it with this parametrized table:

```python
from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


@pytest.mark.parametrize(
    ("example", "expected"),
    [
        ("<feature>.slop", "<exact stdout>"),
    ],
)
def test_example_output(example: str, expected: str):
    result = run_source((EXAMPLES / example).read_text(encoding="utf-8"))
    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == expected
```

4. **Validate.** Run `uv run ruff format`, then `uv run pytest tests/test_example_outputs.py -q`,
   then the full validation commands from the root `AGENTS.md`: `uv run pytest`,
   `uv run ruff format --check`, `uv run ruff check`, and `uv run ty check`.

Expected output follows `docs/spec.md`: numbers in base 10, strings without quotes, booleans
as `✅`/`❌`, nil as `nil`, and functions as `<clanker name>`.
