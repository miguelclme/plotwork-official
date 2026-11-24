#!/usr/bin/env python3
"""Mechanical checks M1–M17 for a work-breakdown.yaml (Plotwork planning standard).

Usage:
    python validate_breakdown.py docs/planning/work-breakdown.yaml [--planning-dir docs/planning]
                                 [--max-features-per-milestone N] [--review PATH | --no-review-check]

Prints the validation report (references/validation-checklists.md format).
Exit code: 0 = no FAIL, 1 = at least one FAIL, 2 = the file could not be read.
M17 runs only for a prototype (kind: prototype).
The review checks R1–R14 need judgement and are done by the independent reviewer agent, not by this script.
"""
import argparse
import pathlib
import re
import sys

sys.dont_write_bytecode = True  # keep the plugin folder free of __pycache__
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import wbtools

CHECK_NAMES = {
    "M1": "Schema", "M2": "Unique IDs", "M3": "ID prefix", "M4": "Parents", "M5": "Dependencies",
    "M6": "References resolve", "M7": "Must coverage", "M8": "Should and Could coverage",
    "M9": "Open questions are current", "M10": "Size signals", "M11": "Milestone load",
    "M12": "ADO IDs", "M13": "Review view current", "M14": "Copied NFR text", "M15": "Terminology",
    "M16": "Epics mirror milestones", "M17": "Prototype shape",
}
DELIVERY_TERMS = re.compile(r"\b(User Stor(?:y|ies)|Product Backlog Items?|PBIs?|Requirements?|Issues?)\b")
STAMP = re.compile(r"generated-from:\s*(\S+)\s+version=(\S+)\s+sha256=([0-9a-f]{64})")
CLOSED_QUESTION = re.compile(r"(answered|closed|resolved)", re.IGNORECASE)

MAX_SCHEMA_ERRORS = 15  # listed in the report; the rest are counted
MAX_FEATURES_PER_EPIC = 10
MAX_ACCEPTANCE_CRITERIA = 8
MIN_COPIED_STATEMENT = 25  # characters; a shorter NFR statement is too generic to call a copy

_NON_ALPHANUMERIC = re.compile(r"[^a-z0-9 ]")
_WHITESPACE = re.compile(r"\s+")


def _norm(text):
    return _WHITESPACE.sub(" ", _NON_ALPHANUMERIC.sub(" ", str(text).lower())).strip()


def _text_of(item):
    parts = [item.get("title", ""), item.get("description", ""), item.get("outcome", "")]
    parts += [str(criterion) for criterion in item.get("acceptance_criteria", []) or []]
    return " ".join(str(part) for part in parts if part)


def _ids(item, field):
    return list(item.get(field, []) or [])


def _failures(details):
    return ("FAIL" if details else "PASS"), details


def _warnings(details):
    return ("WARN" if details else "PASS"), details


class _Breakdown:
    """What the checks read: the work_breakdown mapping, its items grouped a few ways, and the planning IDs."""

    def __init__(self, data, planning_dir):
        self.meta = wbtools.breakdown_of(data)
        self.items = wbtools.items_of(self.meta)
        self.process = self.meta.get("process")
        self.basic = self.process == "Basic"
        self.by_id = {}
        for item in self.items:
            self.by_id.setdefault(item.get("draft_id"), item)
        self.epics = [item for item in self.items if item.get("type") == "Epic"]
        self.features = [item for item in self.items if item.get("type") == "Feature"]
        self.delivery = self.epics if self.basic else self.features  # the items that carry Feature-level content
        self.features_by_parent = {}
        for feature in self.features:
            self.features_by_parent.setdefault(feature.get("parent"), []).append(feature)
        self.planning_dir = planning_dir
        self.planning, self.planning_duplicates = wbtools.read_planning(planning_dir)

    def children(self, epic):
        return self.features_by_parent.get(epic.get("draft_id"), [])


