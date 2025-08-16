from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load dataset
data = fetch_california_housing()
X = data.data[:, [0]]   # Use only 1 feature for simple visualization (MedInc = median income)
y = data.target

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))

# Plot
plt.scatter(X_test, y_test, color="black", label="Actual Prices")
plt.plot(X_test, y_pred, color="blue", linewidth=2, label="Prediction Line")
plt.xlabel("Median Income (in block)")
plt.ylabel("House Price (in 100k USD)")
plt.title("Linear Regression - Predict House Prices")
plt.legend()
plt.show()
