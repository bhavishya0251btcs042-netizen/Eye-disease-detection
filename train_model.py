import pandas as pd
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Configuration
DATASET_DIR = r'c:\Users\DELL\OneDrive\Music\Documents\New_model\dataset'
IMAGES_DIR = os.path.join(DATASET_DIR, 'images')
LABELS_FILE = os.path.join(DATASET_DIR, 'labels.csv')
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 10

def load_data():
    print("Loading data...")
    df = pd.read_csv(LABELS_FILE)
    
    # We will predict 'category' 
    print(f"Original Classes: {df['category'].unique()}")

    images = []
    labels = []

    for index, row in df.iterrows():
        img_name = row['name']
        img_path = os.path.join(IMAGES_DIR, img_name)
        
        if os.path.exists(img_path):
            try:
                img = load_img(img_path, target_size=IMG_SIZE)
                img_array = img_to_array(img) / 255.0  # Normalize
                images.append(img_array)
                labels.append(row['category'])
            except Exception as e:
                print(f"Error loading image {img_name}: {e}")
        else:
            print(f"Image not found: {img_path}")

    # Encode labels to ensure they are 0..N-1 integers
    le = LabelEncoder()
    labels_encoded = le.fit_transform(labels)
    num_classes = len(le.classes_)
    
    print(f"Encoded classes mapping: {dict(zip(le.classes_, le.transform(le.classes_)))}")
    print(f"Number of classes: {num_classes}")

    return np.array(images), labels_encoded, num_classes

def create_model(input_shape, num_classes):
    print("Creating model...")
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def main():
    X, y, num_classes = load_data()
    
    if len(X) == 0:
        print("No data loaded. Exiting.")
        return

    print(f"Loaded {len(X)} images.")

    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model = create_model((IMG_SIZE[0], IMG_SIZE[1], 3), num_classes)
    
    print("Starting training...")
    history = model.fit(X_train, y_train, epochs=EPOCHS, validation_data=(X_val, y_val), batch_size=BATCH_SIZE)
    
    print("Training finished.")
    
    # Save model
    model_save_path = os.path.join(DATASET_DIR, 'simple_model.h5')
    model.save(model_save_path)
    print(f"Model saved to {model_save_path}")

    # Evaluate
    loss, acc = model.evaluate(X_val, y_val, verbose=2)
    print(f"Validation accuracy: {acc:5.2f}")

if __name__ == '__main__':
    main()