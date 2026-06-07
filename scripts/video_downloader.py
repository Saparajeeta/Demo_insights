import os
import pandas as pd
import yt_dlp

def download_top_pattern_videos():
    # Set relative directory layouts safely
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.data_loader import load_and_clean_data
    
    output_dir = os.path.join("data", "videos")
    os.makedirs(output_dir, exist_ok=True)
    
    df, _, _, _, _ = load_and_clean_data()
    print(f"Active video ingestion initializing across {len(df)} mapped assets...")
    
    for idx, row in df.iterrows():
        url = str(row.get("post_url", "")).strip()
        username = str(row.get("username", "")).strip().replace("@", "")
        
        # Ensure it's a direct video link, not a generic account timeline index layout
        if any(marker in url for marker in ["/p/", "/reel/", "/tv/"]):
            filename = f"{username}_{idx}.mp4"
            target_path = os.path.join(output_dir, filename)
            
            if os.path.exists(target_path):
                print(f"Skipping: {filename} is already cached locally.")
                continue
                
            print(f"Downloading media asset for @{username} via direct link...")
            
            # 🎯 UPDATED EXTRACTOR FLAGS USING LOCAL COOKIES.TXT
            ydl_opts = {
                'outtmpl': target_path,
                'format': 'mp4',
                'quiet': False,
                # Points directly to the cookies.txt file you successfully placed in the root directory
                'cookiefile': 'cookies.txt', 
                'ignoreerrors': True
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                print(f"Success. Saved to: {target_path}")
            except Exception as e:
                print(f"Extractor skipped asset path: {str(e)}")
    # Execute automated backup to freeze assets
    try:
        from utils.backup_manager import backup_downloaded_videos
        print("\nLocking down assets...")
        backup_downloaded_videos()
    except Exception as e:
        print(f"Backup manager failed: {e}")

if __name__ == "__main__":
    download_top_pattern_videos()
