"""Shared helpers for the plugin's scripts. Standard library only.

- load_yaml():      uses PyYAML when it is installed, otherwise reads the YAML subset that
                    work-breakdown.yaml uses (block mappings and lists, [flow] lists and {flow} maps,
                    quoted strings, | and > blocks, comments).
- validate_schema(): checks data against the JSON Schema keywords used by work-breakdown.schema.json.
- read_planning():  collects planning IDs (OBJ-1, FR-3, Q-2, ...) with their table row, from the
                    Markdown tables in the planning folder. An ID is defined where it is the first
                    cell of a table row.
- later_section():  the Later list of a prototype plan (prototype-plan.md), or None.
- breakdown_of() / items_of(): the work_breakdown mapping and its item mappings, tolerant of a malformed file.
"""
import hashlib
import json
import pathlib
import re

SHARED_DIR = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_PATH = SHARED_DIR / "templates" / "work-breakdown.schema.json"
PROTOTYPE_PLAN = "prototype-plan.md"


# ── YAML ─────────────────────────────────────────────────────────────────────────────────────

class YamlError(ValueError):
    pass


# Text files are read as utf-8-sig: a UTF-8 BOM (Notepad on Windows) is dropped instead of breaking line 1.
ENCODING = "utf-8-sig"

try:
    import yaml as _pyyaml  # PyYAML, optional
    PARSE_ERRORS = (YamlError, UnicodeDecodeError, _pyyaml.YAMLError)
except ImportError:
    _pyyaml = None
    PARSE_ERRORS = (YamlError, UnicodeDecodeError)
# PARSE_ERRORS: what a script's entry point reports as "cannot read" (exit code 2) instead of a traceback.


def read_text(path):
    return pathlib.Path(path).read_text(encoding=ENCODING)


def load_yaml(path):
    return loads_yaml(read_text(path))


def loads_yaml(text):
    text = text.lstrip("﻿")  # a BOM kept by a caller that read the file as plain utf-8
    if _pyyaml is None:
        return parse_yaml(text)
    return _pyyaml.safe_load(text)


_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_\-]*)\s*:(?:\s+(.*))?$")
_INT_RE = re.compile(r"^[-+]?[0-9]+$")
_FLOAT_RE = re.compile(r"^[-+]?(?:[0-9]+\.[0-9]*|\.[0-9]+)(?:[eE][-+]?[0-9]+)?$")
_ESCAPE_RE = re.compile(r"\\(.)", re.DOTALL)
_BLOCK_HEADER_RE = re.compile(r"^([|>])([+-]?)$")
_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\", "/": "/", "0": "\0"}
_NULLS = frozenset(("null", "Null", "NULL", "~"))
_TRUES = frozenset(("true", "True", "TRUE"))
_FALSES = frozenset(("false", "False", "FALSE"))


def _strip_comment(line):
    kept, quote, pos, length = [], None, 0, len(line)
    while pos < length:
        char = line[pos]
        if quote:
            kept.append(char)
            if quote == "'" and char == "'":
                if pos + 1 < length and line[pos + 1] == "'":
                    kept.append("'")
                    pos += 2
                    continue
                quote = None
            elif quote == '"' and char == "\\" and pos + 1 < length:
                kept.append(line[pos + 1])
                pos += 2
                continue
            elif quote == '"' and char == '"':
                quote = None
        else:
            previous = line[pos - 1] if pos else " "
            if char in "'\"" and previous in " \t[{,:-":
                quote = char
                kept.append(char)
            elif char == "#" and previous in " \t":
                break
            else:
                kept.append(char)
        pos += 1
    return "".join(kept).rstrip()


