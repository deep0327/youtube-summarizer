from urllib.parse import urlparse,parse_qs
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video_parts=urlparse(url)
video_id=parse_qs(video_parts.query)["v"][0]
print(video_parts)
print(video_parts.query)
print(video_id)