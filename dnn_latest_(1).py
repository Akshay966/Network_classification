# -*- coding: utf-8 -*-
"""DNN_LATEST (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1P0t0vJ-T_Y8Ojqt2b2CNI8CluDK-c5Z4
"""

from google.colab import drive
drive.mount('/content/drive')

"""##  Inputing the dataset and checking stats"""

import pandas as pd

# Load the dataset
data_path = '/content/drive/MyDrive/Test/result_bkup1 (2).csv'
data = pd.read_csv(data_path)

# Display the first few rows and the summary of the dataset
data_head = data.head()
data_info = data.info()
data_description = data.describe()

data_head, data_info, data_description



"""## Splitting the data for training and testing"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

# Prepare features and target
X = data.drop('type', axis=1)
y = data['type']

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

"""## Scaling the data"""

# Normalize the feature data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""## One hot encoding the traget variable"""

# Convert target variable to one-hot encoding
y_train_encoded = to_categorical(y_train)
y_test_encoded = to_categorical(y_test)

"""## Model Creation"""

# Define the model
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dense(128, activation='relu'),
    Dense(y_train_encoded.shape[1], activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.summary(),

"""## Model Training"""

# Train the model
history = model.fit(X_train_scaled, y_train_encoded, epochs=50, validation_split=0.1, verbose=1)

"""## Finding Overall Test Accuracy"""

# Evaluate the model on the test set
evaluation = model.evaluate(X_test_scaled, y_test_encoded, verbose=0)
evaluation

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np

# Plot training & validation accuracy values
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')

"""## Plotting the Loss Graph"""

# Plot training & validation loss values
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

"""## Plotting the CONFUSION MATRIX"""

# Predicting the Test set results
y_pred = model.predict(X_test_scaled)
y_pred_classes = np.argmax(y_pred, axis=1)  # Convert predictions classes to one hot vectors
y_true = np.argmax(y_test_encoded, axis=1)  # Convert validation observations to one hot vectors

# Confusion matrix
cm = confusion_matrix(y_true, y_pred_classes)

# Plotting the confusion matrix
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt="d")
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

"""## Predicting PRECISION, RECALL AND F1 SCORE"""

from sklearn.metrics import precision_score, recall_score, f1_score

# Calculating precision, recall, and F1-score
precision = precision_score(y_true, y_pred_classes, average='macro')
recall = recall_score(y_true, y_pred_classes, average='macro')
f1 = f1_score(y_true, y_pred_classes, average='macro')

print("Precision: {:.2f}".format(precision))
print("Recall: {:.2f}".format(recall))
print("F1 Score: {:.2f}".format(f1))

# Print the training and validation accuracy
train_accuracy = history.history['accuracy'][-1]
validation_accuracy = history.history['val_accuracy'][-1]

print("Training Accuracy: {:.2f}%".format(train_accuracy * 100))
print("Validation Accuracy: {:.2f}%".format(validation_accuracy * 100))

"""## TESTING ON SINGLE DATA POINT"""

import numpy as np


example_data_point = [79000,500,7520.8,47.6,50,7900,0,0,0,0,0,0]

# Convert to numpy array and reshape it for prediction
example_data_point = np.array([example_data_point])

# Scale the data point using the same scaler used for training data
example_data_point_scaled = scaler.transform(example_data_point)

# Make prediction using the trained model
predicted_output = model.predict(example_data_point_scaled)
predicted_class = np.argmax(predicted_output, axis=1)

print("Predicted Output (Probabilities):", predicted_output)
print("Predicted Class:", predicted_class[0])
if predicted_class[0]==1:
  print("telnet")
if predicted_class[0]==0:
  print("ping")
if predicted_class[0]==2:
  print("VoIP")
if predicted_class[0]==3:
  print("DNS")

