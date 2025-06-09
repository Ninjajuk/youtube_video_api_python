from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from api.schemas import VideoRequest, VideoMetadata
from services.downloader import download_video
from services.metadat import get_video_metadata
import os
import yt_dlp
import uuid

router = APIRouter()

@router.post("/metadata", response_model=VideoMetadata)
async def fetch_metadata(request: VideoRequest):
    try:
        metadata = get_video_metadata(str(request.url)) 
        return metadata
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch metadata: {str(e)}")

# @router.post("/download")
# async def download_video(request: VideoRequest):
#     try:
#         output_dir = "downloads"
#         os.makedirs(output_dir, exist_ok=True)

#         filename = f"{uuid.uuid4()}.%(ext)s"
#         output_template = os.path.join(output_dir, filename)

#         ydl_opts = {
#             'format': f'bestvideo[height<={request.resolution[:-1]}]+bestaudio/best',
#             'outtmpl': output_template,
#             'merge_output_format': request.format,
#             'quiet': True,
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(str(request.url), download=True)
#             downloaded_file = ydl.prepare_filename(info).replace("%(ext)s", request.format)

#         # Ensure file exists
#         if not os.path.exists(downloaded_file):
#             raise HTTPException(status_code=404, detail="File not found after download")

#         return FileResponse(
#             downloaded_file,
#             media_type=f"video/{request.format}",
#             filename=os.path.basename(downloaded_file)
#         )

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Failed to download video: {str(e)}")

@router.post("/download")
async def download_video(request: VideoRequest):
    try:
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)

        temp_id = uuid.uuid4().hex
        filename_template = os.path.join(output_dir, f"{temp_id}.%(ext)s")

        # ✅ This tells yt-dlp to pick best progressive (muxed) format <= requested height
        ydl_opts = {
            'format': f'best[height<={request.resolution[:-1]}][vcodec!=none][acodec!=none]',
            'outtmpl': filename_template,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(str(request.url), download=True)
            actual_ext = info.get("ext", "mp4")
            downloaded_path = filename_template.replace("%(ext)s", actual_ext)

        if not os.path.exists(downloaded_path):
            raise HTTPException(status_code=404, detail="File not found after download")

        return FileResponse(
            downloaded_path,
            media_type=f"video/{actual_ext}",
            filename=os.path.basename(downloaded_path)
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Download failed: {str(e)}")

# @router.post("/list-formats")
# async def list_formats(request: VideoRequest):
#     try:
#         with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
#             info = ydl.extract_info(str(request.url), download=False)
#         return {"formats": info["formats"]}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Failed to list formats: {str(e)}")


@router.post("/ajuk")
async def samsu():
    return {"message": "I love you Samsu. Ajuk is missing you so much"}