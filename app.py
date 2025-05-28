import streamlit as st
from config import init_database
from challenges.car_price import car_price_challenge
from challenges.wine_quality import wine_quality_challenge

# Initialize database
init_database()

# Page configuration
st.set_page_config(
    page_title="ML Hackathon Platform",
    page_icon="🏆",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("🏆 ML Challenges")
st.sidebar.markdown("Select a challenge:")

page = st.sidebar.selectbox(
    "Choose Challenge:",
    ["🏠 Home", "🚗 Car Price Prediction", "🍷 Wine Quality Classification"]
)

# Main content based on selection
if page == "🏠 Home":
    st.title("🏆 Machine Learning Hackathon Platform")
    st.markdown("""
    Welcome to the ML Hackathon Platform! Choose a challenge from the sidebar to get started.
    
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

elif page == "🚗 Car Price Prediction":
    car_price_challenge()
    
elif page == "🍷 Wine Quality Classification":
    wine_quality_challenge()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using Streamlit")