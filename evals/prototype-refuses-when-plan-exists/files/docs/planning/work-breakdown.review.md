<!-- generated-from: work-breakdown.yaml version=0.1 sha256=259d6a8d79e7961f5bd04ae3c11f28b7272a10375744b9fefb7a31dbbf89a7e2 -->
# Book Club Hub — Work breakdown v0.1 (Scrum)

> Generated from `work-breakdown.yaml` v0.1 on 2026-11-02 by `render_review.py`. **Do not edit**: change the YAML and regenerate.

## 1. Summary

| Epics | Features | Ready | Needs elaboration | Blocked | Low confidence |
|---|---|---|---|---|---|
| 2 | 6 | 8 | 0 | 0 | 0 |

- **Process:** Scrum · **Status:** in-review · **Rigor:** Standard
- **Global constraints:** NFR-1, NFR-2, NFR-3
- **Open questions:** Q-1

## 2. Hierarchy

```text
BCH-EP-001 Run a book club without spreadsheets               Must · ready
  BCH-FT-001 Club setup & membership                          MS-1 · rank 1 · Must · ready
  BCH-FT-002 Meetings                                         MS-1 · rank 2 · Must · ready · depends_on BCH-FT-001
  BCH-FT-003 Choosing the next book                           MS-1 · rank 3 · Must · ready · depends_on BCH-FT-001
  BCH-FT-006 Quality verification before public launch        MS-3 · rank 1 · Must · ready · depends_on BCH-FT-001, BCH-FT-002, BCH-FT-003
BCH-EP-002 Member engagement                                  Should · ready
  BCH-FT-004 Discussion threads per book                      MS-2 · rank 1 · Should · ready · depends_on BCH-FT-003
  BCH-FT-005 Reading progress                                 MS-2 · rank 2 · Should · ready · depends_on BCH-FT-003
```

## 3. Feature cards

### BCH-FT-001 — Club setup & membership

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| BCH-EP-001 | MS-1 | 1 | Must | user-facing | ready | high | — |

Organisers create a club and invite members, who join from an invite link.

- **In scope:** creating a club with a name and a description; sharing an invite link; joining a club from the link
- **Out of scope:** public club discovery (not in SRC-1)

**Acceptance criteria**

1. An organiser can create a club with a name and a description.
2. An organiser can share an invite link for the club.
3. A person with the link can join the club as a member.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3
- **Depends on:** none
- **Traces to:** OBJ-1, CAP-1, FR-1, FR-2 · **Sources:** SRC-1 Phase 1, items 1-2
- **Open questions:** none · **Downstream notes:** none

### BCH-FT-002 — Meetings

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| BCH-EP-001 | MS-1 | 2 | Must | user-facing | ready | high | — |

Organisers schedule meetings, and members see what is coming up.

- **In scope:** scheduling a meeting with a date, a place or an online link, and a book; the list of upcoming meetings
- **Out of scope:** video calls (out of scope in SRC-1)

**Acceptance criteria**

1. An organiser can schedule a meeting with a date, a place or an online link, and the book to discuss.
2. Members see the club's upcoming meetings.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3
- **Depends on:** BCH-FT-001
- **Traces to:** OBJ-1, CAP-2, FR-3 · **Sources:** SRC-1 Phase 1, item 3
- **Open questions:** none · **Downstream notes:** none

### BCH-FT-003 — Choosing the next book

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| BCH-EP-001 | MS-1 | 3 | Must | user-facing | ready | medium | — |

Members propose candidate books and vote; the organiser closes the vote.

- **In scope:** proposing candidate books; one vote per member per round; closing the vote and setting the next book
- **Out of scope:** buying or linking to book shops (out of scope in SRC-1)

**Acceptance criteria**

1. Members can propose candidate books for the next meeting.
2. Each member can vote once per round, and the organiser can close the round.
3. Closing a round sets the winning book for the next meeting, applying the tie rule from Q-1.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3
- **Depends on:** BCH-FT-001
- **Traces to:** OBJ-1, CAP-3, FR-4 · **Sources:** SRC-1 Phase 1, item 4
- **Open questions:** Q-1 · **Downstream notes:** none

### BCH-FT-004 — Discussion threads per book

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| BCH-EP-002 | MS-2 | 1 | Should | user-facing | ready | high | — |

Members discuss each book in its own thread, and the organiser can pin a post.

- **In scope:** a thread for each book the club reads; posting and replying; pinning a post
- **Out of scope:** —

**Acceptance criteria**

1. Each book the club reads has a discussion thread.
2. Members can post and reply in a thread.
3. The organiser can pin a post to the top of a thread.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3
- **Depends on:** BCH-FT-003
- **Traces to:** OBJ-2, CAP-4, FR-5 · **Sources:** SRC-1 Phase 2, item 1
- **Open questions:** none · **Downstream notes:** none

### BCH-FT-005 — Reading progress

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| BCH-EP-002 | MS-2 | 2 | Should | user-facing | ready | high | — |

