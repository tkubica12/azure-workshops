import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser("prep")
parser.add_argument("--raw_data", type=str, help="Raw data file")
parser.add_argument("--processed_data", type=str, help="Processed data file")
args = parser.parse_args()

print(f"Raw data file: {args.raw_data}",)
print(f"Processed data file: {args.processed_data}",)

# Load raw data
df = pd.read_csv(args.raw_data) 

# Create binary label
df['loan_repaid'] = np.where(df['loan_status'] == 'Fully Paid', 1, 0)
df = df.drop(labels='loan_status', axis=1)

# Drop features
df = df.drop(labels=['emp_title', 'emp_length', 'title', 'grade', 'issue_d'] , axis=1)

# Fill-in mort acc
mortmeans = df.groupby(by='total_acc')['mort_acc'].mean()
def myfill(total,mort):
    if pd.isna(mort):
        return mortmeans[total]
    else:
        return mort

df['mort_acc'] = df.apply(lambda x: myfill(x.total_acc, x.mort_acc), axis=1)

# Drop rows with missing data
df = df.dropna()

# Convert term feature to number
def convert_term(x):
    if x == ' 36 months': return 36
    if x == ' 60 months': return 60

df['term'] = df['term'].apply(lambda x: convert_term(x))

# Dummy from sub_grade
df = pd.concat([df, pd.get_dummies(data=df['sub_grade'],drop_first=True)], axis=1)
df = df.drop(labels='sub_grade', axis=1)

# Other dummies
dumm1 = pd.get_dummies(data=df['verification_status'],drop_first=True)
dumm2 = pd.get_dummies(data=df['application_type'],drop_first=True)
dumm3 = pd.get_dummies(data=df['initial_list_status'],drop_first=True)
dumm4 = pd.get_dummies(data=df['purpose'],drop_first=True)
df = pd.concat([df, dumm1, dumm2, dumm3, dumm4],axis=1)
df = df.drop(labels=['verification_status', 'application_type', 'initial_list_status', 'purpose'],axis=1)

# Home ownership feature - join categories, make dummy vars
def homeownership(x):
    if (x == 'NONE') or (x == 'ANY'): return 'OTHER'
    else: return x

df['home_ownership'].apply(lambda x: homeownership(x)).unique()
df = pd.concat([df, pd.get_dummies(data=df['home_ownership'], drop_first=True)], axis=1)
df = df.drop(labels='home_ownership', axis=1)

# Parse zip and create dummy vars
zips = pd.get_dummies(df['address'].str[-5:], drop_first=True)
df = pd.concat([df,zips], axis=1)
df = df.drop(labels='address',axis=1)

# Parse year
df['earliest_cr_year'] = pd.to_numeric(df['earliest_cr_line'].str[-4:])
df = df.drop(labels='earliest_cr_line', axis=1)

# Save processed data
df.to_csv(args.processed_data) 

