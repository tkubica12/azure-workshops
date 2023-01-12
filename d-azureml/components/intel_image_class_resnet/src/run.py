import argparse
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import mlflow
import os

parser = argparse.ArgumentParser("prep")
parser.add_argument("--training-data", type=str, help="Training data folder")
parser.add_argument("--test-data", type=str, help="Test data folder")
args = parser.parse_args()

mlflow.autolog()

# Set folders
train_data_dir = os.path.dirname(os.path.dirname(args.training_data))
validation_data_dir = os.path.dirname(os.path.dirname(args.test_data))

# Normalization
train_datagen = ImageDataGenerator(rescale=1/255)
validation_datagen = ImageDataGenerator(rescale=1/255)

# Generators
train_generator = train_datagen.flow_from_directory(
    train_data_dir,  
    target_size=(150,150), 
    batch_size=100,
    class_mode='categorical')

validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir, 
    target_size=(150,150), 
    batch_size=20,
    class_mode='categorical')

# Define base model InceptionResNetV2 for transfer learning
base_model = tf.keras.applications.InceptionResNetV2(
                include_top=False,        # Do not include the ImageNet classifier at the top, we will train our own.
                weights='imagenet',       # Load weights pre-trained on ImageNet.    
                input_shape=(150,150,3)
                )

base_model.trainable = False  # Freeze the base model

base_model.summary()

# Define model
model = tf.keras.Sequential([
        base_model,                                       # Starting from frozen base model
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),                     # Dropout layer to prevent overfitting
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(6, activation='softmax')    # Final layer for 6 classes
    ])

model.summary()

# Compile model
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Early stopping
callback = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=5)

# Fit model
history = model.fit_generator(
    train_generator,
    epochs=5000,
    verbose=1,
    validation_data = validation_generator,
    callbacks=[callback])