def _scalar(token, line_no):
    text = token.strip()
    if text == "":
        return None
    if text[0] == '"':
        if len(text) < 2 or text[-1] != '"':
            raise YamlError(f"line {line_no}: unterminated double-quoted string")
        return _ESCAPE_RE.sub(lambda match: _ESCAPES.get(match.group(1), match.group(1)), text[1:-1])
    if text[0] == "'":
        if len(text) < 2 or text[-1] != "'":
            raise YamlError(f"line {line_no}: unterminated single-quoted string")
        return text[1:-1].replace("''", "'")
    if text in _NULLS:
        return None
    if text in _TRUES:
        return True
    if text in _FALSES:
        return False
    if _INT_RE.match(text):
        return int(text)
    if _FLOAT_RE.match(text):
        return float(text)
    if text[0] in "&*!%@`|>":
        raise YamlError(f"line {line_no}: unsupported YAML syntax {text[:30]!r} (install PyYAML or simplify)")
    return text


def _flow(text, line_no):
    pos, length = 0, len(text)

    def skip_blanks():
        nonlocal pos
        while pos < length and text[pos] in " \t":
            pos += 1

    def quoted():
        nonlocal pos
        quote, start = text[pos], pos
        pos += 1
        while pos < length:
            if quote == '"' and text[pos] == "\\":
                pos += 2
                continue
            if text[pos] == quote:
                if quote == "'" and pos + 1 < length and text[pos + 1] == "'":
                    pos += 2
                    continue
                pos += 1
                return _scalar(text[start:pos], line_no)
            pos += 1
        raise YamlError(f"line {line_no}: unterminated string in flow collection")

    def plain(stops):
        nonlocal pos
        start = pos
        while pos < length and text[pos] not in stops:
            pos += 1
        return _scalar(text[start:pos], line_no)

    def at(char):
        return pos < length and text[pos] == char

    def expect_more(closer):
        nonlocal pos
        skip_blanks()
        if at(","):
            pos += 1
            return True
        if at(closer):
            pos += 1
            return False
        raise YamlError(f"line {line_no}: expected ',' or '{closer}' in flow collection")

    def flow_list():
        nonlocal pos
        pos += 1  # past "["
        items = []
        skip_blanks()
        if at("]"):
            pos += 1
            return items
        while True:
            items.append(value())
            if not expect_more("]"):
                return items

    def flow_map():
        nonlocal pos
        pos += 1  # past "{"
        mapping = {}
        skip_blanks()
        if at("}"):
            pos += 1
            return mapping
        while True:
            skip_blanks()
            if pos >= length:
                raise YamlError(f"line {line_no}: unexpected end of flow mapping")
            key = quoted() if text[pos] in "'\"" else plain(":,}")
            skip_blanks()
            if not at(":"):
                raise YamlError(f"line {line_no}: expected ':' in flow mapping")
            pos += 1
            mapping[key] = value()
            if not expect_more("}"):
                return mapping

    def value():
        skip_blanks()
        if pos >= length:
            raise YamlError(f"line {line_no}: unexpected end of flow collection")
        char = text[pos]
        if char == "[":
            return flow_list()
        if char == "{":
            return flow_map()
        if char in "'\"":
            return quoted()
        return plain(",]}")

    result = value()
    skip_blanks()
    if pos != length:
        raise YamlError(f"line {line_no}: unexpected text after flow collection")
    return result


class _Reader:
    def __init__(self, text):
        self.lines = text.splitlines()
        self.index = 0
        self._stripped = {}  # line index -> text without its comment; peek() asks for the same line many times

    def peek(self):
        """Next meaningful line as (line number, indent, stripped text), skipping blanks and comments."""
        while self.index < len(self.lines):
            raw = self.lines[self.index]
            stripped = self._stripped.get(self.index)
            if stripped is None:
                stripped = self._stripped[self.index] = _strip_comment(raw).strip()
            if stripped == "" or (stripped in ("---", "...") and not raw[:1].isspace()):
                self.index += 1
                continue
            lead = raw[: len(raw) - len(raw.lstrip(" \t"))]
            if "\t" in lead:
                raise YamlError(f"line {self.index + 1}: tabs are not allowed for indentation")
            return self.index + 1, len(lead), stripped
        return None


def _is_item(text):
    return text == "-" or text.startswith("- ")


