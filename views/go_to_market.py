import streamlit as st
import pandas as pd

def render(df, global_avg_views, global_avg_comments):
    st.title("Content Strategy Calendar & Projections")
    st.subheader("Data-Backed Growth Projections Based on Market Benchmarks")
    st.markdown("---")
    
    st.sidebar.markdown("### Simulation Controls")
    conversion_rate = st.sidebar.slider("Assumed Lead Conversion Rate (%)", 0.1, 5.0, 1.0, step=0.1) / 100.0
    
    st.markdown("### 30-Day Growth Projections")
    st.markdown("Projected consultation bookings generated over the initial 30 days across three deployment strategies.")
    
    # Calculate phase-specific benchmarks from real data
    cred_df = df[df["pillar"].str.contains("credibility", na=False)]
    viral_df = df[df["pillar"].str.contains("viral", na=False)]
    lead_df = df[df["pillar"].str.contains("lead", na=False)]

    phase1_avg_saves = int(cred_df["comments"].mean() * 2.5) if not cred_df.empty and not pd.isna(cred_df["comments"].mean()) else 0
    phase2_avg_views = int(viral_df["views"].mean()) if not viral_df.empty and not pd.isna(viral_df["views"].mean()) else 0
    phase3_avg_leads = int(lead_df["comments"].mean()) if not lead_df.empty and not pd.isna(lead_df["comments"].mean()) else 0

    # Top performing CTA word from real data
    trigger_words = ["comment", "dm", "link", "apply", "free"]
    word_performance = {}
    for word in trigger_words:
        matches = lead_df[lead_df["caption"].str.contains(word, case=False, na=False)]
        if not matches.empty:
            word_performance[word] = matches["comments"].mean()

    best_cta = max(word_performance, key=word_performance.get) if word_performance else "comment"
    
    days = list(range(1, 31))
    
    baseline_leads = []
    optimized_leads = []
    aggressive_leads = []
    
    b_acc, o_acc, a_acc = 0, 0, 0
    for day in days:
        # Simulate daily lead gen based on phase-specific data rather than global averages
        if day <= 10:
            daily_metric = phase1_avg_saves * 0.05
        elif day <= 20:
            daily_metric = phase2_avg_views * 0.0005
        else:
            daily_metric = phase3_avg_leads

        daily_base = daily_metric * 0.5 * conversion_rate
        daily_opt = daily_metric * 0.8 * conversion_rate * (1 + (day/30))
        daily_agg = daily_metric * 1.5 * conversion_rate * (1 + (day/15))
        
        b_acc += daily_base
        o_acc += daily_opt
        a_acc += daily_agg
        
        baseline_leads.append(int(b_acc))
        optimized_leads.append(int(o_acc))
        aggressive_leads.append(int(a_acc))
        
    sim_df = pd.DataFrame({
        "Day": days,
        "Baseline Growth": baseline_leads,
        "Optimized Core Strategy": optimized_leads,
        "High Growth Strategy": aggressive_leads
    }).set_index("Day")
    
    st.line_chart(sim_df)
    
    st.markdown("#### 30-Day Projected Booking Yields")
    c_m1, c_m2, c_m3 = st.columns(3)
    
    base_final = f"{baseline_leads[-1]:,}"
    opt_final = f"{optimized_leads[-1]:,}"
    agg_final = f"{aggressive_leads[-1]:,}"
    
    with c_m1:
        st.metric(label="Baseline Expected", value=base_final)
    with c_m2:
        st.metric(label="Optimized Core", value=opt_final)
    with c_m3:
        st.metric(label="High Growth Strategy", value=agg_final)
        
    st.caption("**Note:** Projections are based on the sidebar conversion rate applied to inbound messages initiated via content triggers.")
    st.markdown("---")

    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.error("Phase 1: Days 1–10")
        st.markdown(f"**Target:** ~{phase1_avg_saves:,} Saves/Post")
        st.markdown("**Focus:** Credibility Building<br>Zero direct sales CTAs. Focus strictly on establishing trust and authority.", unsafe_allow_html=True)
    with p_col2:
        st.warning("Phase 2: Days 11–20")
        st.markdown(f"**Target:** ~{phase2_avg_views:,} Views/Post")
        st.markdown("**Focus:** Audience Expansion<br>Combine educational content with high-reach formats to expand audience size.", unsafe_allow_html=True)
    with p_col3:
        st.success("Phase 3: Days 21–30")
        st.markdown(f"**Target:** ~{phase3_avg_leads:,} Leads/Post")
        st.markdown("**Focus:** Lead Generation<br>Deploy targeted call-to-actions to convert engaged audience members into scheduled consultations.", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Key Execution Deliverables")

    top_p = df.sort_values(by="views", ascending=False)
    h1_user, h1_views, h1_url = top_p.iloc[0]["username"], int(top_p.iloc[0]["views"]), top_p.iloc[0]["post_url"]
    h2_user, h2_views, h2_url = top_p.iloc[min(1, len(df)-1)]["username"], int(top_p.iloc[min(1, len(df)-1)]["views"]), top_p.iloc[min(1, len(df)-1)]["post_url"]
    h3_user, h3_views, h3_url = top_p.iloc[min(2, len(df)-1)]["username"], int(top_p.iloc[min(2, len(df)-1)]["views"]), top_p.iloc[min(2, len(df)-1)]["post_url"]

    # Day 1 Hero Post
    st.error("#### DAY 1 CORE DELIVERABLE: Establishing Authority")
    h1_link_string = "[View Original Post](" + str(h1_url) + ")"
    st.markdown(f"""
    * **Strategic Focus:** Credibility Building
    * **Content Structure:** Negative question + counter-intuitive solution (Reference: `@{h1_user}` | {h1_views:,} Views | {h1_link_string})
    * **Execution Concept:** > **"Why are 94% of busy professionals stalling their progress despite consistent workouts? It isn't a slow metabolism—it is an untracked weekend calorie surplus that erases the weekday deficit."**
    * **Objective:** Maximize saves to build long-term authority.
    """)
    st.markdown("---")

    # Day 15 Hero Post
    st.warning("#### DAY 15 CORE DELIVERABLE: Audience Expansion")
    h2_link_string = "[View Original Post](" + str(h2_url) + ")"
    st.markdown(f"""
    * **Strategic Focus:** Audience Reach
    * **Content Structure:** Direct audience callout + time-saving promise (Reference: `@{h2_user}` | {h2_views:,} Views | {h2_link_string})
    * **Execution Concept:** > **"If you work a high-stress job and want to drop 10kg, try this fast, macro-dense breakfast layout. Stop spending three hours meal-prepping on Sundays."**
    * **Objective:** Expand profile visibility and attract new followers.
    """)
    st.markdown("---")

    # Day 30 Hero Post
    st.success("#### DAY 30 CORE DELIVERABLE: Lead Generation")
    h3_link_string = "[View Original Post](" + str(h3_url) + ")"
    st.markdown(f"""
    * **Strategic Focus:** Inbound Conversion
    * **Content Structure:** Bold claim + personal proof + specific CTA (Reference: `@{h3_user}` | {h3_views:,} Views | {h3_link_string})
    * **Execution Concept:** > **"I help executives drop 15kg without giving up corporate dinners. {best_cta.capitalize()} the word 'STRATEGY' below and I will send you our complete framework."**
    * **Objective:** Drive inbound messages and consultation requests.
    """)
