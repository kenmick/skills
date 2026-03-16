#!/usr/bin/env python3
"""Fetch web page content as markdown/text with fallback chain.

Priority:
1. Jina Reader (https://r.jina.ai/)
2. defuddle.md (https://defuddle.md/)
3. markdown.new (https://markdown.new/)
4. Raw HTML fetch

Usage:
    python3 fetch.py <url> [--output <file>]
"""

import argparse
import sys
import urllib.request


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


def fetch_url(url: str, headers: dict | None = None, timeout: int = 30) -> str:
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_via_jina(target: str) -> str:
    return fetch_url(
        f"https://r.jina.ai/{target}",
        headers={"Accept": "text/markdown"},
    )


def fetch_via_markdown_new(target: str) -> str:
    return fetch_url(f"https://markdown.new/{target}")


def fetch_via_defuddle(target: str) -> str:
    return fetch_url(f"https://defuddle.md/{target}")


def fetch_raw(target: str) -> str:
    return fetch_url(target)


STRATEGIES = [
    ("Jina Reader", fetch_via_jina),
    ("defuddle.md", fetch_via_defuddle),
    ("markdown.new", fetch_via_markdown_new),
    ("Raw HTML", fetch_raw),
]


def fetch(target: str) -> str:
    errors = []
    for name, fn in STRATEGIES:
        try:
            print(f"[{name}] Fetching...", file=sys.stderr)
            content = fn(target)
            print(f"[{name}] Success ({len(content)} chars)", file=sys.stderr)
            return content
        except Exception as e:
            print(f"[{name}] Failed: {e}", file=sys.stderr)
            errors.append((name, str(e)))

    raise RuntimeError(
        "All strategies failed:\n"
        + "\n".join(f"  - {name}: {err}" for name, err in errors)
    )


def main():
    parser = argparse.ArgumentParser(description="Fetch web page content as text")
    parser.add_argument("url", help="Target URL to fetch")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    args = parser.parse_args()

    content = fetch(args.url)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(content)


if __name__ == "__main__":
    main()
