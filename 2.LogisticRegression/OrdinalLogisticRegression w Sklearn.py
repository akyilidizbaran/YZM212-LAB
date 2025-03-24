import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.preprocessing import StandardScaler
import time  # Zaman ölçmek için

# 1. Dosyayı oku (Excel dosyası)
df = pd.read_excel("C:\\Users\\Baran\\OneDrive\\Masaüstü\\2.LogisticRegression\\WineQT.xlsx")

# 2. Sınıf dağılımını kontrol et
print("Quality sınıf dağılımı:\n", df["quality"].value_counts(), "\n")

# 3. Giriş ve çıkış değişkenlerini ayır
X = df.drop(columns=["quality", "Id"])  # Özellikler
y = df["quality"]  # Hedef değişken (ordinal)

# 4. Özellikleri ölçeklendir (standartlaştır)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# 6. Lojistik regresyon modelini tanımla
model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)

# 7. Modeli eğit (zamanı ölç)
start_train = time.time()
model.fit(X_train, y_train)
end_train = time.time()
train_time = end_train - start_train

# 8. Tahmin yap (zamanı ölç)
start_pred = time.time()
y_pred = model.predict(X_test)
end_pred = time.time()
predict_time = end_pred - start_pred

# 9. Tahmin edilen ve gerçek sınıfları yazdır
print("Modelin tahmin ettiği sınıflar:", np.unique(y_pred))
print("Test setindeki gerçek sınıflar:", np.unique(y_test), "\n")

# 10. Confusion Matrix görselleştir
cm = confusion_matrix(y_test, y_pred, labels=np.sort(y.unique()))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.sort(y.unique()))
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()

# 11. Classification Report yazdır (zero_division=0 ile uyarıyı bastır)
print("Classification Report:\n")
print(classification_report(y_test, y_pred, zero_division=0))

# 12. Eğitim ve tahmin sürelerini yazdır
print(f"Eğitim süresi: {train_time:.4f} saniye")
print(f"Tahmin süresi: {predict_time:.4f} saniye")
