from pytube import YouTube
import os
from dotenv import load_dotenv

load_dotenv()

def download_video(url: str, resolution: str | None, format: str) -> str:
    try:
        yt = YouTube(url)
        # Filter for progressive streams (video + audio) in specified format
        stream = yt.streams.filter(
            file_extension=format,
            progressive=True,
            resolution=resolution if resolution else yt.streams.first().resolution
        ).first()
        
        if not stream:
            raise Exception(f"No stream available for resolution {resolution} and format {format}")
        
        download_path = os.getenv("DOWNLOAD_PATH", "./downloads")
        file_path = stream.download(output_path=download_path)
        return file_path
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")