import { spawn } from "node:child_process";
import { readdir } from "node:fs/promises";
import { join } from "node:path";

import { Plugin } from "@opencode/plugin";

interface ExampleResult {
  name: string;
  exitCode: number;
  firstLine: string;
}

interface ProcessResult {
  stdout: string;
  exitCode: number;
}

function runExample(projectDir: string, name: string): Promise<ProcessResult> {
  const target = join(projectDir, "examples", name);

  return new Promise((done) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", target], {
      cwd: projectDir,
      env: process.env,
    });

    let stdout = "";

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });

    child.on("error", () => {
      done({ stdout, exitCode: 127 });
    });

    child.on("close", (code, signal) => {
      done({ stdout, exitCode: signal ? 1 : (code ?? 1) });
    });
  });
}

async function runExamples(projectDir: string): Promise<ExampleResult[]> {
  const entries = await readdir(join(projectDir, "examples"), {
    withFileTypes: true,
  });
  const names = entries
    .filter((entry) => entry.isFile() && entry.name.endsWith(".slop"))
    .map((entry) => entry.name)
    .sort();

  return Promise.all(
    names.map(async (name) => {
      const result = await runExample(projectDir, name);
      return {
        name,
        exitCode: result.exitCode,
        firstLine: result.stdout.split(/\r?\n/, 1)[0] ?? "",
      };
    }),
  );
}

export default Plugin.define({
  id: "sloperator.example-outputs",
  setup: async (ctx) => {
    const projectDir = ctx.location.directory;

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "example_outputs",
        description:
          "Run every examples/*.slop file and return each filename, exit code, and first stdout line.",
        input: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async () => {
          const examples = await runExamples(projectDir);
          return {
            content: JSON.stringify({ examples }),
            metadata: { count: examples.length },
          };
        },
      });
    });
  },
});