# ── Checks: each returns (status, [details]) ─────────────────────────────────────────────────

def check_schema(data):
    """M1"""
    errors = wbtools.validate_schema(data)
    shown = errors[:MAX_SCHEMA_ERRORS]
    if len(errors) > MAX_SCHEMA_ERRORS:
        shown.append(f"... and {len(errors) - MAX_SCHEMA_ERRORS} more")
    return ("FAIL" if errors else "PASS"), shown


def check_unique_ids(breakdown):
    """M2"""
    seen, repeats = set(), []
    for item in breakdown.items:
        draft_id = item.get("draft_id")
        if draft_id in seen:
            repeats.append(f"{draft_id} appears more than once")
        seen.add(draft_id)
    return _failures(repeats)


def check_id_prefix(breakdown):
    """M3"""
    key = breakdown.meta.get("key", "")
    return _failures([f"{item.get('draft_id')} does not start with '{key}-'" for item in breakdown.items
                      if not str(item.get("draft_id", "")).startswith(f"{key}-")])


def check_parents(breakdown):
    """M4"""
    problems = []
    for item in breakdown.items:
        parent = item.get("parent")
        if item.get("type") == "Feature":
            target = breakdown.by_id.get(parent)
            if target is None:
                problems.append(f"{item.get('draft_id')}: parent {parent} is not in the file")
            elif target.get("type") != "Epic":
                problems.append(f"{item.get('draft_id')}: parent {parent} is not an Epic")
        elif parent is not None:
            problems.append(f"{item.get('draft_id')}: an Epic must not have a parent")
    return _failures(problems)


def _find_cycles(graph):
    """Depth-first search over {node: [nodes it depends on]}; each cycle as 'A → B → A'."""
    state, cycles = {}, []

    def visit(node, trail):
        state[node] = "open"
        for target in graph.get(node, []):
            if state.get(target) == "open":
                cycles.append(" → ".join([*trail[trail.index(target):], target]) if target in trail
                              else f"{node} → {target}")
            elif target not in state:
                visit(target, [*trail, target])
        state[node] = "done"

    for node in graph:
        if node not in state:
            visit(node, [node])
    return cycles


def check_dependencies(breakdown):
    """M5"""
    problems, graph = [], {}
    for item in breakdown.items:
        draft_id = item.get("draft_id")
        for dependency in _ids(item, "depends_on"):
            if dependency == draft_id:
                problems.append(f"{draft_id} depends on itself")
            elif str(dependency).startswith("DEP-"):
                if breakdown.planning and dependency not in breakdown.planning:
                    problems.append(f"{draft_id}: {dependency} is not in the planning files")
            elif dependency not in breakdown.by_id:
                problems.append(f"{draft_id}: depends on {dependency}, which is not in the file")
            else:
                graph.setdefault(draft_id, []).append(dependency)
    problems += [f"cycle: {cycle}" for cycle in _find_cycles(graph)]
    return _failures(problems)


def check_references(breakdown):
    """M6"""
    planning = breakdown.planning
    if not planning:
        return "SKIP", [f"no planning tables found in {breakdown.planning_dir}"]
    missing = [f"global_constraints: {ref}" for ref in _ids(breakdown.meta, "global_constraints")
               if ref not in planning]
    for item in breakdown.items:
        refs = _ids(item, "traces_to") + _ids(item, "constraints") + _ids(item, "open_questions")
        if item.get("milestone"):
            refs.append(item["milestone"])
        missing += [f"{item.get('draft_id')}: {ref}" for ref in refs if ref not in planning]
    missing += [f"{planning_id} is defined twice (again in {file_name})"
                for planning_id, file_name in breakdown.planning_duplicates]
    return _failures(missing)


