# Episode 1: Linear Regression - Predict House Prices

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load dataset (using diabetes dataset as Boston is deprecated)
data = load_diabetes()
X = data.data[:, np.newaxis, 2]  # take one feature for simplicity
y = data.target

# Split dataset into training and testing parts
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))

# Plot results
plt.scatter(X_test, y_test, color="black", label="Actual Data")
plt.plot(X_test, y_pred, color="blue", linewidth=2, label="Prediction Line")
plt.legend()
plt.xlabel("Feature (e.g., BMI)")
plt.ylabel("Target (disease progression)")
plt.title("Linear Regression Demo")
plt.show()
