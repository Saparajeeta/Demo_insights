import streamlit as st
import os
from scripts.video_analyzer import analyze_organic_video_asset
def render(df, global_avg_views):
    st.title("Competitor Performance Analysis")
    st.subheader("Analyzing Content Strategies and Recommendations")
    
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
        
        hook_formulas.append(str(row.get("hook_formula", "Pending AI Analysis")))
        conversion_mechanics.append(str(row.get("cognitive_trigger", "Pending AI Analysis")))
            
        if any(x in caption_text[:100] for x in ["i was", "my story", "i transformed"]):
            strategic_action.append("Avoid")
            action_reason.append("Too dependent on this specific creator's personal history or viral timeline to replicate effectively.")
        elif views_val > global_avg_views * 1.5:
            strategic_action.append("Replicate")
            action_reason.append("The script relies on a transferable psychological layout that will convert on a new account.")
        else:
            strategic_action.append("Adapt")
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
        expander_title = "Asset: " + views_str + " Views | Strategy Action: " + action_str
        with st.expander(expander_title):
            if row.get('is_signature_asset', False):
                st.error("SIGNATURE PERFORMANCE BENCHMARK")
                patterns_str = ""
                if row.get('pattern_1_credibility', False):
                    patterns_str += "Pattern 1: High-Value Credibility Anchoring  \n"
                if row.get('pattern_2_conversion', False):
                    patterns_str += "Pattern 2: Low-Friction Conversion Capture  \n"
                if row.get('pattern_3_identity', False):
                    patterns_str += "Pattern 3: Explicit Identity Bridging  \n"
                if patterns_str:
                    st.markdown("**Successfully Executing:**  \n" + patterns_str)

            hook_formula_str = str(row['hook_formula'])
            st.markdown("**Content Hook Strategy:** `" + hook_formula_str + "`")
            
            reason_str = str(row['reason'])
            st.markdown("**Action Recommendation:** **" + action_str + "** — *" + reason_str + "*")
            
            if str(row["post_url"]) != "nan":
                post_url_str = str(row["post_url"])
                st.markdown("[View Original Post](" + post_url_str + ")")
            st.text_area("Original Caption Text", value=row["caption"], height=100, key="deep_" + str(idx))
            
            import os
            username_str = str(row['username'])
            post_id_str = str(idx)
            video_path = "data/videos/" + username_str + "_" + post_id_str + ".mp4"
            with st.expander("Video Content Analysis"):
                if os.path.exists(video_path):
                    st.video(video_path)
                    
                    if st.button("Run Video Analysis", key=f"run_ai_{idx}"):
                        with st.spinner("Analyzing audio frequencies and visual frames..."):
                            analysis_results = analyze_organic_video_asset(video_path)
                            st.session_state[f"cached_analysis_{idx}"] = analysis_results
                    
                    cached = st.session_state.get(f"cached_analysis_{idx}", None)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown("**Verbal Script Delivery & Hook Pacing**")
                        st.info(cached["verbal"] if cached else "Awaiting analysis trigger...")
                    with col2:
                        st.markdown("**Visual Hook Actions & On-Screen Text**")
                        st.info(cached["visual"] if cached else "Awaiting analysis trigger...")
                    with col3:
                        st.markdown("**Physical Body Language & Setting Strategy**")
                        st.info(cached["physical"] if cached else "Awaiting analysis trigger...")
                else:
                    st.warning(f"Media asset file '{username_str}_{post_id_str}.mp4' is not currently cached.")
                    if str(row["post_url"]) != "nan":
                        post_url_str = str(row["post_url"])
                        st.markdown(f"[View Video on Instagram]({post_url_str})")
