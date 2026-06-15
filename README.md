# Fat Loss Inbound Intelligence Engine

An enterprise-grade social media data diagnostic platform built to reverse-engineer competitor customer acquisition funnels. This system processes raw public metrics (views, comments, captions) and synthesizes them into actionable, high-ticket organic content playbooks. 

We recently pivoted the engine to strictly audit the **Top 25 Market Leaders** to isolate true signals and eliminate market noise. The engine dynamically audits peak-performing posts for core copywriting triggers such as High-Value Credibility Anchoring, Low-Friction Conversion Capture, and Explicit Identity Bridging.

## 🚀 Features

- **Automated Video Ingestion Pipeline**: Scrapes high-performing `.mp4` video assets directly from Instagram using `yt-dlp` with automated cookie-based authentication bypass.
- **Live AI Multimodal Video Auditing**: Uses the Google Gemini 2.5 Flash API to analyze video files frame-by-frame, extracting verbal hook pacing, visual text pop-ups, and physical setting strategies.
- **Dynamic AI Text Analysis**: Fully automated hook structure extraction and pillar classification powered by Gemini, featuring multi-layer keyword fallbacks to ensure 100% data integrity.
- **Signature Performance Benchmarks**: Highlights elite-tier content patterns with dynamically calculated confidence scores based on real-time dataset ratios.
- **Dynamic Executive Dashboards**: Fully interactive Streamlit UI featuring:
  - Live Reach vs. Conversion Leak Gap calculations.
  - Interactive 30-Day Go-To-Market Growth Forecast natively driven by phase-specific dataset averages and dynamically selected top CTAs.
  - Live AI-driven Market Gaps Analysis finding unmet demand across the dataset.
  - Failure Mode Distribution Analysis with bar charts and interactive under-performer dataframes.
- **Secure File Lockdown**: Automated `backup_manager.py` that securely archives downloaded media assets to prevent accidental overwrites or data loss.

## 📂 Project Structure

```text
fat_loss_insights/
├── app.py                      # Main entry point for the Streamlit dashboard
├── requirements.txt            # Python dependencies
├── cookies.txt                 # Browser cookies for authenticating video downloads
│
├── data/                       # Datasets & Media
│   ├── classified_insights.csv # AI-processed final intelligence sheet
│   └── videos/                 # Local cache of downloaded Instagram .mp4 files
│
├── system_backups/             # Secure .zip archives of downloaded video assets
│
├── scripts/                    # Automation & processing scripts
│   ├── data_ingestion.py       # Scrapes Instagram metadata
│   ├── ai_classifier.py        # Audits captions using Google Gemini 
│   ├── video_downloader.py     # Downloads .mp4 media assets using yt-dlp
│   └── video_analyzer.py       # Live multimodal Gemini 2.5 Flash video audit engine
│
├── utils/                      # Helper modules
│   ├── data_loader.py          # Loads, cleans, and filters the Top 25 dataset
│   └── backup_manager.py       # Zips and freezes downloaded video assets
│
└── views/                      # Streamlit UI Components
    ├── __init__.py
    ├── macro_market.py         # Visual pattern match rates and calculated funnels
    ├── competitor_deep_dive.py # Deep dive with multimodal video inspector
    ├── what_works.py           # Verification evidence matrix
    ├── go_to_market.py         # Interactive 30-day projection modeling
    └── blind_spots.py          # Execution error frequency charts
```

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fat-loss-inbound-intelligence.git
cd fat_loss_insights
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
The background scripts require API keys to gather and process data. Create a `.env` file in the root directory and add the following:
```env
APIFY_API_TOKEN=your_apify_key_here
GEMINI_API_KEY=your_google_gemini_key_here
```

### 4. Configure Authentication Cookies
To download videos natively, export your active Instagram browser session cookies and save them as `cookies.txt` in the root directory.

## 🏃‍♂️ Running the Engine

### Option A: Run the Dashboard (UI Only)
Launch the fully interactive Streamlit application to explore the data:
```bash
streamlit run app.py
```
*The dashboard will automatically open in your browser at `http://localhost:8501`.*

### Option B: Run the Media Ingestion Pipeline
If you want to pull fresh video files directly from the Instagram API and lock them down:
```bash
python scripts/video_downloader.py
```
*Note: This script automatically calls `utils/backup_manager.py` upon completion to archive your assets safely.*