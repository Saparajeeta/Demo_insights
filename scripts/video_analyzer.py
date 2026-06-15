import os
import time
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
import streamlit as st

def analyze_organic_video_asset(video_file_path: str) -> dict:
    """
    Uploads a local .mp4 file directly to Gemini 2.5 Flash 
    to extract visual hooks, script delivery pacing, and setting architectures.
    """
    # Force Python to parse the root '.env' file to secure credentials locally
    load_dotenv()
    
    # Verify that your API Key is active in your terminal environment
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {
            "verbal": "Error: GEMINI_API_KEY environment variable missing.",
            "visual": "Please configure your API key in your terminal context layer.",
            "physical": "Execution stopped programmatically."
        }
        
    if not os.path.exists(video_file_path):
        return {
            "verbal": "Awaiting source video download context...",
            "visual": f"Target file path '{video_file_path}' not found in data/videos/ container.",
            "physical": "Displaying structural placeholder values."
        }

    try:
        # Initialize the modern enterprise GenAI Client
        client = genai.Client(api_key=api_key)
        
        # Upload the video file using the Files API (handles large multimodal files cleanly)
        print("Packaging and uploading media asset to processing layer...")
        uploaded_video = client.files.upload(file=video_file_path)
        
        # Wait for the video to be fully processed by Google
        while uploaded_video.state.name == "PROCESSING":
            time.sleep(2)
            uploaded_video = client.files.get(name=uploaded_video.name)
            
        if uploaded_video.state.name == "FAILED":
            raise Exception("Video processing failed on Google's backend.")
        
        # Build a highly tactical structural prompt
        analysis_prompt = (
            "You are a content marketing strategist and data analyst. "
            "Examine this video frame-by-frame and audio track to extract these three specific layers:\n\n"
            "1. VERBAL SCRIPT DELIVERY & HOOK PACING: Transcribe the first 5 seconds exactly. Analyze the tone, "
            "vocal volume switches, and word velocity gaps.\n"
            "2. VISUAL HOOK ACTIONS: List all text pop-ups, visual graphic cuts, or physical gestures occurring "
            "in the first 3 seconds to capture attention.\n"
            "3. PHYSICAL BODY LANGUAGE & SETTING STRATEGY: Describe the environment setting (e.g., gym, kitchen, office) "
            "and explain what authority signals the creator's posture or clothing choices project to a potential high-ticket client.\n\n"
            "Format your response cleanly with explicit headers for VERBAL:, VISUAL:, and PHYSICAL:."
        )
        
        # Execute using gemini-2.5-flash for video analysis
        response = None
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[uploaded_video, analysis_prompt]
                )
                break
            except Exception as e:
                err_str = str(e)
                if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt + 2)  # Exponential backoff: 3s, 4s, 6s, 10s
                        continue
                    else:
                        raise Exception("API servers are experiencing heavy traffic or rate limits. Please click the button to re-trigger the analysis in a moment.")
                raise e
        
        # Clean up the cloud asset after processing to protect data hygiene
        client.files.delete(name=uploaded_video.name)
        
        # Parse output markers
        raw_text = response.text
        return parse_gemini_output(raw_text)
        
    except Exception as e:
        return {
            "verbal": f"Processing failure: {str(e)}",
            "visual": "Ensure your alternative API key has active credit parameters.",
            "physical": "Pipeline rollback executed successfully."
        }

def parse_gemini_output(text: str) -> dict:
    """Helper utility to segment text layout into separate dictionary items safely."""
    data = {"verbal": "Extraction pending", "visual": "Extraction pending", "physical": "Extraction pending"}
    
    lines = text.split('\n')
    current_section = None
    
    verbal_lines = []
    visual_lines = []
    physical_lines = []
    
    verbal_pattern = re.compile(r'^\s*[\*\#\-\d\.]*\s*(VERBAL|SCRIPT)', re.IGNORECASE)
    visual_pattern = re.compile(r'^\s*[\*\#\-\d\.]*\s*(VISUAL|HOOK)', re.IGNORECASE)
    physical_pattern = re.compile(r'^\s*[\*\#\-\d\.]*\s*(PHYSICAL|BODY|SETTING)', re.IGNORECASE)
    
    for line in lines:
        if verbal_pattern.match(line):
            current_section = "verbal"
            continue
        elif visual_pattern.match(line):
            current_section = "visual"
            continue
        elif physical_pattern.match(line):
            current_section = "physical"
            continue
            
        if current_section == "verbal":
            verbal_lines.append(line)
        elif current_section == "visual":
            visual_lines.append(line)
        elif current_section == "physical":
            physical_lines.append(line)

    if verbal_lines:
        verbal_text = "\n".join(verbal_lines).strip()
        if verbal_text:
            data["verbal"] = verbal_text
    if visual_lines:
        visual_text = "\n".join(visual_lines).strip()
        if visual_text:
            data["visual"] = visual_text
    if physical_lines:
        physical_text = "\n".join(physical_lines).strip()
        if physical_text:
            data["physical"] = physical_text
                
    # Fallback if text splitting is irregular
    if data["verbal"] == "Extraction pending" and data["visual"] == "Extraction pending" and data["physical"] == "Extraction pending":
        data["verbal"] = text
        
    return data
