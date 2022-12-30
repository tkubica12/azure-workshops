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
parser.add_argument("--saved-scaler", type=str, help="SSaved scaler file to log with model as artefact")
parser.add_argument("--model_output", type=str, help="Path of output model")
parser.add_argument("--finished", type=str, help="Solver hyperparameter")
args = parser.parse_args()

mlflow.autolog()

# Load data
X_train = pd.read_csv(args.x_train) 
X_test = pd.read_csv(args.x_test) 
y_train = pd.read_csv(args.y_train) 
y_test = pd.read_csv(args.y_test) 

# Set tag
mlflow.set_tag("algorithm", "tensorflow")

# Log scaler artefact
mlflow.log_artifact(args.saved_scaler, "model")

# Define model
model = Sequential()

model.add(Dense(150,  activation='relu'))
model.add(Dropout(args.dropout))

model.add(Dense(75, activation='relu'))
model.add(Dropout(args.dropout))

model.add(Dense(37, activation='relu'))
model.add(Dropout(args.dropout))

model.add(Dense(18, activation='relu'))
model.add(Dropout(args.dropout))

model.add(Dense(units=1,activation='sigmoid'))

# Early stopping
from tensorflow.keras.callbacks import EarlyStopping
callback = EarlyStopping(monitor='val_loss', patience=5)

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])

# Fit model
model.fit(x=X_train, 
          y=y_train, 
          epochs=500,
          batch_size=256,
          validation_data=(X_test, y_test), 
          callbacks=[callback]
          )

# Evaluate model
model.evaluate(X_test, y_test, verbose=2)

# Finished
from pathlib import Path
Path(args.finished).touch()