def _block(reader, indent):
    return _seq(reader, indent) if _is_item(reader.peek()[2]) else _map(reader, indent)


def _map(reader, indent, first=None):
    result = {}
    if first is not None:
        key, rest, line_no = first
        result[key] = _value(reader, rest, indent, line_no)
    while True:
        upcoming = reader.peek()
        if upcoming is None:
            break
        line_no, line_indent, text = upcoming
        if line_indent < indent:
            break
        if line_indent > indent:
            raise YamlError(f"line {line_no}: unexpected indentation")
        if _is_item(text):
            raise YamlError(f"line {line_no}: list item where a 'key: value' was expected")
        match = _KEY_RE.match(text)
        if not match:
            raise YamlError(f"line {line_no}: expected 'key: value'")
        key, rest = match.group(1), match.group(2) or ""
        if key in result:
            raise YamlError(f"line {line_no}: duplicate key {key!r}")
        reader.index += 1
        result[key] = _value(reader, rest, indent, line_no)
    return result


def _seq(reader, indent):
    items = []
    while True:
        upcoming = reader.peek()
        if upcoming is None:
            break
        line_no, line_indent, text = upcoming
        if line_indent < indent or (line_indent == indent and not _is_item(text)):
            break
        if line_indent > indent:
            raise YamlError(f"line {line_no}: unexpected indentation")
        reader.index += 1
        after_dash = text[1:]
        body = after_dash.strip()
        key_column = line_indent + 1 + (len(after_dash) - len(after_dash.lstrip()))
        match = _KEY_RE.match(body) if body and body[0] not in "'\"[{" else None
        if body == "":
            items.append(_value(reader, "", indent, line_no))
        elif match:
            items.append(_map(reader, key_column, first=(match.group(1), match.group(2) or "", line_no)))
        else:
            items.append(_value(reader, body, indent, line_no))
    return items


def _value(reader, rest, indent, line_no):
    if rest == "":
        upcoming = reader.peek()
        if upcoming is None:
            return None
        _, line_indent, text = upcoming
        if line_indent > indent:
            return _block(reader, line_indent)
        if line_indent == indent and _is_item(text):
            return _seq(reader, indent)
        return None
    if rest[0] in "|>":
        return _block_scalar(reader, rest, indent, line_no)
    if rest[0] in "[{":
        return _flow(rest, line_no)
    return _scalar(rest, line_no)


def _fold(lines):
    """Join the lines of a > block: lines of a paragraph with a space, a blank line as a newline."""
    parts, previous_blank = [], True
    for line in lines:
        if line == "":
            parts.append("\n")
            previous_blank = True
        else:
            parts.append(line if previous_blank else " " + line)
            previous_blank = False
    return "".join(parts)


def _block_scalar(reader, header, indent, line_no):
    match = _BLOCK_HEADER_RE.match(header.strip())
    if not match:
        raise YamlError(f"line {line_no}: unsupported block scalar header {header!r}")
    style, chomp = match.groups()
    lines, content_indent = [], None
    while reader.index < len(reader.lines):
        raw = reader.lines[reader.index]
        if raw.strip() == "":
            lines.append("")
            reader.index += 1
            continue
        line_indent = len(raw) - len(raw.lstrip(" "))
        if line_indent <= indent or (content_indent is not None and line_indent < content_indent):
            break
        if content_indent is None:
            content_indent = line_indent
        lines.append(raw[content_indent:].rstrip())
        reader.index += 1
    while lines and lines[-1] == "":
        lines.pop()
    text = "\n".join(lines) if style == "|" else _fold(lines)
    return text if chomp == "-" else text + "\n"


def parse_yaml(text):
    reader = _Reader(text)
    first = reader.peek()
    if first is None:
        return None
    result = _block(reader, first[1])
    leftover = reader.peek()
    if leftover is not None:
        raise YamlError(f"line {leftover[0]}: unexpected content")
    return result


# ── JSON Schema (the keywords used by work-breakdown.schema.json) ────────────────────────────

def load_schema(path=SCHEMA_PATH):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


