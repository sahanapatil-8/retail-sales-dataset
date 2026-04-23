from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

app = FastAPI()

# Load data and train model
df = pd.read_csv("data/raw/data.csv")
df["inventory"] = np.random.randint(10, 500, size=len(df))

X = df[["inventory", "Quantity"]]
y = df["Price per Unit"]

model = RandomForestRegressor()
model.fit(X, y)

@app.get("/")
def home():
    return {"message": "Dynamic Pricing API is running"}

@app.get("/predict")
def predict_price(inventory: int, quantity: int):
    pred = model.predict([[inventory, quantity]])
    return {"predicted_price": round(float(pred[0]), 2)}