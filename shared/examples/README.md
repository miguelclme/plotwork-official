# Examples

These are hypothetical projects, planned with the `plan` and `prototype` skills. They show what finished results look like, and they are the test data for the scripts. The `demo` skill (`/plotwork:demo <example_id>`) presents them.

| Example ID | Scenario | Process | Profile | In one line |
|---|---|---|---|---|
| `plant-care` | A — new idea | Basic | Light | A one-line idea becomes 3 Epics after one round of questions |
| `book-club` | B — approved roadmap, broken down directly | Scrum | Standard | A roadmap becomes 2 Epics and 6 Features without rewriting it |
| `tool-share` | A — new idea, as a prototype | Agile | Prototype | An idea becomes a one-milestone prototype of 1 Epic and 3 Features, with a *Later* list |

Each example folder has a `README.md`, which describes the request, how the skill handled it, the result and what to notice, and a `docs/` folder with the files the skill wrote.

To regenerate a review view after changing an example's YAML, run this from the plugin's `shared/` folder:

```bash
python scripts/render_review.py examples/<example_id>/docs/planning/work-breakdown.yaml
```
