#!/usr/bin/env python3
"""Import Anki decks from the markdown sources in this directory.

Usage:
    1. Open Anki desktop. Install the "AnkiConnect" addon (code: 2055492159).
       Tools → Add-ons → Get Add-ons → paste 2055492159 → restart Anki.
    2. Make sure Anki is running.
    3. Run: python3 import_to_anki.py
       (Optional) pip install markdown  for proper rendering of code blocks and bold.

Each markdown file becomes one deck. Each `## N. Title` section becomes one card.
Re-running the script is safe — duplicates are skipped (Anki dedupes on Front).
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ANKI_CONNECT_URL = "http://127.0.0.1:8765"

DECK_PREFIX = "Interview Prep::"
FILES_TO_DECKS = {
    "code-templates.md": "Code Templates",
    "pattern-recognition.md": "Pattern Recognition",
    "complexity.md": "Complexity Reference",
}


def md_to_html(text: str) -> str:
    """Convert markdown to HTML. Uses `markdown` if installed, else a minimal fallback."""
    try:
        import markdown  # type: ignore

        return markdown.markdown(text, extensions=["fenced_code", "tables"])
    except ImportError:
        # Minimal fallback. Extract code spans first (their content is verbatim, not markdown),
        # apply bold only to the remaining prose, then restore code.
        placeholders: list[str] = []

        def stash(html: str) -> str:
            placeholders.append(html)
            return f"\x00{len(placeholders) - 1}\x00"

        def stash_fence(m: re.Match) -> str:
            return stash(f"<pre><code>{m.group(1).strip()}</code></pre>")

        def stash_inline(m: re.Match) -> str:
            return stash(f"<code>{m.group(1)}</code>")

        out = re.sub(r"```\w*\n(.*?)```", stash_fence, text, flags=re.DOTALL)
        out = re.sub(r"`([^`]+)`", stash_inline, out)
        out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
        out = out.replace("\n\n", "<br><br>").replace("\n", "<br>")
        out = re.sub(r"\x00(\d+)\x00", lambda m: placeholders[int(m.group(1))], out)
        return out


def parse_cards(md_text: str) -> list[tuple[str, str]]:
    """Split a markdown deck file into (front, back) pairs."""
    sections = re.split(r"\n---\n", md_text)
    cards: list[tuple[str, str]] = []
    for section in sections:
        if not re.search(r"\*\*Front:\*\*", section):
            continue  # skip the file's intro section
        front_match = re.search(r"\*\*Front:\*\*\s*(.+?)(?=\n\n|\Z)", section, re.DOTALL)
        back_match = re.search(r"\*\*Back:\*\*\s*(.+)", section, re.DOTALL)
        if not front_match or not back_match:
            continue
        front = front_match.group(1).strip()
        back = back_match.group(1).strip()
        cards.append((md_to_html(front), md_to_html(back)))
    return cards


def anki_request(action: str, **params) -> dict:
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(ANKI_CONNECT_URL, data=payload)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except urllib.error.URLError as e:
        sys.exit(f"Cannot reach AnkiConnect at {ANKI_CONNECT_URL} — is Anki running? ({e})")
    if data.get("error"):
        raise RuntimeError(f"AnkiConnect error on {action}: {data['error']}")
    return data["result"]


def ensure_deck(name: str) -> None:
    anki_request("createDeck", deck=name)


def add_card(deck: str, front: str, back: str) -> int | None:
    """Returns note id, or None if duplicate (already imported)."""
    note = {
        "deckName": deck,
        "modelName": "Basic",
        "fields": {"Front": front, "Back": back},
        "options": {"allowDuplicate": False},
        "tags": ["interview-prep", deck.split("::")[-1].lower().replace(" ", "-")],
    }
    try:
        return anki_request("addNote", note=note)
    except RuntimeError as e:
        if "duplicate" in str(e).lower():
            return None
        raise


def main() -> None:
    here = Path(__file__).parent
    total_added = 0
    total_skipped = 0
    for filename, deck_short in FILES_TO_DECKS.items():
        path = here / filename
        if not path.exists():
            print(f"  skip {filename} (not found)")
            continue
        deck = DECK_PREFIX + deck_short
        ensure_deck(deck)
        cards = parse_cards(path.read_text())
        added = skipped = 0
        for front, back in cards:
            if add_card(deck, front, back) is None:
                skipped += 1
            else:
                added += 1
        print(f"  {deck}: {added} added, {skipped} skipped (dupes)")
        total_added += added
        total_skipped += skipped
    print(f"\nDone. {total_added} cards added, {total_skipped} duplicates skipped.")


if __name__ == "__main__":
    main()
