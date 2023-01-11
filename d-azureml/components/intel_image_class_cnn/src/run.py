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

# Define model
model = tf.keras.models.Sequential([
    # Convolution layers
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(150, 150, 3)),  
    tf.keras.layers.MaxPooling2D(2, 2),                                            
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),                        
    tf.keras.layers.MaxPooling2D(2,2),                              
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),                  
    tf.keras.layers.MaxPooling2D(2,2),                                 
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    # Flatten and use DNN to classify
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(6, activation='softmax')
])

model.summary()

# Compile model
model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001), metrics=["accuracy"])

# Early stopping
callback = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=5)

# Fit model
history = model.fit_generator(
    train_generator,
    steps_per_epoch=140,  
    epochs=200,
    verbose=1,
    validation_data = validation_generator,
    validation_steps=150,
    callbacks=[callback])


