import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
file_path = "indian_crop_data.csv"  # Update with your actual file path
df = pd.read_csv(file_path)

# Check and rename columns
df.columns = ["Temperature", "Humidity", "Soil Moisture", "Light Intensity", "Pressure", "Predicted Crop"]

# Encode categorical target variable
label_encoder = LabelEncoder()
df["Predicted Crop"] = label_encoder.fit_transform(df["Predicted Crop"])

# Define features and target variable
X = df.drop(columns=["Predicted Crop"])
y = df["Predicted Crop"]

# Normalize data (important for Logistic Regression)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split dataset into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train Logistic Regression model
log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_train, y_train)

# Make predictions
y_pred = log_reg.predict(X_test)

# Evaluate Model
accuracy = accuracy_score(y_test, y_pred)
print(f"Logistic Regression Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Decode predictions
decoded_predictions = label_encoder.inverse_transform(y_pred)
print("\nSample Predictions:", decoded_predictions[:10])