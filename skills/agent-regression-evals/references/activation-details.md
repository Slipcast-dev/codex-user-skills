# Полные условия применения

Use when an agent, prompt, model or tool change needs proof it did not make the agent worse — setting up a regression eval suite, deciding whether a pass-rate drop is real or noise, grading tool-call trajectories, finding flaky eval cases, or wiring an eval gate into CI that blocks the merge. Runs repeated trials, reports pass@k and pass^k, compares candidate to baseline with paired statistics, and refuses to pass a dropped case, a critical-case regression, or a forbidden tool call.
