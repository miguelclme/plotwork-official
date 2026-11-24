#!/usr/bin/env python3
"""Generate work-breakdown.review.md from work-breakdown.yaml (Plotwork planning standard, Q2).

Usage:
    python render_review.py docs/planning/work-breakdown.yaml [--planning-dir docs/planning] [-o OUTPUT]
                            [--max-features-per-milestone N]

The layout follows templates/work-breakdown.review.md. The first line stamps the YAML's version and
SHA-256, so validate_breakdown.py (M13) can tell when the view is stale. Never edit the output by hand.
A prototype (kind: prototype) gets a Prototype banner and its Later list. Items pushed to Azure DevOps show their ID.
Exit code: 0 = written, 2 = the YAML could not be read.
"""
import argparse
import datetime
import pathlib
import sys

sys.dont_write_bytecode = True  # keep the plugin folder free of __pycache__
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import validate_breakdown
import wbtools

EMPTY = "—"
QUESTION_TEXT_COLUMNS = ("question", "assumption", "entry", "statement", "short label")


def cell(value):
    if value is None or value == "" or value == []:
        return EMPTY
    if isinstance(value, list):
        value = ", ".join(str(element) for element in value)
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def listing(values, empty="none"):
    values = [str(value) for value in values or []]
    return ", ".join(values) if values else empty


def ado(item):
    return f"ADO #{item['ado_id']}" if item.get("ado_id") is not None else None


def order_key(item):
    return (wbtools.milestone_number(item), item.get("rank") or wbtools.UNRANKED, str(item.get("draft_id")))


def _scope(item):
    return item.get("scope") if isinstance(item.get("scope"), dict) else {}


