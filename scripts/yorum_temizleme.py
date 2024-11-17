import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from gensim.models import Word2Vec

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
    
    return words

# CSV'den yorumları yükle
comments_df = pd.read_csv("comments_data.csv", encoding="utf-8-sig")

# Yorumları temizleyip yeni bir sütuna ekle
comments_df["Cleaned_Comments"] = comments_df["Comment"].apply(clean_text)

# Temizlenmiş yorumları yeni CSV dosyasına kaydet
comments_df.to_csv("cleaned_comments_data.csv", index=False, encoding="utf-8-sig")

print("Yorumlar başarıyla temizlendi ve 'cleaned_comments_data.csv' dosyasına kaydedildi.")

# Word2Vec modeli eğitimi
# Temizlenmiş yorumları listeye çevir
sentences = comments_df["Cleaned_Comments"].tolist()

# Word2Vec modelini eğit
w2v_model = Word2Vec(sentences, vector_size=100, window=5, min_count=2, workers=4)

# Modeli kaydet
w2v_model.save("word2vec_model.model")

print("Word2Vec modeli başarıyla eğitildi ve kaydedildi.")
