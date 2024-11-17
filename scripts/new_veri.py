import os
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

# API anahtarınızı buraya ekleyin
API_KEY = 'AIzaSyCrXhHBb6jtQhfzPeSTcH8oZ1gYTJsBjHI' 

# YouTube API istemcisini oluşturma
def get_youtube_comments(video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    
    comments = []
    # İlk 100 yorumu çekmek için YouTube API'sini kullanma
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100  # Max yorum sayısı
    )
    
    while request:
        response = request.execute()
        
        # Yorumları işleme
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            
            comments.append({
                "author": author,
                "comment": comment
            })
        
        # Eğer daha fazla yorum varsa, sonraki sayfayı çekmek
        if "nextPageToken" in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,
                pageToken=response["nextPageToken"]
            )
        else:
            request = None
    
    return comments

# Yorumları CSV dosyasına kaydetme
def save_comments_to_csv(video_id):
    comments = get_youtube_comments(video_id)
    
    # DataFrame oluşturma
    df = pd.DataFrame(comments)
    
    # CSV dosyasına kaydetme
    df.to_csv("new_veri.csv", index=False, encoding="utf-8-sig")
    print("Yorumlar başarıyla kaydedildi: new_veri.csv")


# Yeni eklenen video bilgilerini alma ve kaydetme fonksiyonu
def get_video_info(video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    
    # Video bilgilerini alma
    request = youtube.videos().list(
        part="snippet, statistics",
        id=video_id
    )
    response = request.execute()
    
    video_info = response["items"][0]
    title = video_info["snippet"]["title"]
    channel_name = video_info["snippet"]["channelTitle"]
    views = video_info["statistics"].get("viewCount", 'N/A')
    likes = video_info["statistics"].get("likeCount", 'N/A')
    published_date = video_info["snippet"].get("publishedAt", 'N/A')
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    return {
        "Title": title,
        "Channel Name": channel_name,
        "Views": views,
        "Likes": likes,
        "Published Date": published_date,
        "Video URL": video_url
    }

# Video bilgilerini CSV dosyasına kaydetme fonksiyonu
def save_video_info_to_csv(video_id):
    video_info = get_video_info(video_id)
    
    # DataFrame oluşturma
    df = pd.DataFrame([video_info])
    
    # Video bilgilerini CSV dosyasına kaydetme
    df.to_csv("newvideo_data.csv", index=False, encoding="utf-8-sig")
    print("Video bilgileri başarıyla kaydedildi: newvideo_data.csv")

# Video ID'si (Verdiğiniz video linkindeki ID'yi kullanıyoruz)
video_id = "VEF_xt-AYaM"  # YouTube video ID'si

# Yorumları ve video bilgilerini kaydetme
save_comments_to_csv(video_id)
save_video_info_to_csv(video_id)
