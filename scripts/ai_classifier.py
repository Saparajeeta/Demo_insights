import os
import json
import time
import pandas as pd
from google import genai
from google.genai import types
from google.genai.errors import APIError
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

def extract_structural_mechanics(caption, max_retries=5):
    """Processes the caption strictly through the direct-response structural blueprint."""
    prompt = f"""
    You are a direct-response copywriting analyst. Analyze this Instagram caption and extract ONLY structural mechanics — no tone descriptions, no vibe observations.
    
    Return a JSON object with:
    - hook_structure: the exact format of the first 1–2 lines (e.g. "Pain question + bold claim", "Contrarian stat + challenge", "You're doing X wrong + proof")
    - hook_word_count: integer
    - cta_type: one of [DM_keyword, comment_keyword, link_in_bio, none]
    - cta_placement: one of [first_3_seconds, mid_video, end_only]
    - pillar: one of [credibility_building, viral_reach, lead_generation]
    - why_it_converts: one sentence. Describe the structural mechanic, not the tone. Why does this specific format trigger saves/DMs/comments? Reference cognitive triggers (curiosity gap, loss aversion, social proof, specificity) where applicable.
    - red_flags: any structural weaknesses (buried CTA, no clear hook, etc.)
    
    Caption: {caption}
    """
    
    wait_time = 5
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            return json.loads(response.text)
        except APIError as e:
            if e.code == 429:
                print(f"⚠️ Rate limit hit. Backing off for {wait_time}s...")
                time.sleep(wait_time)
                wait_time *= 2
            else:
                return {"hook_structure": "Unknown Structure", "hook_word_count": 0, "cta_type": "none", "cta_placement": "end_only", "pillar": "viral_reach", "why_it_converts": "Fallback due to API error.", "red_flags": "None"}
        except Exception:
            return {"hook_structure": "Unknown Structure", "hook_word_count": 0, "cta_type": "none", "cta_placement": "end_only", "pillar": "viral_reach", "why_it_converts": "General system error.", "red_flags": "None"}
            
    return {"hook_structure": "Unknown Structure", "hook_word_count": 0, "cta_type": "none", "cta_placement": "end_only", "pillar": "viral_reach", "why_it_converts": "Quota limitation threshold met.", "red_flags": "None"}

try:
    df = pd.read_csv("../data/raw_top_posts.csv")
except FileNotFoundError:
    print("❌ Error: '../data/raw_top_posts.csv' missing.")
    exit()

processed_records = []
print("🧠 Extracting direct-response structural metrics...")

for idx, row in df.iterrows():
    print(f"Analyzing {idx + 1}/{len(df)}: @{row['username']}...")
    analysis = extract_structural_mechanics(row['caption'])
    
    processed_records.append({
        "username": row["username"],
        "views": row["views"],
        "likes": row["likes"],
        "comments": row["comments"],
        "post_url": row["post_url"],
        "caption": row["caption"],
        "hook_structure": analysis.get("hook_structure"),
        "hook_word_count": analysis.get("hook_word_count"),
        "cta_type": analysis.get("cta_type"),
        "cta_placement": analysis.get("cta_placement"),
        "pillar": analysis.get("pillar"),
        "why_it_converts": analysis.get("why_it_converts"),
        "red_flags": analysis.get("red_flags")
    })
    time.sleep(1.5)

df_final = pd.DataFrame(processed_records)
df_final.to_csv("../data/classified_insights.csv", index=False)
print("🎯 High-fidelity pattern library compiled successfully into 'classified_insights.csv'!")