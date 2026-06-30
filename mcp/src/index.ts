#!/usr/bin/env node
// LTM Wiki MCP server (optional, opt-in). Exposes the same memory store as the
// file/skill path over stdio. Resolves the store via ~/.ltm-wiki/config.json.
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { TOOLS, dispatch } from "./tools.js";

const server = new Server(
  { name: "ltm-wiki", version: "0.5.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args } = req.params;
  // The SDK's CallToolResult is a wide union (incl. task-style results); our
  // {content, isError} shape is valid at runtime, so cast to the handler's type.
  try {
    return (await dispatch(name, args ?? {})) as never;
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    return { content: [{ type: "text", text: `error: ${message}` }], isError: true } as never;
  }
});

async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  // stderr so we never corrupt the stdio JSON-RPC channel
  process.stderr.write("ltm-wiki MCP server running on stdio\n");
}

main().catch((err) => {
  process.stderr.write(`fatal: ${err instanceof Error ? err.message : String(err)}\n`);
  process.exit(1);
});
