// Nexluna — Markdown-for-Agents content negotiation (Netlify Edge Function).
//
// When a client sends `Accept: text/markdown`, we serve the matching `.md`
// document with `Content-Type: text/markdown`. Browsers (Accept: text/html)
// are untouched and keep receiving HTML. This satisfies the Cloudflare
// "Agent-Ready" Markdown Negotiation check.
//
// Mapping of HTML routes -> markdown files (all pre-generated under /md/):
//   /                       -> /md/index.md
//   /converters/<cat>.html  -> /md/converters/<cat>.md
//   /index.html             -> /md/index.md

const CONVERTERS = new Set([
  "length", "weight", "area", "volume", "temperature", "data", "speed",
  "time", "pressure", "energy", "power", "angle", "fuel", "frequency",
]);

function wantsMarkdown(accept) {
  if (!accept) return false;
  // Only when markdown is explicitly requested (and not clearly preferring html).
  const a = accept.toLowerCase();
  if (!a.includes("text/markdown")) return false;
  // If the client explicitly asks for html with higher priority, keep html.
  // Simple heuristic: markdown present -> serve markdown for agents.
  return true;
}

function mapToMarkdown(pathname) {
  if (pathname === "/" || pathname === "/index.html") return "/md/index.md";
  const m = pathname.match(/^\/converters\/([a-z0-9_-]+)\.html$/i);
  if (m && CONVERTERS.has(m[1].toLowerCase())) {
    return "/md/converters/" + m[1].toLowerCase() + ".md";
  }
  return null;
}

export default async function handler(request, context) {
  const accept = request.headers.get("accept") || "";
  if (!wantsMarkdown(accept)) {
    return; // fall through to normal (HTML) response
  }

  const url = new URL(request.url);
  const mdPath = mapToMarkdown(url.pathname);
  if (!mdPath) {
    return; // no markdown twin for this route -> serve HTML as usual
  }

  const mdUrl = new URL(mdPath, url.origin);
  const res = await context.rewrite(mdUrl);
  // Wrap with correct Content-Type so agents see markdown.
  const body = await res.text();
  const headers = new Headers(res.headers);
  headers.set("Content-Type", "text/markdown; charset=utf-8");
  headers.set("Vary", "Accept");
  headers.set("X-Content-Negotiation", "markdown");
  return new Response(body, { status: 200, headers });
}

export const config = {
  path: ["/", "/index.html", "/converters/*"],
};
