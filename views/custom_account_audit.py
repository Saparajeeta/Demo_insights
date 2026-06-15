import streamlit as st
import pandas as pd

def render(df):
    st.title("Custom Account Audit")
    st.subheader("Deep-Dive Performance Analytics for a Specific Profile")
    st.markdown("---")

    username_input = st.text_input("Enter Instagram Username (without @):", "").strip().lower()

    if username_input:
        # Filter dataframe for the requested user
        user_df = df[df["username"].str.lower() == username_input].copy()

        if user_df.empty:
            st.warning("This account is not in the current database. Add them to profiles.csv and re-run the pipeline to include them.")
        else:
            st.markdown(f"### Performance Overview: `@{username_input}`")
            
            # Calculate metrics
            total_posts = len(user_df)
            peak_views = int(user_df["views"].max()) if not user_df["views"].empty else 0
            avg_views = int(user_df["views"].mean()) if not user_df["views"].empty else 0
            
            # Safely calculate avg comments
            if "comments" in user_df.columns and not user_df["comments"].isna().all():
                avg_comments = int(user_df["comments"].mean())
            else:
                avg_comments = 0

            # 1. Total posts found for that account
            # 2. Peak view count
            # 3. Average views
            # 4. Average comments
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Posts", total_posts)
            with col2:
                st.metric("Peak View Count", f"{peak_views:,}")
            with col3:
                st.metric("Average Views", f"{avg_views:,}")
            with col4:
                st.metric("Average Comments", f"{avg_comments:,}")

            st.markdown("---")
            
            # 5. Their pillar mix
            st.markdown("#### Content Pillar Mix")
            if "pillar" in user_df.columns:
                pillar_counts = user_df["pillar"].value_counts().reset_index()
                pillar_counts.columns = ["Pillar", "Post Count"]
                
                # Display as columns for a cleaner look
                cols = st.columns(len(pillar_counts) if len(pillar_counts) > 0 else 1)
                for i, row in pillar_counts.iterrows():
                    with cols[i % len(cols)]:
                        st.metric(str(row["Pillar"]).title(), row["Post Count"])
            else:
                st.info("Pillar data not available.")

            st.markdown("---")

            # 7. Their single best performing post highlighted separately
            st.markdown("#### Top Performing Asset")
            best_post = user_df.sort_values(by="views", ascending=False).iloc[0]
            
            views_str = f"{int(best_post['views']):,}"
            url_str = str(best_post.get("post_url", "https://instagram.com"))
            
            st.success(f"**Peak Performance:** {views_str} Views")
            st.markdown(f"[View Original Post]({url_str})")
            st.text_area("Full Caption Text", value=str(best_post.get("caption", "")), height=150, disabled=True)

            st.markdown("---")

            # 6. A table showing each post
            st.markdown("#### Complete Post Inventory")
            
            # If the specific columns aren't in the global df, calculate them on the fly
            if "hook_formula" not in user_df.columns:
                hook_formulas, conversion_mechanics, actions, reasons = [], [], [], []
                global_avg_views = int(df["views"].mean()) if not df["views"].empty else 0
                
                for idx, row in user_df.iterrows():
                    caption_text = str(row.get("caption", "")).lower()
                    views_val = row.get("views", 0)
                    
                    hook_formulas.append(str(row.get("hook_formula", "Pending AI Analysis")))
                    conversion_mechanics.append(str(row.get("cognitive_trigger", "Pending AI Analysis")))
                        
                    if any(x in caption_text[:100] for x in ["i was", "my story", "i transformed"]):
                        actions.append("Avoid")
                        reasons.append("Too dependent on personal history.")
                    elif views_val > global_avg_views * 1.5:
                        actions.append("Replicate")
                        reasons.append("Transferable psychological layout.")
                    else:
                        actions.append("Adapt")
                        reasons.append("Topic is strong but needs adaptation.")
                
                user_df["hook_formula"] = hook_formulas
                user_df["conversion_mechanic"] = conversion_mechanics
                user_df["action"] = actions
                user_df["reason"] = reasons
            
            # Request columns safely
            desired_columns = ["views", "comments", "pillar", "hook_formula", "conversion_mechanic", "action", "reason", "post_url"]
            available_columns = [col for col in desired_columns if col in user_df.columns]
            
            # Sort by views descending before displaying
            display_df = user_df.sort_values(by="views", ascending=False)[available_columns]
            
            st.dataframe(display_df, use_container_width=True)
