import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser("prep")
parser.add_argument("--raw-data", type=str, help="Raw data file")
parser.add_argument("--processed-data", type=str, help="Processed data file")
args = parser.parse_args()

print(f"Raw data file: {args.raw_data}",)
print(f"Processed data file: {args.processed_data}",)

# Load raw data
df = pd.read_csv(args.raw_data) 

# Create binary label
if 'loan_status' in df:
    print("loan_status column exists, create binary label loan_repaid")
    df['loan_repaid'] = np.where(df['loan_status'] == 'Fully Paid', 1, 0)
    df = df.drop(labels='loan_status', axis=1)
else:
    print("loan_status column does not exist, ignore")

# Drop features
df = df.drop(labels=['grade', 'issue_d'] , axis=1)

# Fill-in mort acc
mortmeans = df.groupby(by='total_acc')['mort_acc'].mean()
def myfill(total,mort):
    if pd.isna(mort):
        return mortmeans[total]
    else:
        return mort

df['mort_acc'] = df.apply(lambda x: myfill(x.total_acc, x.mort_acc), axis=1)

# Keep top 30 most frequent values for emp_title
top_values = df['emp_title'].groupby(df['emp_title']).count().sort_values(ascending=False).head(30).index.tolist()
df['emp_title'] = df['emp_title'].apply(lambda x: 'Other' if x not in top_values else x)

# Keep top 30 most frequent values for title
top_values = df['title'].groupby(df['title']).count().sort_values(ascending=False).head(30).index.tolist()
df['title'] = df['title'].apply(lambda x: 'Other' if x not in top_values else x)

# Drop rows with missing data
df = df.dropna()

# Convert term feature to number
def convert_term(x):
    if x == ' 36 months': return 36
    if x == ' 60 months': return 60

df['term'] = df['term'].apply(lambda x: convert_term(x))

# Home ownership feature - join categories
def homeownership(x):
    if (x == 'NONE') or (x == 'ANY'): return 'OTHER'
    else: return x

df['home_ownership'].apply(lambda x: homeownership(x)).unique()

# Parse zip and create dummy vars
df['address'] = df['address'].str[-5:]

# Parse year
df['earliest_cr_year'] = pd.to_numeric(df['earliest_cr_line'].str[-4:])
df = df.drop(labels='earliest_cr_line', axis=1)

# Get dummies (OHE)
df = pd.get_dummies(columns=['sub_grade', 'verification_status', 'application_type', 'initial_list_status', 'purpose', 'home_ownership', 'address', 'emp_title', 'title', 'emp_length'], data=df,drop_first=True)


# Save processed data
from pathlib import Path  
filepath = Path(args.processed_data) 
filepath.parent.mkdir(parents=True, exist_ok=True)  

df.to_csv(args.processed_data) 

