# challenges/car_price.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from utils import handle_username_input, save_score, display_leaderboard

def car_price_challenge():
    """Car price prediction challenge page"""
    st.title("🚗💰 Car Price Prediction Challenge")
    
    st.markdown("""
    **Objective**: Predict car prices using regression
    **Metric**: RMSE (Root Mean Square Error) - lower is better
    **Format**: Upload a CSV with a 'price' column containing your predictions
    """)
    
    # Get test data
    try:
        URL_CAR_TEST_Y = st.secrets["URL_CAR_TEST_Y"]
        y_true = pd.read_csv(URL_CAR_TEST_Y)["price"].to_numpy()
    except Exception as e:
        st.error(f"Error loading test data: {e}")
        return
    
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
                    return
                
                preds = preds_df["price"].to_numpy()
                
                if len(preds) != len(y_true):
                    st.error(f"Wrong number of rows: {len(preds)} vs {len(y_true)} expected")
                    return
                
                rmse = np.sqrt(mean_squared_error(y_true, preds))
                st.success(f"Your RMSE: {rmse:,.2f}")
                
                # Save if better
                def is_better(new, old):
                    return new < old
                
                saved = save_score(username, rmse, "car_scores", "rmse", is_better)
                
                if saved:
                    st.success("New personal best saved! 🎉")
                
            except Exception as e:
                st.error(f"Error processing file: {e}")
        else:
            st.error("Please enter your username")
    
    # Display leaderboard
    st.subheader("🏆 Leaderboard (Best RMSE)")
    display_leaderboard("car_scores", "rmse", ascending=True)