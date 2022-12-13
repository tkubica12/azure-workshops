import argparse
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation,Dropout
from tensorflow.keras.constraints import max_norm
from tensorflow.keras.models import load_model
import mlflow

parser = argparse.ArgumentParser("prep")
parser.add_argument("--x-train", type=str, help="Training features file")
parser.add_argument("--x-test", type=str, help="Testing features file")
parser.add_argument("--y-train", type=str, help="Training labels file")
parser.add_argument("--y-test", type=str, help="Testing labels file")
parser.add_argument("--dropout", type=float, help="Set dropout rate between layers")
args = parser.parse_args()

mlflow.autolog()

# Load data
X_train = pd.read_csv(args.x_train) 
X_test = pd.read_csv(args.x_test) 
y_train = pd.read_csv(args.y_train) 
y_test = pd.read_csv(args.y_test) 

# Define model
model = Sequential()

model.add(Dense(80,  activation='relu'))
model.add(Dropout(args.dropout))

model.add(Dense(40, activation='relu'))
model.add(Dropout(args.dropout))

model.add(Dense(20, activation='relu'))
model.add(Dropout(args.dropout))

model.add(Dense(units=1,activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit model
model.fit(x=X_train, 
          y=y_train, 
          epochs=25,
          batch_size=256,
          validation_data=(X_test, y_test), 
          )

# Evaluate model
model.evaluate(X_test, y_test, verbose=2)