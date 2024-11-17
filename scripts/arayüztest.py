import tkinter as tk
from tkinter import ttk
import csv

# Tkinter penceresini oluştur
root = tk.Tk()
root.title("Video Bilgileri ve Yorumlar")

# Video bilgileri için bir Frame oluştur
video_frame = ttk.Frame(root)
video_frame.grid(row=0, column=0, padx=10, pady=10)

# Video bilgilerini içeren etiketler
title_label = ttk.Label(video_frame, text="Başlık:")
title_label.grid(row=0, column=0, sticky="w")

channel_label = ttk.Label(video_frame, text="Kanal:")
channel_label.grid(row=1, column=0, sticky="w")

views_label = ttk.Label(video_frame, text="Görüntüleme:")
views_label.grid(row=2, column=0, sticky="w")

likes_label = ttk.Label(video_frame, text="Beğeni:")
likes_label.grid(row=3, column=0, sticky="w")

published_label = ttk.Label(video_frame, text="Tarih:")
published_label.grid(row=4, column=0, sticky="w")

url_label = ttk.Label(video_frame, text="URL:")
url_label.grid(row=5, column=0, sticky="w")

# Yorumlar için bir Frame oluştur
comments_frame = ttk.Frame(root)
comments_frame.grid(row=1, column=0, padx=10, pady=10)

# Yorumlar Tablosu
comments_table = ttk.Treeview(comments_frame, columns=("author", "comment", "sentiment"), show="headings")
comments_table.heading("author", text="Kullanıcı")
comments_table.heading("comment", text="Yorum")
comments_table.heading("sentiment", text="Duygu Durumu")
comments_table.grid(row=0, column=0, sticky="nsew")

# Veriyi oku ve arayüzü doldur
def load_data():
    with open('newvideo_data.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Başlık satırını atla
        row = next(reader)  # İlk satırdaki veriyi al
        title, channel, views, likes, published, url = row
        title_label.config(text=f"Başlık: {title}")
        channel_label.config(text=f"Kanal: {channel}")
        views_label.config(text=f"Görüntüleme: {views}")
        likes_label.config(text=f"Beğeni: {likes}")
        published_label.config(text=f"Tarih: {published}")
        url_label.config(text=f"URL: {url}")

    # Yorumları yükle
    with open('newveri_sınıf.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Başlık satırını atla
        for row in reader:
            author, comment, sentiment = row
            comments_table.insert("", "end", values=(author, comment, sentiment))

# Başlangıçta veriyi yükle
load_data()

# Tkinter penceresini başlat
root.mainloop()
