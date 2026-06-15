import streamlit as st
from utils.data_loader import load_and_clean_data
from views import macro_market, competitor_deep_dive, what_works, go_to_market, blind_spots, custom_account_audit

st.set_page_config(page_title="Content Analytics Dashboard", layout="wide")

# Load data
df, total_profiles, total_posts, global_avg_views, global_avg_comments = load_and_clean_data()

# Sidebar Executive Control
st.sidebar.title("Executive Dashboard")
st.sidebar.markdown(f"**Profiles Evaluated:** {total_profiles} | **Verified Assets:** {total_posts}")
page = st.sidebar.radio("Dashboard Sections:", [
    "Page 1: Market Acquisition Overview", 
    "Page 2: Competitor Performance Analysis", 
    "Page 3: Proven Content Strategies",
    "Page 4: 30-Day Growth Projections",
    "Page 5: Market Gaps & Execution Errors",
    "Page 6: Custom Account Audit"
])

# Page Routing
if page == "Page 1: Market Acquisition Overview":
    macro_market.render(df)
elif page == "Page 2: Competitor Performance Analysis":
    competitor_deep_dive.render(df, global_avg_views)
elif page == "Page 3: Proven Content Strategies":
    what_works.render(df, total_posts, total_profiles, global_avg_views)
elif page == "Page 4: 30-Day Growth Projections":
    go_to_market.render(df, global_avg_views, global_avg_comments)
elif page == "Page 5: Market Gaps & Execution Errors":
    blind_spots.render(df)
else:
    custom_account_audit.render(df)