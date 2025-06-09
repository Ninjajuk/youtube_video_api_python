# from pytube import YouTube

# def get_video_metadata(url: str) -> dict:
#     try:
#         print(f"[DEBUG] Downloading metadata from: {url}")
#         yt = YouTube(url)
#         print(f"[DEBUG] Title: {yt.title}")
#         return {
#             "title": yt.title,
#             "author": yt.author,
#             "length": yt.length,
#             "views": yt.views,
#             "publish_date": yt.publish_date.strftime('%Y-%m-%d'),
#             "description": yt.description[:200]
#         }
#     except Exception as e:
#         print(f"[ERROR] Failed in get_video_metadata: {e}")
#         raise e  # Rethrow so the FastAPI route catches it


import yt_dlp

def get_video_metadata(url: str) -> dict:
    try:
        print(f"[DEBUG] Fetching metadata from: {url}")
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return {
            "title": info.get("title"),
            "author": info.get("uploader"),
            "length": info.get("duration"),
            "views": info.get("view_count"),
            "publish_date": info.get("upload_date", "")[:4] + "-" + info.get("upload_date", "")[4:6] + "-" + info.get("upload_date", "")[6:],
            "description": info.get("description", "")[:200],
        }

    except Exception as e:
        print(f"[ERROR] yt-dlp failed: {e}")
        raise e