def check_coverage(breakdown):
    """M7 and M8: [(status, details) for Must, (status, details) for Should and Could]"""
    if not breakdown.planning:
        skipped = ("SKIP", ["no planning files, so coverage cannot be computed"])
        return skipped, skipped
    traced, constrained = set(), set(_ids(breakdown.meta, "global_constraints"))
    for item in breakdown.items:
        traced.update(_ids(item, "traces_to"))
        constrained.update(_ids(item, "constraints"))
        scope = item.get("scope") if isinstance(item.get("scope"), dict) else {}
        traced.update(ref for ref in scope.get("in", []) or [] if isinstance(ref, str) and ref.startswith("CAP-"))
    must_gaps, other_gaps = [], []
    for planning_id, entry in breakdown.planning.items():
        prefix = planning_id.split("-")[0]
        if prefix not in ("CAP", "FR", "NFR") or wbtools.is_inactive(entry):
            continue
        if planning_id in traced or (prefix == "NFR" and planning_id in constrained):
            continue
        priority = wbtools.priority_of(entry)
        if prefix == "CAP" or priority == "Must":
            must_gaps.append(f"{planning_id} ({priority or 'in scope'}) is not covered by any item")
        elif priority in ("Should", "Could"):
            other_gaps.append(f"{planning_id} ({priority}) is not covered by any item")
        else:
            other_gaps.append(f"{planning_id} has no priority, and nothing covers it")
    return _failures(must_gaps), _warnings(other_gaps)


def check_open_questions(breakdown):
    """M9"""
    if not breakdown.planning:
        return "SKIP", ["no planning files"]
    stale = []
    for item in breakdown.items:
        for question in _ids(item, "open_questions"):
            entry = breakdown.planning.get(question)
            if entry and CLOSED_QUESTION.match(wbtools.status_of(entry)):
                stale.append(f"{item.get('draft_id')}: {question} is {wbtools.status_of(entry)!r}; update the item")
    return _warnings(stale)


def check_size(breakdown):
    """M10"""
    signals = []
    if not breakdown.basic:
        for epic in breakdown.epics:
            feature_count = len(breakdown.children(epic))
            if feature_count == 0 and epic.get("readiness") != "blocked":
                signals.append(f"{epic.get('draft_id')} has no Features")
            elif feature_count == 1:
                signals.append(f"{epic.get('draft_id')} has a single Feature (combine or justify)")
            elif feature_count > MAX_FEATURES_PER_EPIC:
                signals.append(f"{epic.get('draft_id')} has {feature_count} Features (consider splitting)")
    for item in breakdown.delivery:
        criteria_count = len(item.get("acceptance_criteria", []) or [])
        if criteria_count > MAX_ACCEPTANCE_CRITERIA:
            signals.append(f"{item.get('draft_id')} has {criteria_count} acceptance criteria (consider splitting)")
    return _warnings(signals)


def check_milestone_load(breakdown, max_per_milestone):
    """M11"""
    if not max_per_milestone:
        return "SKIP", ["no capacity given (--max-features-per-milestone)"]
    load = {}
    for item in breakdown.delivery:
        load.setdefault(item.get("milestone") or "no milestone", []).append(item.get("draft_id"))
    return _warnings([f"{milestone}: {len(draft_ids)} items (capacity {max_per_milestone})"
                      for milestone, draft_ids in sorted(load.items()) if len(draft_ids) > max_per_milestone])


def check_ado_ids(breakdown):
    """M12: all empty (not pushed yet), or all filled on an approved breakdown (pushed by /plotwork:push).
    Some filled means a push stopped halfway, or a pushed prototype has grown: run the push again."""
    items = breakdown.items
    pushed = [item for item in items if item.get("ado_id") is not None]
    if not pushed:
        return "PASS", []
    if len(pushed) < len(items):
        waiting = ", ".join(item.get("draft_id") for item in items if item.get("ado_id") is None)
        return "WARN", [(f"{len(pushed)} of {len(items)} items have an ado_id; {waiting} not yet in Azure DevOps. "
                         "Run /plotwork:push again to create the rest")]
    status = breakdown.meta.get("status")
    if status != "approved":
        return "FAIL", [(f"every item has an ado_id, but status is {status!r}: only an approved breakdown is "
                         "pushed, and a pushed one is changed in Azure DevOps, not here")]
    return "PASS", ["every item is in Azure DevOps"]


