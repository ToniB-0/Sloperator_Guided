# Parser conventions

These rules apply to `sloperator/parser/parser.py`.

- **Use one method per grammar rule.** Each production in the grammar from
  `docs/spec.md` gets exactly one `Parser` method named after it (`logic_or`,
  `logic_and`, `equality`, `comparison`, `term`, `factor`, `unary`, `call`,
  `primary`, and so on). Keep a rule's repetition loop inside its method; do not
  split one production across helper methods such as `*_tail`.
- **Make syntax errors describe what token was found.** Report errors through
  `self.error(token, message)` so every diagnostic names the offending token
  (`found '<lexeme>'`) or says it reached end of file. Phrase the message as the
  expectation first, for example `expected ')' after arguments`.
