import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Gerekli veri setlerini indir
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

# Türkçe stopword'leri indir
stop_words = set(stopwords.words("turkish"))

# Yorum temizleme fonksiyonu
def clean_text(text):
    # Küçük harfe çevir
    text = text.lower()
    
    # URL ve özel karakterleri kaldır
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^a-zA-ZğüşöçıİĞÜŞÖÇ0-9\s]", "", text)
    
    # Kelimeleri boşluklarla bölerek ayır
    words = text.split()
    
    # Stopword'leri çıkar
    words = [word for word in words if word not in stop_words]
    
    return " ".join(words)  # Temizlenmiş yorumları birleştirip döndür

# CSV'den yorumları yükle
comments_df = pd.read_csv("new_veri.csv", encoding="utf-8-sig")

# Yorumları temizleyip yeni bir sütuna ekle
comments_df["Cleaned_Comments"] = comments_df["comment"].apply(clean_text)

# Temizlenmiş yorumları yeni CSV dosyasına kaydet
comments_df.to_csv("new_veri_cleaned.csv", index=False, encoding="utf-8-sig")

print("Yorumlar başarıyla temizlendi ve 'new_veri_cleaned.csv' dosyasına kaydedildi.")
