import streamlit as st
import requests

st.title("Dynamic Pricing Engine 💰")

inventory = st.slider("Inventory", 10, 500, 100)
quantity = st.slider("Quantity Sold", 1, 20, 5)

if st.button("Predict Price"):
    url = "https://dynamic-pricing-backend-rywt.onrender.com/predict"
    params = {
        "inventory": inventory,
        "quantity": quantity
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Price: ₹{result['predicted_price']}")
    else:
        st.error("Failed to get prediction from backend")