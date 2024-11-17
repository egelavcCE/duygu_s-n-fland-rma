import pandas as pd

# Temizlenmiş yorumları içeren CSV dosyasını yükle
comments_df = pd.read_csv("cleaned_comments_data.csv", encoding="utf-8-sig")

# Yeni bir "Sentiment" sütunu ekleyin (etiketler için)
comments_df["Sentiment"] = None

# Yorumları tek tek gözden geçirip manuel olarak etiketleyin
for index, row in comments_df.iterrows():
    print(f"Yorum {index + 1}: {row['Comment']}")  # Yorumu yazdır
    sentiment = input("Yorumun duygu durumu nedir? (Pozitif / Negatif / Nötr): ")
    comments_df.at[index, "Sentiment"] = sentiment  # Etiketi sütuna ekle

# Düzenlenmiş veriyi yeni bir dosyaya kaydedin
comments_df.to_csv("comments_with_labels.csv", index=False, encoding="utf-8-sig")

print("Yorumlar etiketlendi ve 'comments_with_labels.csv' dosyasına kaydedildi.")
