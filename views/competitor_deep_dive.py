import streamlit as st

def render(df, global_avg_views):
    st.title("🔍 Advanced Competitor System Audit")
    st.subheader("Top 25 Market Leaders: Extracting Direct Copywriting Mechanics and Steal Scores")
    
    selected_creator = st.selectbox("Select a Competitor Profile to Dissect:", sorted(df["username"].unique()))
    c_df = df[df["username"] == selected_creator].copy().sort_values(by="views", ascending=False)
    
    st.markdown("---")
    st.write(f"#### Performance Inventory for `@{selected_creator}`")

    hook_formulas = []
    conversion_mechanics = []
    strategic_action = []
    action_reason = []
    
    for idx, row in c_df.iterrows():
        caption_text = row["caption"].lower()
        views_val = row["views"]
        
        if "?" in row["caption"][:60]:
            hook_formulas.append("Negative question + shocking number")
        elif any(x in caption_text[:60] for x in ["i ate", "i lost", "my client"]):
            hook_formulas.append("Contrarian claim + personal proof")
        elif any(x in caption_text[:60] for x in ["you", "stop", "if you're"]):
            hook_formulas.append("Direct callout + time promise")
        else:
            hook_formulas.append("Direct Problem Callout Framework")
            
        if "stop" in caption_text or "wrong" in caption_text:
            conversion_mechanics.append("loss_aversion")
        elif "why" in caption_text or "secret" in caption_text:
            conversion_mechanics.append("curiosity_gap")
        else:
            conversion_mechanics.append("specificity_trust")
            
        if any(x in caption_text[:100] for x in ["i was", "my story", "i transformed"]):
            strategic_action.append("SKIP")
            action_reason.append("Too dependent on this specific creator's personal history or viral timeline to replicate effectively.")
        elif views_val > global_avg_views * 1.5:
            strategic_action.append("STEAL")
            action_reason.append("The script relies on a purely structural, transferable psychological layout that will convert on a new account.")
        else:
            strategic_action.append("BUILD")
            action_reason.append("The informational topic is strong, but the script format needs adaptation to break through with low follower counts.")
            
    c_df["hook_formula"] = hook_formulas
    c_df["conversion_mechanic"] = conversion_mechanics
    c_df["action"] = strategic_action
    c_df["reason"] = action_reason

    display_cols = ["views", "comments", "hook_formula", "conversion_mechanic", "action", "reason"]
    st.dataframe(c_df[display_cols], width="stretch")
    
    st.markdown("---")
    st.write("#### Raw Captions & Deployment Proof Panels")
    for idx, row in c_df.iterrows():
        views_str = f"{int(row['views']):,}"
        action_str = str(row['action'])
        expander_title = "📌 Asset: " + views_str + " Views | Strategy Action: " + action_str
        with st.expander(expander_title):
            if row.get('is_alpha', False):
                st.error("🔥 PEAK-VIEW ALPHA POST")
                patterns_str = ""
                if row.get('pattern_1_credibility', False):
                    patterns_str += "✓ Pattern 1: High-Value Credibility Anchoring  \n"
                if row.get('pattern_2_conversion', False):
                    patterns_str += "✓ Pattern 2: Low-Friction Conversion Capture  \n"
                if row.get('pattern_3_identity', False):
                    patterns_str += "✓ Pattern 3: Explicit Identity Bridging  \n"
                if patterns_str:
                    st.markdown("**Successfully Executing:**  \n" + patterns_str)

            hook_formula_str = str(row['hook_formula'])
            st.markdown("**Structural Hook Formula:** `" + hook_formula_str + "`")
            
            reason_str = str(row['reason'])
            st.markdown("**Action Recommendation:** **" + action_str + "** — *" + reason_str + "*")
            
            if str(row["post_url"]) != "nan":
                post_url_str = str(row["post_url"])
                st.markdown("[🔗 Verify Exact Post Evidence](" + post_url_str + ")")
            st.text_area("Scraped Inbound Caption Text", value=row["caption"], height=100, key="deep_" + str(idx))
