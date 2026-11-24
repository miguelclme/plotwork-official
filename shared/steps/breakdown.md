# Step: write the Epics and Features (Stage 3)

<!-- Shared by the plan, prototype and from-app skills. Paths are relative to the plugin's shared/ folder
     (${CLAUDE_PLUGIN_ROOT}/shared/). Stage 3 needs the ADO process. -->

1. **Read** the selected process's section of `references/processes.md`, then `references/decomposition-patterns.md`.
2. **Write `docs/planning/work-breakdown.yaml`** from `templates/work-breakdown.yaml`. The rules that matter most:
   - **Allowed types:** only Epics and Features. In Basic, only Epics, and each one carries the Feature-level keys (D18).
   - **Full description** (D8): every in-scope item is fully described, whatever milestone it targets. Where information is missing, list the Q in `open_questions` and mark the item `needs-elaboration`.
   - **Acceptance criteria** describe observable capability, not UI or technical detail. Each one must come from a source, an ASM or a Q. A criterion nothing supports is invented scope: record it as an ASM or a Q, so it appears in the G3 message, or leave it out.
   - **Phases are milestones, not Epics** (§8.5). Form Epics by capability, and let their Features target different milestones. A phase may yield an Epic only when it coincides with exactly one capability area, and the assessment says so.
   - **NFRs** go into `global_constraints` (applies to everything) or a Feature's `constraints`. Add enabler or verification Features where D11 calls for them, under the Epic they affect most. A quality-only phase ("Polish & performance") never gets an Epic of its own.
   - **Traceability:** every item traces to planning IDs (`traces_to`) and to sources.
   - **Sources' delivery-level content** (user stories, "shall" statements, Task-sized steps) goes into the owning Feature's `downstream_notes`. Never turn it into items.
   - **IDs:** draft IDs are `<KEY>-EP-001` and `<KEY>-FT-001`. `ado_id` stays `null`: only `/plotwork:push` writes it.
