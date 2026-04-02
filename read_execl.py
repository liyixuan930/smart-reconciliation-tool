import pandas as pd
bank = pd.read_excel("bank.xlsx")
account = pd.read_excel("account.xlsx")
print("银行流水：")
print(bank)
print("财务账：")
print(account)