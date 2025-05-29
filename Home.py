# Home.py (main page)
import streamlit as st
from config import init_database

# Initialize database
init_database()

# Page configuration
st.set_page_config(
    page_title="ML Hackathon Platform",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Machine Learning Hackathon Platform")
st.markdown("""
Welcome to the ML Hackathon Platform! Navigate through the challenges using the sidebar.

## Available Challenges:

### 🚗 Car Price Prediction
- **Type**: Regression
- **Metric**: RMSE (Root Mean Square Error)
- **Goal**: Predict car prices as accurately as possible

### 🍷 Wine Quality Classification  
- **Type**: Multiclass Classification
- **Metric**: Accuracy
- **Goal**: Classify wine quality scores

## How to Participate:
1. Choose your username (it will be saved in the URL for convenience)
2. Download the training data and develop your model
3. Upload your predictions as a CSV file
4. See your score and compete on the leaderboard!

Good luck! 🚀
""")

st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using Streamlit")