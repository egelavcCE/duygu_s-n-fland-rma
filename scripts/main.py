import pandas as pd
from googleapiclient.discovery import build

# YouTube API anahtarınızı buraya girin
API_KEY = 'AIzaSyCrXhHBb6jtQhfzPeSTcH8oZ1gYTJsBjHI'
query = "teknik ve temel analiz eğitimi"

# YouTube API istemcisini başlatma
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Arama fonksiyonu: İlk 5 videoyu arar ve bilgilerini toplar
def search_videos(query, max_results=5):
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    video_data = []
    
    for item in response.get("items", []):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        url = f"https://www.youtube.com/watch?v={video_id}"
        channel_id = item['snippet']['channelId']
        channel_name = item['snippet']['channelTitle']
        
        # Kanal bilgilerini ve video istatistiklerini toplama
        channel_info = get_channel_info(channel_id)
        video_stats = get_video_stats(video_id)
        
        video_data.append({
            "Title": title,
            "URL": url,
            "Channel Name": channel_name,
            "Subscriber Count": channel_info["Subscriber Count"],
            "Likes": video_stats["Likes"],
            "Views": video_stats["Views"],
            "Published Date": video_stats["Published Date"]
        })
        
    return video_data

# Kanal bilgilerini alma fonksiyonu
def get_channel_info(channel_id):
    request = youtube.channels().list(
        part="statistics",
        id=channel_id
    )
    response = request.execute()
    stats = response['items'][0]['statistics']
    return {
        "Subscriber Count": stats.get('subscriberCount', 'N/A')
    }

# Video istatistiklerini alma fonksiyonu
def get_video_stats(video_id):
    request = youtube.videos().list(
        part='statistics, snippet',
        id=video_id
    )
    response = request.execute()
    stats = response['items'][0]['statistics']
    snippet = response['items'][0]['snippet']
    
    return {
        "Likes": stats.get('likeCount', 'N/A'),
        "Views": stats.get('viewCount', 'N/A'),
        "Published Date": snippet.get('publishedAt', 'N/A')
    }

# Yorumları alma fonksiyonu
def get_comments(video_id, max_comments=20):
    comments_data = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_comments,
        textFormat="plainText"
    )
    response = request.execute()
    
    for item in response.get("items", []):
        comment_info = item['snippet']['topLevelComment']['snippet']
        comments_data.append({
            "Video ID": video_id,
            "Author": comment_info['authorDisplayName'],
            "Comment": comment_info['textDisplay'],
            "Likes": comment_info.get('likeCount', 0),
            "Reply Count": item['snippet'].get('totalReplyCount', 0),
            "Comment Date": comment_info.get('publishedAt', 'N/A')
        })
        
    return comments_data

# Ana işlem
videos = search_videos(query)
video_data = []
comments_data = []

for video in videos:
    video_data.append({
        "Title": video["Title"],
        "URL": video["URL"],
        "Channel Name": video["Channel Name"],
        "Subscriber Count": video["Subscriber Count"],
        "Likes": video["Likes"],
        "Views": video["Views"],
        "Published Date": video["Published Date"]
    })
    
    # Yorumları ekle
    comments = get_comments(video["URL"].split('=')[-1])
    comments_data.extend(comments)

# Verileri CSV dosyalarına kaydetme
video_df = pd.DataFrame(video_data)
video_df.to_csv("video_data.csv", index=False, encoding='utf-8-sig')

comments_df = pd.DataFrame(comments_data)
comments_df.to_csv("comments_data.csv", index=False, encoding='utf-8-sig')

print("Video ve yorum verileri başarıyla kaydedildi.")


