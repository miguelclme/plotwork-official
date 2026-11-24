# <Project name> — Work breakdown v<version> (<process>)

<!-- LAYOUT TEMPLATE for the generated review view (§9.8, Q2).
     render_review.py fills it from work-breakdown.yaml. Claude fills it only when the script cannot run,
     and then uses the second banner line instead of the first.
     Order: Feature cards by milestone, then rank. In Basic there are no Features: section 3 shows one card per Epic,
     and section 4 is left out. -->

> Generated from `work-breakdown.yaml` v<version> on <YYYY-MM-DD> by `render_review.py`. **Do not edit**: change the YAML and regenerate.
>
> *(fallback)* Rendered manually by Claude from `work-breakdown.yaml` v<version> on <YYYY-MM-DD>, because the script could not run.

## 1. Summary

| Epics | Features | Ready | Needs elaboration | Blocked | Low confidence |
|---|---|---|---|---|---|
| <n> | <n> | <n> | <n> | <n> | <n> |

- **Process:** <process> · **Status:** <draft | in-review | approved> · **Rigor:** <profile>
- **Global constraints:** <NFR-n, … or "none">
- **Open questions:** <Q-n, AQ-n, … or "none">

## 2. Hierarchy

```text
<KEY>-EP-001 <title>                              <priority> · <readiness>
  <KEY>-FT-001 <title>                            MS-<n> · rank <n> · <priority> · <readiness>
  <KEY>-FT-002 <title>                            MS-<n> · rank <n> · <priority> · <readiness> · depends_on <id>
```

## 3. Feature cards

### <KEY>-FT-001 — <title>

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| <KEY>-EP-001 | MS-<n> | <n> | <priority> | <nature> | <readiness> | <confidence> | <size_hint or —> |

<description>

- **In scope:** <…>
- **Out of scope:** <…>

**Acceptance criteria**

1. <…>

- **Constraints:** <NFR-n …> plus global <NFR-n …>
- **Depends on:** <ids or "none">
- **Traces to:** <ids> · **Sources:** <refs>
- **Open questions:** <ids or "none"> · **Downstream notes:** <notes or "none">

## 4. Epics *(Agile, Scrum, CMMI)*

| Epic | Outcome | Scope in / out | Priority | Features | Milestones | Readiness |
|---|---|---|---|---|---|---|
| <KEY>-EP-001 | <outcome> | <…> | <priority> | <n> | MS-<n>…MS-<n> | <readiness> |

## 5. Traceability coverage

| Planning ID | Priority | Covered by | Status |
|---|---|---|---|
| FR-<n> | <priority> | <KEY>-FT-<nnn> | Covered · **Gap** |

## 6. Constraints and NFR coverage (D11)

| NFR | Priority | Global | Constrains | Implemented or verified by |
|---|---|---|---|---|
| NFR-<n> | <priority> | Yes · No | <item IDs or "—"> | <enabler or verification item IDs, or "—"> |

## 7. Dependencies

| Item | Depends on | Crosses Epics? |
|---|---|---|
| <KEY>-FT-<nnn> | <KEY>-FT-<nnn> · DEP-<n> | Yes · No |

## 8. Open questions and assumptions

| ID | Question or assumption | Severity | Affects |
|---|---|---|---|
| Q-<n> | <…> | Blocking · Material · Minor | <ids> |

## 9. Not ready

| Item | Readiness | Confidence | Held by |
|---|---|---|---|
| <KEY>-FT-<nnn> | needs-elaboration · blocked | <confidence> | Q-<n> |

## 10. Validation report

```text
PASS  <check> (<detail>)
WARN  <check>: <item> (<what to do>)
FAIL  <check>: <item> (<what is wrong>)
Ready <n> · Needs elaboration <n> · Blocked <n>
```
