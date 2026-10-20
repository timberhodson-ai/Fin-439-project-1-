"""Project 1 required finance system — ADP.
Self-contained, standard-library Python 3.10+. Offline frozen evidence snapshot.
Run: py "project 1 required finance system.py"
Optional: --show-code forecast | --verify-portable | --output-dir PATH
Embedded sections preserve the reviewed lab engines in isolated namespaces.
No sibling Python files or pre-generated reports are required.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import io
import json
import platform
import statistics
import sys
import types
from contextlib import redirect_stdout

EMBEDDED = {}

# ===== Lab 10_proforma.py: frozen reviewed engine =====
EMBEDDED['project1_legacy'] = r'''
"""Five-year integrated financial model and FCFE equity valuation for Automatic Data Processing, Inc. (ADP).

FIN 439 - Lab 10
Educational coursework only. Not financial or investment advice, and not a
recommendation to buy, sell, or hold any security. Outputs depend on simplified
assumptions and unresolved data limitations described in the accompanying report.
Projects FY2027E to FY2031E income statement, balance sheet, cash flow / FCFE,
performs balance sheet equilibrium checks, and computes discounted FCFE equity valuation.
Standard library only; no external package dependencies.
"""

# ==============================================================================
# Model Assumptions and Opening Balance Sheet (FY2026 ended June 30, 2026)
# ==============================================================================

# Operational Judgments & History
REVENUE_GROWTH = 0.055      # Total reported revenue; FY27 guidance midpoint, later years judgment
GROSS_MARGIN = 0.5333        # Contribution margin BEFORE R&D and D&A (history/judgment)
SGA_RATIO = (4408.2 - (585.9 - 490.8)) / 11706.8  # Exclude D&A outside cost of revenues
RD_RATIO = 0.0469            # 4.69% R&D as % of Revenue (history: $1,028.8M on $21,947.4M)
DEPR_PPE_RATIO = 201.1 / 655.4  # PP&E depr / opening PP&E (~30.68%, history)
IMPAIRMENT = 0.0             # $0.0M non-cash impairment (history/judgment)
CAPEX_PPE = 212.5            # FY27 $200-225M guidance midpoint; held flat by judgment
SOFTWARE_CAPEX_RATIO = 468.5 / 21947.4  # Capitalized intangibles scale with revenue
AMORT_INTANG_RATIO = 384.8 / 1603.0    # Amortization / opening net intangible assets
TAX_RATE = 0.230             # 23.0% effective tax rate (history/guidance: 3-yr average 23.0%)

# Working Capital & Operating History
INV_DAYS = 0.0               # ADP carries no physical product inventory (history: None)
FLOOR_PLAN_RATIO = 0.0       # ADP has no dealership floor plan debt (history: None)
OWC_REV_RATIO = 0.012        # Other working capital = 1.2% of change in revenue (judgment)

# Liquidity, Debt & Capital Allocation
MIN_CASH = 500.0             # Operating cash floor $500.0M (history/judgment)
REVOLVER_LIMIT = 2000.0      # Credit facility capacity $2,000.0M (judgment)
REVOLVER_RATE = 0.055        # 5.5% credit facility borrowing rate (judgment)
DEBT_REPAYMENT = 200.0       # $200.0M term debt repayment / retirement annually (judgment)
SHAREHOLDER_DIST = 3500.0    # $3,500.0M annual dividends + net share repurchases (judgment)

# Interest & Capital Rates
DEBT_INTEREST_RATE = 0.045   # Judgment: simplified corporate borrowing rate, not historical total expense
COST_OF_EQUITY = 0.0483 + 0.83 * 0.045  # CAPM = 8.565%; inherited inputs, not refreshed market estimates
TERMINAL_GROWTH = 0.025      # 2.50% nominal terminal growth rate (judgment)
SHARES_OUTSTANDING = 403.3   # 403.3 million diluted shares (fact: FY2026 10-K, p. 45)

# Opening Balance Sheet, FY2026 Ended June 30, 2026 (USD millions, 10-K p. 47)
FY2026_REVENUE = 21947.4
FY2026_CASH = 4230.1          # Corporate cash and cash equivalents
FY2026_INVENTORY = 0.0        # None
FY2026_PPE = 641.3            # Property, plant and equipment, net
FY2026_OTHER_ASSETS = 58321.9 # Receivables, client funds asset ($43,957.8M), intangibles, goodwill, other
FY2026_INTANGIBLES = 1653.3
FY2026_CLIENT_ASSETS = 43957.8
FY2026_CLIENT_OBLIGATIONS = 44415.5
FY2026_FLOOR_PLAN = 0.0       # None
FY2026_TERM_DEBT = 5104.4     # Long-term debt $4,964.1M + current $1.0M + reverse repos $139.3M
FY2026_REVOLVER = 0.0         # Commercial paper / credit facility drawn: $0.0M
FY2026_OTHER_LIABILITIES = 52057.7 # Client funds obligations ($44,415.5M), payables, accrued, other
FY2026_EQUITY = 6031.2        # Total stockholders' equity

YEARS = [2027, 2028, 2029, 2030, 2031]

# Separate snapshot of all original independent assumptions and opening balances.
from copy import deepcopy

BASE_INPUTS = deepcopy({key: value for key, value in globals().copy().items()
                        if key.isupper()})
BASE_INPUTS['MARGIN_SHIFT_BY_YEAR'] = {year: 0.0 for year in YEARS}


def run_with_inputs(inputs, override_2027_cash=None):
    """Run the existing engine in an independent namespace, without global mutation."""
    from types import FunctionType
    namespace = dict(globals())
    namespace.update(deepcopy(inputs))
    engine = FunctionType(run_model.__code__, namespace, run_model.__name__,
                          run_model.__defaults__)
    return engine(override_2027_cash=override_2027_cash)


MARGIN_SHIFT_BY_YEAR = deepcopy(BASE_INPUTS['MARGIN_SHIFT_BY_YEAR'])


def run_model(override_2027_cash=None):
    """Return income statement, balance sheet, cash flow and check dictionaries."""
    is_rows = {
        "Total revenues": [],
        "Operating expenses (direct cost)": [],
        "Contribution before R&D and D&A": [],
        "SG&A excluding D&A": [],
        "Research & development": [],
        "Depreciation & amortization": [],
        "Sensitivity operating cost adjustment": [],
        "Operating income (EBIT)": [],
        "Interest expense": [],
        "Pretax income": [],
        "Provision for income taxes": [],
        "Net earnings": [],
    }

    bs_rows = {
        "Corporate cash & equivalents": [],
        "Inventories": [],
        "Property, plant & equipment, net": [],
        "Intangible assets, net": [],
        "Funds held for clients": [],
        "Other corporate assets": [],
        "Total assets": [],
        "Floor plan notes": [],
        "Term borrowings & debt": [],
        "Credit facility / revolver": [],
        "Client funds obligations": [],
        "Other corporate liabilities": [],
        "Total liabilities": [],
        "Stockholders' equity": [],
        "Total liabilities & equity": [],
    }

    cf_rows = {
        "Net earnings": [],
        "Depreciation & amortization": [],
        "PP&E capital expenditures": [],
        "Capitalized intangible additions": [],
        "Change in other working capital": [],
        "Debt repayment": [],
        "FCFE before revolver financing": [],
        "Opening corporate cash": [],
        "Shareholder distributions (divs/buybacks)": [],
        "Revolver draw / (repayment)": [],
        "Free cash flow to equity (FCFE)": [],
        "Closing corporate cash": [],
    }

    checks = {
        "Assets - liabilities - equity": [],
        "Cash at or above minimum (500.0)": [],
        "Balance sheet gap": [],
    }

    # Initialize tracking variables with FY2026 opening balances
    prior_rev = FY2026_REVENUE
    prior_cash = FY2026_CASH
    prior_ppe = FY2026_PPE
    prior_intangibles = FY2026_INTANGIBLES
    prior_other_assets = FY2026_OTHER_ASSETS - FY2026_INTANGIBLES - FY2026_CLIENT_ASSETS
    prior_debt = FY2026_TERM_DEBT
    prior_revolver = FY2026_REVOLVER
    prior_other_liab = FY2026_OTHER_LIABILITIES - FY2026_CLIENT_OBLIGATIONS
    prior_equity = FY2026_EQUITY

    for idx, year in enumerate(YEARS):
        # 1. Income Statement
        rev = prior_rev * (1.0 + REVENUE_GROWTH)
        change_in_rev = rev - prior_rev
        direct_opex = rev * (1.0 - GROSS_MARGIN)
        gp = rev * GROSS_MARGIN
        sga = gp * SGA_RATIO
        rd = rev * RD_RATIO
        depr = prior_ppe * DEPR_PPE_RATIO
        amort = prior_intangibles * AMORT_INTANG_RATIO
        total_da = depr + amort
        software_capex = rev * SOFTWARE_CAPEX_RATIO
        # Positive margin shift reduces cash operating costs; all linked statements recalculate.
        cost_adjustment = -rev * MARGIN_SHIFT_BY_YEAR.get(year, 0.0)
        op_inc = gp - sga - rd - total_da - IMPAIRMENT - cost_adjustment

        interest = prior_debt * DEBT_INTEREST_RATE + prior_revolver * REVOLVER_RATE
        pretax = op_inc - interest
        tax = max(0.0, pretax) * TAX_RATE
        net_inc = pretax - tax

        is_rows["Total revenues"].append(rev)
        is_rows["Operating expenses (direct cost)"].append(direct_opex)
        is_rows["Contribution before R&D and D&A"].append(gp)
        is_rows["SG&A excluding D&A"].append(sga)
        is_rows["Research & development"].append(rd)
        is_rows["Depreciation & amortization"].append(total_da)
        is_rows["Sensitivity operating cost adjustment"].append(cost_adjustment)
        is_rows["Operating income (EBIT)"].append(op_inc)
        is_rows["Interest expense"].append(interest)
        is_rows["Pretax income"].append(pretax)
        is_rows["Provision for income taxes"].append(tax)
        is_rows["Net earnings"].append(net_inc)

        # 2. Balance Sheet (except cash)
        ppe = prior_ppe + CAPEX_PPE - depr
        intangibles = prior_intangibles + software_capex - amort
        change_owc = OWC_REV_RATIO * change_in_rev
        other_assets = prior_other_assets + change_owc - IMPAIRMENT
        debt_repayment = min(DEBT_REPAYMENT, prior_debt)
        debt = prior_debt - debt_repayment
        other_liab = prior_other_liab
        equity = prior_equity + net_inc - SHAREHOLDER_DIST

        # 3. Free Cash Flow to Equity (FCFE)
        fcfe = net_inc + total_da + IMPAIRMENT - CAPEX_PPE - software_capex - change_owc - debt_repayment

        # 4. Cash and Revolver Mechanics
        tentative_cash = prior_cash + fcfe - SHAREHOLDER_DIST
        revolver = prior_revolver
        revolver_activity = 0.0

        if tentative_cash < MIN_CASH:
            shortfall = MIN_CASH - tentative_cash
            draw = min(shortfall, REVOLVER_LIMIT - prior_revolver)
            revolver = prior_revolver + draw
            cash = tentative_cash + draw
            revolver_activity = draw
        elif tentative_cash > MIN_CASH and prior_revolver > 0.0:
            surplus = tentative_cash - MIN_CASH
            repay = min(surplus, prior_revolver)
            revolver = prior_revolver - repay
            cash = tentative_cash - repay
            revolver_activity = -repay
        else:
            cash = tentative_cash

        # Intentional test hook for broken balance sheet check
        if year == 2027 and override_2027_cash is not None:
            cash = override_2027_cash

        # Record Balance Sheet lines
        total_assets = cash + ppe + intangibles + FY2026_CLIENT_ASSETS + other_assets
        total_liab = debt + revolver + FY2026_CLIENT_OBLIGATIONS + other_liab
        total_liab_equity = total_liab + equity

        bs_rows["Corporate cash & equivalents"].append(cash)
        bs_rows["Inventories"].append(0.0)
        bs_rows["Property, plant & equipment, net"].append(ppe)
        bs_rows["Intangible assets, net"].append(intangibles)
        bs_rows["Funds held for clients"].append(FY2026_CLIENT_ASSETS)
        bs_rows["Other corporate assets"].append(other_assets)
        bs_rows["Total assets"].append(total_assets)
        bs_rows["Floor plan notes"].append(0.0)
        bs_rows["Term borrowings & debt"].append(debt)
        bs_rows["Credit facility / revolver"].append(revolver)
        bs_rows["Client funds obligations"].append(FY2026_CLIENT_OBLIGATIONS)
        bs_rows["Other corporate liabilities"].append(other_liab)
        bs_rows["Total liabilities"].append(total_liab)
        bs_rows["Stockholders' equity"].append(equity)
        bs_rows["Total liabilities & equity"].append(total_liab_equity)

        # Record Cash Flow Statement lines
        cf_rows["Net earnings"].append(net_inc)
        cf_rows["Depreciation & amortization"].append(total_da)
        cf_rows["PP&E capital expenditures"].append(CAPEX_PPE)
        cf_rows["Capitalized intangible additions"].append(software_capex)
        cf_rows["Change in other working capital"].append(change_owc)
        cf_rows["Debt repayment"].append(debt_repayment)
        cf_rows["FCFE before revolver financing"].append(fcfe)
        cf_rows["Opening corporate cash"].append(prior_cash)
        cf_rows["Shareholder distributions (divs/buybacks)"].append(SHAREHOLDER_DIST)
        cf_rows["Revolver draw / (repayment)"].append(revolver_activity)
        cf_rows["Free cash flow to equity (FCFE)"].append(fcfe + revolver_activity)
        cf_rows["Closing corporate cash"].append(cash)

        # 5. Balance Sheet & Liquidity Checks
        gap = total_assets - total_liab - equity
        checks["Assets - liabilities - equity"].append(gap)
        checks["Cash at or above minimum (500.0)"].append(cash >= (MIN_CASH - 1e-4))
        checks["Balance sheet gap"].append(gap)

        # Roll forward balances
        prior_rev = rev
        prior_cash = cash
        prior_ppe = ppe
        prior_intangibles = intangibles
        prior_other_assets = other_assets
        prior_debt = debt
        prior_revolver = revolver
        prior_other_liab = other_liab
        prior_equity = equity

    return is_rows, bs_rows, cf_rows, checks


def assert_balanced(checks):
    """Raises an error naming the year and the gap if any check fails."""
    for idx, year in enumerate(YEARS):
        gap = checks["Balance sheet gap"][idx]
        is_above_min = checks["Cash at or above minimum (500.0)"][idx]
        if abs(gap) > 1e-3:
            raise AssertionError(
                f"Balance sheet check failed in FY{year}E: gap of {gap:+.1f} (assets - liabilities - equity != 0)"
            )
        if not is_above_min:
            raise AssertionError(
                f"Liquidity check failed in FY{year}E: cash below minimum of ${MIN_CASH:.1f}M"
            )


def print_table(title, rows, years=YEARS):
    """Prints a financial statement table with years across, formatted to one decimal."""
    print(f"\n=== {title} (USD Millions) ===")
    header = f"{'Line Item':<40}" + "".join(f"{f'FY{y}E':>12}" for y in years)
    print(header)
    print("-" * len(header))
    for label, values in rows.items():
        val_str = "".join(f"{v:>12.1f}" for v in values)
        print(f"{label:<40}{val_str}")


def print_checks(checks, years=YEARS):
    """Prints the check block for all projection years."""
    print("\n=== Balance Sheet and Liquidity Checks ===")
    header = f"{'Check':<40}" + "".join(f"{f'FY{y}E':>12}" for y in years)
    print(header)
    print("-" * len(header))
    gap_str = "".join(f"{g:>12.1f}" for g in checks["Assets - liabilities - equity"])
    print(f"{'Assets - liabilities - equity':<40}{gap_str}")
    min_str = "".join(f"{('Pass' if ok else 'FAIL'):>12}" for ok in checks["Cash at or above minimum (500.0)"])
    print(f"{'Cash >= Minimum ($500.0M)':<40}{min_str}")


def perform_valuation(fcfe_list):
    """Calculates discounted FCFE equity value, terminal value, and value per share."""
    if len(fcfe_list) != len(YEARS):
        raise ValueError("Provide one FCFE for each forecast year.")
    if not COST_OF_EQUITY > TERMINAL_GROWTH:
        raise ValueError("Cost of equity must exceed terminal growth.")
    if any(f <= 0 for f in fcfe_list):
        raise ValueError("Nonpositive FCFE: review funding and terminal assumptions before valuation.")
    discount_factors = [(1.0 + COST_OF_EQUITY) ** t for t in range(1, 6)]
    pv_fcfe_list = [f / df for f, df in zip(fcfe_list, discount_factors)]
    pv_explicit_fcfe = sum(pv_fcfe_list)

    # Terminal judgment: scheduled term repayments are refinanced after FY2031.
    # This removes net term repayments, not interest expense or reinvestment.
    terminal_cash_flow = (fcfe_list[-1] + DEBT_REPAYMENT) * (1.0 + TERMINAL_GROWTH)
    terminal_value = terminal_cash_flow / (COST_OF_EQUITY - TERMINAL_GROWTH)
    pv_terminal_value = terminal_value / ((1.0 + COST_OF_EQUITY) ** 5)

    total_equity_value = pv_explicit_fcfe + pv_terminal_value
    tv_share = pv_terminal_value / total_equity_value
    value_per_share = total_equity_value / SHARES_OUTSTANDING

    print("\n=== Equity Valuation (Discounted FCFE Model) ===")
    print(f"Cost of Equity (r_e):                 {COST_OF_EQUITY * 100:.3f}%")
    print(f"Terminal Growth Rate (g):             {TERMINAL_GROWTH * 100:.2f}%")
    print(f"Diluted Shares Outstanding:           {SHARES_OUTSTANDING:.1f} million")
    print("-" * 60)
    for yr, pv, f in zip(YEARS, pv_fcfe_list, fcfe_list):
        print(f"FY{yr}E FCFE: ${f:>7.1f}M  |  PV: ${pv:>7.2f}M")
    print(f"PV of 5-Year Explicit FCFE:           ${pv_explicit_fcfe:>10.2f}M")
    print(f"Normalized FY2031 Cash Flow (FCFE+Repay): ${fcfe_list[-1] + DEBT_REPAYMENT:>8.2f}M")
    print(f"Terminal Value (at FY2031E):          ${terminal_value:>10.2f}M")
    print(f"PV of Terminal Value:                 ${pv_terminal_value:>10.2f}M")
    print(f"Total Equity Value:                   ${total_equity_value:>10.2f}M")
    print(f"Share of Value after FY2031:          {tv_share * 100:>10.2f}%")
    print(f"Model Implied Value Per Share:        ${value_per_share:>10.2f}")

    return total_equity_value, tv_share, value_per_share


def main():
    print("Projecting 5 Years of Integrated Financial Statements for Automatic Data Processing (ADP)...")
    is_rows, bs_rows, cf_rows, checks = run_model()

    # Print the three statements
    print_table("Income Statement", is_rows)
    print_table("Balance Sheet", bs_rows)
    print_table("Cash Flow Statement (FCFE)", cf_rows)

    # Print check block
    print_checks(checks)

    # Verify model balance before performing valuation
    assert_balanced(checks)
    print("\n[Pass] All balance sheet and liquidity checks verified: assert_balanced passed.")

    # Perform Valuation
    perform_valuation(cf_rows["Free cash flow to equity (FCFE)"])


if __name__ == "__main__":
    import sys
    if '--sensitivity' in sys.argv:
        from adp_sensitivity import main as sensitivity_main
        sensitivity_main()
    else:
        main()

'''

# ===== adp_reconciliation.py: frozen reviewed engine =====
EMBEDDED['adp_reconciliation'] = r'''
"""Historical ADP reconciliation; standard library, USD millions.
Run: py adp_reconciliation.py. Writes ADP_cash_flow_reconciliation.md.
Source: FY2026 10-K pp. 34, 45, 47, 49; retrieved 2026-10-19.
This reconciles reported facts, not a completed normalized valuation.
"""
from decimal import Decimal as D
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent
SOURCE = 'https://www.sec.gov/Archives/edgar/data/8670/000000867026000030/adp-20260630.htm'
YEARS = (2026, 2025, 2024)
# Signed statement-of-cash-flow contributions, in the filing's column order.
ROWS = {
    'Net earnings': ('4413.5', '4079.7', '3752.0'),
    'D&A': ('585.9', '582.4', '561.9'),
    'Contract-cost amortization': ('1200.5', '1145.3', '1067.6'),
    'Deferred tax': ('156.4', '37.0', '-37.4'),
    'Stock compensation': ('242.6', '266.1', '243.5'),
    'Bad debt': ('47.5', '53.2', '54.6'),
    'Pension': ('-15.4', '-19.7', '-22.9'),
    'Securities accretion': ('-88.2', '-72.2', '-42.6'),
    'Other': ('4.2', '13.4', '-1.7'),
    'Receivables': ('1.0', '-146.6', '-483.7'),
    'Contract-cost investment': ('-1307.9', '-1290.3', '-1271.2'),
    'Other assets': ('-204.5', '-59.8', '-157.2'),
    'Payables': ('-4.5', '60.6', '1.8'),
    'Accrued/other liabilities': ('410.1', '290.6', '492.9'),
}
EXPECTED_OCF = tuple(map(D, ('5441.2', '4939.7', '4157.6')))


def reconcile(rows):
    totals = tuple(sum((D(values[i]) for values in rows.values()), D(0))
                   for i in range(3))
    for year, actual, expected in zip(YEARS, totals, EXPECTED_OCF):
        if actual != expected:
            raise ArithmeticError(f'FY{year} OCF mismatch: {actual - expected:+}')
    return totals


def require_equal(name, actual, expected):
    if actual != expected:
        raise ArithmeticError(f'{name}: {actual} != {expected}')


def main():
    ocf = reconcile(ROWS)
    # Exact reported-income reconstruction, not the company's labeled EBIT.
    operating_profit = D('21947.4') - D('11760.2') - D('4408.2')
    pretax = operating_profit - D('459.3') + D('410.6')
    require_equal('Pretax income', pretax, D('5730.3'))
    require_equal('Net income', pretax - D('1316.8'), D('4413.5'))
    # D&A reclassification in the old model can reconstruct operating profit
    # if exact historical inputs are used, rather than rounded forecast drivers.
    sga_ex_da = D('4408.2') - (D('585.9') - D('490.8'))
    historical_recast = (D('21947.4') - D('10240.6') - sga_ex_da
                         - D('1028.8') - D('585.9'))
    require_equal('D&A reclassification', historical_recast, operating_profit)
    adjusted = sum(map(D, ('5730.3', '141.0', '-92.9', '-4.5',
                           '91.1', '-8.4', '18.0')))
    require_equal('Management adjusted EBIT', adjusted, D('5874.6'))
    # Full cash-flow totals include restricted cash; do not call them corporate cash.
    change_total = D('5441.2') - D('4713.8') + D('4881.0') - D('37.8')
    require_equal('Total cash movement', change_total, D('5570.6'))
    require_equal('Total closing cash', D('5054.6') + change_total, D('10625.2'))
    restricted_change = D('6395.1') - D('1706.8')
    corporate_change = change_total - restricted_change
    require_equal('Corporate cash movement', corporate_change,
                  D('4230.1') - D('3347.8'))
    contract_net = D('1200.5') - D('1307.9')
    contract_residual = (D('3244.1') - D('3154.1')) - (-contract_net)
    # Deliberately corrupt a load-bearing source row: reconciliation must fail.
    broken = dict(ROWS)
    broken['Contract-cost investment'] = ('0', '-1290.3', '-1271.2')
    try:
        reconcile(broken)
    except ArithmeticError:
        failure_check = 'PASS: omitted contract investment was rejected.'
    else:
        raise AssertionError('Missing investment escaped reconciliation')
    # Audit the existing lab without altering it or using its valuation.
    import project1_legacy as old
    income, balance, cashflow, checks = old.run_with_inputs(old.BASE_INPUTS)
    old.assert_balanced(checks)
    rev = old.FY2026_REVENUE
    old_base_op = (rev * old.GROSS_MARGIN * (1 - old.SGA_RATIO)
                   - rev * old.RD_RATIO - 585.9)
    # Reproduce the previously published proxy, explicitly not finalized FCFF.
    levered = ocf[0] - D('196.6') - D('468.5')
    proxy = levered + D('141.0') * D('.77') - D('92.9') * D('.77') - D('242.6')
    lines = [
        '# ADP historical cash-flow reconciliation', '',
        'Generated by `adp_reconciliation.py`; USD millions. Research date: October 19, 2026.', '',
        f'[FY2026 10-K]({SOURCE}), printed pp. 34, 45, 47, 49. Facts below are reported; calculations and policy choices are labeled. This is not a normalized valuation.', '',
        '## Earnings to operating cash flow', '',
        '| Signed contribution | FY2026 | FY2025 | FY2024 |',
        '|---|---:|---:|---:|',
    ]
    for label, values in ROWS.items():
        lines.append('| ' + label + ' | ' + ' | '.join(values) + ' |')
    lines += [
        '| Reconstructed OCF | ' + ' | '.join(map(str, ocf)) + ' |',
        '| Residual to filing | 0.0 | 0.0 | 0.0 |', '',
        '## Income and cash checks', '',
        f'- Calculated operating profit before other income/financing: {operating_profit}.',
        f'- Less interest plus other income produces pretax income {pretax}; less taxes produces 4413.5.',
        f'- Exact D&A reclassification reproduces operating profit: {historical_recast}.',
        f'- Management adjusted EBIT reconciliation: {adjusted}. Its base labeled EBIT is pretax income; the adjusted measure retains client-strategy financing and selected income.',
        f'- Total cash movement: {change_total}; restricted component: {restricted_change}; corporate component: {corporate_change}. All tie exactly.',
        f'- Contract cash adjustment: {contract_net}. Contract asset change is 90.0, leaving {contract_residual} versus investment less amortization. Do not force that residual into cash working capital; investigate FX/acquisition/other movements.', '',
        '## Existing Lab 10 diagnosis', '',
        f'- Existing forecast balance/liquidity checks pass. FY2027 EBIT is {income["Operating income (EBIT)"][0]:.2f}; this is a forecast, not a historical reconciliation.',
        f'- Evaluating its rounded contribution/R&D ratios at FY2026 revenue and historical D&A gives operating profit {old_base_op:.2f}, versus {operating_profit}. The D&A reclassification is sound; rounding explains this small difference.',
        '- The model omits other income and simplifies interest. Thus a correct operating-cost recast is not a complete net-income or cash reconciliation.',
        '- Cash-flow items beyond net income and D&A sum to +441.8 in FY2026. The old working-capital allowance cannot be assumed to represent these economically different adjustments.',
        '- Retaining stock compensation as an expense can be a valuation policy, but reported cash flow must first add it back. Its equity credit/dilution must also be tracked.',
        '- Deferred contract investment and amortization need paired schedules. Neither their gross investment nor their net difference should be deducted twice.', '',
        '## Transition to FCFF: what is and is not established', '',
        f'- OCF less PP&E/intangible investment: {levered}; a levered starting measure, not normalized FCFF.',
        f'- Prior proxy reproduced: {levered} + 141.0 x 77% - 92.9 x 77% - 242.6 = {proxy}.',
        '- 141.0 is non-client interest EXPENSE, not a separately disclosed corporate CASH-interest payment. 23% is a tax proxy. No exact corporate cash-interest split has been established.',
        '- Removing non-client investment income requires consistent treatment of the corresponding assets; pledged investments cannot simply be labeled freely distributable.',
        '- Management excludes selected initiative/legal/venture items from adjusted earnings. Expense normalization does not prove matching cash payments or accrual reversals, so do not apply those adjustments mechanically to OCF.',
        '- Next build: reported earnings -> explicit normalization -> operating taxes -> paired noncash/reinvestment schedules -> FCFF, with a reconciliation back to reported OCF.', '',
        '## Validation and remaining evidence', '',
        '- PASS: three reported OCF totals; income, D&A recast, adjusted measure, and corporate/restricted cash ties.',
        '- ' + failure_check,
        '- This is an AI-authored failure probe, not the assignment\'s human-authored AI-off Locked Changed-Input Record or training-case reconciliation.',
        '- Historical statement reconciliation is complete at displayed precision. Normalized FCFF is provisional pending interest/tax classification, contract asset residual, and normalization cash timing.',
        '- Original lab and Edition A files were not edited. No new share value is claimed.', '',
    ]
    (ROOT / 'ADP_cash_flow_reconciliation.md').write_text('\n'.join(lines), encoding='utf-8')
    print('PASS: 3-year OCF, income, cash ties, and missing-investment failure probe.')
    print(f'Historical operating profit {operating_profit}; levered starting cash {levered}; provisional prior proxy {proxy}.')
    print('Wrote ADP_cash_flow_reconciliation.md. Normalized FCFF remains provisional.')


if __name__ == '__main__':
    main()

'''

# ===== adp_project_forecast.py: frozen reviewed engine =====
EMBEDDED['adp_project_forecast'] = r'''
"""ADP Edition B: explicit five-year schedules, no DCF yet. USD millions.
Run py adp_project_forecast.py; reports and full traces are written locally.
All forecast policies are analyst assumptions; see generated report.
"""
from copy import deepcopy
from pathlib import Path
import json
import math
from adp_reconciliation import reconcile, ROWS

ROOT = Path(__file__).resolve().parent
SOURCE = 'https://www.sec.gov/Archives/edgar/data/8670/000000867026000030/adp-20260630.htm'
BASE = dict(cash=4230.1, ar=3521.1, current_assets=852.1, ppe=641.3,
            intangibles=1653.3, contracts=3244.1, client_assets=43957.8,
            fixed_assets=388.6+1420.5+3284.4,
            ap=162.5, accruals=3218.5-1, payroll=1039.4,
            deferred_revenue=267.5+385.9, tax_payable=110.3,
            deferred_tax=339.1, debt=4965.1, repos=139.3,
            client_liabilities=44415.5, fixed_liabilities=306.7+1141.4+671.9,
            equity=6031.2)
ASSETS = ('cash','ar','current_assets','ppe','intangibles','contracts',
          'client_assets','fixed_assets')
LIABILITIES = ('ap','accruals','payroll','deferred_revenue','tax_payable',
               'deferred_tax','debt','repos','client_liabilities','fixed_liabilities')
WC_ASSETS = ('ar', 'current_assets')
WC_LIABS = ('ap', 'accruals', 'payroll', 'deferred_revenue')
ASSUMPTIONS = dict(growth=[.055]*5, contract_spend_ratio=1307.9/21947.4,
                   contract_amort_rate=1200.5/3154.1,
                   core_cost_ratio=(11760.2+4408.2-585.9-1200.5)/21947.4,
                   ppe_capex=212.5, software_ratio=468.5/21947.4,
                   depreciation_rate=201.1/655.4, intangible_amort_rate=384.8/1603,
                   tax_rate=.23, deferred_tax_fraction=0.,
                   payable_fraction=110.3/(1316.8-156.4),
                   financing_interest=141., strategy_net_income=278.1-318.3,
                   distributions=3500., stock_comp_ratio=242.6/21947.4,
                   wc_scale=1.)


def close(a, b, name):
    if not math.isfinite(a) or not math.isfinite(b) or abs(a-b) > 1e-7:
        raise ArithmeticError(f'{name}: {a} != {b}')


def balance(s):
    assets = sum(s[k] for k in ASSETS)
    liabilities = sum(s[k] for k in LIABILITIES)
    close(assets, liabilities+s['equity'], 'Balance sheet')
    return assets, liabilities


def taxes(profit, opening_payable, a):
    expense = max(profit, 0)*a['tax_rate']
    deferred = expense*a['deferred_tax_fraction']
    current = expense-deferred
    ending_payable = current*a['payable_fraction']
    cash = current-(ending_payable-opening_payable)
    return dict(expense=expense, deferred=deferred, current=current,
                ending_payable=ending_payable, cash=cash)


def forecast(a):
    a = deepcopy(a)
    if len(a['growth']) != 5 or any(g <= -1 for g in a['growth']):
        raise ValueError('Five growth rates above -100% required')
    for key in ('revenue_path','core_cost_path','contract_spend_path','strategy_net_path',
                'software_capex_path','stock_comp_path','wc_revenue_path'):
        if key in a and (len(a[key]) != 5 or any(not math.isfinite(x) for x in a[key])):
            raise ValueError(f'{key}: five finite amounts required')
    if not 0 <= a['tax_rate'] <= 1 or not 0 <= a['deferred_tax_fraction'] <= 1:
        raise ValueError('Invalid tax assumptions')
    balance(BASE)
    prev = deepcopy(BASE)
    rev_prev = 21947.4
    wc_prev = a.get('wc_base_revenue', 21947.4)
    operating_tax_payable = BASE['tax_payable']
    results = []
    for index, (year, growth) in enumerate(zip(range(2027,2032), a['growth'])):
        rev = a['revenue_path'][index] if 'revenue_path' in a else rev_prev*(1+growth)
        if rev <= 0:
            raise ValueError('Revenue must be positive')
        s = deepcopy(prev)
        spend = (a['contract_spend_path'][index] if 'contract_spend_path' in a
                 else rev*a['contract_spend_ratio'])
        amort = min(prev['contracts'], prev['contracts']*a['contract_amort_rate'])
        s['contracts'] = prev['contracts']+spend-amort
        depr = min(prev['ppe'], prev['ppe']*a['depreciation_rate'])
        intangible_amort = min(prev['intangibles'], prev['intangibles']*a['intangible_amort_rate'])
        software = (a['software_capex_path'][index] if 'software_capex_path' in a
                    else rev*a['software_ratio'])
        s['ppe'] += a['ppe_capex']-depr
        s['intangibles'] += software-intangible_amort
        # Aggregate contract amortization is removed from base costs, then
        # charged exactly once. No invented split between SG&A and service costs.
        core_cost = (a['core_cost_path'][index] if 'core_cost_path' in a
                     else rev*a['core_cost_ratio'])
        strategy_net = (a['strategy_net_path'][index] if 'strategy_net_path' in a
                        else a['strategy_net_income']*(rev/21947.4))
        operating_earnings = rev-core_cost-amort-depr-intangible_amort+strategy_net
        interest = a['financing_interest']
        pretax = operating_earnings-interest
        tax = taxes(pretax, prev['tax_payable'], a)
        op_tax = taxes(operating_earnings, operating_tax_payable, a)
        operating_tax_payable = op_tax['ending_payable']
        ni = pretax-tax['expense']
        wc_revenue = a['wc_revenue_path'][index] if 'wc_revenue_path' in a else rev
        for key in WC_ASSETS+WC_LIABS:
            # Opening ratios retained. wc_scale changes incremental investment,
            # not the full stock, avoiding a first-year revaluation.
            s[key] += BASE[key]/a.get('wc_base_revenue',21947.4)*(wc_revenue-wc_prev)*a['wc_scale']
        wc_investment = (sum(s[k]-prev[k] for k in WC_ASSETS)
                         -sum(s[k]-prev[k] for k in WC_LIABS))
        s['tax_payable'] = tax['ending_payable']
        s['deferred_tax'] += tax['deferred']
        stock_comp = (a['stock_comp_path'][index] if 'stock_comp_path' in a
                      else rev*a['stock_comp_ratio'])
        cfo = (ni+depr+intangible_amort+amort+stock_comp+tax['deferred']
               +(s['tax_payable']-prev['tax_payable'])-spend-wc_investment)
        capex = a['ppe_capex']+software
        investing = -capex
        financing = -a['distributions'] # No new borrowing or debt retirement.
        s['cash'] += cfo+investing+financing
        # Compensation expense is noncash, with its corresponding equity credit.
        s['equity'] += ni+stock_comp-a['distributions']
        assets, liabilities = balance(s)
        close(s['cash']-prev['cash'], cfo+investing+financing, 'Cash-flow tie')
        close(s['contracts']-prev['contracts'], spend-amort, 'Contract roll-forward')
        close(tax['expense'], tax['cash']+tax['deferred']
              +s['tax_payable']-prev['tax_payable'], 'Tax tie')
        # Retain stock compensation as an economic expense in FCFF, while
        # reconciling reported-style CFO with its required noncash addback.
        fcff = (operating_earnings-op_tax['cash']+depr+intangible_amort
                +amort-spend-wc_investment-capex)
        fcff_from_cfo = cfo+interest-(op_tax['cash']-tax['cash'])-stock_comp-capex
        close(fcff, fcff_from_cfo, 'Independent FCFF route')
        if min(s[k] for k in ASSETS+LIABILITIES) < -1e-7:
            raise ArithmeticError(f'FY{year}: negative balance requires funding/reclassification')
        results.append(dict(year=year, revenue=rev, core_cost=core_cost,
                            operating_earnings=operating_earnings, strategy_net=strategy_net,
                            interest=interest, pretax=pretax, net_income=ni,
                            contract_spend=spend, contract_amort=amort,
                            depreciation=depr, intangible_amort=intangible_amort,
                            software_capex=software, ppe_capex=a['ppe_capex'],
                            wc_investment=wc_investment, stock_comp=stock_comp,
                            tax=tax, operating_tax=op_tax, cfo=cfo, investing=investing,
                            financing=financing, fcff=fcff, opening_cash=prev['cash'],
                            balance=s, total_assets=assets, total_liabilities=liabilities))
        prev, rev_prev = s, rev
        wc_prev = wc_revenue
    return results


def main():
    reconcile(ROWS)
    rows = forecast(ASSUMPTIONS)
    # AI-authored pre-run prediction: more contract investment, with everything
    # else fixed, lowers same-year FCFF and increases the contract asset.
    changed = deepcopy(ASSUMPTIONS)
    changed['contract_spend_ratio'] += .01
    stressed = forecast(changed)
    close(rows[0]['fcff']-stressed[0]['fcff'], rows[0]['revenue']*.01,
          'Contract investment directional test')
    if not stressed[0]['balance']['contracts'] > rows[0]['balance']['contracts']:
        raise AssertionError('Contract asset did not increase')
    deferred_case = deepcopy(ASSUMPTIONS)
    deferred_case['deferred_tax_fraction'] = .15
    deferred_rows = forecast(deferred_case)
    if not deferred_rows[0]['tax']['cash'] < rows[0]['tax']['cash']:
        raise AssertionError('Deferred tax did not delay cash taxes')
    distribution_case = deepcopy(ASSUMPTIONS)
    distribution_case['distributions'] += 100
    distribution_rows = forecast(distribution_case)
    for base, changed_row in zip(rows, distribution_rows):
        close(base['fcff'], changed_row['fcff'], 'Distribution independence of FCFF')
    loss_tax = taxes(-100, 0, ASSUMPTIONS)
    close(loss_tax['expense'], 0, 'No invented loss tax benefit')
    broken = deepcopy(BASE)
    broken['contracts'] += 100
    try:
        balance(broken)
    except ArithmeticError:
        pass
    else:
        raise AssertionError('Broken base year accepted')
    report = ['# ADP Edition B: five-year scheduled forecast', '',
              'Working model, not a completed valuation. USD millions; FY2027–FY2031.', '',
              f'Historical basis: [FY2026 10-K]({SOURCE}), statements and Notes 1–2; research October 19, 2026. Base-year cash-flow reproduction is in [the reconciliation report](ADP_cash_flow_reconciliation.md).', '',
              '## Income and cash-flow forecast', '',
              '| Item | '+' | '.join(str(r['year']) for r in rows)+' |',
              '|---|'+'---:|'*5]
    fields = [('Revenue','revenue'),('Operating earnings incl. client strategy','operating_earnings'),
              ('Corporate financing interest','interest'),('Pretax income','pretax'),
              ('Net earnings','net_income'),('Contract spending','contract_spend'),
              ('Contract amortization','contract_amort'),('PP&E depreciation','depreciation'),
              ('Intangible amortization','intangible_amort'),('Working-capital investment','wc_investment'),
              ('Stock compensation','stock_comp'),('PP&E capex','ppe_capex'),
              ('Software capex','software_capex'),('Operating cash flow','cfo'),
              ('Investing cash flow','investing'),('Financing cash flow','financing'),
              ('FCFF after economic compensation cost','fcff')]
    for label,key in fields:
        report.append('| '+label+' | '+' | '.join(f'{r[key]:,.2f}' for r in rows)+' |')
    for label,key in [('Tax expense','expense'),('Deferred tax','deferred'),
                      ('Current tax provision','current'),('Cash taxes','cash')]:
        report.append('| '+label+' | '+' | '.join(f'{r["tax"][key]:,.2f}' for r in rows)+' |')
    report += ['', '## Balance sheet', '', '| Item | '+' | '.join(str(r['year']) for r in rows)+' |',
               '|---|'+'---:|'*5]
    for key in ASSETS+LIABILITIES+('equity',):
        report.append('| '+key+' | '+' | '.join(f'{r["balance"][key]:,.2f}' for r in rows)+' |')
    for key in ('total_assets','total_liabilities'):
        report.append('| '+key+' | '+' | '.join(f'{r[key]:,.2f}' for r in rows)+' |')
    report += ['', '## Assumptions and interpretation', '',
               '- Revenue grows 5.5% annually: inherited first-year guidance midpoint, extended by judgment. No segment/client-yield forecast is claimed.',
               '- Core operating costs exclude contract amortization and D&A; historical aggregate costs are recast before applying the ratio. Contract amortization is charged once separately.',
               '- Contract investment scales with revenue; amortization uses an opening-asset rate. This is an aggregate proxy, not a cohort schedule. No unexplained historical residual is repeated as forecast cash.',
               '- Net receivables, other current assets, payables, accrued operating liabilities, payroll and deferred revenue retain opening revenue ratios. The current debt portion is removed from accruals and included in debt once. Classification is provisional; future noncurrent operating movements are not separately modeled.',
               '- Deferred tax expense defaults to zero. Current tax is 23% of positive pretax income; payable timing uses the historical ending-payable/current-provision ratio. This is an analyst timing proxy, not a proven tax-payment calendar. Loss tax benefits are not assumed.',
               '- Operating FCFF uses a separate unlevered cash-tax/payable schedule; its tax shield timing is reconciled to CFO rather than assuming interest times 77% always equals the cash adjustment.',
               '- Client-strategy interest is retained in operations: derived strategy income 371.0 minus 92.9; strategy cost 459.3 minus 141.0. Their net contribution scales with revenue. Corporate financing expense remains 141.0 as a proxy. Other nonoperating income is not forecast. This separation requires further validation before DCF.',
               '- Client principal, repos, and other fixed balances are held constant. No client principal becomes distributable corporate cash. No acquisitions, debt maturity/refinancing, lease changes or OCI are forecast.',
               '- Stock compensation is added back to accounting CFO and credited to equity, but deducted from cash available for valuation. A future per-share bridge must avoid charging the same future awards again.',
               '- Distribution policy is 3500 annually, inherited judgment. It affects cash and equity, not enterprise FCFF. No minimum cash or revolver is silently imposed.',
               '- The starting balance sheet ties to reported totals. Forecast balance sheets articulate under stated policies; this does not independently prove those policies are correct.', '',
               '## Validation', '',
               '- PASS: historical OCF and opening balance sheet; five annual balance sheets, cash ties, contract roll-forwards, tax ties, and two FCFF routes.',
               '- PASS: extra contract investment lowers first-year FCFF by exactly the extra spending and increases the contract asset.',
               '- PASS: corrupted opening contract asset triggers failure.',
               '- PASS: deferred-tax scenario reduces first-year cash tax and still articulates; no tax benefit is invented for a loss. Higher distributions leave FCFF unchanged.',
               '- These are AI-authored checks; they do not replace the human AI-off locked prediction, training-case test or recorded cold run.', '',
               '## Next valuation work', '',
               'Validate growth/margin and client-yield scenarios; refine operating classifications, cash-tax and contract assumptions; refresh WACC; decide bridge/share policy; implement dated discounting and terminal reinvestment. No price target is produced here.', '']
    (ROOT/'ADP_scheduled_forecast.md').write_text('\n'.join(report),encoding='utf-8')
    (ROOT/'ADP_scheduled_forecast.json').write_text(json.dumps(dict(assumptions=ASSUMPTIONS,
                      opening=BASE, years=rows),indent=2,allow_nan=False),encoding='utf-8')
    print('PASS: all historical/opening and five-year articulation checks; directional and failure probes.')
    print('FY2027 FCFF %.2f; FY2031 FCFF %.2f (provisional assumptions, no valuation).'%
          (rows[0]['fcff'],rows[-1]['fcff']))


if __name__ == '__main__':
    main()

'''

# ===== adp_assumption_challenge.py: frozen reviewed engine =====
EMBEDDED['adp_assumption_challenge'] = r'''
"""Causal operating challenges, not price targets or probability forecasts.
Run py adp_assumption_challenge.py. Original reference assumptions are preserved.
"""
from copy import deepcopy
from pathlib import Path
import json
from adp_project_forecast import ASSUMPTIONS, forecast, close

ROOT = Path(__file__).resolve().parent
RELEASE = 'https://www.sec.gov/Archives/edgar/data/8670/000000867026000025/q4fy26exhibit99.htm'
FILING = 'https://www.sec.gov/Archives/edgar/data/8670/000000867026000030/adp-20260630.htm'
# Fee revenue here is an analyst residual, not a reported segment or pure organic sales.
FEE_BASE = 21947.4-4607.3-1354.8
PASS_BASE = 4607.3
FEE_CORE_COST = (11760.2+4408.2-585.9-1200.5)-PASS_BASE


def case(fee_growth, pass_growth, balance_growth, yields, cost_pressure, contract_extra):
    a = deepcopy(ASSUMPTIONS)
    a['wc_base_revenue'] = FEE_BASE
    paths = {k: [] for k in ('revenue_path','core_cost_path',
                             'contract_spend_path','strategy_net_path',
                             'software_capex_path','stock_comp_path','wc_revenue_path')}
    fee, passthrough, average_funds = FEE_BASE, PASS_BASE, 40400.
    drivers = []
    for i in range(5):
        fee *= 1+fee_growth[i]
        passthrough *= 1+pass_growth[i]
        average_funds *= 1+balance_growth[i]
        client_interest = average_funds*yields[i]
        revenue = fee+passthrough+client_interest
        # Pass-through costs match revenue dollar for dollar. Client yield does
        # not create a proportional service cost, unlike the old aggregate model.
        core_cost = fee*(FEE_CORE_COST/FEE_BASE+cost_pressure[i])+passthrough
        contract_spend = fee*(1307.9/FEE_BASE+contract_extra[i])
        strategy_net = 5.*average_funds/(40400*1.035)
        for key, value in zip(paths,(revenue,core_cost,contract_spend,strategy_net,
                                    fee*468.5/FEE_BASE,fee*242.6/FEE_BASE,fee)):
            paths[key].append(value)
        drivers.append(dict(fee_revenue=fee,pass_through=passthrough,
                            average_funds=average_funds,effective_yield=yields[i],
                            client_interest=client_interest,cost_pressure=cost_pressure[i],
                            contract_extra=contract_extra[i]))
    a.update(paths)
    return dict(inputs=a, drivers=drivers, years=forecast(a))


def main():
    five = lambda x: [x]*5
    reference = dict(inputs=deepcopy(ASSUMPTIONS),drivers=[],years=forecast(ASSUMPTIONS))
    proposed = case([.045,.045,.0425,.04,.04],five(.06),five(.035),
                    [.037,.037,.036,.035,.034],five(0),five(0))
    downside = case([.01,.02,.03,.035,.04],five(.04),[0,.01,.02,.025,.03],
                    [.034,.032,.031,.032,.033],[.01,.015,.015,.01,.005],five(.005))
    upside = case(five(.06),five(.06),five(.04),
                  [.037,.038,.038,.037,.037],[-.003,-.005,-.007,-.007,-.007],five(0))
    cases = dict(reference=reference,proposed_base=proposed,downside=downside,upside=upside)
    # Controlled one-variable causal probes, authored by AI before execution.
    # Increase only the first-year cash operating-cost amount: FCFF must fall.
    margin_a = deepcopy(proposed['inputs'])
    margin_a['core_cost_path'][0] += .01*proposed['years'][0]['revenue']
    margin_rows = forecast(margin_a)
    if not margin_rows[0]['fcff'] < proposed['years'][0]['fcff']:
        raise AssertionError('Higher cash cost did not lower cash flow')
    # Isolate a 50bp effective portfolio-yield decline, leaving costs/spending fixed.
    yield_a = deepcopy(proposed['inputs'])
    yield_a['revenue_path'][0] -= proposed['drivers'][0]['average_funds']*.005
    yield_rows = forecast(yield_a)
    if not yield_rows[0]['fcff'] < proposed['years'][0]['fcff']:
        raise AssertionError('Lower portfolio yield did not lower cash flow')
    # Isolate zero-margin pass-through growth. It leaves operating earnings
    # unchanged; ancillary investment and tax timing can still affect FCFF.
    pass_a = deepcopy(proposed['inputs'])
    pass_a['revenue_path'][0] += 100
    pass_a['core_cost_path'][0] += 100
    pass_rows = forecast(pass_a)
    close(pass_rows[0]['operating_earnings'],proposed['years'][0]['operating_earnings'],
          'Zero-margin pass-through earnings')
    close(forecast(ASSUMPTIONS)[0]['fcff'], reference['years'][0]['fcff'], 'Reference preserved')
    report = ['# ADP assumption challenge — Edition B', '',
              'Research and scenario design: October 19, 2026. Valuation cutoff October 16. USD millions. AI-authored proposals; student endorsement pending. No scenario probabilities or price targets.', '',
              '## Evidence and challenges', '',
              f'[July 29 guidance]({RELEASE}): FY2027 revenue growth 5–6%, retention down 10–30bp, adjusted margin expansion 70–90bp, client interest 1540–1560 and extended-strategy contribution 1545–1565. PEO fee growth guidance excludes zero-margin benefits. These are management expectations, not five-year promises.', '',
              f'[10-K]({FILING}), revenue/cost presentation and non-GAAP reconciliation: the model separates zero-margin benefits and client interest from the remaining revenue. The remaining category is an analyst residual, not a reported segment. Unadjusted operating costs and management adjusted margins are not definitionally identical.', '',
              '| Driver | Proposed value and basis | Challenge | Evidence that changes it |',
              '|---|---|---|---|',
              '| Fee-related residual growth | 4.5%, 4.5%, 4.25%, 4%, 4%; analyst fade, calibrated within first-year consolidated guidance | Retention/employment/pricing can disappoint; first-year total guidance cannot justify perpetual fee growth | Retention below guidance, bookings conversion, pays-per-control and PEO fee growth |',
              '| Benefits pass-through | 6% annually; analyst assumption | This creates revenue without direct profit; aggregate margin methods can invent profit | Reported benefits costs and revenue mix |',
              '| Client balances | Average 40,400 grows 3.5% annually; first year guidance midpoint | Balances depend on payroll, employment and timing | Average balances, not just fiscal closing balance |',
              '| Effective portfolio yield | 3.7%, 3.7%, 3.6%, 3.5%, 3.4%; first year guidance, later analyst fade | Existing maturities delay rate effects; a Fed cut is not an equal instant portfolio-yield cut | Maturity/reinvestment data, yield and financing outlook |',
              '| Extended-strategy net adjustment | 5 in FY2027 then scales with balances; derived midpoint difference, not a separately guided line | Gross income and financing costs could diverge | Full strategy contribution reconciliation |',
              '| Cash service-cost ratio | Exact residual historical ratio, flat in proposed base | AI/R&D/service spending may rise faster than fees | Cost trends, productivity evidence, retention; stock price expectations are not operating evidence |',
              '| Contract spending | Historical spending/fee residual ratio | Sales and implementation spending can rise before revenue | Spending, amortization and retained-customer economics |', '',
              '## Causal cases', '',
              '- Proposed base: moderate fee growth fades, benefits remain zero-margin, and portfolio income gradually normalizes. No discretionary margin-expansion benefit is assumed.',
              '- Downside: weak employment/retention slows fees, client balances stall initially, effective yield falls, cash service-cost ratio rises 1–1.5 percentage points of fee revenue initially, and contract spending rises 0.5 points. These stresses are analyst choices, not company guidance.',
              '- Upside: fee growth stays 6%, balances grow 4%, yields remain supportive, and cash service-cost ratio improves gradually by up to 0.7 points. Productivity must be evidenced before adopting it.',
              '- Historical partner concern from Lab 10: a student-described partner questioned optimistic margins because AI research is expensive. Challenger name was not supplied. This record credits that historical concern without claiming a new exchange or treating the hypothetical Lab 12 dialogue as real.', '',
              '| Case | FY2027 revenue | FY2027 margin* | FY2027 FCFF | FY2031 revenue | FY2031 margin* | FY2031 FCFF | Five-year FCFF sum** |',
              '|---|---:|---:|---:|---:|---:|---:|---:|']
    for name,c in cases.items():
        first,last = c['years'][0],c['years'][-1]
        report.append(f'| {name} | {first["revenue"]:.2f} | {first["operating_earnings"]/first["revenue"]:.2%} | {first["fcff"]:.2f} | {last["revenue"]:.2f} | {last["operating_earnings"]/last["revenue"]:.2%} | {last["fcff"]:.2f} | {sum(r["fcff"] for r in c["years"]):.2f} |')
    f = proposed['years'][0]
    d = proposed['drivers'][0]
    report += ['', '*Model operating earnings including client strategy divided by reported revenue; not automatically management adjusted EBIT margin.',
               '**Undiscounted sum is a cash-flow comparison, not enterprise value or an investment return.', '',
               '## First-year guidance cross-check', '',
               f'- Proposed reported revenue growth: {f["revenue"]/21947.4-1:.2%}.',
               f'- Proposed client interest: {d["client_interest"]:.2f}; strategy contribution including net adjustment: {d["client_interest"]+f["strategy_net"]:.2f}. These fall inside the cited first-year ranges.',
               '- No automatic match to adjusted margin guidance is claimed. A formal normalization bridge and cash timing are still required. Guidance compliance is not independent proof of forecast accuracy.', '',
               '## Controlled challenge results', '',
               f'- First-year operating cost +1% of revenue: FCFF change {margin_rows[0]["fcff"]-f["fcff"]:+.2f}.',
               f'- First-year effective portfolio yield -50bp: FCFF change {yield_rows[0]["fcff"]-f["fcff"]:+.2f}. Costs held fixed; linked tax, working capital and investment recalculate.',
               '- PASS: equal benefits revenue/cost additions create no direct operating profit. PASS: reference restored without input mutation.',
               '- Every case and controlled probe passes five-year statement, cash, tax and FCFF-route checks. These are AI-authored probes, not the student locked AI-off record.', '',
               '## Judgment and unresolved limits', '',
               '- Qualify the old aggregate 5.5% forecast: it mixed fee growth, zero-margin revenue and client-funds income. Use component scenarios for further development, while retaining the old reference for comparison.',
               '- Reject the inference that AI benefits being priced into the stock validates a profit-margin assumption.',
               '- The downside can undermine an initiation thesis; its actual effect on the committee action cannot be measured until the dated DCF and equity bridge are complete.',
               '- Average client balances are operating drivers only. Closing client assets/obligations remain frozen in the underlying statements; a complete client principal/funding schedule is still needed. No claim of full client-funds integration is made.',
               '- Software investment, compensation and incremental operating working capital now scale with fee-related revenue, so pass-throughs and portfolio yield do not automatically drive these costs. This is a simplified proxy: PEO pass-through settlement exposure and detailed operating classifications remain unmodeled. No causal retention-to-revenue formula is invented.',
               '- Proposed base is a candidate for student review, not a silently approved replacement for the reference or a final recommendation.', '']
    (ROOT/'ADP_assumption_challenge.md').write_text('\n'.join(report),encoding='utf-8')
    (ROOT/'ADP_assumption_challenge.json').write_text(json.dumps(cases,indent=2,allow_nan=False),encoding='utf-8')
    print('PASS: four cases and three controlled probes; reference preserved.')
    for name,c in cases.items():
        print(f'{name}: FY2027 FCFF {c["years"][0]["fcff"]:.2f}; FY2031 {c["years"][-1]["fcff"]:.2f}')


if __name__ == '__main__':
    main()

'''

# ===== adp_project_dcf.py: frozen reviewed engine =====
EMBEDDED['adp_project_dcf'] = r'''
"""Dated pro-forma-driven FCFF DCF. Run py adp_project_dcf.py.
Standard library only. Outputs ADP_project_DCF.md and JSON traces.
"""
from datetime import date
from pathlib import Path
import json
import math
from adp_assumption_challenge import case
from adp_project_forecast import close

ROOT = Path(__file__).resolve().parent
VALUATION_DATE = date(2026,10,16)
PRICE = 288.90
SHARES = 403.3 # FY2026 diluted weighted average; disclosed denominator proxy.
BASIC_WEIGHT_SHARES = 397.262737 # July 31 cover page, not October count.
RF, BETA, ERP, KD, TAX = .0509, .83, .045, .0514, .23
DEBT = 4803.+1.8 # Notes fair value plus other debt; June 30 proxy.
OPERATING_CASH = 500. # Analyst buffer, not company requirement.
EXCESS_CASH = 4230.1-OPERATING_CASH-.7 # Exclude pledged cash.
G, TERMINAL_ROIC = .025, .20
TREASURY = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve'
FILING = 'https://www.sec.gov/Archives/edgar/data/8670/000000867026000030/adp-20260630.htm'


def cases(shift=0.):
    five = lambda x: [x]*5
    base = case([g+shift for g in [.045,.045,.0425,.04,.04]],five(.06),five(.035),
                [.037,.037,.036,.035,.034],five(0),five(0))
    if shift:
        return base
    return dict(base=base,
                downside=case([.01,.02,.03,.035,.04],five(.04),[0,.01,.02,.025,.03],
                              [.034,.032,.031,.032,.033],[.01,.015,.015,.01,.005],five(.005)),
                upside=case(five(.06),five(.06),five(.04),
                            [.037,.038,.038,.037,.037],[-.003,-.005,-.007,-.007,-.007],five(0)))


def dcf(rows, wacc, g=G, roic=TERMINAL_ROIC, cash=EXCESS_CASH, debt=DEBT, shares=SHARES):
    if not all(math.isfinite(x) for x in (wacc,g,roic,cash,debt,shares)):
        raise ValueError('Nonfinite valuation input')
    if wacc <= g or g < 0 or roic <= g or shares <= 0 or debt < 0 or cash < 0:
        raise ValueError('Require WACC > growth >= 0, ROIC > growth, positive shares')
    if len(rows) != 5:
        raise ValueError('Five pro-forma years required')
    flows=[]
    for i,r in enumerate(rows):
        end = date(r['year'],6,30)
        years = (end-VALUATION_DATE).days/365
        if years <= 0:
            raise ValueError('Past cash flow cannot be valued as future')
        fraction = ((end-VALUATION_DATE).days/(end-date(r['year']-1,6,30)).days
                    if i == 0 else 1.)
        cashflow = r['fcff']*fraction
        flows.append(dict(year=r['year'],annual_fcff=r['fcff'],remaining_fraction=fraction,
                          valued_fcff=cashflow,discount_years=years,pv=cashflow/(1+wacc)**years))
    # Economic compensation stays expensed in operating earnings. Terminal cash
    # taxes normalize to accrual tax; reinvestment funds perpetual growth.
    nopat = rows[-1]['operating_earnings']*(1-TAX)*(1+g)
    reinvestment = nopat*g/roic
    terminal_fcff = nopat-reinvestment
    if terminal_fcff <= 0:
        raise ValueError('Nonpositive terminal cash flow requires separate review')
    tv = terminal_fcff/(wacc-g)
    terminal_pv = tv/(1+wacc)**flows[-1]['discount_years']
    explicit = sum(f['pv'] for f in flows)
    enterprise = explicit+terminal_pv
    equity = enterprise+cash-debt
    close(equity-enterprise,cash-debt,'Enterprise-equity bridge')
    return dict(flows=flows,wacc=wacc,g=g,roic=roic,terminal_nopat=nopat,
                terminal_reinvestment=reinvestment,terminal_fcff=terminal_fcff,
                terminal_pv=terminal_pv,explicit_pv=explicit,enterprise=enterprise,
                cash_added=cash,debt_subtracted=debt,equity=equity,shares=shares,
                per_share=equity/shares,tv_share=terminal_pv/enterprise)


def main():
    equity_weight_value = PRICE*BASIC_WEIGHT_SHARES
    ke = RF+BETA*ERP
    wacc = (equity_weight_value*ke+DEBT*KD*(1-TAX))/(equity_weight_value+DEBT)
    operating = cases()
    values = {name:dcf(c['years'],wacc) for name,c in operating.items()}
    base = values['base']
    grid = [[dcf(operating['base']['years'],w,g)['per_share']
             for g in (.015,.025,.035)] for w in (wacc-.01,wacc,wacc+.01)]
    for row in grid:
        if not row[0] < row[1] < row[2]:
            raise AssertionError('Growth monotonicity failed')
    for j in range(3):
        if not grid[0][j] > grid[1][j] > grid[2][j]:
            raise AssertionError('WACC monotonicity failed')
    close(dcf(operating['base']['years'],wacc,cash=EXCESS_CASH+100)['equity']-base['equity'],100,'Cash bridge')
    close(dcf(operating['base']['years'],wacc,debt=DEBT+100)['equity']-base['equity'],-100,'Debt bridge')
    try:
        dcf(operating['base']['years'],G)
    except ValueError:
        pass
    else:
        raise AssertionError('Invalid terminal spread accepted')
    # Independent known-answer fixture: terminal value plus five dated payments.
    fixture = [dict(year=y,fcff=100.,operating_earnings=100/(1-TAX)) for y in range(2027,2032)]
    known = dcf(fixture,.10,g=0,cash=0,debt=0,shares=1)
    end = date(2031,6,30)
    manual = sum(100*((date(2027,6,30)-VALUATION_DATE).days/365 if y==2027 else 1)
                 /1.1**((date(y,6,30)-VALUATION_DATE).days/365) for y in range(2027,2032))
    manual += 1000/1.1**((end-VALUATION_DATE).days/365)
    close(known['equity'],manual,'Known-answer synthetic DCF')
    # Reverse DCF: shift each annual fee-growth assumption, all else fixed.
    def implied_value(shift):
        c = operating['base'] if shift == 0 else cases(shift)
        return dcf(c['years'],wacc)['per_share']
    lo,hi=-.02,.15
    reverse=None
    if implied_value(lo) <= PRICE <= implied_value(hi):
        for _ in range(70):
            mid=(lo+hi)/2
            if implied_value(mid) < PRICE:
                lo=mid
            else:
                hi=mid
        reverse=(lo+hi)/2
        close(implied_value(reverse),PRICE,'Reverse DCF price')
    roic_values={str(r):dcf(operating['base']['years'],wacc,roic=r)['per_share'] for r in (.15,.20,.30)}
    report=['# ADP — dated FCFF DCF and equity bridge','',
            'Valuation: October 16, 2026. Research/run: October 19, 2026. USD millions except per share. Conditional coursework analysis; student decision pending.','',
            '## Result','',
            '| Operating case | Enterprise value | Equity value | Value/share | Terminal share of EV |',
            '|---|---:|---:|---:|---:|']
    for name,v in values.items():
        report.append(f'| {name} | {v["enterprise"]:,.2f} | {v["equity"]:,.2f} | ${v["per_share"]:.2f} | {v["tv_share"]:.1%} |')
    low,high=min(v['per_share'] for v in values.values()),max(v['per_share'] for v in values.values())
    report += ['',f'Operating-case range **${low:.0f}–${high:.0f}/share**, using common WACC and terminal assumptions; base ${base["per_share"]:.2f}. This is not a confidence interval or a complete uncertainty envelope.',
               f'Reference close: $288.90. Proposed action: **watch/defer** while no tested operating case supports an entry with margin of safety. This is a model-dependent proposed judgment, not student endorsement.','',
               '## Discount rate and dated inputs','',
               f'- Risk-free rate: **5.09%**, October 16 ten-year Treasury par yield, [Treasury table]({TREASURY}); retrieved October 19.',
               '- Beta 0.83 and ERP 4.5% are retained analyst assumptions from prior labs, not newly measured October facts. Cost of debt 5.14% is a historical note effective-rate proxy, not a fresh market yield; tax shield 23% is an assumption.',
               f'- Cost of equity {ke:.3%}; financing debt weight {DEBT/(equity_weight_value+DEBT):.2%}; WACC **{wacc:.3%}**. Equity weights use $288.90 times 397.262737M July 31 basic shares; debt uses June fair values. These dated proxies are not October balance-sheet measurements.','',
               '## Timing and terminal convention','',
               '- Year-end discounting uses actual days/365 from October 16. FY2027 FCFF is prorated for only the remaining fiscal-year days; previously elapsed cash flow is excluded. Uniform annual generation is an approximation, not a claim about quarterly seasonality.',
               '- June opening cash/debt remain valuation-date proxies; no unverified stub-period balance-sheet update or buyback adjustment is invented.',
               '- Terminal starts after June 2031. NOPAT grows 2.5%, cash taxes normalize to 23%, and reinvestment = NOPAT × growth / 20% incremental ROIC. ROIC is analyst judgment, tested below; it is not historical reported ROIC.',
               f'- FY2032 NOPAT {base["terminal_nopat"]:.2f}; reinvestment {base["terminal_reinvestment"]:.2f}; FCFF {base["terminal_fcff"]:.2f}. The terminal cash flow replaces the last-year schedule with steady-state economics rather than blindly growing its temporary tax/reinvestment mix.','',
               '## Base-case cash flows','',
               '| Fiscal year | Full-year FCFF | Remaining fraction | FCFF valued | Years to receipt | PV |',
               '|---|---:|---:|---:|---:|---:|']
    for f in base['flows']:
        report.append(f'| {f["year"]} | {f["annual_fcff"]:.2f} | {f["remaining_fraction"]:.4f} | {f["valued_fcff"]:.2f} | {f["discount_years"]:.4f} | {f["pv"]:.2f} |')
    report += ['', '## Enterprise-to-equity bridge','',
               f'[Filing evidence]({FILING}), balance sheet, cover page, Notes 5 and 10. Classification is analyst policy, not a company fair-value assertion.','',
               f'- PV explicit FCFF {base["explicit_pv"]:.2f} + PV terminal {base["terminal_pv"]:.2f} = EV {base["enterprise"]:.2f}.',
               f'- Add excess corporate cash {EXCESS_CASH:.1f}: 4230.1 less 500 operating buffer and 0.7 pledged cash.',
               f'- Subtract corporate financing debt {DEBT:.1f}: 4803.0 notes fair value + 1.8 other debt. Client-strategy repos and their pledged securities stay in operating economics; do not subtract financing twice. Their frozen balances remain a modeling limitation.',
               '- Do not add client principal or 138.6 of pledged corporate securities separately. Operating leases remain operating costs; no additional lease debt deduction. No separate pension/venture asset valuation is assumed.',
               f'- Equity {base["equity"]:.2f} / 403.3M historical diluted average shares = ${base["per_share"]:.2f}. This denominator is a disclosed proxy, not October point-in-time diluted shares. Future stock compensation remains an expense; no second forecast dilution charge is added.',
               f'- Debt carrying-value alternative 4965.1 gives ${dcf(operating["base"]["years"],wacc,debt=4965.1)["per_share"]:.2f}/share. This isolates bridge choice, holding WACC fixed.','',
               '## Base operating case: WACC / perpetual-growth sensitivity','',
               '| WACC | g 1.5% | g 2.5% | g 3.5% |','|---|---:|---:|---:|']
    for w,row in zip((wacc-.01,wacc,wacc+.01),grid):
        report.append('| '+f'{w:.3%}'+' | '+' | '.join(f'${p:.2f}' for p in row)+' |')
    report += ['', 'Terminal ROIC sensitivity (base WACC/g): '+', '.join(f'{float(k):.0%}: ${v:.2f}' for k,v in roic_values.items())+'.', '',
               '## Reverse DCF and conditional decision','',
               (f'Matching $288.90 requires adding **{reverse*100:.2f} percentage points** to every annual fee-growth assumption, holding costs/intensity rules, client yields, WACC and terminal ROIC/g fixed. First-year fee growth becomes {(.045+reverse):.2%}. This solves a conditional market expectation, not a forecast.' if reverse is not None else 'Market price is not bracketed by the tested fee-growth shifts; no implied rate is reported.'),
               f'- Candidate entry screen: at least 20% below base value, approximately ${base["per_share"]*.8:.0f}, provided operating evidence and capital assumptions remain intact. This is an analyst margin-of-safety rule, not proof of the separate 8% total-return hurdle.',
               '- Reassess if retention falls below the guided 91.8–92.0% range, bookings/pays-per-control weaken, costs rise without productivity gains, or client-interest outlook misses its published range. These are monitoring flags, not automatic proof of structural deterioration.',
               '- Reversal toward initiation requires a qualifying price or independently supported cash-flow improvement; structural competitive damage would instead support stopping the initiation thesis.','',
               '## Checks and limits','',
               '- PASS: scenario articulation, bridge arithmetic, cash/debt dollar-for-dollar tests, WACC/g monotonicity, invalid-spread rejection, synthetic independently calculated known answer, and reverse price reconciliation when bracketed.',
               '- Synthetic DCF fixture is not the course-published training-case reconciliation, the human AI-off test, or the recorded fresh-environment cold run.',
               '- Material remaining limits: incomplete intervening-disclosure check, provisional normalization, beta/ERP/debt-cost assumptions, simplified client funding, tax timing, stub timing and stale balance-sheet/share proxies. This completes the runnable DCF layer, not the seven-part submission.', '']
    (ROOT/'ADP_project_DCF.md').write_text('\n'.join(report),encoding='utf-8')
    (ROOT/'ADP_project_DCF.json').write_text(json.dumps(dict(values=values,operating=operating,
                         wacc=wacc,grid=grid,reverse_fee_growth_shift=reverse),indent=2,allow_nan=False),encoding='utf-8')
    print(f'PASS: DCF/bridge/monotonicity/known-answer/reverse checks. WACC {wacc:.3%}')
    for name,v in values.items():
        print(f'{name}: ${v["per_share"]:.2f}; terminal share {v["tv_share"]:.1%}')
    print(f'Wrote ADP_project_DCF.md; reverse fee-growth shift: {reverse}')


if __name__ == '__main__':
    main()

'''

# ===== Single-command finance system =====
PEER_POLICY = """Policy carried forward from Lab 8, before this price refresh:
public profitable USD payroll/HCM operating businesses with recurring service
economics. Qualify client size, PEO mix, acquisition costs and capital intensity.
Use latest completed annual reported GAAP measures for every company, not a
mixture of adjusted, forward and trailing figures. Calendar year ends differ.
This is an annual-snapshot comparison, NOT current TTM. More recent quarterly
disclosures exist but are not spliced into these annual denominators.
"""
PEER_INPUTS = [
    dict(ticker='ADP',price=288.90,eps=10.94,shares=397.8,cash=4230.1,
         debt=4965.1,operating_income=5779.,period='2026-06-30',
         source='https://www.sec.gov/Archives/edgar/data/8670/000000867026000030/adp-20260630.htm'),
    dict(ticker='PAYX',price=111.63,eps=4.89,shares=355.6,cash=1088.2,
         debt=4556.1,operating_income=2510.5,period='2026-05-31',
         source='https://investor.paychex.com/sec-filings/all-sec-filings/content/0001193125-26-280314/payx-ex99_1.htm'),
    dict(ticker='PAYC',price=251.64,eps=8.08,shares=54.8,cash=370.,
         debt=0.,operating_income=567.2,period='2025-12-31',
         source='https://investors.paycom.com/news/news-details/2026/Paycom-Software-Inc--Reports-Fourth-Quarter-and-Year-End-2025-Results/default.aspx'),
]
PRICE_SOURCES = {
    'ADP':'https://stockanalysis.com/stocks/adp/history/',
    'PAYX':'https://stockanalysis.com/stocks/payx/history/',
    'PAYC':'https://chartexchange.com/symbol/nyse-payc/historical/',
}


def load_engines(output):
    modules={}
    for name,source in EMBEDDED.items():
        module=types.ModuleType(name)
        module.__file__=str(Path(__file__).resolve())
        sys.modules[name]=module
        exec(compile(source,f'{__file__}::{name}','exec'),module.__dict__)
        module.ROOT=output
        modules[name]=module
    return modules


def peer_comparison(output):
    results=[]
    seen=set()
    for p in PEER_INPUTS:
        if p['ticker'] in seen:
            raise ValueError('Duplicate peer')
        seen.add(p['ticker'])
        if min(p[k] for k in ('price','eps','shares','operating_income'))<=0:
            raise ValueError('Nonpositive multiple denominator')
        r=dict(p)
        r['market_equity']=p['price']*p['shares']
        r['ev']=r['market_equity']+p['debt']-p['cash']
        r['pe']=p['price']/p['eps']
        r['ev_operating_income']=r['ev']/p['operating_income']
        if abs(r['ev']-r['market_equity']-p['debt']+p['cash'])>1e-7:
            raise ArithmeticError('Peer EV bridge failure')
        results.append(r)
    target=results[0]
    peers=results[1:]
    pe_values=[r['pe']*target['eps'] for r in peers]
    ev_values=[(r['ev_operating_income']*target['operating_income']
                +target['cash']-target['debt'])/403.3 for r in peers]
    lines=['# Comparable-company cross-check','',PEER_POLICY,'',
           'Prices: October 16, 2026 closes. Research: October 19, 2026. Financial figures USD millions; EPS/price USD. Shares are fiscal closing basic counts, not October counts.', '',
           '| Company | Annual end | Price | Diluted EPS | Basic shares | Cash | Debt | GAAP operating income | P/E | EV/operating income |',
           '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in results:
        lines.append(f'| {r["ticker"]} | {r["period"]} | {r["price"]:.2f} | {r["eps"]:.2f} | {r["shares"]:.2f} | {r["cash"]:.2f} | {r["debt"]:.2f} | {r["operating_income"]:.2f} | {r["pe"]:.2f} | {r["ev_operating_income"]:.2f} |')
    lines += ['',f'Peer P/E implied ADP prices: ${min(pe_values):.2f}–${max(pe_values):.2f}; median ${statistics.median(pe_values):.2f}.',
              f'Peer EV/operating-income implied ADP prices: ${min(ev_values):.2f}–${max(ev_values):.2f}; median ${statistics.median(ev_values):.2f}.', '',
              'Definition check: EV = price × fiscal closing basic shares + corporate financing debt carrying value − corporate cash; exclude client principal, marketable investments and operating leases. Denominator = reported revenue less operating costs, before separately reported interest and other income. SBC remains expensed. P/E uses annual GAAP diluted EPS. No extra cash/debt adjustment is made to P/E.',
              'The peer bridge differs deliberately from DCF excess-cash/fair-value-debt policy; do not mix the two bridges. ADP here uses 5779.0 conventional operating profit, not its filing label EBIT (pretax income) or adjusted EBIT. Client-strategy funding differences limit economic comparability even with consistent formulas.',
              'PAYX qualification: SMB exposure and Paycor acquisition/amortization affect reported earnings. PAYC qualification: software mix, facilities spending and different fiscal period; its reported earnings include other-income items and SBC effects. Annual balances/shares are stale proxies for October EV, particularly PAYC. This is a qualified cross-check, not a fully synchronized TTM peer valuation.',
              'With two peers, removing either leaves only the other estimate: the implied ranges show peer-selection dependence. No transaction multiple is used because no defensible control/synergy/time comparison was established.',
              'Do not average these estimates with DCF: market multiples embed different growth and return expectations, while DCF funds explicit reinvestment, uses dated cash flows and normalizes terminal economics.', '', '## Source map','']
    for p in PEER_INPUTS:
        lines.append(f'- [{p["ticker"]} financial statements]({p["source"]}); annual end {p["period"]}. [October 16 price]({PRICE_SOURCES[p["ticker"]]}).')
    (output/'ADP_peer_comparison.md').write_text('\n'.join(lines),encoding='utf-8')
    return dict(inputs=PEER_INPUTS,results=results,pe_implied=pe_values,ev_implied=ev_values)


def validation_record(output):
    record=dict(status='Student completion required; no prediction fabricated',
                human_ai_off_prediction=None,precommit_timestamp_or_commit=None,
                input_name=None,old_value=None,new_value=None,units=None,
                expected_direction=None,actual_direction=None,decision_effect=None,
                diagnosis_or_no_change_reason=None)
    path=output/'Locked Changed-Input Record.json'
    if not path.exists():
        path.write_text(json.dumps(record,indent=2),encoding='utf-8')
    text='''# Finance-system validation status

Automated: historical source reconciliation, statement articulation, cash/tax/
contract ties, separate FCFF routes, scenario isolation, directional cost/yield
probes, rejected missing investment and corrupted balance, DCF boundary and
monotonicity, enterprise/equity checks, synthetic known-answer and peer definition
checks. AI output corrected/qualified: PDF-reading claim corrected in historical
record; aggregate growth qualified; price expectations rejected as margin evidence.

Pending student/external evidence:
- Published training-case known answers must be supplied and independently matched.
  The synthetic fixture is not a substitute for that course requirement.
- Human-authored AI-off prediction and precommit BEFORE its designated changed run.
  The blank JSON record is a template, not completed evidence. Do not backdate it.
- Personal source/definition check and final student judgment/attestation.
- Recorded fresh-environment cold run. --verify-portable can do an unrecorded
  machine check in a new venv, but cannot create the student's recording.
- Edition A checkpoint receipt and final access/submission receipt are unverified.

Economic limitations: normalization remains provisional; client-funding balances
are frozen, contract/tax/working-capital schedules use proxies, balance-sheet and
share counts are dated, and annual peer periods differ. Do not describe this system
as satisfying every assignment requirement merely because code checks pass.
'''
    (output/'VALIDATION STATUS.md').write_text(text,encoding='utf-8')


def run_system(output):
    output.mkdir(parents=True,exist_ok=True)
    mods=load_engines(output)
    captured=io.StringIO()
    stages=[('Historical source reconciliation','adp_reconciliation'),
            ('Five-year statements and tax/contract schedules','adp_project_forecast'),
            ('Causal operating scenarios and challenges','adp_assumption_challenge'),
            ('Dated FCFF DCF, bridge and sensitivity','adp_project_dcf')]
    print('PROJECT 1 REQUIRED FINANCE SYSTEM | ADP | October 16, 2026 | USD')
    for title,name in stages:
        print(f'\n{title}')
        with redirect_stdout(captured):
            mods[name].main()
        print('  PASS')
    peers=peer_comparison(output)
    validation_record(output)
    data=json.loads((output/'ADP_project_DCF.json').read_text(encoding='utf-8'))
    print('\nVALUATION RESULTS - conditional operating scenarios')
    for name in ('downside','base','upside'):
        v=data['values'][name]
        print(f'  {name:<9} ${v["per_share"]:7.2f}/share | terminal share {v["tv_share"]:.1%}')
    print(f'  WACC {data["wacc"]:.3%} | reference close $288.90 | proposed WATCH / DEFER')
    print('  Peer comparisons are separate cross-checks; no mechanical average.')
    print('  Student-only validation and economic limitations remain; see report.')
    (output/'run_log.txt').write_text(captured.getvalue(),encoding='utf-8')
    combined=['# Project 1 required finance system — ADP','',
              'Self-contained offline Python system. Valuation October 16, 2026; evidence researched October 19. Proposed watch/defer; student review pending. Standard library only. All values are conditional on documented assumptions.', '',
              '## Read this first','',
              'The DCF operating-case range is not a confidence interval. The comparator multiples are qualified annual-snapshot cross-checks, not synchronized TTM estimates. No student prediction, receipt, partner exchange or recording is fabricated.', '',
              '## Visible source inputs and historical normalization choices','',
              '- Reported facts are reconstructed in the reconciliation. Facts, derived cash/debt definitions and analyst forecasts are separated in subsequent sections.',
              '- Keep reported operating costs as the conservative starting point. Do not automatically add back every management adjustment. Initiative/legal cash timing remains unresolved, so complete normalization is not claimed.',
              '- Remove non-client investment income from enterprise operating forecasts; retain client-strategy funding income/costs together. Exclude restricted principal from corporate excess cash.',
              '- Separate PEO zero-margin revenue, capitalized software and contract-cost amortization/investment; retain compensation cost economically.',
              '- Reconcile the filing label EBIT to pretax income before comparing conventional operating profit. These basis changes are the documented contamination/definition catalog.', '']
    for filename in ('ADP_project_DCF.md','ADP_assumption_challenge.md',
                     'ADP_peer_comparison.md','ADP_cash_flow_reconciliation.md',
                     'ADP_scheduled_forecast.md','VALIDATION STATUS.md'):
        combined += ['---','',f'<!-- {filename} -->','',
                     (output/filename).read_text(encoding='utf-8'),'']
    combined += ['## Current component-case financial statements','',
                 'The earlier scheduled tables are the preserved reference. The following are the current base/downside/upside statements that actually feed DCF. Full precision is in ADP_project_DCF.json.','']
    for name in ('base','downside','upside'):
        rows=data['operating'][name]['years']
        combined += [f'### {name}', '', '| Item | '+' | '.join(str(r['year']) for r in rows)+' |','|---|'+'---:|'*5]
        for key in ('revenue','core_cost','contract_amort','depreciation','intangible_amort',
                    'strategy_net','operating_earnings','interest','pretax','net_income',
                    'cfo','investing','financing','fcff'):
            combined.append('| '+key+' | '+' | '.join(f'{r[key]:,.2f}' for r in rows)+' |')
        for key in ('expense','deferred','current','cash','ending_payable'):
            combined.append('| Tax '+key+' | '+' | '.join(f'{r["tax"][key]:,.2f}' for r in rows)+' |')
        for key in ('total_assets','total_liabilities'):
            combined.append('| '+key+' | '+' | '.join(f'{r[key]:,.2f}' for r in rows)+' |')
        for key in rows[0]['balance']:
            combined.append('| BS '+key+' | '+' | '.join(f'{r["balance"][key]:,.2f}' for r in rows)+' |')
        combined.append('')
    (output/'Project 1 Finance System Report.md').write_text('\n'.join(combined),encoding='utf-8')
    (output/'ADP_peer_comparison.json').write_text(json.dumps(peers,indent=2),encoding='utf-8')
    files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir()
           if p.is_file() and p.name!='manifest.json'}
    manifest=dict(run_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  valuation_date='2026-10-16',files=files)
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(f'\nReport: {output/"Project 1 Finance System Report.md"}')
    return data


def portable_check(output):
    import subprocess
    import tempfile
    import shutil
    import venv
    with tempfile.TemporaryDirectory(prefix='adp_project1_') as tmp:
        root=Path(tmp)
        env=root/'clean_python'
        venv.EnvBuilder(with_pip=False).create(env)
        interpreter=env/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
        script=root/Path(__file__).name
        shutil.copy2(__file__,script)
        result=subprocess.run([str(interpreter),'-I',str(script),'--output-dir',str(root/'results')],
                              cwd=root,capture_output=True,text=True,timeout=120)
        log={'utc':datetime.now(timezone.utc).isoformat(),'returncode':result.returncode,
             'only_analysis_input':'single Python script; no sibling labs, packages or internet',
             'environment':'new venv without pip; isolated mode',
             'stdout':result.stdout,'stderr':result.stderr,
             'recording_status':'unrecorded machine verification; student video remains pending'}
        if result.returncode==0:
            normal=json.loads((output/'ADP_project_DCF.json').read_text(encoding='utf-8'))
            clean=json.loads((root/'results'/'ADP_project_DCF.json').read_text(encoding='utf-8'))
            if normal!=clean:
                raise AssertionError('Clean-run numerical output differs')
        (output/'portable_run_log.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
        if result.returncode:
            raise RuntimeError(result.stderr)
        print('PASS: single-file clean-venv run matches numerical results exactly (unrecorded).')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent/'Project 1 Finance System Output')
    parser.add_argument('--verify-portable',action='store_true')
    parser.add_argument('--show-code',choices=('reconciliation','forecast','challenge','dcf'))
    args=parser.parse_args()
    if args.show_code:
        names={'reconciliation':'adp_reconciliation','forecast':'adp_project_forecast',
               'challenge':'adp_assumption_challenge','dcf':'adp_project_dcf'}
        print(EMBEDDED[names[args.show_code]])
        return
    output=args.output_dir.resolve()
    run_system(output)
    if args.verify_portable:
        portable_check(output)
    # Manifest should include the clean-run log when requested.
    manifest=json.loads((output/'manifest.json').read_text(encoding='utf-8'))
    manifest['files']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in output.iterdir() if p.is_file() and p.name!='manifest.json'}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')


if __name__=='__main__':
    main()
