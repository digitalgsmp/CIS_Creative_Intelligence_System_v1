# CIS_LIVE — Active Scratchpad
Format: Bullets | 15 lines max | Newest first | Ends with ACTION

## ADR-045 Step 7 — cold start recovery validation — 2026-05-01 22:39 [OPEN]
Problem: Worker has a _recover_crashed_jobs() function that resets stuck running jobs to queued on startup. Need to validate this works by simulating a crash: manually insert a job with status=running into the DB, restart Flask, confirm the worker resets it to queued on startup. Expected return point: Step 7 complete, proceed to Step 8 (FIFO enforcement validation under load).

### Round 1 — 2026-05-01 22:44
[YOU]: The cold start recovery is validated.

### Round 2 — 2026-05-01 22:44
[RESPONSES]: Simulated crash by inserting job 14 with status=running and no payload into DB. Restarted Flask. Worker logged: "Cold-start recovery: reset 1 stuck job(s) to queued". Worker then claimed and attempted job 14, failing correctly on missing payload — not a recovery defect. Cold start recovery validated end-to-end. Step 7 complete.

---
