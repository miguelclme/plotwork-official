#!/usr/bin/env python3
r"""Write Figma design links into the `design` key of a work-breakdown.yaml (used by from-app and from-app-update).

Usage:
    python set_design_links.py docs/planning/work-breakdown.yaml \
        'TSH-FT-001=My tools — /tools|https://www.figma.com/design/KEY/Name?node-id=12-34' \
        'TSH-FT-001=Add a tool — /tools/new|https://www.figma.com/design/KEY/Name?node-id=12-56' \
        'TSH-FT-003='

Put each argument in single quotes, so the shell passes it as written ($ and backticks included). An apostrophe
inside the text is written '\'' (close the quote, an escaped apostrophe, open the quote again), as in
'TSH-FT-001=Owner'\''s tools — /owner|https://…'.
Each argument is DRAFT-ID=<screen>|<link>. The text is split at the LAST "|", so a screen name may contain one.
The link is taken as given (surrounding spaces dropped): the script doesn't check its form.
DRAFT-ID= with nothing after it removes the item's `design` key.
For every draft ID named, the script replaces the item's whole `design` list with one string per screen given,
"<screen> — <link>", in the order given. Give every screen of the item, not only the new ones. The key is added
just before the item's ado_id line when the item has none.
An existing key is rewritten as a block list, whatever it was: `[]`, an empty value, a flow list `[a, b]`, or a
block list at the key's indent or deeper. The key may sit on the dash line.

Nothing but the `design` key of the named items changes. Every other line stays byte for byte: comments,
downstream_notes, quoting, the line endings (CRLF or LF), a BOM and a missing final newline. An item whose
`design` already holds the screens given is left alone. Before writing, the script parses the old and the new
text and checks that they are equal once the `design` key of the named items is set aside, and that each named
item's `design` is exactly what was asked. If not, nothing is written.
Exit code: 0 = written, or nothing to change; 1 = a link could not be set (nothing is written);
2 = the file could not be read or written.
"""
import argparse
import copy
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True  # keep the plugin folder free of __pycache__
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import set_ado_ids
import wbtools

ASSIGNMENT = re.compile(rf"^({set_ado_ids.DRAFT_ID})=(.*)$", re.DOTALL)
KEY_LINE = re.compile(r"^(\s*)design:(?:\s+(.*))?$")
LINE = re.compile(r"[^\r\n]*(?:\r\n|\r|\n)|[^\r\n]+$")
SEPARATOR = " — "


def _split_lines(text):
    """The lines of `text` with their line endings, splitting only at CRLF, LF or CR."""
    return LINE.findall(text)


def _design_lines(texts, start, end, key_column):
    """[(line index, KEY_LINE match)] for the design keys of the entry in lines start..end."""
    hits = []
    for index in range(start, end):
        body = texts[index]
        if index == start:  # the first key shares the line with the dash: look at it as if it stood alone
            body = " " * key_column + body[key_column:]
        match = KEY_LINE.match(body)
        if match and len(match.group(1)) == key_column:
            hits.append((index, match))
    return hits


def _is_continuation(text, key_column):
    """A line that belongs to the design key above it: deeper than the key, or a dash at the key's own column."""
    indent = set_ado_ids._indent(text)
    return indent > key_column or (indent == key_column and (text.strip() == "-" or text.lstrip().startswith("- ")))


def _block_end(texts, index, end, key_column):
    """The last line of the design key that starts at `index`: its value, then its list, wherever it goes."""
    last = index
    for position in range(index + 1, end):
        if set_ado_ids._is_blank_or_comment(texts[position]):
            continue
        if not _is_continuation(texts[position], key_column):
            break
        last = position
    return last


def _line_ending(lines, texts, index):
    """The line ending of line `index`, or that of any other line, or LF."""
    for position in [index, *range(len(lines))]:
        ending = lines[position][len(texts[position]):]
        if ending:
            return ending
    return "\n"


def _quoted(text):
    return json.dumps(text, ensure_ascii=False)


