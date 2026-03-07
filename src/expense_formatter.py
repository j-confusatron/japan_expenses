import csv
import json
import re

'''
Reads in the raw expenses CSV (data/raw_expenses.csv).
This file was created by converting the app output PDF to Excel using Adobe's online converter.
https://www.adobe.com/acrobat/online/pdf-to-excel.html
The raw expenses are converted to JSON format, suitable for downstream processing.
The output is written to: data/expenses.json.
'''

RAW_EXPENSES = 'data/raw_expenses.csv'
EXPENSES = 'data/expenses.json'

# Read the raw expenses from CSV.
with open(RAW_EXPENSES, 'r', encoding="utf8") as file:
    raw_exp = list(csv.reader(file))

# Determine the payee order.
payee_order = raw_exp.pop(0)[8:-1]

# Iter over and formate each individual expense.
def record_expense(e):
    ex = {
            'title': e[0],
            'rec_amount': e[3],
            'paid_by': e[5],
            'date': e[6],
            'recorded_on': e[7]
        }
    
    amounts = debts(e[8:-1])
    ex['act_amount'] = amounts[0]
    ex['owed'] = amounts[1]
    
    return ex

def debts(d):
    act_amount = 0.0
    owed = []
    for i, a in enumerate(d):
        pos, neg = amnt(a)
        if pos:
            act_amount = pos
        if neg:
            owed.append({'debtor': payee_order[i], 'amount': -1*neg})
    return (act_amount, owed)

def amnt(a):
    amounts = [0.0, 0.0]
    if a:
        a = re.sub('[$,¥]', '', a)
        a = re.sub(r'\s+', ',', a)
        for (num) in a.split(','):
            num = float(num)
            if num > 0:
                amounts[0] = num
            elif num < 0:
                amounts[1] = num
    return tuple(amounts)

expenses = [record_expense(e) for e in raw_exp]

# Write the formatted expenses.
with open(EXPENSES, 'w', encoding='utf-8') as file:
    json.dump(expenses, file)