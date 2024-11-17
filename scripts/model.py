import pandas as pd
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# Temizlenmiş yorumları içeren CSV dosyasını yükle
df = pd.read_csv("./cleaned_comments_data.csv", encoding="utf-8-sig")

# Yorumları tokenize etme
def tokenize_text(text):
    # Eğer text bir liste ise doğrudan döndür, yoksa split et
    if isinstance(text, list):
        return text
    else:
        return text.split()

# Yorumları tokenize ederek listeye çevir
tokenized_comments = df["Cleaned_Comments"].apply(eval).apply(tokenize_text)

# Word2Vec modelini eğit
w2v_model = Word2Vec(sentences=tokenized_comments, vector_size=100, window=5, min_count=2, workers=4)

# Eğitilmiş modeli kaydet
w2v_model.save("./word2vec_model.model")

print("Word2Vec modeli başarıyla eğitildi ve kaydedildi.")

# --- Görselleştirme ---
# Modeldeki vektörleri ve kelimeleri al
words = list(w2v_model.wv.index_to_key)
word_vectors = w2v_model.wv[words]

# Vektörleri 2D'ye indirgemek için TSNE kullan
tsne = TSNE(n_components=2, random_state=42, perplexity=40, n_iter=300)
reduced_vectors = tsne.fit_transform(word_vectors)

# Görselleştirme
plt.figure(figsize=(16, 16))
for i, word in enumerate(words):
    plt.scatter(reduced_vectors[i, 0], reduced_vectors[i, 1])
    plt.annotate(word, (reduced_vectors[i, 0], reduced_vectors[i, 1]), fontsize=9)

# Görüntüyü kaydet
plt.savefig("./word2vec_visualization.png")
plt.show()
