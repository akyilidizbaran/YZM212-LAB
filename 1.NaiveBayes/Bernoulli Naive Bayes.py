import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Zaman ölçümünü başlat
start_time = time.time()

# 1. Veri setini yükleyin (xlsx dosyasından)
data = pd.read_excel('C:\\Users\\Baran\\OneDrive\\Masaüstü\\1.NaiveBayes\\Veri.xlsx') 

# 2. Özellikler (X) ve hedef (y) ayrımı
# Son sütunun hedef değişken olduğu varsayılmıştır.
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# 3. Verileri binarize etme (Bernoulli NB için)
medyan_deger = np.median(X, axis=0)
X_bin = np.where(X > medyan_deger, 1, 0)

# 4. Eğitim ve test setlerine ayırma (%80 eğitim, %20 test)
indices = np.arange(X_bin.shape[0])
np.random.shuffle(indices)
train_size = int(0.8 * len(indices))
train_idx, test_idx = indices[:train_size], indices[train_size:]
X_train, X_test = X_bin[train_idx], X_bin[test_idx]
y_train, y_test = y[train_idx], y[test_idx]

# 5. Bernoulli Naive Bayes sınıfını Numpy kullanarak oluşturma
class BernoulliNB:
    def __init__(self, alpha=1.0):
        self.alpha = alpha  # Laplace düzeltmesi için

    def fit(self, X, y):
        self.classes = np.unique(y)
        n_samples, n_features = X.shape

        # Sınıf önceliklerini (prior) log olarak hesapla
        self.class_log_prior = {}
        # Her sınıf için, her özelliğin P(x_j=1|y=c) değerlerini tutacak sözlük
        self.feature_probs = {}

        for c in self.classes:
            X_c = X[y == c]  # o sınıfa ait örnekler
            # Laplace düzeltmesi: (1'lerin sayısı + alpha) / (örnek sayısı + 2*alpha)
            self.feature_probs[c] = (np.sum(X_c, axis=0) + self.alpha) / (X_c.shape[0] + 2*self.alpha)
            self.class_log_prior[c] = np.log(X_c.shape[0] / n_samples)

    def predict(self, X):
        preds = []
        for x in X:
            class_scores = {}
            for c in self.classes:
                # x[j] == 1 ise log(P(x_j=1|y=c)), 0 ise log(1 - P(x_j=1|y=c))
                log_likelihood = np.sum(
                    x * np.log(self.feature_probs[c]) + 
                    (1 - x) * np.log(1 - self.feature_probs[c])
                )
                class_scores[c] = self.class_log_prior[c] + log_likelihood

            preds.append(max(class_scores, key=class_scores.get))
        return np.array(preds)

# 6. Modeli eğitme
model = BernoulliNB(alpha=1.0)
model.fit(X_train, y_train)

# 7. Test seti üzerinde tahmin yapma ve doğruluk hesaplama
y_pred = model.predict(X_test)
accuracy = np.mean(y_pred == y_test)
print("Accuracy:", accuracy)

# 8. Confusion Matrix hesaplama (sınıfların 0 ve 1 olduğunu varsayıyoruz)
TN = np.sum((y_test == 0) & (y_pred == 0))
FP = np.sum((y_test == 0) & (y_pred == 1))
FN = np.sum((y_test == 1) & (y_pred == 0))
TP = np.sum((y_test == 1) & (y_pred == 1))

conf_mat = np.array([[TN, FP], [FN, TP]])

print("Confusion Matrix:")
print(conf_mat)

# 9. Confusion Matrix görselleştirme
plt.figure(figsize=(6, 5))
plt.imshow(conf_mat, interpolation='nearest', cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.colorbar()

# Eksen etiketleri
class_names = ["Negative", "Positive"]  # 0 ve 1'e karşılık
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)

# Hücre içi sayısal değerleri yazdırma
thresh = conf_mat.max() / 2.
for i in range(conf_mat.shape[0]):
    for j in range(conf_mat.shape[1]):
        plt.text(j, i, str(conf_mat[i, j]),
                 horizontalalignment="center",
                 color="white" if conf_mat[i, j] > thresh else "black")

plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.tight_layout()
plt.show()

# Zaman ölçümünü sonlandır
end_time = time.time()
print(f"Running time: {end_time - start_time:.4f} seconds")
