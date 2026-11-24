#!/usr/bin/env python3
"""Write Azure DevOps IDs into a work-breakdown.yaml, one item at a time (used by the push skill).

Usage:
    python set_ado_ids.py docs/planning/work-breakdown.yaml BCH-EP-001=1233 BCH-FT-001=1234 ...

Every item has the same `ado_id: null` line, so a plain text edit cannot tell them apart. This script finds
the list entry whose draft_id is given (in any key position, with any spacing after the dash) and changes
only that entry's ado_id line. Indentation, comments, line endings and every other line stay as they are.
Setting an ID an item already has is a no-op; replacing a different ID is refused.
Exit code: 0 = written, 1 = an ID could not be set (nothing is written), 2 = the file could not be read.
"""
import argparse
import pathlib
import re
import sys

sys.dont_write_bytecode = True  # keep the plugin folder free of __pycache__
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import wbtools

DRAFT_ID = r"[A-Z][A-Z0-9]{1,5}-(?:EP|FT)-[0-9]{3,}"
LIST_ENTRY = re.compile(r"^(\s*)-(\s+)(\S.*)$")
DRAFT_ID_LINE = re.compile(rf"^draft_id:\s*[\"']?({DRAFT_ID})[\"']?\s*(?:#.*)?$")
ADO_LINE = re.compile(r"^(\s*ado_id:)(\s*)([^#\s]*)(\s*)(#.*)?$")
ASSIGNMENT = re.compile(rf"^({DRAFT_ID})=([1-9][0-9]*)$")
EMPTY_VALUES = ("null", "~", "")


def _indent(text):
    return len(text) - len(text.lstrip())


def _is_blank_or_comment(text):
    return not text.strip() or text.lstrip().startswith("#")


def _entry_end(texts, start, indent):
    """Index of the first line after the entry that starts at `start`: the next non-blank, non-comment line
    indented no deeper than its dash."""
    for index in range(start + 1, len(texts)):
        if not _is_blank_or_comment(texts[index]) and _indent(texts[index]) <= indent:
            return index
    return len(texts)


def _item_ranges(texts):
    """Return {draft_id: [(first line, end line, key column)]} for every list entry that holds a draft_id.

    `texts` are the file's lines without their line endings. An entry starts at a "- " line, and ends at the
    next non-blank, non-comment line indented no deeper than its dash. Its keys sit at the column of the first
    key after the dash, whatever the spacing, and draft_id may be any of them, not only the first.
    """
    ranges = {}
    for start, text in enumerate(texts):
        entry = LIST_ENTRY.match(text)
        if not entry:
            continue
        indent = len(entry.group(1))
        key_column = indent + 1 + len(entry.group(2))
        end = _entry_end(texts, start, indent)
        for index in range(start, end):
            body = entry.group(3) if index == start else texts[index]
            if index != start and _indent(body) != key_column:
                continue
            draft_id = DRAFT_ID_LINE.match(body.strip())
            if draft_id:
                ranges.setdefault(draft_id.group(1), []).append((start, end, key_column))
                break
    return ranges


def _ado_lines(texts, start, end, key_column):
    """[(line index, ADO_LINE match)] for the ado_id keys of the entry in lines start..end."""
    hits = []
    for index in range(start, end):
        body = texts[index]
        if index == start:  # the first key shares the line with the dash: look at it as if it stood alone
            body = " " * key_column + body[key_column:]
        match = ADO_LINE.match(body)
        if match and _indent(body) == key_column:
            hits.append((index, match))
    return hits


def _with_value(match, value):
    """The ado_id line of `match` holding `value`, keeping a trailing comment in its column when there is room."""
    key, spacing_before, current, spacing_after, comment = match.groups()
    spacing_after = spacing_after or ""
    if comment:
        spacing_after = " " * max(1, len(current) + len(spacing_after) - len(value))
    return f"{key}{spacing_before or ' '}{value}{spacing_after}{comment or ''}".rstrip()


def set_ids(text, assignments):
    """Return (new text, [messages], ok)."""
    lines = text.splitlines(keepends=True)
    texts = [line.rstrip("\r\n") for line in lines]
    ranges = _item_ranges(texts)
    messages, ok = [], True
    for draft_id, ado_id in assignments:
        spans = ranges.get(draft_id, [])
        if len(spans) != 1:
            messages.append(f"{draft_id}: {'not found' if not spans else 'appears more than once'}")
            ok = False
            continue
        hits = _ado_lines(texts, *spans[0])
        if len(hits) != 1:
            messages.append(f"{draft_id}: {'has no ado_id line' if not hits else 'has more than one ado_id line'}")
            ok = False
            continue
        index, match = hits[0]
        current, value = match.group(3), str(ado_id)
        if current == value:
            messages.append(f"{draft_id}: ado_id is already {ado_id}")
            continue
        if current not in EMPTY_VALUES:
            messages.append(f"{draft_id}: ado_id is already {current}; refusing to replace it with {ado_id}")
            ok = False
            continue
        line_ending = lines[index][len(texts[index]):]
        texts[index] = _with_value(match, value)
        lines[index] = texts[index] + line_ending
        messages.append(f"{draft_id}: ado_id {current or 'empty'} → {ado_id}")
    return "".join(lines), messages, ok


def _missed_ids(new_text, assignments):
    """The draft IDs whose ado_id the parsed new text does not hold (empty when every edit landed)."""
    breakdown = wbtools.breakdown_of(wbtools.loads_yaml(new_text))
    items = {item.get("draft_id"): item for item in wbtools.items_of(breakdown)}
    return [draft_id for draft_id, ado_id in assignments if items.get(draft_id, {}).get("ado_id") != ado_id]


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Write ADO IDs into a work-breakdown.yaml.")
    parser.add_argument("yaml", help="path to work-breakdown.yaml")
    parser.add_argument("ids", nargs="+", metavar="DRAFT-ID=ADO-ID", help="for example BCH-FT-001=1234")
    args = parser.parse_args(argv)
    assignments = []
    for pair in args.ids:
        match = ASSIGNMENT.match(pair)
        if not match:
            print(f"ERROR: {pair!r} is not DRAFT-ID=ADO-ID (for example BCH-FT-001=1234)")
            return 1
        assignments.append((match.group(1), int(match.group(2))))
    path = pathlib.Path(args.yaml)
    try:
        with path.open(encoding="utf-8", newline="") as handle:  # not utf-8-sig: a BOM must survive the rewrite
            text = handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: cannot read {path}: {exc}")
        return 2
    new_text, messages, ok = set_ids(text, assignments)
    print("\n".join(messages))
    if not ok:
        print("Nothing was written.")
        return 1
    if new_text != text:
        # check the result still parses and holds the IDs before writing it
        try:
            missed = _missed_ids(new_text, assignments)
        except Exception as exc:  # noqa: BLE001 (wbtools.YamlError, PyYAML's own error, or a parser bug: never write)
            print(f"ERROR: the edited file would not parse ({exc}). Nothing was written.")
            return 1
        if missed:
            print(f"ERROR: the edit did not land on {', '.join(missed)}. Nothing was written.")
            return 1
        with path.open("w", encoding="utf-8", newline="") as handle:
            handle.write(new_text)
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
