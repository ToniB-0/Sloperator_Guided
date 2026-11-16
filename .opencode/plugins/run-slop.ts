import { spawn } from "node:child_process";
import { isAbsolute, resolve } from "node:path";

import { Plugin } from "@opencode/plugin";

interface RunResult {
  stdout: string;
  stderr: string;
  exitCode: number;
}

function runSloperator(projectDir: string, filePath: string): Promise<RunResult> {
  const target = isAbsolute(filePath) ? filePath : resolve(projectDir, filePath);

  return new Promise((done) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", target], {
      cwd: projectDir,
      env: process.env,
    });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });

    child.on("error", (error) => {
      done({ stdout, stderr: `${stderr}${error.message}`, exitCode: 127 });
    });

    child.on("close", (code, signal) => {
      if (signal) stderr += `\nterminated by signal ${signal}`;
      done({ stdout, stderr, exitCode: code ?? 1 });
    });
  });
}

export default Plugin.define({
  id: "sloperator.run-slop",
  setup: async (ctx) => {
    const projectDir = ctx.location.directory;

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description:
          "Run a Sloperator program (.slop file) from the project root and return its stdout, stderr, and exit code as JSON.",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description:
                "Path to the .slop file to run, e.g. examples/hello.slop. Relative paths are resolved against the project root.",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path } = input as { path: string };
          const result = await runSloperator(projectDir, path);

          return {
            content: JSON.stringify(result),
            metadata: { path, exitCode: result.exitCode },
          };
        },
      });
    });
  },
});
