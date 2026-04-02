import pandas as pd

bank = pd.read_excel("bank.xlsx")
account = pd.read_excel("account.xlsx")

matched = bank.merge(account, on="金额", how="inner")
print("匹配成功的记录：", len(matched))
print(matched)

unmatched_bank = bank[~bank["金额"].isin(account["金额"])]
print("银行侧未匹配：", len(unmatched_bank))
print(unmatched_bank)