def _insert_position(texts, start, end, key_column):
    """Where a missing design key goes: before the ado_id line, else after the last line holding content."""
    hits = set_ado_ids._ado_lines(texts, start, end, key_column)
    if len(hits) == 1:
        return hits[0][0] if hits[0][0] > start else start + 1
    last = end - 1
    while last > start and set_ado_ids._is_blank_or_comment(texts[last]):
        last -= 1
    return last + 1


def _replacement(texts, key_line, key_column, match, screens, last):
    """The new text lines (without endings) for the existing design key in lines key_line..last."""
    rest = match.group(2) or ""
    comment = rest[len(wbtools._strip_comment(rest)):].strip()  # a trailing comment on the key line stays
    comment = " " + comment if comment else ""
    list_indent = key_column + 2
    for position in range(key_line + 1, last + 1):
        text = texts[position]
        if text.lstrip().startswith("-") and set_ado_ids._indent(text) >= key_column:
            list_indent = set_ado_ids._indent(text)
            break
    head = texts[key_line][:key_column] + "design:" + comment
    return [head, *[" " * list_indent + "- " + _quoted(screen) for screen in screens]]


def set_links(text, wanted):
    """Return (new text, [messages], ok). `wanted` is {draft_id: [design strings], or None to remove the key}."""
    lines = _split_lines(text)
    texts = [line.rstrip("\r\n") for line in lines]
    ranges = set_ado_ids._item_ranges(texts)
    try:
        items = {item.get("draft_id"): item for item in wbtools.items_of(wbtools.breakdown_of(wbtools.loads_yaml(text)))}
    except wbtools.PARSE_ERRORS:
        items = {}
    messages, ok, edits = [], True, []
    for draft_id, screens in wanted.items():
        spans = ranges.get(draft_id, [])
        if len(spans) != 1:
            messages.append(f"{draft_id}: {'not found' if not spans else 'appears more than once'}")
            ok = False
            continue
        item = items.get(draft_id, {})
        if (screens is None and "design" not in item) or (screens is not None and item.get("design") == screens):
            messages.append(f"{draft_id}: design is already as given")
            continue
        start, end, key_column = spans[0]
        hits = _design_lines(texts, start, end, key_column)
        if len(hits) > 1:
            messages.append(f"{draft_id}: has more than one design key")
            ok = False
        elif screens is None:
            index = hits[0][0]
            edits.append((index, _block_end(texts, index, end, key_column) + 1, []))
            messages.append(f"{draft_id}: design removed")
        elif hits:
            index, match = hits[0]
            last = _block_end(texts, index, end, key_column)
            new_texts = _replacement(texts, index, key_column, match, screens, last)
            edits.append((index, last + 1, new_texts))
            messages.append(f"{draft_id}: design replaced, {len(screens)} screen(s)")
        else:
            position = _insert_position(texts, start, end, key_column)
            new_texts = [" " * key_column + "design:", *[" " * (key_column + 2) + "- " + _quoted(s) for s in screens]]
            edits.append((position, position, new_texts))
            messages.append(f"{draft_id}: design added, {len(screens)} screen(s)")
    if not ok:
        return text, messages, False
    for first, after, new_texts in sorted(edits, reverse=True):  # from the bottom, so earlier indexes stay valid
        if not new_texts:  # a removal
            if after == len(lines) and first > 0:  # the removed key ended the file: keep the file's last ending
                lines[first - 1] = texts[first - 1] + lines[after - 1][len(texts[after - 1]):]
            del lines[first:after]
            del texts[first:after]
            continue
        ending = _line_ending(lines, texts, first if first < len(lines) else len(lines) - 1)
        last_ending = lines[after - 1][len(texts[after - 1]):] if after > first else ending
        new_lines = [line + ending for line in new_texts]
        if after == first and first == len(lines) and lines and not lines[-1].endswith(("\n", "\r")):
            lines[-1] += ending  # inserting after a last line that has no ending
            new_lines[-1] = new_texts[-1]
        elif after > first:
            new_lines[-1] = new_texts[-1] + last_ending
        lines[first:after] = new_lines
        texts[first:after] = new_texts
    return "".join(lines), messages, True


