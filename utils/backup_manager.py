import os
import shutil
import datetime

def backup_downloaded_videos():
    """
    Creates a secure, timestamped zip archive of all downloaded .mp4 files 
    and saves it to a separate safe root directory named 'system_backups/'.
    """
    source_dir = os.path.join("data", "videos")
    backup_dir = "system_backups"
    
    # Check if there is anything to backup
    if not os.path.exists(source_dir) or not os.listdir(source_dir):
        print("No videos found to backup in data/videos/.")
        return

    # Create the backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate timestamp for the archive name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = os.path.join(backup_dir, f"videos_backup_{timestamp}")
    
    print(f"Creating secure backup archive: {archive_name}.zip...")
    
    try:
        # Create a zip archive of the data/videos directory
        shutil.make_archive(archive_name, 'zip', source_dir)
        print(f"✅ Secure backup successfully created at {archive_name}.zip")
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")

if __name__ == "__main__":
    backup_downloaded_videos()
