import pandas as pd

df = pd.read_excel('data.xlsx',skiprows=1)

print(df.head())

df.to_json(
    'out.json',
    orient='records',
    indent=4
)

print("Excel to JSON Converted ....")
