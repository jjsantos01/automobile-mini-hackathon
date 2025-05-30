# pages/3_📊_PISA_Math.py
import streamlit as st
import pandas as pd
from sklearn.metrics import mean_absolute_error
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import handle_username_input, save_score, display_leaderboard, display_user_attempts

st.set_page_config(page_title="PISA Math Performance", page_icon="📊")

st.title("📊🧮 PISA Math Performance Prediction")

st.markdown("""
**Objective**: Predict student performance in PISA mathematics tests  
**Metric**: MAE (Mean Absolute Error) - lower is better  
**Target**: Mathematics performance scores  
**Format**: Upload a CSV with a 'math_score' column containing your predictions
""")

# Get test data
try:
    URL_TEST_Y = st.secrets["URL_PISA_TEST_Y"]
    y_true = pd.read_csv(URL_TEST_Y)["math_score"].to_numpy()
except Exception as e:
    st.error(f"Error loading test data: {e}")
    st.info("Make sure to add URL_PISA_TEST_Y to your Streamlit secrets")
    st.stop()

# Show dataset info
st.info(f"Dataset contains {len(y_true)} students with math scores ranging from {y_true.min():.1f} to {y_true.max():.1f}")

# Handle username
username = handle_username_input()

# File upload
uploaded = st.file_uploader("📤 Upload your predictions CSV", type="csv")

if uploaded:
    if username:
        try:
            preds_df = pd.read_csv(uploaded)
            
            if "math_score" not in preds_df.columns:
                st.error("CSV must contain a 'math_score' column")
                st.stop()
            
            preds = preds_df["math_score"].to_numpy()
            
            if len(preds) != len(y_true):
                st.error(f"Wrong number of rows: {len(preds)} vs {len(y_true)} expected")
                st.stop()
            
            mae = mean_absolute_error(y_true, preds)
            st.success(f"Your MAE: {mae:.2f}")
            
            # Save score and attempt
            is_better = lambda new, old: new < old
            is_new_best = save_score(username, mae, "pisa_scores", "pisa_attempts", "mae", is_better)
            
            if is_new_best:
                st.success("New personal best saved! 🎉")
            else:
                st.info("Score saved! Keep trying to beat your best.")
            
        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.error("Please enter your username")

# Display leaderboard
st.subheader("🏆 Leaderboard (Best MAE)")
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Refresh", key="refresh_pisa"):
        st.rerun()
with col1:
    display_leaderboard("pisa_scores", "mae", ascending=True)

# Display user's attempt history
display_user_attempts(username, "pisa_attempts", "mae")