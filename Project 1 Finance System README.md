# Project 1 required finance system — ADP

## Run

Open a terminal in the folder containing [project 1 required finance system.py](project%201%20required%20finance%20system.py):

```powershell
py "project 1 required finance system.py"
```

Python 3.10 or later; no third-party packages, network connection, sibling lab scripts or saved reports are required. The single file contains frozen copies of the reviewed engines and source inputs. It creates `Project 1 Finance System Output` beside itself. Move only this Python file to another folder or computer to run the same snapshot. It does not download live data.

The [combined report](Project%201%20Finance%20System%20Output/Project%201%20Finance%20System%20Report.md) is the main readable result. Keep it with the code for grading without execution. JSON traces retain full precision. The manifest records hashes, Python version and run timestamp.

## What the file contains

1. Reported earnings-to-cash reconciliation and source locators.
2. Five-year statements with contract, working-capital and tax schedules.
3. Causal base/downside/upside cases and assumption challenges.
4. Dated FCFF DCF, WACC, terminal reinvestment and equity bridge.
5. WACC/g and terminal-return sensitivity, reverse DCF, accounting and failure checks.
6. Qualified annual-snapshot peer P/E and EV/operating-income calculations, definitions and sources.
7. Visible financial inputs, all scenario statements, validation status and run evidence.

All amounts are USD millions except per-share values. The valuation date is October 16, 2026; evidence was researched October 19. Historical annual shares and cash/debt balances are dated proxies, not current October balances. Discount-rate and forecasting assumptions are identified as judgments.

The result remains approximately **$157–$199/share**, base **$178**, with proposed **watch/defer**. Peer comparisons are cross-checks with different annual ends, not estimates to average into DCF. Read the economic limitations before presenting a conclusion.

## Inspect code or verify portability

```powershell
py "project 1 required finance system.py" --show-code forecast
py "project 1 required finance system.py" --show-code dcf
py "project 1 required finance system.py" --verify-portable
```

`--show-code` prints the actual embedded calculation section for inspection. The file's embedded sections are readable Python source in isolated namespaces, rather than imports from the original labs. The optional portability check makes a new temporary venv without pip, copies only the script, runs it in isolated mode and compares exact numeric outputs. It was successfully executed; the generated log explicitly states that it is an **unrecorded** machine check.

Change output location if desired:

```powershell
py "project 1 required finance system.py" --output-dir "video run"
```

## Requirements that still need student or course evidence

- Published training-case known answers and verification against them. The existing synthetic test is separately labeled.
- A human-authored, AI-off changed-input prediction, precommitted before the designated run. The generated blank JSON is only a template; reruns preserve it.
- Personal source check, final independent judgment and truthful contribution/AI-use attestations.
- Recorded cold run and later videos/transcripts/presentation. No recording has been created.
- Checkpoint and final submission receipts/access checks.

Financial-method limitations remain disclosed: partial base-year normalization, simplified client funding and tax/contract schedules, incomplete intervening-disclosure review, retained beta/ERP/debt-cost assumptions and stale annual peer/share/balance proxies. The file is runnable and portable; that does not establish completion of every Project 1 requirement.

## Development copies

Original labs and Edition A are unchanged. `build_project1_system.py` and `project1_system_runtime.txt` are local development helpers for rebuilding the standalone file; they are **not needed to run the delivered system**. Its embedded source is a frozen snapshot: editing an old lab does not change the packaged system until rebuilt. Rebuild only after deliberately reviewing changes.