Members mark chapters as read, and the club sees its overall progress.

- **In scope:** marking chapters of the current book as read; the club's overall progress for the current book
- **Out of scope:** —

**Acceptance criteria**

1. Members can mark chapters of the current book as read.
2. The club sees overall reading progress for the current book.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3
- **Depends on:** BCH-FT-003
- **Traces to:** OBJ-2, CAP-4, FR-6 · **Sources:** SRC-1 Phase 2, item 2
- **Open questions:** none · **Downstream notes:** none

### BCH-FT-006 — Quality verification before public launch

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| BCH-EP-001 | MS-3 | 1 | Must | verification | ready | high | — |

Verify the accessibility and page speed of the core flows before the public launch.

- **In scope:** an accessibility audit of the core flows against WCAG 2.1 AA; page-speed measurement of the core flows on 4G
- **Out of scope:** fixing issues found (handled in the Feature that owns the flow)

**Acceptance criteria**

1. An accessibility audit of the core flows finds no WCAG 2.1 AA failures.
2. Core pages load in under 2 seconds on a 4G connection.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3
- **Depends on:** BCH-FT-001, BCH-FT-002, BCH-FT-003
- **Traces to:** OBJ-3, NFR-2, NFR-3 · **Sources:** SRC-1 Phase 3
- **Open questions:** none · **Downstream notes:** none

## 4. Epics

| Epic | Outcome | Scope in / out | Priority | Features | Milestones | Readiness |
|---|---|---|---|---|---|---|
| BCH-EP-001 | A club can run its whole meeting cycle in the app. | in: CAP-1, CAP-2, CAP-3 · out: selling books, video calls | Must | 4 | MS-1, MS-3 | ready |
| BCH-EP-002 | Members take part between meetings. | in: CAP-4 · out: — | Should | 2 | MS-2 | ready |

## 5. Traceability coverage

| Planning ID | Priority | Covered by | Status |
|---|---|---|---|
| CAP-1 | Must | BCH-EP-001, BCH-FT-001 | Covered |
| CAP-2 | Must | BCH-EP-001, BCH-FT-002 | Covered |
| CAP-3 | Must | BCH-EP-001, BCH-FT-003 | Covered |
| CAP-4 | Should | BCH-EP-002, BCH-FT-004, BCH-FT-005 | Covered |
| FR-1 | Must | BCH-FT-001 | Covered |
| FR-2 | Must | BCH-FT-001 | Covered |
| FR-3 | Must | BCH-FT-002 | Covered |
| FR-4 | Must | BCH-FT-003 | Covered |
| FR-5 | Should | BCH-FT-004 | Covered |
| FR-6 | Should | BCH-FT-005 | Covered |

## 6. Constraints and NFR coverage (D11)

| NFR | Priority | Global | Constrains | Implemented or verified by |
|---|---|---|---|---|
| NFR-1 | Must | Yes | — | — |
| NFR-2 | Must | Yes | — | BCH-FT-006 |
| NFR-3 | Should | Yes | — | BCH-FT-006 |

## 7. Dependencies

| Item | Depends on | Crosses Epics? |
|---|---|---|
| BCH-FT-002 | BCH-FT-001 | No |
| BCH-FT-003 | BCH-FT-001 | No |
| BCH-FT-006 | BCH-FT-001 | No |
| BCH-FT-006 | BCH-FT-002 | No |
| BCH-FT-006 | BCH-FT-003 | No |
| BCH-FT-004 | BCH-FT-003 | Yes |
| BCH-FT-005 | BCH-FT-003 | Yes |

## 8. Open questions and assumptions

| ID | Question or assumption | Severity | Affects |
|---|---|---|---|
| Q-1 | How are tied votes for the next book resolved? | Minor | BCH-FT-003 |
| ASM-1 | This is a new project: nothing is built and nothing is in Azure DevOps yet | Assumption | Whole plan |
| ASM-2 | Each member has one vote per round, and the organiser closes the round | Assumption | BCH-FT-003 |

## 9. Not ready

_Every item is ready._

## 10. Validation report

```text
Validation — BCH work breakdown v0.1 (process: Scrum) · checks run by render_review.py
PASS  M1   Schema
PASS  M2   Unique IDs
PASS  M3   ID prefix
PASS  M4   Parents
PASS  M5   Dependencies
PASS  M6   References resolve
PASS  M7   Must coverage
PASS  M8   Should and Could coverage
PASS  M9   Open questions are current
PASS  M10  Size signals
SKIP  M11  Milestone load
            - no capacity given (--max-features-per-milestone)
PASS  M12  ado_id empty
SKIP  M13  Review view current
            - checked when the review view is validated, not while it is being generated
PASS  M14  Copied NFR text
PASS  M15  Terminology
PASS  M16  Epics mirror milestones
Ready 8 · Needs elaboration 0 · Blocked 0 · Low confidence 0
Mechanical result: FAIL 0 · WARN 0 · PASS 14 · SKIP 2. Review checks R1–R14 are done by the independent reviewer.
```