def check_review_view(yaml_path, review_path):
    """M13"""
    review = pathlib.Path(review_path) if review_path else yaml_path.with_name(yaml_path.stem + ".review.md")
    if not review.exists():
        return "WARN", [f"{review.name} has not been generated yet (run render_review.py)"]
    stamp = STAMP.search(wbtools.read_text(review))
    if not stamp:
        return "WARN", [f"{review.name} has no generation stamp (rendered manually?)"]
    if stamp.group(3) != wbtools.file_sha256(yaml_path):
        return "FAIL", [f"{review.name} was generated from an older version of the YAML; re-render it"]
    return "PASS", []


def check_copied_nfr_text(breakdown, item_texts):
    """M14"""
    copied, normalized = [], None
    for planning_id, entry in breakdown.planning.items():
        if not planning_id.startswith("NFR-"):
            continue
        statement = _norm(entry["row"].get("statement", ""))
        if len(statement) < MIN_COPIED_STATEMENT:
            continue
        if normalized is None:
            normalized = [_norm(text) for text in item_texts]
        copied += [f"{item.get('draft_id')} repeats the text of {planning_id}; reference the ID instead"
                   for item, text in zip(breakdown.items, normalized) if statement in text]
    return _warnings(copied)


def check_terminology(breakdown, item_texts):
    """M15"""
    mentions = []
    for item, text in zip(breakdown.items, item_texts):
        found = sorted(set(DELIVERY_TERMS.findall(text)))
        if found:
            mentions.append(f"{item.get('draft_id')} mentions {', '.join(found)}")
    return _warnings(mentions)


def check_epics_mirror_milestones(breakdown):
    """M16 (a phase turned into an Epic, §8.5)"""
    problems, milestones_by_epic = [], {}
    for epic in breakdown.epics:
        own = [epic] if breakdown.basic else breakdown.children(epic)
        milestones_by_epic[epic.get("draft_id")] = {item.get("milestone") for item in own if item.get("milestone")}
        if not breakdown.basic and own and all(feature.get("nature") == "verification" for feature in own):
            problems.append(f"{epic.get('draft_id')} holds only verification Features; "
                            "put them under the Epic they verify")
    single = [next(iter(milestones)) for milestones in milestones_by_epic.values() if len(milestones) == 1]
    if len(breakdown.epics) >= 2 and len(single) == len(breakdown.epics) and len(set(single)) == len(single):
        pairs = ", ".join(f"{epic_id} → {next(iter(milestones))}" for epic_id, milestones in milestones_by_epic.items())
        problems.append(f"each Epic targets one milestone of its own ({pairs}); check that no phase became an Epic, "
                        "or note in the assessment that the phase coincides with exactly one capability area")
    return _warnings(problems)


def check_prototype_shape(breakdown):
    """M17 (only for kind: prototype): one milestone and a Later list. The size is not limited."""
    fails = []
    used = sorted({item.get("milestone") for item in breakdown.delivery if item.get("milestone")})
    if len(used) > 1:
        fails.append(f"a prototype has one milestone, but the items target {', '.join(used)}")
    if wbtools.later_section(breakdown.planning_dir) is None:
        fails.append(f"{wbtools.PROTOTYPE_PLAN} has no Later section listing the deferred capabilities")
    return ("FAIL" if fails else "PASS"), fails


def _count(items, field, value):
    return sum(1 for item in items if item.get(field) == value)


