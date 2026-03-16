---
name: web-fetcher
description: Fetch web page content as clean markdown/text from a URL. Use when the user provides a URL and wants to read, extract, or analyze its content. Triggers on requests like "fetch this page", "read this URL", "grab the content from", "summarize this article", or any task requiring web page text extraction.
---

# Web Fetcher

Extract web page content as clean text/markdown from a given URL.

## Usage

Run the fetch script:

```bash
python3 <skill-path>/scripts/fetch.py <url>
```

Save to file:

```bash
python3 <skill-path>/scripts/fetch.py <url> -o output.md
```

## Fallback Chain

The script tries these sources in order, falling back on failure:

1. **Jina Reader** (`https://r.jina.ai/{url}`) — best markdown quality
2. **defuddle.md** (`https://defuddle.md/{url}`)
3. **markdown.new** (`https://markdown.new/{url}`)
4. **Raw HTML** — direct fetch as last resort

Progress and errors are printed to stderr. Only the final content goes to stdout.
