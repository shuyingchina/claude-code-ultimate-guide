#!/usr/bin/env python3
"""
Translate guide/ultimate-guide.md from English into a target language.

Usage  : python3 scripts/translate-guide.py [--lang fr|zh|...]
Output : guide/ultimate-guide.<lang>.md
Resume : .translation-cache-<lang>/ (chunk files, auto-cleaned on success)
Model  : claude-sonnet-4-6

Default language is French (fr) to preserve the original behaviour.
"""

import argparse
import sys
import time
import traceback
from pathlib import Path

import anthropic

MAX_RETRIES = 3
RETRY_BACKOFF = [5, 15, 30]  # seconds between retries

# ── Config ────────────────────────────────────────────────────────────────────
SOURCE = Path("guide/ultimate-guide.md")
MODEL  = "claude-sonnet-4-6"

# Max lines before forcing a split at the next heading
MAX_LINES_H2  = 200
MAX_LINES_H3  = 450

# Supported target languages: code → human-readable name used in the prompt.
LANGUAGES = {
    "fr": "French",
    "zh": "Simplified Chinese (简体中文)",
}

# Per-language note appended to the TRANSLATE section when extra guidance helps.
LANG_NOTES = {
    "zh": (
        "- Use natural, idiomatic Simplified Chinese; do not translate "
        "word-for-word\n"
        "- Keep a single space between Chinese text and inline English terms "
        "or `code` for readability"
    ),
}


def build_system(lang_name: str, lang_code: str) -> str:
    extra = LANG_NOTES.get(lang_code, "")
    if extra:
        extra = "\n" + extra
    return f"""\
You are a technical translator English → {lang_name} for the Claude Code Ultimate Guide.

KEEP IN ENGLISH — do not translate:
- All code blocks and inline code (`…`, ```…```)
- Shell commands, CLI flags (--flag), environment variables
- File/path names: CLAUDE.md, settings.json, .claude/, etc.
- Proper nouns: Claude Code, Claude, Anthropic, GitHub, VS Code, Cursor
- Technical identifiers: hooks, skills, agents, MCP, API, slash commands,
  SubAgent, TaskCreate, HEREDOC, worktree, compact, ultrathink
- Markdown structural syntax: ##, **, *, >, |, ```, [ ], ( ), ---

TRANSLATE to {lang_name}:
- All prose, section titles (## headings text), table cell text, list items,
  callout text, admonitions, descriptions, explanations
- Maintain technical, clear, direct tone — no marketing language{extra}

PRESERVE exactly:
- All blank lines and spacing
- All markdown formatting structure
- All URLs (translate anchor text if it is prose)

OUTPUT: translated markdown only — no preamble, no commentary, no code fences \
wrapping the whole output.\
"""


# ── Chunking ──────────────────────────────────────────────────────────────────

def make_chunks(text: str) -> list[str]:
    lines   = text.split("\n")
    chunks  = []
    current = []

    for line in lines:
        if line.startswith("## ") and len(current) > MAX_LINES_H2:
            chunks.append("\n".join(current))
            current = [line]
        elif line.startswith("### ") and len(current) > MAX_LINES_H3:
            chunks.append("\n".join(current))
            current = [line]
        else:
            current.append(line)

    if current:
        chunks.append("\n".join(current))

    return chunks


# ── Translation ───────────────────────────────────────────────────────────────

def translate_chunk(
    client: anthropic.Anthropic,
    system: str,
    chunk:  str,
    idx:    int,
    total:  int,
) -> str:
    words = len(chunk.split())
    min_expected_chars = max(200, words * 0.5)  # reject obvious meta-responses only

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"  [{idx:3d}/{total}] {words:4d} words … ", end="", flush=True)
        t0 = time.time()

        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=8000,
                system=system,
                messages=[{"role": "user", "content": chunk}],
            )
            elapsed = time.time() - t0

            result = next(
                (b.text for b in resp.content if hasattr(b, "text") and b.type == "text"),
                None,
            )

            if result is None:
                raise ValueError(f"No text block in response (blocks: {[type(b).__name__ for b in resp.content]})")

            if len(result) < min_expected_chars:
                raise ValueError(f"Output too short ({len(result)} chars for {words} words — likely meta-response)")

            print(f"{elapsed:.1f}s")
            return result

        except KeyboardInterrupt:
            raise
        except Exception as exc:
            print(f"FAIL (attempt {attempt}/{MAX_RETRIES}): {exc}")
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF[attempt - 1]
                print(f"  Retrying in {wait}s…")
                time.sleep(wait)
            else:
                raise


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lang",
        default="fr",
        choices=sorted(LANGUAGES),
        help="Target language code (default: fr)",
    )
    args = parser.parse_args()

    lang_code = args.lang
    lang_name = LANGUAGES[lang_code]
    output    = Path(f"guide/ultimate-guide.{lang_code}.md")
    cache     = Path(f".translation-cache-{lang_code}")
    system    = build_system(lang_name, lang_code)

    cache.mkdir(exist_ok=True)
    client = anthropic.Anthropic()

    print(f"Reading {SOURCE} …")
    content     = SOURCE.read_text(encoding="utf-8")
    total_words = len(content.split())
    chunks      = make_chunks(content)

    cost_est = (total_words * 1.3 / 1e6 * 3) + (total_words * 1.3 * 1.1 / 1e6 * 15)
    print(f"  Target: {lang_name}  →  {output}")
    print(f"  {total_words:,} words  |  {len(chunks)} chunks  |  ~${cost_est:.2f} est.")
    print(f"  Model: {MODEL}\n")

    t_start = time.time()

    for i, chunk in enumerate(chunks, 1):
        chunk_file = cache / f"chunk_{i:04d}.md"

        if chunk_file.exists():
            print(f"  [{i:3d}/{len(chunks)}] cached — skip")
            continue

        try:
            result = translate_chunk(client, system, chunk, i, len(chunks))
            chunk_file.write_text(result, encoding="utf-8")
        except KeyboardInterrupt:
            print("\nInterrupted. Run again to resume from this chunk.")
            return 1
        except Exception as exc:
            print(f"\nError on chunk {i}:")
            traceback.print_exc()
            print("Run again to resume.")
            return 1

    # ── Assemble ──────────────────────────────────────────────────────────────
    cached = sorted(cache.glob("chunk_*.md"))

    if len(cached) != len(chunks):
        print(f"\nPartial: {len(cached)}/{len(chunks)} chunks done. Run again to continue.")
        return 1

    print(f"\nAssembling {len(cached)} chunks → {output}")
    output.write_text(
        "\n\n".join(f.read_text(encoding="utf-8") for f in cached),
        encoding="utf-8",
    )

    out_words = len(output.read_text(encoding="utf-8").split())
    total_sec = time.time() - t_start
    print(f"Done! {out_words:,} words | {total_sec:.0f}s total")

    # Clean up cache
    for f in cached:
        f.unlink()
    cache.rmdir()

    return 0


if __name__ == "__main__":
    sys.exit(main())