_TYPE_CHECKS = {
    "null": lambda value: value is None,
    "string": lambda value: isinstance(value, str),
    "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
    "number": _is_number,
    "array": lambda value: isinstance(value, list),
    "object": lambda value: isinstance(value, dict),
    "boolean": lambda value: isinstance(value, bool),
}


def validate_schema(data, schema=None):
    root = schema or load_schema()

    def resolve(ref):
        node = root
        for part in ref[2:].split("/"):
            node = node[part]
        return node

    def check(value, rule, path):
        errors = []
        if "$ref" in rule:
            errors += check(value, resolve(rule["$ref"]), path)
        if "type" in rule:
            types = rule["type"] if isinstance(rule["type"], list) else [rule["type"]]
            if not any(_TYPE_CHECKS[type_name](value) for type_name in types):
                return [*errors, f"{path}: expected {' or '.join(types)}, got {type(value).__name__}"]
        if "enum" in rule and value not in rule["enum"]:
            errors.append(f"{path}: {value!r} is not one of {rule['enum']}")
        if "const" in rule and value != rule["const"]:
            errors.append(f"{path}: {value!r} must be {rule['const']!r}")
        if isinstance(value, str):
            if "pattern" in rule and not re.search(rule["pattern"], value):
                errors.append(f"{path}: {value!r} does not match {rule['pattern']}")
            if "minLength" in rule and len(value) < rule["minLength"]:
                errors.append(f"{path}: must not be empty")
        if _is_number(value) and "minimum" in rule and value < rule["minimum"]:
            errors.append(f"{path}: must be at least {rule['minimum']}")
        if isinstance(value, list):
            if "minItems" in rule and len(value) < rule["minItems"]:
                errors.append(f"{path}: needs at least {rule['minItems']} item(s)")
            if rule.get("uniqueItems"):
                distinct = {json.dumps(element, sort_keys=True, default=str) for element in value}
                if len(distinct) != len(value):
                    errors.append(f"{path}: has duplicate entries")
            if "items" in rule:
                for index, element in enumerate(value):
                    errors += check(element, rule["items"], f"{path}[{index}]")
        if isinstance(value, dict):
            errors += [f"{path}: missing '{key}'" for key in rule.get("required", []) if key not in value]
            properties = rule.get("properties", {})
            for key, element in value.items():
                if key in properties:
                    errors += check(element, properties[key], f"{path}.{key}")
                elif rule.get("additionalProperties") is False:
                    errors.append(f"{path}: unexpected key '{key}'")
        for sub_rule in rule.get("allOf", []):
            errors += check(value, sub_rule, path)
        if "if" in rule and "then" in rule and not check(value, rule["if"], path):
            errors += check(value, rule["then"], path)
        if "not" in rule and not check(value, rule["not"], path):
            errors.append(f"{path}: value is not allowed here")
        return errors

    return check(data, root, "$")


# ── Planning files ───────────────────────────────────────────────────────────────────────────

PLANNING_ID = re.compile(r"^(SRC|OBJ|CAP|FR|NFR|BR|CON|MS|DEC|ASM|RSK|DEP|Q|AQ)-[0-9]+$")
_SEPARATOR = re.compile(r"^:?-{3,}:?$")
_EMPHASIS = re.compile(r"[*`]")
_PRIORITY = re.compile(r"\b(Must|Should|Could|Won't|Wont)\b", re.IGNORECASE)
_INACTIVE_STATUS = re.compile(r"(dropped|deferred)", re.IGNORECASE)


def _cells(line):
    text = line.strip().removeprefix("|").removesuffix("|")
    return [cell.strip() for cell in text.split("|")]


def _clean(cell):
    return _EMPHASIS.sub("", cell).strip()


def _is_table_line(line):
    return line.strip().startswith("|")


def _is_separator(cells):
    return all(_SEPARATOR.match(cell) for cell in cells if cell)


