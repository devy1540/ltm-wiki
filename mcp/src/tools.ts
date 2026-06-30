// Tool definitions and dispatch for the LTM Wiki MCP server.
import {
  resolveStore, listPages, getPage, searchMemory, capturePage, appendLog, scanSecret,
  type CaptureInput,
} from "./store.js";

interface ToolResult {
  content: { type: "text"; text: string }[];
  isError?: boolean;
}

export const TOOLS = [
  {
    name: "ltm_status",
    description: "Show the active LTM Wiki store: path, backend, sync, and memory count.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "ltm_recall",
    description:
      "Search long-term memory by keywords. Ranks active pages by hit count then confidence. Optionally filter by type.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Keywords to search for." },
        type: { type: "string", description: "Optional memory type filter (e.g. preference, concept)." },
        limit: { type: "number", description: "Max results (default 10)." },
      },
      required: ["query"],
    },
  },
  {
    name: "ltm_get",
    description: "Read a single memory page by slug or store-relative path.",
    inputSchema: {
      type: "object",
      properties: { id: { type: "string", description: "Slug (e.g. ltm-wiki-architecture) or rel path." } },
      required: ["id"],
    },
  },
  {
    name: "ltm_list",
    description: "List active memory pages, optionally filtered by type.",
    inputSchema: {
      type: "object",
      properties: { type: { type: "string", description: "Optional memory type filter." } },
    },
  },
  {
    name: "ltm_capture",
    description:
      "Create a durable memory page (full frontmatter, slug, log entry). Rejects secret-like content.",
    inputSchema: {
      type: "object",
      properties: {
        type: { type: "string", description: "Memory type: preference, concept, procedural, episodic, open-loop, synthesis, question, entity, source, semantic." },
        title: { type: "string", description: "Human-readable title." },
        body: { type: "string", description: "Markdown body." },
        tags: { type: "array", items: { type: "string" } },
        confidence: { type: "string", description: "high | medium | low (default medium)." },
        provenance: { type: "string", description: "user-stated | inferred | source-backed | system-generated (default inferred)." },
      },
      required: ["type", "title", "body"],
    },
  },
  {
    name: "ltm_log",
    description: "Append an operation entry to memory/log.md.",
    inputSchema: {
      type: "object",
      properties: {
        op: { type: "string", description: "Operation label, e.g. capture, maintenance." },
        summary: { type: "string", description: "One-line result." },
      },
      required: ["op", "summary"],
    },
  },
];

export async function dispatch(name: string, args: Record<string, unknown>): Promise<ToolResult> {
  const store = resolveStore();
  switch (name) {
    case "ltm_status": {
      const count = listPages(store).length;
      return text(
        JSON.stringify(
          { root: store.root, backend: store.backend, sync: store.sync, storeName: store.storeName, memoryPages: count },
          null,
          2
        )
      );
    }
    case "ltm_recall": {
      const q = String(args.query ?? "");
      const limit = typeof args.limit === "number" ? args.limit : 10;
      const hits = searchMemory(store, q, { type: optStr(args.type) }).slice(0, limit);
      if (hits.length === 0) return text("no matches");
      return text(
        hits.map((p) => `- ${p.slug} [${p.data.type ?? "?"}] (${p.data.confidence ?? "?"}) — ${p.rel}`).join("\n")
      );
    }
    case "ltm_get": {
      const p = getPage(store, String(args.id ?? ""));
      if (!p) return text(`not found: ${String(args.id)}`, true);
      return text(`# ${p.slug} (${p.rel})\n\n---\n${JSON.stringify(p.data, null, 2)}\n---\n${p.body.trim()}`);
    }
    case "ltm_list": {
      let pages = listPages(store).filter((p) => p.data.status !== "archived");
      const t = optStr(args.type);
      if (t) pages = pages.filter((p) => p.data.type === t);
      if (pages.length === 0) return text("no pages");
      return text(pages.map((p) => `- ${p.slug} [${p.data.type ?? "?"}] — ${p.rel}`).join("\n"));
    }
    case "ltm_capture": {
      const title = String(args.title ?? "");
      const body = String(args.body ?? "");
      if (!title || !body) return text("title and body are required", true);
      if (scanSecret(body) || scanSecret(title))
        return text("REJECTED: secret-like content detected. Redact credentials before storing.", true);
      const input: CaptureInput = {
        type: String(args.type ?? "concept"),
        title,
        body,
        tags: Array.isArray(args.tags) ? (args.tags as unknown[]).map(String) : undefined,
        confidence: optStr(args.confidence),
        provenance: optStr(args.provenance),
      };
      const rel = capturePage(store, input);
      appendLog(store, "capture", `MCP captured ${rel}`);
      return text(`captured: ${rel}`);
    }
    case "ltm_log": {
      const op = String(args.op ?? "note");
      const summary = String(args.summary ?? "");
      if (!summary) return text("summary is required", true);
      appendLog(store, op, summary);
      return text(`logged: [${op}] ${summary}`);
    }
    default:
      return text(`unknown tool: ${name}`, true);
  }
}

function text(t: string, isError = false): ToolResult {
  return { content: [{ type: "text", text: t }], ...(isError ? { isError: true } : {}) };
}

function optStr(v: unknown): string | undefined {
  return typeof v === "string" && v.length > 0 ? v : undefined;
}