def _without_design(data, draft_ids):
    """A copy of the parsed file with the design key of the named items set aside."""
    data = copy.deepcopy(data)
    for item in wbtools.items_of(wbtools.breakdown_of(data)):
        if item.get("draft_id") in draft_ids:
            item.pop("design", None)
    return data


def _problem(old_data, new_text, wanted):
    """Why the edited text can't be written, or None when it parses, holds the screens and changes nothing else."""
    try:
        new_data = wbtools.loads_yaml(new_text)
    except Exception as exc:  # noqa: BLE001 (wbtools.YamlError, PyYAML's own error, or a parser bug: never write)
        return f"the edited file would not parse ({exc})"
    if _without_design(old_data, wanted) != _without_design(new_data, wanted):
        return "the edit would change more than the design key"
    items = {item.get("draft_id"): item for item in wbtools.items_of(wbtools.breakdown_of(new_data))}
    missed = [draft_id for draft_id, screens in wanted.items()
              if (screens is None and "design" in items.get(draft_id, {}))
              or (screens is not None and items.get(draft_id, {}).get("design") != screens)]
    return f"the edit did not land on {', '.join(missed)}" if missed else None


def _parse_arguments(pairs):
    """Return ({draft_id: [design strings], or None to remove the key}, error or None)."""
    wanted = {}
    for pair in pairs:
        match = ASSIGNMENT.match(pair)
        if match and not match.group(2).strip():  # DRAFT-ID= : remove the key
            if wanted.get(match.group(1)):
                return {}, f"{match.group(1)} is given both screens and nothing"
            wanted[match.group(1)] = None
            continue
        screen, bar, link = match.group(2).rpartition("|") if match else ("", "", "")
        screen, link = screen.strip(), link.strip()
        if not match or not bar or not screen or not link:
            return {}, f"{pair!r} is not DRAFT-ID=<screen>|<link>, or DRAFT-ID= to remove the key"
        if any(ord(char) < 32 for char in screen + link):
            return {}, f"{pair!r}: the screen name or the link has a line break or another control character"
        if match.group(1) in wanted and wanted[match.group(1)] is None:
            return {}, f"{match.group(1)} is given both screens and nothing"
        entry = f"{screen}{SEPARATOR}{link}"
        designs = wanted.setdefault(match.group(1), [])
        if entry not in designs:
            designs.append(entry)
    return wanted, None


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="%(prog)s YAML 'DRAFT-ID=<screen>|<link>' ['DRAFT-ID=<screen>|<link>' | 'DRAFT-ID=' ...]")
    parser.add_argument("yaml", help="path to work-breakdown.yaml")
    parser.add_argument("designs", nargs="+", metavar="DRAFT-ID=<screen>|<link>",
                        help="a screen of the item and the link of its Figma frame; repeat for every screen. "
                             "DRAFT-ID= with nothing after it removes the item's design key")
    args = parser.parse_args(argv)
    wanted, error = _parse_arguments(args.designs)
    if error:
        print(f"ERROR: {error}")
        return 1
    path = pathlib.Path(args.yaml)
    try:
        with path.open(encoding="utf-8", newline="") as handle:  # not utf-8-sig: a BOM must survive the rewrite
            text = handle.read()
        old_data = wbtools.loads_yaml(text)
    except (OSError, *wbtools.PARSE_ERRORS) as exc:
        print(f"ERROR: cannot read {path}: {exc}")
        return 2
    new_text, messages, ok = set_links(text, wanted)
    print("\n".join(messages))
    if not ok:
        print("Nothing was written.")
        return 1
    if new_text != text:
        problem = _problem(old_data, new_text, wanted)
        if problem:
            print(f"ERROR: {problem}. Nothing was written.")
            return 1
        try:
            with path.open("w", encoding="utf-8", newline="") as handle:
                handle.write(new_text)
        except OSError as exc:
            print(f"ERROR: cannot write {path}: {exc}")
            return 2
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
