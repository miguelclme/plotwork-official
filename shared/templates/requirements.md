# Requirements & Scope Register — <Project name>

| | |
|---|---|
| **Project key** | <KEY> |
| **Version** | v1 |
| **Date** | <YYYY-MM-DD> |
| **Status** | Draft · Reviewed at G2 · Approved |

<!-- Stage 2 (§8.2–§8.4). Product-level needs only (D19): what users and stakeholders need from each capability,
     enough to define Features and their acceptance criteria. No technical requirements: Tech Leads and Developers
     write those downstream.
     Status lifecycle: Proposed → Approved → Changed | Deferred | Dropped. Only Approved entries, or entries
     covered by an ASM, feed Stage 3. -->

## Capability map *(required)*

| ID | Capability | Purpose | Traces to | In scope | Out of scope | Priority | Milestone | Status |
|---|---|---|---|---|---|---|---|---|
| CAP-1 | <…> | <…> | OBJ-1 | <…> | <…> | Must · Should · Could · Won't | MS-1 | Proposed |

## Functional requirements *(required)*

<!-- What, not how. Each FR traces to at least one OBJ (or to a CON or DEC, for imposed needs) and to at least one source. -->

| ID | Statement (what, not how) | CAP | Priority | Acceptance measure | Source | Traces to | Status |
|---|---|---|---|---|---|---|---|
| FR-1 | <Users can …> | CAP-1 | Must | <how you know it is met> | SRC-1 §x | OBJ-1 | Proposed |

## Non-functional requirements *(conditional: quality attributes are relevant)*

<!-- Classify each NFR with an ISO/IEC 25010 category. Assign its D11 pattern(s); an NFR can have more than one:
     Constraint   = referenced on the Features it affects, or once in global_constraints;
     Capability   = needs an enabler Feature;
     Verification = needs a verification Feature, or an acceptance criterion if the effort is small. -->

| ID | Statement | Quality attribute | Applies to | D11 pattern | Priority | Target / acceptance measure | Source | Traces to | Status |
|---|---|---|---|---|---|---|---|---|---|
| NFR-1 | <…> | Security · Performance efficiency · Reliability · Usability · Maintainability · Compatibility · Portability | Global · CAP-n | Constraint · Capability · Verification | Must | <…> | SRC-1 §x | OBJ-1 | Proposed |

## Business rules *(conditional: domain rules exist)*

| ID | Rule | CAP | Source | Status |
|---|---|---|---|---|
| BR-1 | <…> | CAP-1 | SRC-1 §x | Proposed |

## Constraints *(required: "None known" is allowed)*

<!-- A constraint is an imposed "how". If the "how" is still open, it is an AQ in the RAID Log instead. -->

| ID | Constraint | Imposed by / reason | Source | Status |
|---|---|---|---|---|
| CON-1 | <…> | <…> | SRC-1 §x | Proposed |

## Glossary *(conditional: domain terms are ambiguous)*

| Term | Meaning |
|---|---|
| <…> | <…> |

## Merged entries *(conditional: duplicates were merged)*

<!-- §8.4: merge duplicates into one ID. The other ID stays here as an alias. -->

| Alias | Merged into | Reason |
|---|---|---|
| <FR-n> | <FR-m> | <…> |

## G2 review

| Gate | Proposed result | Your decision | Date |
|---|---|---|---|
| G2 | Ready · Ready with documented assumptions · Partially ready · Not ready | <…> | <YYYY-MM-DD> |

## Changelog

| Version | Date | Type | Summary | Ref |
|---|---|---|---|---|
| v1 | <YYYY-MM-DD> | New decision | First register | — |
