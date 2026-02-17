import json

EXPENSES = 'data/expenses.json'
BALANCES = 'data/balances.json'

# Read in the individual expenses.
with open(EXPENSES, 'r', encoding='utf-8') as f_expenses:
    expenses = json.load(f_expenses)

# Determine the people to be paid and the people who owe.
people = set([exp['paid_by'] for exp in expenses])

# Setup the initial balance tracking structure.
balances = {payer: {'debtors': {}} for payer in people}

# Iter over the expenses and record each individual debt.
for exp in expenses:
    payer = balances[exp['paid_by']]
    for debt in exp['owed']:
        if debt['debtor'] not in payer['debtors']:
            payer['debtors'][debt['debtor']] = {'amount': 0.0, 'expenses': []}
        debtor = payer['debtors'][debt['debtor']]
        debtor['amount'] += debt['amount']
        debtor['expenses'].append({'title': exp['title'], 'date': exp['recorded_on'], 'amount': debt['amount']})

# Cleanup total balances with rounding.
for payer in balances.values():
    for debtor in payer['debtors'].values():
        debtor['amount'] = round(debtor['amount'], 2)

# Compare amounts owed in both directions to determine who owes whom.
total_due = []
for payer_name, payer in balances.items():
    for debtor_name, debtor in payer['debtors'].items():
        debtor_owes_payer = debtor['amount']
        payer_owes_debtor = balances[debtor_name]['debtors'][payer_name]['amount'] \
            if payer_name in balances[debtor_name]['debtors'] else 0.0
        debtor['amount_owed_to'] = payer_owes_debtor
        if debtor_owes_payer > payer_owes_debtor:
            total_due.append(f'{debtor_name} owes {payer_name} ${round(debtor_owes_payer - payer_owes_debtor, 2)}')

# Write the balances due.
with open(BALANCES, 'w', encoding='utf-8') as f_balances:
    json.dump({'balances': balances, 'totals': total_due}, f_balances)