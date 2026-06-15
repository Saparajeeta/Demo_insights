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
                return {"hook_structure": "Unknown Structure", "hook_word_count": 0, "cta_type": "none", "cta_placement": "end_only", "pillar": "429_error", "why_it_converts": "Fallback due to API error.", "red_flags": "None"}
        except Exception:
            return {"hook_structure": "Unknown Structure", "hook_word_count": 0, "cta_type": "none", "cta_placement": "end_only", "pillar": "429_error", "why_it_converts": "General system error.", "red_flags": "None"}
            
    return {"hook_structure": "Unknown Structure", "hook_word_count": 0, "cta_type": "none", "cta_placement": "end_only", "pillar": "429_error", "why_it_converts": "Quota limitation threshold met.", "red_flags": "None"}

def classify_hook_formula(caption, max_retries=5):
    prompt = f"""
    Analyze the opening hook of this Instagram caption.
    Return ONLY a JSON object with these keys:
    
    - hook_formula: the exact structural pattern used
      (e.g. "Pain question + shocking stat", 
      "Contrarian claim + personal proof",
      "Direct callout + time promise",
      "Myth bust + clinical fact",
      "Before/after + identity claim")
      Do NOT say "uses humor" or describe tone.
      Describe the STRUCTURE only.
    
    - hook_word_count: integer, words in first sentence only
    
    - cognitive_trigger: one of [curiosity_gap, 
      loss_aversion, social_proof, specificity_trust, 
      identity_claim, authority_transfer]
    
    - confidence: high/medium/low based on how clearly 
      this caption follows a recognizable formula
    
    Caption: {caption[:300]}
    
    Return only valid JSON. No explanation. No markdown.
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
                return {"hook_formula": "Unknown", "hook_word_count": 0, "cognitive_trigger": "none", "confidence": "low"}
        except Exception:
            return {"hook_formula": "Unknown", "hook_word_count": 0, "cognitive_trigger": "none", "confidence": "low"}
            
    return {"hook_formula": "Unknown", "hook_word_count": 0, "cognitive_trigger": "none", "confidence": "low"}

def find_market_gaps(df):
    all_captions = " ".join(df["caption"].dropna().tolist())
    
    prompt = f"""
    You are analyzing Instagram captions from 100 fat loss creators.
    
    Find 3 content gaps — topics where:
    1. Creators mention it briefly or audience asks about it 
       in passing (showing demand exists)
    2. But fewer than 5 dedicated posts exist on this topic
       (showing low supply)
    
    For each gap return:
    - gap_name: short title
    - demand_signal: exact phrase or pattern from the 
      captions showing people want this
    - estimated_posts_on_topic: integer
    - opportunity: one sentence on why a new brand 
      should own this topic
    
    Return only a JSON array of 3 objects.
    
    Captions sample: {all_captions[:4000]}
    """
    print("🧠 Analyzing captions to extract market gaps...")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        gaps = json.loads(response.text)
        with open("../data/market_gaps.json", "w") as f:
            json.dump(gaps, f, indent=4)
        print("🎯 Market gaps saved to 'market_gaps.json'")
    except Exception as e:
        print(f"⚠️ Error generating market gaps: {e}")

def classify_pillar(caption, gemini_result):
    # Layer 1: Trust Gemini if it returned cleanly
    if gemini_result and "429" not in str(gemini_result):
        return gemini_result
    
    # Layer 2: Keyword fallback if Gemini failed
    caption_lower = caption.lower()
    
    lead_keywords = ["dm me", "comment", "link in bio", 
                     "apply", "free call", "consultation",
                     "slots open", "message me", "book"]
    
    viral_keywords = ["recipe", "calories", "macro", 
                      "try this", "hack", "tip", "trick",
                      "easy", "quick", "simple"]
    
    credibility_keywords = ["study", "research", "science",
                            "clinical", "doctor", "proof",
                            "evidence", "data", "published",
                            "my client", "case study",
                            "before and after", "results"]
    
    lead_score = sum(1 for w in lead_keywords if w in caption_lower)
    viral_score = sum(1 for w in viral_keywords if w in caption_lower)
    cred_score = sum(1 for w in credibility_keywords if w in caption_lower)
    
    scores = {"lead_generation": lead_score, 
              "viral_reach": viral_score,
              "credibility_building": cred_score}
    
    return max(scores, key=scores.get)

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
    hook_analysis = classify_hook_formula(row['caption'])
    final_pillar = classify_pillar(row['caption'], analysis.get("pillar"))
    
    processed_records.append({
        "username": row["username"],
        "views": row["views"],
        "likes": row["likes"],
        "comments": row["comments"],
        "post_url": row["post_url"],
        "caption": row["caption"],
        "hook_structure": analysis.get("hook_structure"),
        "hook_formula": hook_analysis.get("hook_formula"),
        "hook_word_count": hook_analysis.get("hook_word_count", analysis.get("hook_word_count")),
        "cognitive_trigger": hook_analysis.get("cognitive_trigger"),
        "confidence": hook_analysis.get("confidence"),
        "cta_type": analysis.get("cta_type"),
        "cta_placement": analysis.get("cta_placement"),
        "pillar": final_pillar,
        "why_it_converts": analysis.get("why_it_converts"),
        "red_flags": analysis.get("red_flags")
    })
    time.sleep(1.5)

df_final = pd.DataFrame(processed_records)
df_final.to_csv("../data/classified_insights.csv", index=False)
print("🎯 High-fidelity pattern library compiled successfully into 'classified_insights.csv'!")

# Run the one-time market gaps analysis
find_market_gaps(df)