def run_checks(yaml_path, planning_dir=None, review_path=None, max_per_milestone=None, check_review=True):
    """Return (data, results, counts). results: list of (code, status, [details])."""
    yaml_path = pathlib.Path(yaml_path)
    planning_dir = pathlib.Path(planning_dir) if planning_dir else yaml_path.parent
    data = wbtools.load_yaml(yaml_path)
    breakdown = _Breakdown(data, planning_dir)
    item_texts = [_text_of(item) for item in breakdown.items]  # read by M14 and M15
    must_coverage, other_coverage = check_coverage(breakdown)
    if check_review:
        review_view = check_review_view(yaml_path, review_path)
    else:
        review_view = ("SKIP", ["checked when the review view is validated, not while it is being generated"])

    results = [
        ("M1", *check_schema(data)),
        ("M2", *check_unique_ids(breakdown)),
        ("M3", *check_id_prefix(breakdown)),
        ("M4", *check_parents(breakdown)),
        ("M5", *check_dependencies(breakdown)),
        ("M6", *check_references(breakdown)),
        ("M7", *must_coverage),
        ("M8", *other_coverage),
        ("M9", *check_open_questions(breakdown)),
        ("M10", *check_size(breakdown)),
        ("M11", *check_milestone_load(breakdown, max_per_milestone)),
        ("M12", *check_ado_ids(breakdown)),
        ("M13", *review_view),
        ("M14", *check_copied_nfr_text(breakdown, item_texts)),
        ("M15", *check_terminology(breakdown, item_texts)),
        ("M16", *check_epics_mirror_milestones(breakdown)),
    ]
    if breakdown.meta.get("kind") == "prototype":
        results.append(("M17", *check_prototype_shape(breakdown)))

    items = breakdown.items
    counts = {
        "epics": len(breakdown.epics),
        "features": len(breakdown.features),
        "ready": _count(items, "readiness", "ready"),
        "needs-elaboration": _count(items, "readiness", "needs-elaboration"),
        "blocked": _count(items, "readiness", "blocked"),
        "low": _count(items, "confidence", "low"),
    }
    return data, results, counts


def format_report(data, results, counts, runner="validate_breakdown.py"):
    meta = wbtools.breakdown_of(data)
    lines = [(f"Validation — {meta.get('key', '?')} work breakdown v{wbtools.version_text(meta.get('version'))} "
              f"(process: {meta.get('process', '?')}) · checks run by {runner}")]
    for code, status, details in results:
        lines.append(f"{status:<5} {code:<4} {CHECK_NAMES[code]}")
        if status != "PASS":
            lines += [f"            - {wbtools.one_line(detail)}" for detail in details]
    lines.append(f"Ready {counts['ready']} · Needs elaboration {counts['needs-elaboration']} · "
                 f"Blocked {counts['blocked']} · Low confidence {counts['low']}")
    statuses = [status for _, status, _ in results]
    tally = " · ".join(f"{status} {statuses.count(status)}" for status in ("FAIL", "WARN", "PASS", "SKIP"))
    lines.append(f"Mechanical result: {tally}. Review checks R1–R14 are done by the independent reviewer.")
    return "\n".join(lines)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Validate a work-breakdown.yaml (checks M1–M17).")
    parser.add_argument("yaml", help="path to work-breakdown.yaml")
    parser.add_argument("--planning-dir", help="folder with the planning .md files (default: the YAML's folder)")
    parser.add_argument("--review",
                        help="path to the review view (default: work-breakdown.review.md next to the YAML)")
    parser.add_argument("--no-review-check", action="store_true", help="skip M13")
    parser.add_argument("--max-features-per-milestone", type=int, help="capacity for M11")
    args = parser.parse_args(argv)
    try:
        data, results, counts = run_checks(args.yaml, args.planning_dir, args.review,
                                           args.max_features_per_milestone, not args.no_review_check)
    except (OSError, *wbtools.PARSE_ERRORS) as exc:
        print(f"ERROR: cannot read {args.yaml}: {exc}")
        return 2
    print(format_report(data, results, counts))
    return 1 if any(status == "FAIL" for _, status, _ in results) else 0


if __name__ == "__main__":
    sys.exit(main())
