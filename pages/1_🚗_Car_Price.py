# pages/1_🚗_Car_Price.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import handle_username_input, save_score, display_leaderboard, display_user_attempts

st.set_page_config(page_title="Car Price Prediction", page_icon="🚗")

st.title("🚗💰 Car Price Prediction Challenge")

st.markdown("""
**Objective**: Predict car prices using regression  
**Metric**: RMSE (Root Mean Square Error) - lower is better  
**Format**: Upload a CSV with a 'price' column containing your predictions
""")

# Get test data
try:
    URL_TEST_Y = st.secrets["URL_CAR_TEST_Y"]
    y_true = pd.read_csv(URL_TEST_Y)["price"].to_numpy()
except Exception as e:
    st.error(f"Error loading test data: {e}")
    st.stop()

# Handle username
username = handle_username_input()

# File upload
uploaded = st.file_uploader("📤 Upload your predictions CSV", type="csv")

if uploaded:
    if username:
        try:
            preds_df = pd.read_csv(uploaded)
            
            if "price" not in preds_df.columns:
                st.error("CSV must contain a 'price' column")
                st.stop()
            
            preds = preds_df["price"].to_numpy()
            
            if len(preds) != len(y_true):
                st.error(f"Wrong number of rows: {len(preds)} vs {len(y_true)} expected")
                st.stop()
            
            rmse = np.sqrt(mean_squared_error(y_true, preds))
            st.success(f"Your RMSE: {rmse:,.2f}")
            
            # Save score and attempt
            is_better = lambda new, old: new < old
            is_new_best = save_score(username, rmse, "car_scores", "car_attempts", "rmse", is_better)
            
            if is_new_best:
                st.success("New personal best saved! 🎉")
            else:
                st.info("Score saved! Keep trying to beat your best.")
            
        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.error("Please enter your username")

# Display leaderboard
st.subheader("🏆 Leaderboard (Best RMSE)")
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Refresh", key="refresh_car"):
        st.rerun()
with col1:
    display_leaderboard("car_scores", "rmse", ascending=True)

# Display user's attempt history
display_user_attempts(username, "car_attempts", "rmse")