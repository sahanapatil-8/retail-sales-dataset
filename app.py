import streamlit as st
import numpy as np

st.title("Dynamic Pricing Engine 💰")

inventory = st.slider("Inventory", 10, 500, 100)
quantity = st.slider("Quantity Sold", 1, 20, 5)

prediction = inventory * 0.5 + quantity * 2

st.write("### Predicted Price:", prediction)