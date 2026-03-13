# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

A two-script pipeline to calculate who owes whom money after a group trip to Japan. Scripts must be run from the project root directory.

## Pipeline

Run scripts in order from the project root:

```bash
python src/expense_formatter.py   # converts raw_expenses.csv → expenses.json
python src/balances.py            # converts expenses.json → balances.json
```

## Data Flow

1. **Input**: `data/raw_expenses.csv` — exported from a group expense-tracking app (PDF → Excel via Adobe, then saved as CSV). The first row defines column headers; columns 9 onward are per-person amounts (positive = paid, negative = owed).

2. **Intermediate**: `data/expenses.json` — normalized list of expense objects. Each has `title`, `rec_amount`, `paid_by`, `date`, `recorded_on`, `act_amount`, and `owed` (list of `{debtor, amount}` pairs).

3. **Output**: `data/balances.json` — contains:
   - `balances`: nested dict of `payer → debtor → {amount, expenses[], amount_owed_to}` tracking gross amounts in both directions
   - `totals`: list of net settlement strings (e.g. `"Rian owes Jeff $639.5"`) after netting out reciprocal debts

## Key Parsing Details

- `expense_formatter.py` strips `$`, `,`, `¥` and whitespace from amount strings; positive values in a cell = amount paid, negative = amount owed
- `balances.py` computes net totals by comparing `debtor_owes_payer` vs `payer_owes_debtor` and only emits a `totals` entry when one direction exceeds the other
- Both scripts use relative paths (`data/...`), so they must be run from the project root
