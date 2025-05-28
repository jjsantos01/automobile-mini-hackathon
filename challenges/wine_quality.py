# challenges/wine_quality.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from utils import handle_username_input, save_score, display_leaderboard

def wine_quality_challenge():
    """Wine quality classification challenge page"""
    st.title("🍷📊 Wine Quality Classification Challenge")
    
    st.markdown("""
    **Objective**: Predict wine quality using multiclass classification
    **Metric**: Accuracy - higher is better
    **Classes**: Quality scores (typically 3-9)
    **Format**: Upload a CSV with a 'quality' column containing your predictions
    """)
    
    # Get test data
    try:
        URL_WINE_TEST_Y = st.secrets["URL_WINE_TEST_Y"]
        y_true = pd.read_csv(URL_WINE_TEST_Y)["quality"].to_numpy()
    except Exception as e:
        st.error(f"Error loading test data: {e}")
        st.info("Make sure to add URL_WINE_TEST_Y to your Streamlit secrets")
        return
    
    # Show dataset info
    unique_classes = np.unique(y_true)
    st.info(f"Dataset contains {len(y_true)} samples with quality classes: {list(unique_classes)}")
    
    # Handle username
    username = handle_username_input()
    
    # File upload
    uploaded = st.file_uploader("📤 Upload your predictions CSV", type="csv")
    
    if uploaded:
        if username:
            try:
                preds_df = pd.read_csv(uploaded)
                
                if "quality" not in preds_df.columns:
                    st.error("CSV must contain a 'quality' column")
                    return
                
                preds = preds_df["quality"].to_numpy()
                
                if len(preds) != len(y_true):
                    st.error(f"Wrong number of rows: {len(preds)} vs {len(y_true)} expected")
                    return
                
                # Check if predictions are valid classes
                unique_preds = np.unique(preds)
                invalid_preds = set(unique_preds) - set(unique_classes)
                if invalid_preds:
                    st.warning(f"Invalid quality classes in predictions: {invalid_preds}")
                
                accuracy = accuracy_score(y_true, preds)
                st.success(f"Your Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
                
                # Save if better
                def is_better(new, old):
                    return new > old
                
                saved = save_score(username, accuracy, "wine_scores", "accuracy", is_better)
                
                if saved:
                    st.success("New personal best saved! 🎉")
                
            except Exception as e:
                st.error(f"Error processing file: {e}")
        else:
            st.error("Please enter your username")
    
    # Display leaderboard
    st.subheader("🏆 Leaderboard (Best Accuracy)")
    display_leaderboard("wine_scores", "accuracy", ascending=False)