def _table_header(*columns):
    return ["| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]


class _View:
    """The parsed breakdown, grouped the way the sections of the review view read it."""

    def __init__(self, yaml_path, data, planning_dir):
        self.yaml_path = yaml_path
        self.planning_dir = planning_dir
        self.planning, _ = wbtools.read_planning(planning_dir)
        self.meta = wbtools.breakdown_of(data)
        self.items = wbtools.items_of(self.meta)
        self.process = self.meta.get("process", "?")
        self.basic = self.process == "Basic"
        self.prototype = self.meta.get("kind") == "prototype"
        self.version = wbtools.version_text(self.meta.get("version"))
        self.global_constraints = self.meta.get("global_constraints", []) or []
        self.epics = sorted((item for item in self.items if item.get("type") == "Epic"), key=order_key)
        self.features = [item for item in self.items if item.get("type") == "Feature"]
        self.by_draft_id = {item.get("draft_id"): item for item in self.items}
        self.features_by_parent = {}
        for feature in self.features:
            self.features_by_parent.setdefault(feature.get("parent"), []).append(feature)
        self.open_questions = sorted({question for item in self.items
                                      for question in item.get("open_questions", []) or []})

    def children(self, epic):
        return self.features_by_parent.get(epic.get("draft_id"), [])

    def cards(self):
        return self.epics if self.basic else sorted(self.features, key=order_key)


# ── Sections: each returns its lines, ending with a blank one ────────────────────────────────

def _banner(view):
    name = view.yaml_path.name
    lines = [
        f"<!-- generated-from: {name} version={view.version} sha256={wbtools.file_sha256(view.yaml_path)} -->",
        f"# {view.meta.get('project', '?')} — Work breakdown v{view.version} ({view.process})",
        "",
        (f"> Generated from `{name}` v{view.version} on {datetime.date.today().isoformat()} by "
         "`render_review.py`. **Do not edit**: change the YAML and regenerate."),
        "",
    ]
    if view.prototype:
        lines += [("> **Prototype.** One milestone, and only what the prototype must prove. The capabilities left "
                   "for later are listed under *Later*; `/plotwork:plan` can grow this into a full plan, keeping "
                   "its IDs."), ""]
    return lines


def _summary(view, counts):
    meta = view.meta
    lines = ["## 1. Summary", ""]
    lines += _table_header("Epics", "Features", "Ready", "Needs elaboration", "Blocked", "Low confidence")
    lines += [
        (f"| {counts['epics']} | {counts['features']} | {counts['ready']} | {counts['needs-elaboration']} "
         f"| {counts['blocked']} | {counts['low']} |"),
        "",
        (f"- **Process:** {view.process} · **Status:** {meta.get('status', '?')} · "
         f"**Rigor:** {meta.get('rigor', '?')}"),
        f"- **Global constraints:** {listing(view.global_constraints)}",
        f"- **Open questions:** {listing(view.open_questions)}",
    ]
    pushed = sum(1 for item in view.items if item.get("ado_id") is not None)
    if pushed:
        lines.append(f"- **In Azure DevOps:** {pushed} of {len(view.items)} items")
    return [*lines, ""]


def _later(view):
    if not view.prototype:
        return []
    later = wbtools.later_section(view.planning_dir)
    return ["## Later — not in this prototype", "",
            later or f"_No Later list was found in `{wbtools.PROTOTYPE_PLAN}`._", ""]


def _tree_line(indent, item, tail):
    label = wbtools.one_line(f"{item.get('draft_id')} {item.get('title')}").ljust(60 - indent)
    return " " * indent + label + "  " + " · ".join(wbtools.one_line(part) for part in tail)


def _dependency_and_ado(item):
    tail = []
    if item.get("depends_on"):
        tail.append("depends_on " + ", ".join(item["depends_on"]))
    if ado(item):
        tail.append(ado(item))
    return tail


def _hierarchy(view):
    lines = ["## 2. Hierarchy", "", "```text"]
    for epic in view.epics:
        tail = [str(epic.get("priority", "")), str(epic.get("readiness", ""))]
        if view.basic:
            tail = [epic.get("milestone", EMPTY), f"rank {epic.get('rank', EMPTY)}", *tail]
            tail += _dependency_and_ado(epic)
        elif ado(epic):
            tail.append(ado(epic))
        lines.append(_tree_line(0, epic, tail))
        for feature in sorted(view.children(epic), key=order_key):
            tail = [feature.get("milestone", EMPTY), f"rank {feature.get('rank', EMPTY)}",
                    feature.get("priority", ""), feature.get("readiness", ""), *_dependency_and_ado(feature)]
            lines.append(_tree_line(2, feature, tail))
    return [*lines, "```", ""]


def _card(view, item):
    lines = [wbtools.one_line(f"### {item.get('draft_id')} — {item.get('title')}"), ""]
    ado_ref = ado(item)
    if ado_ref:
        parent_ref = "" if view.basic else f" · Epic {ado(view.by_draft_id.get(item.get('parent'), {})) or EMPTY}"
        lines += [f"**{ado_ref}**{parent_ref}", ""]
    columns = ["Milestone", "Rank", "Priority", "Nature", "Readiness", "Confidence", "Size"]
    values = [item.get(field) for field in
              ("milestone", "rank", "priority", "nature", "readiness", "confidence", "size_hint")]
    if not view.basic:
        columns, values = ["Epic", *columns], [item.get("parent"), *values]
    lines += _table_header(*columns)
    lines += ["| " + " | ".join(cell(value) for value in values) + " |", ""]
    if view.basic and item.get("outcome"):
        lines += [f"**Outcome:** {str(item['outcome']).strip()}", ""]
    if item.get("description"):
        lines += [str(item["description"]).strip(), ""]
    scope = _scope(item)
    criteria = item.get("acceptance_criteria", []) or []
    own_constraints = item.get("constraints", []) or []
    notes = "; ".join(item.get("downstream_notes", []) or []) or "none"
    lines += [
        f"- **In scope:** {'; '.join(str(entry) for entry in scope.get('in', []) or []) or EMPTY}",
        f"- **Out of scope:** {'; '.join(str(entry) for entry in scope.get('out', []) or []) or EMPTY}",
        "",
        "**Acceptance criteria**",
        "",
        *([f"{number}. {str(criterion).strip()}" for number, criterion in enumerate(criteria, 1)]
          or ["_None yet._"]),
        "",
        (f"- **Constraints:** {listing(own_constraints, 'none of its own')} · "
         f"global: {listing(view.global_constraints)}"),
        f"- **Depends on:** {listing(item.get('depends_on'))}",
        f"- **Traces to:** {listing(item.get('traces_to'))} · **Sources:** {listing(item.get('sources'))}",
        f"- **Open questions:** {listing(item.get('open_questions'))} · **Downstream notes:** {notes}",
        "",
    ]
    lines += _design(item)
    return lines


def _design(item):
    """The Figma screens of an item (the design key), as a short list. Nothing for an item without the key."""
    screens = [wbtools.one_line(screen) for screen in item.get("design") or [] if screen]
    if not screens:
        return []
    return ["**Design**", "", *[f"- {screen}" for screen in screens], ""]


def _cards(view):
    lines = ["## 3. Epic cards" if view.basic else "## 3. Feature cards", ""]
    for item in view.cards():
        lines += _card(view, item)
    return lines


def _epics(view):
    """Only for three-level processes: in Basic, the Epic cards already say all of this."""
    if view.basic:
        return []
    lines = ["## 4. Epics", ""]
    lines += _table_header("Epic", "Outcome", "Scope in / out", "Priority", "Features", "Milestones", "Readiness")
    for epic in view.epics:
        children = view.children(epic)
        milestones = sorted({child.get("milestone") for child in children if child.get("milestone")},
                            key=wbtools.milestone_index)
        scope = _scope(epic)
        lines.append(f"| {epic.get('draft_id')} | {cell(epic.get('outcome'))} | in: {cell(scope.get('in'))} · "
                     f"out: {cell(scope.get('out'))} | {cell(epic.get('priority'))} | {len(children)} "
                     f"| {cell(milestones)} | {cell(epic.get('readiness'))} |")
    lines.append("")
    for epic in view.epics:
        if epic.get("design"):
            lines += [wbtools.one_line(f"**{epic.get('draft_id')}**"), "", *_design(epic)]
    return lines


def _covers(item, planning_id):
    return planning_id in (item.get("traces_to") or []) or planning_id in (_scope(item).get("in") or [])


def _coverage(view):
    lines = ["## 5. Traceability coverage", ""]
    if not view.planning:
        return [*lines, "_No planning tables were found, so coverage could not be computed._", ""]
    lines += _table_header("Planning ID", "Priority", "Covered by", "Status")
    for planning_id, entry in view.planning.items():
        if planning_id.split("-")[0] not in ("CAP", "FR"):
            continue
        covered_by = [item.get("draft_id") for item in view.items if _covers(item, planning_id)]
        status = "n/a" if wbtools.is_inactive(entry) else ("Covered" if covered_by else "**Gap**")
        lines.append(f"| {planning_id} | {cell(wbtools.priority_of(entry))} | {cell(covered_by)} | {status} |")
    return [*lines, ""]


def _nfr_coverage(view):
    planning, items = view.planning, view.items
    lines = ["## 6. Constraints and NFR coverage (D11)", ""]
    nfrs = [planning_id for planning_id in planning if planning_id.startswith("NFR-")]
    referenced = {ref for item in items for ref in (item.get("constraints") or []) + (item.get("traces_to") or [])
                  if str(ref).startswith("NFR-")}
    nfrs += sorted({ref for ref in referenced if ref not in planning}
                   | {ref for ref in view.global_constraints if ref not in planning})
    if not nfrs:
        return [*lines, "_No non-functional requirements._", ""]
    lines += _table_header("NFR", "Priority", "Global", "Constrains", "Implemented or verified by")
    for nfr in nfrs:
        entry = planning.get(nfr)
        constrains = [item.get("draft_id") for item in items if nfr in (item.get("constraints") or [])]
        implemented = [item.get("draft_id") for item in items if nfr in (item.get("traces_to") or [])
                       and item.get("nature") in ("enabler", "verification")]
        lines.append(f"| {nfr} | {cell(wbtools.priority_of(entry) if entry else None)} | "
                     f"{'Yes' if nfr in view.global_constraints else 'No'} | {cell(constrains)} | "
                     f"{cell(implemented)} |")
    return [*lines, ""]


def _epic_of(item):
    return item.get("parent") if item.get("type") == "Feature" else item.get("draft_id")


def _dependencies(view):
    lines = ["## 7. Dependencies", ""]
    dependencies = [(item, target) for item in view.items for target in item.get("depends_on", []) or []]
    if not dependencies:
        return [*lines, "_No dependencies._", ""]
    lines += _table_header("Item", "Depends on", "Crosses Epics?")
    for item, target in dependencies:
        other = view.by_draft_id.get(target)
        if other is None:
            crosses = "n/a"
        elif view.basic:
            crosses = "Yes"
        else:
            crosses = "Yes" if _epic_of(item) != _epic_of(other) else "No"
        lines.append(f"| {item.get('draft_id')} | {target} | {crosses} |")
    return [*lines, ""]


def _entry_text(entry):
    row = entry["row"]
    for column in QUESTION_TEXT_COLUMNS:
        if row.get(column):
            return row[column]
    return EMPTY


def _questions(view):
    lines = ["## 8. Open questions and assumptions", ""]
    rows = []
    for question in view.open_questions:
        entry = view.planning.get(question, {"row": {}})
        affects = [item.get("draft_id") for item in view.items if question in (item.get("open_questions") or [])]
        rows.append((question, _entry_text(entry), entry["row"].get("severity", EMPTY), affects))
    for planning_id, entry in view.planning.items():
        if planning_id.startswith("ASM-") and not wbtools.status_of(entry).lower().startswith(
                ("confirmed", "invalidated")):
            rows.append((planning_id, _entry_text(entry), "Assumption", [entry["row"].get("affects", EMPTY)]))
    if not rows:
        return [*lines, "_None._", ""]
    lines += _table_header("ID", "Question or assumption", "Severity", "Affects")
    lines += [f"| {row_id} | {cell(text)} | {cell(severity)} | {cell(affects)} |"
              for row_id, text, severity, affects in rows]
    return [*lines, ""]


def _not_ready(view):
    lines = ["## 9. Not ready", ""]
    held = [item for item in view.items if item.get("readiness") != "ready" or item.get("confidence") == "low"]
    if not held:
        return [*lines, "_Every item is ready._", ""]
    lines += _table_header("Item", "Readiness", "Confidence", "Held by")
    lines += [f"| {item.get('draft_id')} | {cell(item.get('readiness'))} | {cell(item.get('confidence'))} | "
              f"{cell(item.get('open_questions'))} |" for item in sorted(held, key=order_key)]
    return [*lines, ""]


def render(yaml_path, planning_dir=None, max_per_milestone=None):
    yaml_path = pathlib.Path(yaml_path)
    planning_dir = pathlib.Path(planning_dir) if planning_dir else yaml_path.parent
    data, results, counts = validate_breakdown.run_checks(
        yaml_path, planning_dir, None, max_per_milestone, check_review=False)
    report = validate_breakdown.format_report(data, results, counts, runner="render_review.py")
    view = _View(yaml_path, data, planning_dir)
    lines = [
        *_banner(view),
        *_summary(view, counts),
        *_later(view),
        *_hierarchy(view),
        *_cards(view),
        *_epics(view),
        *_coverage(view),
        *_nfr_coverage(view),
        *_dependencies(view),
        *_questions(view),
        *_not_ready(view),
        "## 10. Validation report", "", "```text", report, "```", "",
    ]
    return "\n".join(lines)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Generate the review view for a work-breakdown.yaml.")
    parser.add_argument("yaml", help="path to work-breakdown.yaml")
    parser.add_argument("--planning-dir", help="folder with the planning .md files (default: the YAML's folder)")
    parser.add_argument("-o", "--output", help="output path (default: work-breakdown.review.md next to the YAML)")
    parser.add_argument("--max-features-per-milestone", type=int, help="capacity for check M11")
    args = parser.parse_args(argv)
    yaml_path = pathlib.Path(args.yaml)
    output = pathlib.Path(args.output) if args.output else yaml_path.with_name(yaml_path.stem + ".review.md")
    try:
        text = render(yaml_path, args.planning_dir, args.max_features_per_milestone)
    except (OSError, *wbtools.PARSE_ERRORS) as exc:
        print(f"ERROR: cannot read {args.yaml}: {exc}")
        return 2
    output.write_text(text, encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
