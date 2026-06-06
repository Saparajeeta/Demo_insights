import os
import pandas as pd
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Target the exact successful run ID from your terminal log
RUN_ID = "Mhen6nYHjPCGoObQu"

print(f"📥 Connecting directly to cloud run storage [{RUN_ID}]...")

try:
    # Fetch the specific run details
    run_details = client.run(RUN_ID).get()
    dataset_id = run_details["defaultDatasetId"]
    print(f"✅ Found Dataset ID: {dataset_id}. Downloading 846 posts...")
    
    raw_posts = []
    for item in client.dataset(dataset_id).iterate_items():
        raw_posts.append({
            "username": item.get("ownerUsername"),
            "caption": item.get("caption", ""),
            "likes": item.get("likesCount", 0),
            "comments": item.get("commentsCount", 0),
            "views": item.get("videoViewCount", 0 if item.get("videoViewCount") is None else item.get("videoViewCount")), 
            "post_url": item.get("url")
        })

    df_all_posts = pd.DataFrame(raw_posts)
    print(f"📊 Successfully pulled {len(df_all_posts)} raw posts from the cloud storage.")

    # Filter for the TOP 3 highest-performing posts per competitor
    df_top_posts = (
        df_all_posts.sort_values(by=["username", "views", "likes"], ascending=[True, False, False])
        .groupby("username")
        .head(3)
        .reset_index(drop=True)
    )

    # Save to your local directory
    df_top_posts.to_csv("raw_top_posts.csv", index=False)
    print(f"✅ Success! Isolated top performers and saved {len(df_top_posts)} rows to 'raw_top_posts.csv'.")

except Exception as e:
    print(f"❌ Direct download failed: {e}")
    print("Please make sure your APIFY_API_TOKEN in your .env matches the account that initiated the run.")