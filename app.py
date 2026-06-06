import streamlit as st
from utils.data_loader import load_and_clean_data
from views import macro_market, competitor_deep_dive, what_works, go_to_market, blind_spots

st.set_page_config(page_title="Fat Loss Inbound Intelligence Engine", layout="wide")

# Load data
df, total_profiles, total_posts, global_avg_views, global_avg_comments = load_and_clean_data()

# Sidebar Executive Control
st.sidebar.title("💎 Executive Control Portal")
st.sidebar.markdown(f"**Profiles Evaluated:** {total_profiles} | **Verified Assets:** {total_posts}")
page = st.sidebar.radio("Navigate Growth Engine Layers:", [
    "📊 Page 1: Macro Market Analysis", 
    "🔍 Page 2: Competitor Deep-Dive", 
    "📈 Page 3: What Actually Works (5 Patterns)",
    "📅 Page 4: Our First 30 Days Growth Forecast",
    "🕳️ Page 5: Market Blind Spots & Failure Modes"
])

# Page Routing
if page == "📊 Page 1: Macro Market Analysis":
    macro_market.render(df)
elif page == "🔍 Page 2: Competitor Deep-Dive":
    competitor_deep_dive.render(df, global_avg_views)
elif page == "📈 Page 3: What Actually Works (5 Patterns)":
    what_works.render(df, total_posts, total_profiles, global_avg_views)
elif page == "📅 Page 4: Our First 30 Days Growth Forecast":
    go_to_market.render(df, global_avg_views, global_avg_comments)
else:
    blind_spots.render(df)