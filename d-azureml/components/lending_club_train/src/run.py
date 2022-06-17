import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation,Dropout
from tensorflow.keras.constraints import max_norm
from tensorflow.keras.models import load_model

parser = argparse.ArgumentParser("prep")
parser.add_argument("--data", type=str, help="Data file")
parser.add_argument("--model_file", type=str, help="Filename for resulting model to be saved")
args = parser.parse_args()

print(f"Data file: {args.raw_data}",)
print(f"Model file: {args.model_file}",)

# Load raw data
df = pd.read_csv(args.raw_data) 

# Get features and labels
X = df.drop('loan_repaid',axis=1).values
y = df['loan_repaid'].values

# Split data into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=101)

# Scale features
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define model
model = Sequential()

model.add(Dense(78,  activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(39, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(19, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(units=1,activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam')

# Fit model
model.fit(x=X_train, 
          y=y_train, 
          epochs=25,
          batch_size=256,
          validation_data=(X_test, y_test), 
          )

# Save model
model.save(args.model_file)  

