import yt_dlp
import json

URL = "https://www.youtube.com/watch?v=uynKueSBZm0"

ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)

    print(ydl.sanitize_info(info)["title"])

    # # ℹ️ ydl.sanitize_info makes the info json-serializable
    # with open("example.json", "w") as write_file:
    #     json.dump(ydl.sanitize_info(info), write_file, indent=4)