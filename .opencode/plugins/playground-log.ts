import { appendFile, mkdir } from "node:fs/promises";
import { join } from "node:path";

import { Plugin } from "@opencode/plugin";

const LOG_DIR = "logs";
const LOG_FILE = "plugin-playground.log";

export default Plugin.define({
  id: "sloperator.playground-log",
  setup: async (ctx) => {
    const logDir = join(ctx.location.directory, LOG_DIR);
    const logPath = join(logDir, LOG_FILE);

    await ctx.tool.hook("execute.before", async ({ tool, input }) => {
      if (tool !== "shell" && tool !== "bash") return;

      const command = (input as { command?: unknown } | null)?.command;
      if (typeof command !== "string") return;
      if (!command.includes("playground/server.py")) return;

      await mkdir(logDir, { recursive: true });
      await appendFile(logPath, "playground shell request\n", "utf8");
    });
  },
});
