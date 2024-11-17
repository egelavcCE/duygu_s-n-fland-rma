import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from gensim.models import Word2Vec  # Word2Vec modelini kullan
import pickle

# Veriyi yükleyin
df = pd.read_csv("comments_with_labels.csv", encoding="utf-8-sig")

# Yorumlar ve etiketler
X = df['Cleaned_Comments']
y = df['Sentiment']

# NaN değerlerini kontrol et ve kaldır
y = y.dropna()  # NaN olan satırları çıkar
X = X[y.index]  # X'i de aynı şekilde temizle

# Eğitim ve test verilerini ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Word2Vec modelini yükle
word2vec_model = Word2Vec.load("./word2vec_model.model")

# Yorumları vektörlere dönüştürmek için fonksiyon
def get_word2vec_embeddings(text):
    embeddings = []
    for word in text.split():
        try:
            embeddings.append(word2vec_model.wv[word])  # Word2Vec modelinden kelime vektörünü al
        except KeyError:
            continue  # Kelime modelde yoksa atla
    return embeddings

# Eğitim verilerini Word2Vec vektörlerine dönüştür
X_train_vectors = X_train.apply(get_word2vec_embeddings)
X_test_vectors = X_test.apply(get_word2vec_embeddings)

# Vektörleri tek bir vektöre dönüştürmek için fonksiyon
def average_word2vec(embeddings):
    if len(embeddings) == 0:
        return [0] * word2vec_model.vector_size  # Boş metin için sıfır vektörü döndür
    return [sum(col) / len(col) for col in zip(*embeddings)]

# Vektörleri ortalamaya al
X_train_vectors = X_train_vectors.apply(average_word2vec)
X_test_vectors = X_test_vectors.apply(average_word2vec)

# X_train ve X_test'i liste haline getir
X_train_vectors = list(X_train_vectors)
X_test_vectors = list(X_test_vectors)

# Modeli tanımlayın
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Modeli eğit
clf.fit(X_train_vectors, y_train)

# Modelin doğruluğunu değerlendirin
y_pred = clf.predict(X_test_vectors)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Doğruluğu: {accuracy * 100:.2f}%")

# Modeli kaydedin
with open("sentiment_model.pkl", "wb") as f:
    pickle.dump(clf, f)

# Vektörize edilmiş eğitim verilerini kaydedin
with open("X_train_vectors.pkl", "wb") as f:
    pickle.dump(X_train_vectors, f)

with open("X_test_vectors.pkl", "wb") as f:
    pickle.dump(X_test_vectors, f)

# Etiket verilerini kaydedin
y_train.to_csv("y_train.csv", index=False)
y_test.to_csv("y_test.csv", index=False)

print("Model eğitildi ve kaydedildi.")
