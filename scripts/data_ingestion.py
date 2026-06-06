import os
import re
import pandas as pd
from apify_client import ApifyClient
from dotenv import load_dotenv

# Load tokens
load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")
client = ApifyClient(APIFY_TOKEN)

# Load profile list
profiles_df = pd.read_csv("../data/profiles.csv")

# 🔍 DEFENSIVE SANITIZATION: Only keep usernames that match Instagram's strict naming rules
valid_username_regex = re.compile(r"^[A-Za-z0-9._-]+$")
usernames_list = []

for name in profiles_df["username"].tolist():
    cleaned_name = name.strip().replace("@", "")
    if valid_username_regex.match(cleaned_name):
        usernames_list.append(cleaned_name)
    else:
        print(f"⚠️ Skipping invalid character username: '{name}'")

# Configure input using the verified clean list
run_input = {
    "directUrls": [f"https://www.instagram.com/{user}/" for user in usernames_list],
    "resultsLimit": 10,             
    "resultsType": "posts",
    "searchType": "user",
    "searchLimit": 1
}

print(f"🚀 Initializing Apify Cloud Infrastructure for {len(usernames_list)} profiles...")
print("Please wait, handling residential proxies and bypassing login walls safely...")

try:
    # Call the specialized actor
    run = client.actor("apify/instagram-scraper").call(run_input=run_input)
    
    # 4. Extract items from the cloud dataset storage
    raw_posts = []
    print("📥 Extraction successful! Downloading items from Apify dataset storage...")
    
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        # Clean and extract metrics
        raw_posts.append({
            "username": item.get("ownerUsername"),
            "caption": item.get("caption", ""),
            "likes": item.get("likesCount", 0),
            "comments": item.get("commentsCount", 0),
            "views": item.get("videoViewCount", 0 if item.get("videoViewCount") is None else item.get("videoViewCount")), 
            "post_url": item.get("url")
        })

    # 5. Handle empty datasets if profiles are misspelled or set to private
    if not raw_posts:
        print("⚠️ Warning: Apify returned 0 items. Ensure your profile names in profiles.csv are public and spelled correctly.")
        exit()

    df_all_posts = pd.DataFrame(raw_posts)
    print(f"📊 Downloaded {len(df_all_posts)} total raw posts.")

    # 6. Filter for the TOP 3 highest-performing posts per user based on Views
    # If a post is an image (views=0), likes will serve as secondary sorting metric
    df_top_posts = (
        df_all_posts.sort_values(by=["username", "views", "likes"], ascending=[True, False, False])
        .groupby("username")
        .head(3)
        .reset_index(drop=True)
    )

    # Save to local directory
    df_top_posts.to_csv("../data/raw_top_posts.csv", index=False)
    print(f"✅ Success! Isolated the top 3 posts per profile. Saved {len(df_top_posts)} rows to 'raw_top_posts.csv'.")

except Exception as e:
    print(f"❌ An error occurred during runtime: {e}")