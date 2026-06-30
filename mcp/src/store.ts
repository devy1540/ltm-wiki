// Resolves and operates on the LTM Wiki memory store. Same SSOT as the file/skill
// path: global pointer (~/.ltm-wiki/config.json) -> defaultStore -> memory/.
// Follows meta/store-structure.md and meta/conventions.md.
import {
  existsSync, readFileSync, writeFileSync, readdirSync, mkdirSync,
} from "node:fs";
import { homedir } from "node:os";
import { join, dirname, basename, relative } from "node:path";
import { parse as parseYaml, stringify as stringifyYaml } from "yaml";

export interface StoreInfo {
  root: string;
  backend: string;
  sync: string;
  storeName: string;
}

export interface Page {
  path: string;
  rel: string;
  slug: string;
  data: Record<string, unknown>;
  body: string;
}

const CATEGORY_BY_TYPE: Record<string, string> = {
  preference: "preferences",
  procedural: "procedures",
  "open-loop": "open-loops",
  concept: "concepts",
  semantic: "concepts",
  entity: "entities",
  synthesis: "syntheses",
  question: "questions",
  episodic: "episodes",
  source: "sources",
};

const SECRET_RE =
  /(AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|password\s*[:=])/i;

export function resolveStore(start: string = process.cwd()): StoreInfo {
  // 1) local .ltm-wiki/config.json, walking up. Skip the home dir (that holds the
  //    global pointer) and any config carrying `defaultStore` (also a pointer, not
  //    a store config) so we don't mistake the pointer for a local store.
  const home = homedir();
  let dir = start;
  for (;;) {
    const cfg = join(dir, ".ltm-wiki", "config.json");
    if (dir !== home && existsSync(cfg)) {
      const c = readJson(cfg);
      if (!("defaultStore" in c)) {
        return {
          root: dir,
          backend: str(c.backend, "markdown-files"),
          sync: "none",
          storeName: str(c.storeName, basename(dir)),
        };
      }
    }
    const parent = dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  // 2) global pointer
  const gp = join(homedir(), ".ltm-wiki", "config.json");
  if (existsSync(gp)) {
    const c = readJson(gp);
    const ds = typeof c.defaultStore === "string" ? c.defaultStore : "";
    if (ds && existsSync(ds)) {
      return {
        root: ds,
        backend: str(c.backend, "markdown-files"),
        sync: str(c.sync, "none"),
        storeName: basename(ds),
      };
    }
  }
  throw new Error(
    "No LTM Wiki store found. Set up the store first (ltm-setup) so ~/.ltm-wiki/config.json exists."
  );
}

export function parsePage(path: string, root: string): Page {
  const raw = readFileSync(path, "utf8");
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  let data: Record<string, unknown> = {};
  let body = raw;
  if (m) {
    data = (parseYaml(m[1]) as Record<string, unknown>) ?? {};
    body = m[2];
  }
  return {
    path,
    rel: relative(root, path),
    slug: basename(path).replace(/\.md$/, ""),
    data,
    body,
  };
}

export function listPages(store: StoreInfo): Page[] {
  const memDir = join(store.root, "memory");
  const out: Page[] = [];
  const walk = (d: string): void => {
    for (const e of readdirSync(d, { withFileTypes: true })) {
      const p = join(d, e.name);
      if (e.isDirectory()) walk(p);
      else if (e.name.endsWith(".md") && e.name !== "log.md")
        out.push(parsePage(p, store.root));
    }
  };
  if (existsSync(memDir)) walk(memDir);
  return out;
}

export function searchMemory(
  store: StoreInfo,
  query: string,
  opts: { type?: string; includeArchived?: boolean } = {}
): Page[] {
  const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
  if (terms.length === 0) return [];
  let pages = listPages(store);
  if (!opts.includeArchived) pages = pages.filter((p) => p.data.status !== "archived");
  if (opts.type) pages = pages.filter((p) => p.data.type === opts.type);
  const scored = pages
    .map((p) => {
      const hay = (JSON.stringify(p.data) + "\n" + p.body).toLowerCase();
      const score = terms.reduce((s, t) => s + (hay.split(t).length - 1), 0);
      return { p, score };
    })
    .filter((x) => x.score > 0);
  scored.sort((a, b) => b.score - a.score || confRank(b.p) - confRank(a.p));
  return scored.map((x) => x.p);
}

export function getPage(store: StoreInfo, slugOrRel: string): Page | null {
  const direct = join(store.root, slugOrRel);
  if (existsSync(direct)) return parsePage(direct, store.root);
  const want = slugOrRel.replace(/\.md$/, "");
  return listPages(store).find((p) => p.slug === want) ?? null;
}

export interface CaptureInput {
  type: string;
  title: string;
  body: string;
  tags?: string[];
  confidence?: string;
  provenance?: string;
  category?: string;
}

export function capturePage(store: StoreInfo, input: CaptureInput): string {
  const today = new Date().toISOString().slice(0, 10);
  const category = input.category ?? CATEGORY_BY_TYPE[input.type] ?? "concepts";
  const slug = slugify(input.title);
  const dir = join(store.root, "memory", category);
  mkdirSync(dir, { recursive: true });
  const path = join(dir, `${slug}.md`);
  const fm = {
    type: input.type,
    status: "active",
    created: today,
    updated: today,
    sources: [],
    tags: input.tags ?? [],
    aliases: [],
    confidence: input.confidence ?? "medium",
    provenance: input.provenance ?? "inferred",
    last_reviewed: today,
  };
  const content = `---\n${stringifyYaml(fm).trim()}\n---\n# ${input.title}\n\n${input.body.trim()}\n`;
  writeFileSync(path, content, "utf8");
  return relative(store.root, path);
}

export function appendLog(store: StoreInfo, op: string, summary: string): void {
  const today = new Date().toISOString().slice(0, 10);
  const logPath = join(store.root, "memory", "log.md");
  const entry = `\n## [${today}] ${op} | ${summary}\n\n- Operation: ${op}\n- Result: ${summary}\n`;
  const cur = existsSync(logPath) ? readFileSync(logPath, "utf8") : "# Memory Log\n";
  writeFileSync(logPath, cur.replace(/\s+$/, "") + "\n" + entry, "utf8");
}

export function scanSecret(text: string): boolean {
  return SECRET_RE.test(text);
}

export function slugify(title: string): string {
  const s = title
    .toLowerCase()
    .trim()
    .replace(/[^\wÀ-ɏ぀-ヿ가-힣]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 60);
  return s || "memory";
}

function confRank(p: Page): number {
  const c = p.data.confidence;
  return c === "high" ? 3 : c === "medium" ? 2 : c === "low" ? 1 : 0;
}

function readJson(path: string): Record<string, unknown> {
  return JSON.parse(readFileSync(path, "utf8")) as Record<string, unknown>;
}

function str(v: unknown, fallback: string): string {
  return typeof v === "string" ? v : fallback;
}
