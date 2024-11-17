from googleapiclient.discovery import build
import csv
import pandas as pd
from tkinter import Tk, Label, Listbox, Button, Scrollbar, RIGHT, Y, END

# YouTube API ayarları
API_KEY = "AIzaSyCrXhHBb6jtQhfzPeSTcH8oZ1gYTJsBjHI"  # Buraya kendi API anahtarınızı girin
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
PLAYLIST_ID = "PL5kIOunpmSBO0Z9Wlp_OehbWnqp5VL214"  # Oynatma listesinin ID'si

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

# Videoları oynatma listesinden çek
def fetch_videos(playlist_id):
    video_data = []
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            video_data.append({
                "videoId": item["snippet"]["resourceId"]["videoId"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"]
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_data

# Yorumları çek
def fetch_comments(video_id):
    comments = []
    next_page_token = None
    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        try:
            response = request.execute()
        except Exception as e:
            print(f"Error fetching comments for video {video_id}: {e}")
            break

        for item in response["items"]:
            comments.append(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return comments

# Verileri CSV'ye kaydet
def save_to_csv(video_data, comments_data):
    # Video bilgileri
    with open("video_info.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["videoId", "title", "description"])
        writer.writeheader()
        writer.writerows(video_data)

    # Yorumlar
    with open("video_comments.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["videoId", "comment"])
        for video_id, comments in comments_data.items():
            for comment in comments:
                writer.writerow([video_id, comment])

# Veri çekme ve kaydetme işlemleri
def main():
    print("Fetching videos...")
    video_data = fetch_videos(PLAYLIST_ID)

    print("Fetching comments...")
    comments_data = {}
    for video in video_data:
        video_id = video["videoId"]
        comments_data[video_id] = fetch_comments(video_id)

    print("Saving data to CSV...")
    save_to_csv(video_data, comments_data)
    print("Data saved!")

# Basit GUI tasarımı
def display_gui():
    root = Tk()
    root.title("YouTube Video Viewer")

    # Video bilgilerini ve yorumları yükle
    video_info = pd.read_csv("video_info.csv")
    comments_data = pd.read_csv("video_comments.csv")

    # Video listesi
    Label(root, text="Videos").pack()
    video_listbox = Listbox(root, width=80, height=20)
    video_listbox.pack()

    # Yorum listesi
    Label(root, text="Comments").pack()
    comment_listbox = Listbox(root, width=80, height=20)
    comment_scroll = Scrollbar(root, orient="vertical")
    comment_scroll.pack(side=RIGHT, fill=Y)
    comment_listbox.config(yscrollcommand=comment_scroll.set)
    comment_scroll.config(command=comment_listbox.yview)
    comment_listbox.pack()

    # Video bilgilerini yükle
    for _, row in video_info.iterrows():
        video_listbox.insert(END, f"{row['title']}")

    # Yorumları seçilen videoya göre görüntüle
    def display_comments(event):
        selected_index = video_listbox.curselection()
        if selected_index:
            video_id = video_info.iloc[selected_index[0]]["videoId"]
            video_comments = comments_data[comments_data["videoId"] == video_id]["comment"]
            comment_listbox.delete(0, END)
            for comment in video_comments:
                comment_listbox.insert(END, comment)

    video_listbox.bind("<<ListboxSelect>>", display_comments)

    root.mainloop()

if __name__ == "__main__":
    main()
    display_gui()