def read_planning(planning_dir):
    """Return ({id: {"file": name, "row": {header: cell}}}, [(duplicate id, file)])."""
    entries, duplicates = {}, []
    folder = pathlib.Path(planning_dir)
    if not folder.is_dir():
        return entries, duplicates
    for md_file in sorted(folder.glob("*.md")):
        if md_file.name.endswith(".review.md"):
            continue
        lines = read_text(md_file).splitlines()
        in_fence, headers = False, None
        for line_index, line in enumerate(lines):
            if line.strip().startswith("```"):
                in_fence, headers = not in_fence, None
                continue
            if in_fence or not _is_table_line(line):
                headers = None
                continue
            cells = _cells(line)
            if headers is None:
                next_line = lines[line_index + 1] if line_index + 1 < len(lines) else ""
                next_cells = _cells(next_line) if _is_table_line(next_line) else []
                if next_cells and _is_separator(next_cells):
                    headers = [_clean(cell).lower() for cell in cells]
                continue
            if _is_separator(cells):
                continue
            planning_id = _clean(cells[0])
            if not PLANNING_ID.match(planning_id):
                continue
            if planning_id in entries:
                duplicates.append((planning_id, md_file.name))
            else:
                row = {header: (cells[column] if column < len(cells) else "") for column, header in enumerate(headers)}
                entries[planning_id] = {"file": md_file.name, "row": row}
    return entries, duplicates


def priority_of(entry):
    match = _PRIORITY.search(entry["row"].get("priority", ""))
    return match.group(1).capitalize().replace("Wont", "Won't") if match else None


def status_of(entry):
    return entry["row"].get("status", "").strip()


def is_inactive(entry):
    """Dropped, deferred and Won't entries need no coverage."""
    return bool(_INACTIVE_STATUS.match(status_of(entry))) or priority_of(entry) == "Won't"


_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_LATER = re.compile(r"\bLater\b")
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def later_section(planning_dir):
    """Return the body of the prototype plan's Later section (heading excluded), or None when there is none."""
    path = pathlib.Path(planning_dir) / PROTOTYPE_PLAN
    if not path.is_file():
        return None
    body, level = None, None
    for line in read_text(path).splitlines():
        heading = _HEADING.match(line)
        if body is None:
            if heading and _LATER.search(heading.group(2)):
                body, level = [], len(heading.group(1))
            continue
        if heading and len(heading.group(1)) <= level:
            break
        body.append(line)
    if body is None:
        return None
    return _HTML_COMMENT.sub("", "\n".join(body)).strip()


# ── Work breakdown ───────────────────────────────────────────────────────────────────────────

def breakdown_of(data):
    """The work_breakdown mapping of a parsed file, or {} when the file has none (M1 reports why)."""
    breakdown = data.get("work_breakdown", {}) if isinstance(data, dict) else {}
    return breakdown if isinstance(breakdown, dict) else {}


def items_of(breakdown):
    """The items of a work breakdown that are mappings; anything else is left to the schema check."""
    items = breakdown.get("items") or []
    return [item for item in items if isinstance(item, dict)] if isinstance(items, list) else []


# ── Misc ─────────────────────────────────────────────────────────────────────────────────────

_MILESTONE = re.compile(r"^MS-([0-9]+)$")
_WHITESPACE = re.compile(r"\s+")
UNRANKED = 10 ** 6  # sorts after any real milestone number or rank


def file_sha256(path):
    # Line endings are normalised, so a git checkout with CRLF and one with LF give the same hash
    return hashlib.sha256(pathlib.Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def version_text(version):
    return str(version) if version is not None else "?"


def milestone_index(value):
    """The n of 'MS-n', or a large number for anything else, so malformed milestones sort last and never crash."""
    match = _MILESTONE.match(str(value if value is not None else ""))
    return int(match.group(1)) if match else UNRANKED


def milestone_number(item):
    return milestone_index(item.get("milestone"))


def one_line(value):
    """Text for a single line of Markdown: newlines and runs of whitespace collapsed, so an item's text can
    neither close a code fence nor start a new line in the review view."""
    return _WHITESPACE.sub(" ", str(value if value is not None else "")).strip()
