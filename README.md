# Fat Loss Inbound Intelligence Engine

An enterprise-grade social media data diagnostic platform built to reverse-engineer competitor customer acquisition funnels. This system processes raw public metrics (views, comments, captions) and synthesizes them into actionable, high-ticket organic content playbooks. 

We recently pivoted the engine to strictly audit the **Top 25 Market Leaders** to isolate true alpha signals and eliminate market noise. The engine dynamically audits peak-performing posts for core copywriting triggers such as High-Value Credibility Anchoring, Low-Friction Conversion Capture, and Explicit Identity Bridging.

## 🚀 Features

- **Automated Data Ingestion**: Scrapes the highest-performing assets from target competitor profiles using the Apify cloud infrastructure.
- **Top 25 Market Leader Pivot**: Filters datasets down to the absolute top 25 accounts based on cumulative view velocity.
- **Alpha Post Pattern Auditing**: Uses Google Gemini API to analyze the structural mechanics of top posts (Hooks, CTAs, conversion mechanics).
- **Executive Control Dashboard**: A modular Streamlit application providing 5 distinct strategic lenses:
  1. Macro Market Acquisition Analytics
  2. Competitor System Audit
  3. Validated Inbound Funnel Patterns
  4. 30-Day Go-To-Market Growth Forecast
  5. Under-Served Market Gaps & Failure Modes
- **Smart Link Routing**: Dynamically maps insights back to the original source posts via deep links or engineered Google Search verification queries.

## 📂 Project Structure

```text
fat_loss_insights/
├── app.py                      # Main entry point for the Streamlit dashboard
├── requirements.txt            # Python dependencies
│
├── data/                       # Datasets
│   ├── profiles.csv            # Target competitor handles
│   ├── raw_top_posts.csv       # Scraped raw metrics
│   └── classified_insights.csv # AI-processed final intelligence sheet
│
├── scripts/                    # Automation & processing scripts
│   ├── generate_profiles.py    # Generates initial target profile database
│   ├── data_ingestion.py       # Scrapes Instagram data via Apify
│   └── ai_classifier.py        # Audits captions using Google Gemini 
│
├── utils/                      # Helper modules
│   └── data_loader.py          # Safely loads, cleans, and filters the Top 25 dataset
│
└── views/                      # Streamlit UI Components
    ├── __init__.py
    ├── macro_market.py         
    ├── competitor_deep_dive.py 
    ├── what_works.py           
    ├── go_to_market.py         
    └── blind_spots.py          
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

## 🏃‍♂️ Running the Engine

### Option A: Run the Dashboard (UI Only)
If you just want to explore the data using the pre-compiled `classified_insights.csv` dataset, you can launch the dashboard immediately:
```bash
streamlit run app.py
```
*The dashboard will automatically open in your browser at `http://localhost:8501`.*

### Option B: Run the Full Data Pipeline
If you want to pull fresh data from Instagram and run the AI classification pipeline from scratch:

1. **Generate target profiles**:
   ```bash
   python scripts/generate_profiles.py
   ```
2. **Scrape live market data** (Requires Apify key):
   ```bash
   python scripts/data_ingestion.py
   ```
3. **Run the AI Pattern Audit** (Requires Gemini key):
   ```bash
   python scripts/ai_classifier.py
   ```
4. **Launch the Dashboard**:
   ```bash
   streamlit run app.py
   ```