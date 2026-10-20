# Lab 3 Edition B — Project 1 Valuation: Automatic Data Processing

**Valuation date:** October 16, 2026  
**Revision date:** October 19, 2026  
**Security/currency:** Nasdaq: ADP common stock; USD  
**Decision horizon:** Five years  
**Prepared with:** Student-directed AI research, coding and revision  
**Status:** Completed collaborative Edition B draft; student review and submission pending.

## Decision and intended user

The fund holds no ADP position. This analysis supports its investment committee's decision to initiate, watch/defer, or do not initiate.

**The proposed action is watch/defer.** The revised FCFF model supports an operating-case range of **$157–$199 per share**, with a base estimate of approximately **$178**, compared with the October 16 closing price of **$288.90**. The tested cases do not support initiating at that price under the stated assumptions. The range is conditional, not a confidence interval or a comprehensive measure of uncertainty.

This recommendation remains for student review. The analysis does not establish that the original five-year 8% expected-return hurdle is achieved at a particular entry price.

## What changed from Edition A

Edition A, dated September 1, identified a durable business and proposed watch/defer while valuation work remained incomplete. Its original file is [preserved unchanged](Project%201%20Edition%20A.md). This revision adds a historical reconciliation, scheduled five-year statements, causal operating scenarios and a pro-forma-driven enterprise valuation.

| Edition A starting point | Edition B revision | Why it matters |
|---|---|---|
| Delayed reference quote $280.83 | October 16 close $288.90 | Aligns the market comparison to a defined valuation date |
| Business quality supported further research | Cash-flow valuation still supports watch/defer | Quality alone does not establish an attractive purchase price |
| Normalized cash generation unknown | Reported OCF reconciles over three years; normalized forecast policies are explicit | Separates source facts from forecasting judgment |
| Broad growth and margin assumptions | Fee-related revenue, zero-margin benefits and client interest are separated | Different revenue components have different profit and cash effects |
| No completed intrinsic-value range | $157–$199 operating-case range | Makes the decision conditional on tested economics |
| AI durability was an open question | Higher service/AI costs are stressed; productivity benefits require evidence | Stock-price expectations cannot validate an operating-margin forecast |

Edition A's unchanged status does not prove a successful checkpoint submission or AI-closed authorship. The recovered historical transcript shows AI assistance; no Brightspace receipt has been supplied.

## Evidence and its dates

The financial base is ADP's FY2026 annual filing, accession 0000008670-26-000030, filed August 5, covering June 30, 2026. Reported facts, management guidance, analyst assumptions and calculated outputs are identified separately in the linked reports. Dollar model inputs are millions unless stated otherwise.

