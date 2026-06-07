import pandas as pd
import streamlit as st

@st.cache_data
def load_and_clean_data():
    try:
        df = pd.read_csv("data/classified_insights.csv")
    except FileNotFoundError:
        st.error("Missing 'data/classified_insights.csv'. Please run your ingestion/classification scripts first!")
        st.stop()

    # Attempt to merge real post_urls from raw_top_posts if it exists
    try:
        raw_df = pd.read_csv("data/raw_top_posts.csv")
        raw_urls = raw_df[['username', 'caption', 'post_url']].drop_duplicates(subset=['username', 'caption'])
        df = df.merge(raw_urls, on=['username', 'caption'], how='left')
    except FileNotFoundError:
        pass

    if "pillar" not in df.columns:
        df["pillar"] = df["category"].str.lower().str.replace(" ", "_") if "category" in df.columns else "viral_reach"

    if "why_it_converts" not in df.columns:
        df["why_it_converts"] = df["marketing_takeaway"] if "marketing_takeaway" in df.columns else "High-performing structural framework pattern."

    df["why_it_converts"] = df["why_it_converts"].astype(str).apply(
        lambda x: "⏳ Rate limit hit — cached on next run" if "429" in x or "error" in x.lower() else x
    )

    if "hook_structure" not in df.columns:
        df["hook_structure"] = "Hook analysis pending"
    else:
        df["hook_structure"] = df["hook_structure"].astype(str).apply(
            lambda x: x if len(x) > 20 else "Hook analysis pending"
        )

    if "post_url" not in df.columns:
        df["post_url"] = "https://instagram.com"

    df["caption"] = df["caption"].astype(str)
    df["pillar"] = df["pillar"].astype(str).str.lower().str.strip()
    df["username"] = df["username"].astype(str).str.replace("@", "", regex=False).str.strip()

    import re
    
    def clean_post_url(row):
        url = str(row.get("post_url", ""))
        username = str(row.get("username", ""))
        caption = str(row.get("caption", ""))
        
        # If it's already a direct post link, preserve it
        if "/p/" in url or "/reel/" in url:
            return url
            
        # If it's missing or generic, build Instagram native link
        if not url or url == "nan" or url.strip() in ["https://instagram.com", "https://instagram.com/"]:
            if username and username != "nan" and username != "N/A":
                hook_text = caption[:30]
                cleaned_hook_word = re.sub(r'[^a-zA-Z0-9]', '', hook_text)
                if cleaned_hook_word:
                    search_url = f"https://www.instagram.com/explore/tags/{cleaned_hook_word}/"
                else:
                    search_url = f"https://www.instagram.com/{username}/reels/"
                return search_url
            return "https://instagram.com"
            
        return url

    df["post_url"] = df.apply(clean_post_url, axis=1)

    # Top 25 Market Leaders Logic
    user_views = df.groupby('username')['views'].sum().reset_index()
    top_25_users = user_views.sort_values(by='views', ascending=False).head(25)['username'].tolist()
    
    df = df[df['username'].isin(top_25_users)].copy()
    
    # Alpha Post Identification
    alpha_indices = df.groupby('username')['views'].idxmax()
    df['is_alpha'] = False
    df.loc[alpha_indices, 'is_alpha'] = True
    
    # Pattern Audit
    df['pattern_1_credibility'] = False
    df['pattern_2_conversion'] = False
    df['pattern_3_identity'] = False
    
    cred_keywords = ['myth', 'clinical', 'case study', 'science', 'research']
    df.loc[df['is_alpha'], 'pattern_1_credibility'] = df.loc[df['is_alpha']].apply(
        lambda row: 'credibility' in str(row['pillar']) or 'authority' in str(row['pillar']) or any(kw in str(row['caption']).lower() for kw in cred_keywords), axis=1
    )
    
    df.loc[df['is_alpha'], 'pattern_2_conversion'] = df.loc[df['is_alpha'], 'caption'].str.contains(r'comment\s+\w+', case=False, na=False)
    
    identity_keywords = ['i help', 'i coach', 'my clients', 'i transform', 'my mission', 'we help']
    df.loc[df['is_alpha'], 'pattern_3_identity'] = df.loc[df['is_alpha'], 'caption'].apply(
        lambda x: any(kw in str(x).lower() for kw in identity_keywords)
    )

    total_profiles = df["username"].nunique()
    total_posts = len(df)
    global_avg_views = int(df["views"].mean()) if total_posts > 0 else 0
    global_avg_comments = int(df["comments"].mean()) if total_posts > 0 else 0
    
    return df, total_profiles, total_posts, global_avg_views, global_avg_comments
