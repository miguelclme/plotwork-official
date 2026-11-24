---
type: llm
focus: trace
weight: 1
---

app-inventory.md records the loan rules that the code and its tests enforce: a loan lasts 14 days at most, nobody borrows their own tool, requests for the same tool can't overlap, and only the owner marks a tool returned.
