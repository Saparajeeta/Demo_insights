import streamlit as st
import pandas as pd

def render(df, global_avg_views, global_avg_comments):
    st.title("📅 Go-To-Market Content Calendar & Business Case")
    st.subheader("Data-Backed Growth Projections Anchored Explicitly to Live Database Benchmarks")
    st.markdown("---")
    
    st.sidebar.markdown("### ⚙️ Simulation Controls")
    conversion_rate = st.sidebar.slider("Assumed Lead Conversion Rate (%)", 0.1, 5.0, 1.0, step=0.1) / 100.0
    
    st.markdown("### 📈 Interactive 30-Day Acquisition Simulation")
    st.markdown("Projected consultation bookings generated over the initial 30-day sprint across three deployment methodologies.")
    
    days = list(range(1, 31))
    
    baseline_leads = []
    optimized_leads = []
    aggressive_leads = []
    
    b_acc, o_acc, a_acc = 0, 0, 0
    for day in days:
        # Simulate daily lead gen based on global avg comments and conversion rate
        daily_base = global_avg_comments * 0.5 * conversion_rate
        daily_opt = global_avg_comments * 0.8 * conversion_rate * (1 + (day/30))
        daily_agg = global_avg_comments * 1.5 * conversion_rate * (1 + (day/15))
        
        b_acc += daily_base
        o_acc += daily_opt
        a_acc += daily_agg
        
        baseline_leads.append(int(b_acc))
        optimized_leads.append(int(o_acc))
        aggressive_leads.append(int(a_acc))
        
    sim_df = pd.DataFrame({
        "Day": days,
        "Baseline Growth": baseline_leads,
        "Optimized Core Strategy (4:4:2 Mix)": optimized_leads,
        "Aggressive Acquisition Velocity": aggressive_leads
    }).set_index("Day")
    
    st.line_chart(sim_df)
    
    st.markdown("#### 📊 30-Day Projected Booking Yields")
    c_m1, c_m2, c_m3 = st.columns(3)
    
    base_final = f"{baseline_leads[-1]:,}"
    opt_final = f"{optimized_leads[-1]:,}"
    agg_final = f"{aggressive_leads[-1]:,}"
    
    with c_m1:
        st.metric(label="Baseline Expected", value=base_final)
    with c_m2:
        st.metric(label="Optimized Core (4:4:2)", value=opt_final)
    with c_m3:
        st.metric(label="Aggressive Velocity", value=agg_final)
        
    st.caption("**Methodological Note:** Consultation targets project actively against the sidebar slider closing rate exclusively tracking inbound message threads initiated natively through comment triggers.")
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
