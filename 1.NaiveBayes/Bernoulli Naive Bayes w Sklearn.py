import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

# Kodun başlangıcında zaman ölçümünü başlatıyoruz
start_time = time.time()

# 1. Veri Setini Yükleme
data = pd.read_excel("C:\\Users\\Baran\\OneDrive\\Masaüstü\\1.NaiveBayes\\Veri.xlsx")
print("Veri seti örnekleri:")
print(data.head())

# 2. Özellikler (X) ve Etiket (y) Belirleme
X = data.drop("label", axis=1)
y = data["label"]

# 3. Eğitim ve Test Verilerine Ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Bernoulli Naive Bayes Modelini Oluşturma ve Eğitme
model = BernoulliNB()
model.fit(X_train, y_train)

# 5. Test Verileri Üzerinde Tahmin Yapma
y_pred = model.predict(X_test)

# 6. Model Performansını Değerlendirme
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# 7. Karışıklık Matrisini Görselleştirme
plt.figure(figsize=(5, 4))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.colorbar()
tick_marks = np.arange(len(cm))
plt.xticks(tick_marks, ['Negative', 'Positive'])
plt.yticks(tick_marks, ['Negative', 'Positive'])
plt.xlabel("Predicted Label")
plt.ylabel("True Label")

thresh = cm.max() / 2.
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

plt.tight_layout()
plt.show()

# Kodun sonunda zaman ölçümünü bitirip sonucu yazdırıyoruz
end_time = time.time()
print(f"Kodun çalışma süresi: {end_time - start_time:.4f} saniye")
