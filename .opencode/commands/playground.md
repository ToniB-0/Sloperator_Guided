---
description: Start the Sloperator playground on a port, reusing a server that is already running
---

Use port `$ARGUMENTS` for the playground. If `$ARGUMENTS` is empty, use `8080`.

Existing TCP listeners:

!`lsof -nP -iTCP -sTCP:LISTEN`

Check the listener list above for an existing Sloperator playground server. If one is already listening, reuse it and do not start another. Otherwise, start `uv run playground/server.py <port>` in the background, substituting the port above (`8080` when no argument was given), then verify that it is listening.
