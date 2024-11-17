import pandas as pd
import pickle
import numpy as np
from gensim.models import Word2Vec

# Eğitimli modelin yüklenmesi (duygu sınıflandırma modeli)
with open("sentiment_model.pkl", "rb") as f:
    sentiment_model = pickle.load(f)

# Word2Vec modelini yükle
word2vec_model = Word2Vec.load("word2vec_model.model")

# Yorumları Word2Vec ile vektörlere dönüştürme fonksiyonu
def get_word2vec_embeddings(text):
    if isinstance(text, str):  # Eğer text bir string ise
        embeddings = []
        for word in text.split():  # Kelimeleri ayır ve vektörlerini al
            try:
                embeddings.append(word2vec_model.wv[word])  # Kelime vektörünü al
            except KeyError:
                continue  # Eğer kelime modelde yoksa, atla
        return embeddings
    return []  # Eğer text boşsa ya da string değilse, boş liste döndür

# Vektörleri ortalamaya al
def average_word2vec(embeddings):
    if len(embeddings) == 0:
        return [0] * 100  # Eğer boş bir metin varsa, sıfır vektörü döndür
    return np.mean(embeddings, axis=0)

# CSV'den temizlenmiş veriyi yükle
comments_df = pd.read_csv("new_veri_cleaned.csv", encoding="utf-8-sig")

# Yorumları vektörlere dönüştür
comments_df["Word2Vec_Embeddings"] = comments_df["Cleaned_Comments"].apply(get_word2vec_embeddings)

# Vektörleri ortalamaya al
comments_df["Avg_Word2Vec"] = comments_df["Word2Vec_Embeddings"].apply(average_word2vec)

# Yeni verileri sınıflandırma (Duygu Tahmin Etme)
predictions = sentiment_model.predict(list(comments_df["Avg_Word2Vec"]))

# Tahminleri DataFrame'e ekle
comments_df["Predicted_Sentiment"] = predictions

# Kullanıcı ismi, temizlenmiş yorum ve duygu sınıfı ile yeni DataFrame
# Eğer 'Username' sütunu farklıysa, burayı ona göre güncelleyin
final_df = comments_df[["author", "Cleaned_Comments", "Predicted_Sentiment"]]

# Sonuçları 'newveri_sınıf.csv' dosyasına kaydet
final_df.to_csv("newveri_sınıf.csv", index=False, encoding="utf-8-sig")

# Word2Vec ortalama vektörlerini ayrı bir dosyaya kaydet
word2vec_df = comments_df[["author", "Avg_Word2Vec"]]

# Word2Vec vektörlerini 'word2vec_embeddings.csv' dosyasına kaydet
word2vec_df.to_csv("word2vec_embeddings.csv", index=False, encoding="utf-8-sig")

# Başarı oranını hesaplamak için gerçek etiketler gerekmektedir. Eğer gerçek etiketler varsa:
# accuracy = accuracy_score(y_true, predictions)
# print(f"Başarı oranı: {accuracy * 100:.2f}%")

print("Yeni verilerin sınıflandırması tamamlandı ve 'newveri_sınıf.csv' dosyasına kaydedildi.")
print("Word2Vec embeddings'ler 'word2vec_embeddings.csv' dosyasına kaydedildi.")
