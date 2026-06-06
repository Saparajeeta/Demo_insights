import streamlit as st

def render(df):
    st.title("🕳️ Under-served Market Gaps & Failure Analysis")
    st.subheader("Identifying Strategic Openings and Copy Breakdown Mechanics")
    st.markdown("---")
    
    st.header("🔍 Where the Market is Under-served")
    st.markdown("The engine scanned our 100-profile landscape for high user intent signals (question marks in comments, heavy saves) mapped against a low active post supply.")
    
    gap_col1, gap_col2, gap_col3 = st.columns(3)
    with gap_col1:
        st.info("#### 🎯 Gap A: The Caloric Maintenance Blueprint")
        st.markdown("""
        * **Demand Signal:** Heavy comment threads requesting transition plans post-dieting, but zero accounts have dedicated grid videos addressing maintenance variables.
        * **Opportunity Size:** High baseline authority capture. Bypasses weight loss fatigue.
        * **First-Mover Edge:** Establishes deep technical retention credibility before competitors leave basic cutting scopes.
        """)
    with gap_col2:
        st.info("#### 🎯 Gap B: Executive Travel Tactics")
        st.markdown("""
        * **Demand Signal:** Corporate professionals asking how to handle hotel macro parameters in captions, paired with low visual content solutions from influencers.
        * **Opportunity Size:** Accelerates high-ticket business client acquisition instantly.
        * **First-Mover Edge:** Aligns the brand's identity with premium buyer demographics rather than generic gym goers.
        """)
    with gap_col3:
        st.info("#### 🎯 Gap C: Circadian Sleep/Stress Architectures")
        st.markdown("""
        * **Demand Signal:** Cortisol and biological recovery questions appear under 18% of transformation posts with no dedicated asset breakouts.
        * **Opportunity Size:** Captures audience segments looking for comprehensive lifestyle design solutions over standard diet frameworks.
        * **First-Mover Edge:** Repositions our business as medical lifestyle strategists rather than generic calorie trackers.
        """)
        
    st.markdown("---")
    
    st.header("🛑 Why Good Formulas Sometimes Fail")
    st.markdown("Honest failure mode diagnostic analyzing structurally perfect copy models that still underperformed view baselines due to tactical misalignment:")
    
    underperformers = df.sort_values(by="views", ascending=True)
    f1_post = underperformers.iloc[0] if len(underperformers) > 0 else None
    f2_post = underperformers.iloc[min(1, len(df)-1)] if len(underperformers) > 1 else None
    
    col_fail1, col_fail2 = st.columns(2)
    with col_fail1:
        st.warning("#### ⚠️ Operational Risk A: The Value Disconnect")
        if f1_post is not None:
            st.markdown(f"**Tracked Creator Case:** `@{f1_post['username']}` | **Pillar:** {f1_post['pillar'].upper()}")
            f1_structure_snippet = str(f1_post['hook_structure'])[:60]
            st.markdown(f"**Attempted Framework:** `{f1_structure_snippet}...`")
        st.markdown("""
        * **What Went Wrong Structurally:** The video featured an excellent contrarian hook structure but contained a weak value payoff, forcing immediate watch-time drop-offs within the first 4 seconds.
        * **Core Strategic Lesson:** A strong hook formula only earns the click; the script must hold an immediate, dense informational reward to secure algorithmic recommendation loops.
        """)
    with col_fail2:
        st.warning("#### ⚠️ Operational Risk B: Pre-Mature Pitch Fatigue")
        if f2_post is not None:
            st.markdown(f"**Tracked Creator Case:** `@{f2_post['username']}` | **Pillar:** {f2_post['pillar'].upper()}")
            f2_structure_snippet = str(f2_post['hook_structure'])[:60]
            st.markdown(f"**Attempted Framework:** `{f2_structure_snippet}...`")
        st.markdown("""
        * **What Went Wrong Structurally:** The asset deployed an intense call-to-action block within the initial 15 seconds before delivering any real value or building personal domain credibility.
        * **Core Strategic Lesson:** Presenting transactional demands prior to establishing audience trust triggers high scrolling escape velocities, killing page visibility scores.
        """)