- **Market fact:** October 16 close $288.90. [Price history](https://stockanalysis.com/stocks/adp/history/). Analyst calculation: 26.41 times FY2026 reported diluted EPS of $10.94.
- **Annual filing facts:** cash 4,230.1; diluted annual-average shares 403.3; operating cash flow 5,441.2. Corporate cash, pledged securities and client money have different definitions. [10-K, financial statements and notes](https://www.sec.gov/Archives/edgar/data/8670/000000867026000030/adp-20260630.htm).
- **Management expectations:** July 29 FY2027 guidance included 5–6% revenue growth, 70–90bp adjusted margin expansion, and a 10–30bp decline in retention. These are not five-year promises. [Earnings release and reconciliations](https://www.sec.gov/Archives/edgar/data/8670/000000867026000025/q4fy26exhibit99.htm).
- **Discount-rate fact:** October 16 ten-year Treasury par yield 5.09%. [Treasury daily rates](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve).

Sources were accessed October 19. The valuation excludes information first published after October 16; the complete intervening-disclosure search remains a limitation. Scheduled October 28 quarterly results are excluded.

## Cash-flow method and model corrections

The [historical reconciliation](ADP_cash_flow_reconciliation.md) reproduces reported operating cash flow for FY2024–FY2026 with zero residual at reported precision. It also checks FY2026 earnings and corporate versus restricted cash movement.

The new model forecasts income, assets, liabilities and cash together. Contract spending increases its asset; amortization reduces it and is charged once in earnings. Working-capital schedules distinguish operating assets and liabilities. Tax expense, deferred taxes, tax payable and cash taxes have separate schedules. Stock compensation is added back in accounting CFO and credited to equity, but remains an economic expense in valuation cash flow.

FCFF is calculated from operating earnings after operating cash taxes, adding noncash charges and subtracting reinvestment. A second route from CFO adjusts financing and tax effects and produces the same FCFF. Client-strategy financing remains in operating economics; corporate financing is treated separately.

The original Lab 10 D&A reclassification was sound with exact historical inputs. The larger weakness was incomplete earnings-to-cash schedules. Its FCFE valuation at cost of equity also differed from this assignment's required FCFF/WACC architecture.

## Consequential assumptions and challenges

| Driver | Working assumption and basis | Challenge / evidence that changes it |
|---|---|---|
| Fee-related growth | 4.5%, 4.5%, 4.25%, 4%, 4%; analyst fade | Retention, bookings conversion, employment and pricing may not sustain this path |
| Benefits pass-through | 6% annually; equal direct revenue and cost | Revenue mix cannot be treated as incremental profit |
| Average client balances and yield | Balances grow 3.5%; yield path 3.7%, 3.7%, 3.6%, 3.5%, 3.4% | Portfolio repricing, payroll balances and financing costs can change income; a Fed cut does not instantly reprice the entire portfolio |
| Service costs and AI | Historical residual cost intensity retained in base | Higher R&D/service costs without evidenced productivity gains weaken cash flow |
| Reinvestment | Contract spending, software and compensation follow fee-related revenue | Customer acquisition and implementation spending can precede revenue; historical ratios may change |
| Working capital and cash tax | Opening balance ratios and payment-timing proxy | Mix shifts, collection timing and tax payments require revision if evidence differs |
| WACC | 8.629%; updated Treasury rate with retained beta 0.83, ERP 4.5%, debt-cost proxy 5.14%, tax 23% | Beta/ERP and marginal debt cost are assumptions, not verified October market observations |
| Terminal economics | Growth 2.5%; incremental ROIC 20% | Persistent growth requires reinvestment; test discount rate, growth and ROIC together |

The student-described Lab 10 partner's concern about optimistic margins and expensive AI research is credited in the [challenge record](ADP_assumption_challenge.md); the partner's name was not supplied. New scenarios are AI-authored proposals. No new human partner conversation is claimed.

## Valuation range and bridge

| Case | FY2027 FCFF, $M | FY2031 FCFF, $M | EV, $M | Equity, $M | Value/share |
|---|---:|---:|---:|---:|---:|
| Downside | 4,120.67 | 4,705.39 | 64,441.61 | 63,366.21 | $157.12 |
| Base | 4,601.21 | 5,281.33 | 72,961.34 | 71,885.94 | $178.24 |
| Upside | 4,705.02 | 5,905.00 | 81,332.83 | 80,257.43 | $199.00 |

Downside combines weaker fee growth, client balances and yields with higher service and contract costs. Upside assumes stronger fees and balance growth plus productivity improvements. Scenarios use the same WACC and terminal policy; they have no assigned probabilities.

Base enterprise value is **18,504.07** of explicit cash-flow PV plus **54,457.27** of terminal PV. Add **3,729.4** excess corporate cash and subtract **4,804.8** corporate financing debt to reach **71,885.94** equity value. Divide by **403.3 million** historical diluted average shares.

The bridge excludes client principal and separately adding pledged securities. Repos remain in client-strategy operating treatment. Cash includes a $500 million analyst operating buffer and excludes pledged cash. Debt uses June notes fair value plus other debt. These are dated proxies; they are not October measured balances or a current diluted share count.

Only the remaining 70.41% of FY2027 cash flow is valued, using uniform-generation proration; cash flows are discounted to October 16 with year-end actual-day timing. Terminal cash flow uses normalized operating taxes and reinvestment equal to NOPAT times growth divided by incremental ROIC.

## Sensitivity and market-implied expectations

Approximately **75% of EV is terminal value**. The base operating forecast spans approximately **$144–$244** across WACC ±1 percentage point and terminal growth 1.5–3.5%; this is a separate parameter sensitivity, not the operating-case range. At base WACC/g, changing terminal ROIC from 15% to 30% gives approximately $172–$185.

Reverse DCF requires about **12.31 additional percentage points of annual fee growth** to match $288.90 under the otherwise fixed model rules. That is a conditional market-implied requirement, not a prediction.

The old $228.10 standalone DCF and $200.99 FCFE outputs used different forecasts, discounting, financing and terminal policies. Earlier peer estimates also used different market dates and earnings comparisons. They are historical cross-checks, not current estimates to average mechanically. The prior P/E work remains available in [Lab 8](Lab%208.md). The packaged system now includes an [October-price annual-snapshot peer comparison](Project%201%20Finance%20System%20Output/ADP_peer_comparison.md): peer P/E implies approximately $250–$341 and EV/operating income approximately $245–$337. These higher cross-checks reflect market-relative pricing and different earnings, growth, fiscal-period and reinvestment assumptions; stale annual balances and client-strategy differences limit comparability. They are not averaged with DCF or presented as synchronized TTM valuations.

## Conditions, monitoring and reversal triggers

Watch/defer remains the proposed action while the price exceeds the tested value range. A candidate entry screen is approximately **$143**, 20% below the base estimate, provided operating evidence remains intact. This analyst rule is not a guaranteed return or an approved fund mandate.

Reassess if retention falls below the guided 91.8–92.0% range, bookings or employment indicators weaken, client-interest expectations fall, or costs rise without demonstrated productivity. Initiation would require a qualifying price or independently supported cash-flow improvement. Evidence of lasting competitive damage would instead support abandoning the initiation thesis.

## Unknowns and material limits

- Average client balances drive income, while closing client-principal and funding balances remain fixed. Detailed funding dynamics are not modeled.
- Contract amortization, operating balances and tax timing use aggregate proxies; the historical contract-asset residual and exact corporate cash-interest split remain unresolved.
- Base-year reported statements reconcile, but complete economic normalization and cash timing of unusual items remain provisional.
- No acquisitions, detailed debt maturity/refinancing, pension/venture asset valuation, or full lease schedule is forecast.
- June cash/debt, historical shares and some discount-rate inputs are proxies. The October stub and terminal transition are approximations.
- The student has not yet supplied the final independent decision, required AI-off locked prediction, training-case verification, recorded cold run or submission receipt.

## Validation, reproducibility and supporting files

The preferred runnable artifact is now the self-contained [project 1 required finance system.py](project%201%20required%20finance%20system.py). It embeds the existing engines, adds qualified peer comparisons and generates a [consolidated report](Project%201%20Finance%20System%20Output/Project%201%20Finance%20System%20Report.md). See the [README](Project%201%20Finance%20System%20README.md). A single-file run in a new venv matched numerical outputs exactly; the check was unrecorded and does not substitute for the student's recorded cold run.

Passed: historical OCF reconciliation; opening and five-year balance checks; cash, contract and tax ties; two FCFF routes; scenario isolation; cost/yield directional probes; invalid-input rejection; bridge checks; WACC/g monotonicity; a synthetic known-answer DCF; reverse-price reconciliation. These AI-authored checks do not substitute for student-only or course-specific validation requirements.

Run from this folder with Python and no third-party dependencies:

```powershell
py adp_reconciliation.py
py adp_project_forecast.py
py adp_assumption_challenge.py
py adp_project_dcf.py
```

The reports show inputs and results without requiring execution:

- [Historical reconciliation](ADP_cash_flow_reconciliation.md)
- [Reference scheduled statements](ADP_scheduled_forecast.md)
- [Current component scenarios and challenge record](ADP_assumption_challenge.md)
- [DCF, bridge and sensitivity tables](ADP_project_DCF.md)
- [Work record](Project%201%20Edition%20B%20Work%20Record.md)
- [Archived working draft](Lab%203%20Edition%20B%20working%20archive.md)

This file completes the collaborative Edition B draft. It does not establish completion or submission of the seven-part Project 1 bundle. Student attestation and actual teammate contributions must be supplied truthfully by the student.

