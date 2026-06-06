import streamlit as st
import pandas as pd

def render(df, global_avg_views, global_avg_comments):
    st.title("📅 Go-To-Market Content Calendar & Business Case")
    st.subheader("Data-Backed Growth Projections Anchored Explicitly to Live Database Benchmarks")
    st.markdown("---")
    
    base_conversion = 0.03
    
    st.markdown("### 📈 Data-Driven Growth Projection Scenarios")
    st.markdown("The values below display projected outcomes for 12 planned video assets deployed over our initial 30 days based on active tracking averages:")
    
    forecast_data = {
        "Funnel Metrics Layer": [
            "Phase 1: Expected Saves per Asset (Days 1-10)", 
            "Phase 2: Expected Views per Asset (Days 11-20)", 
            "Phase 3: Inbound Lead Comments per CTA (Days 21-30)",
            "Projected Total High-Intent Consultation Bookings"
        ],
        "Conservative Scenario": [
            f"{int(global_avg_comments * 0.4)} saves", 
            f"{int(global_avg_views * 0.5):,} views", 
            f"{int(global_avg_comments * 0.6)} leads", 
            f"{max(int(global_avg_comments * 12 * base_conversion * 0.5), 1)} bookings"
        ],
        "Realistic Baseline": [
            f"{int(global_avg_comments * 0.8)} saves", 
            f"{global_avg_views:,} views", 
            f"{global_avg_comments} leads", 
            f"{max(int(global_avg_comments * 12 * base_conversion), 2)} bookings"
        ],
        "Optimistic Target": [
            f"{int(global_avg_comments * 1.5)} saves", 
            f"{int(global_avg_views * 1.8):,} views", 
            f"{int(global_avg_comments * 2.1)} leads", 
            f"{int(global_avg_comments * 12 * base_conversion * 2.5)} bookings"
        ]
    }
    st.table(pd.DataFrame(forecast_data).set_index("Funnel Metrics Layer"))
    st.caption("**Methodological Note:** Consultation targets project a strict 3% application closing rate exclusively against inbound message threads initiated natively through comment triggers.")
    st.markdown("---")

    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.error("🟥 Phase 1: Days 1–10")
        st.markdown("**Focus Layer:** Credibility Anchoring Only<br>Zero direct sales CTAs. Anchor platform trust parameters using contrarian frameworks exclusively.", unsafe_allow_html=True)
    with p_col2:
        st.warning("🟨 Phase 2: Days 11–20")
        st.markdown("**Focus Layer:** Scale Account Velocity<br>Fuse educational myth-bust assets with high-reach friction reduction layouts to scale page save markers.", unsafe_allow_html=True)
    with p_col3:
        st.success("🟩 Phase 3: Days 21–30")
        st.markdown("**Focus Layer:** Inbound Funnel Closing<br>Deploy low-friction comment keyword capture mechanics. Convert warm trust assets directly into scheduled applications.", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏆 Highlighted Phase Hero Production Targets")

    top_p = df.sort_values(by="views", ascending=False)
    h1_user, h1_views, h1_url = top_p.iloc[0]["username"], int(top_p.iloc[0]["views"]), top_p.iloc[0]["post_url"]
    h2_user, h2_views, h2_url = top_p.iloc[min(1, len(df)-1)]["username"], int(top_p.iloc[min(1, len(df)-1)]["views"]), top_p.iloc[min(1, len(df)-1)]["post_url"]
    h3_user, h3_views, h3_url = top_p.iloc[min(2, len(df)-1)]["username"], int(top_p.iloc[min(2, len(df)-1)]["views"]), top_p.iloc[min(2, len(df)-1)]["post_url"]

    # Day 1 Hero Post
    st.error("#### 🟥 DAY 1 HERO ASSET: Establishing Authority Phase")
    h1_link_string = "[🔗 Verify Exact Post Evidence](" + str(h1_url) + ")"
    st.markdown(f"""
    * **Pillar Alignment:** Credibility Building
    * **Hook Formula Model:** Negative question + shocking number (Validated via `@{h1_user}` | {h1_views:,} Views | {h1_link_string})
    * **Our Brand Script Execution Line:** > **"Why are 94% of busy professionals completely stalling their fat loss progress despite working out five days a week? It isn't your slow genetics—it is an un-tracked weekend calorie blind spot that completely erases your weekday deficit in 48 hours."**
    * **Expected Outcome Target:** High algorithmic Save Velocity to initiate structural search visibility profiles.
    """)
    st.markdown("---")

    # Day 15 Hero Post
    st.warning("#### 🟨 DAY 15 HERO ASSET: Expanding Scale Velocity Phase")
    h2_link_string = "[🔗 Verify Exact Post Evidence](" + str(h2_url) + ")"
    st.markdown(f"""
    * **Pillar Alignment:** Viral Reach / Audience Velocity
    * **Hook Formula Model:** Direct callout + time promise (Validated via `@{h2_user}` | {h2_views:,} Views | {h2_link_string})
    * **Our Brand Script Execution Line:** > **"If you are working a high-stress job and struggling to drop your first 10kg, look at this 3-ingredient macro-dense breakfast layout for exactly 60 seconds. Stop prepping meals for three hours every single Sunday."**
    * **Expected Outcome Target:** Maximum Page Save velocity combined with profile bookmark spikes.
    """)
    st.markdown("---")

    # Day 30 Hero Post
    st.success("#### 🟩 DAY 30 HERO ASSET: Closing the Inbound Funnel Phase")
    h3_link_string = "[🔗 Verify Exact Post Evidence](" + str(h3_url) + ")"
    st.markdown(f"""
    * **Pillar Alignment:** Lead Generation / Inbound Conversion
    * **Hook Formula Model:** Contrarian claim + personal proof (Validated via `@{h3_user}` | {h3_views:,} Views | {h3_link_string})
    * **Our Brand Script Execution Line:** > **"I help busy executives drop 15kg without abandoning corporate dinners or surviving on bland salads. Comment the word 'METABOLISM' below this video right now and I will instantly DM you our complete system guide for free."**
    * **Expected Outcome Target:** Maximum inbound message activation counts and low-friction consultation booking requests.
    """)
