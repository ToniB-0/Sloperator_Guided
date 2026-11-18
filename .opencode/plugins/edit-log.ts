import { appendFile, mkdir } from "node:fs/promises";
import { join } from "node:path";

import { Plugin } from "@opencode/plugin";

const LOG_DIR = "logs";
const LOG_FILE = "plugin-tools.log";
const FILE_CHANGING_TOOLS = new Set(["edit", "write", "patch"]);

export default Plugin.define({
  id: "sloperator.edit-log",
  setup: async (ctx) => {
    const logDir = join(ctx.location.directory, LOG_DIR);
    const logPath = join(logDir, LOG_FILE);

    await ctx.tool.hook("execute.after", async (event) => {
      if (event.status !== "completed") return;
      if (!FILE_CHANGING_TOOLS.has(event.tool)) return;

      await mkdir(logDir, { recursive: true });
      await appendFile(
        logPath,
        `${JSON.stringify({ tool: event.tool, status: event.status })}\n`,
        "utf8",
      );
    });
  },
});
