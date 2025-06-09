import yt_dlp

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

ydl_opts = {
    'quiet': True,
    'skip_download': True,
    'forcejson': True
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    formats = info['formats']
    for fmt in formats:
        print(f"{fmt['format_id']}: {fmt.get('ext')} - {fmt.get('height')}p - {fmt.get('vcodec')} / {fmt.get('acodec')}")
