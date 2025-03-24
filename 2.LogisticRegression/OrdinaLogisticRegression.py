import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Veriyi oku
df = pd.read_excel("C:\\Users\\Baran\\OneDrive\\Masaüstü\\2.LogisticRegression\\WineQT.xlsx")

# 2. Bağımsız ve bağımlı değişkenler
y = df['quality'].values
X = df.drop(columns=['quality', 'Id']).values

# 3. Veriyi standardize et
X = (X - X.mean(axis=0)) / X.std(axis=0)

# 4. Kategori bilgileri
categories = np.sort(np.unique(y))
n_classes = len(categories)
n_features = X.shape[1]

# Başlangıç parametreleri
beta = np.zeros(n_features)
cutpoints = np.linspace(-1, 1, n_classes - 1)

# Sigmoid fonksiyonu
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Tahmin fonksiyonu
def predict(X, beta, cutpoints):
    preds = []
    for i in range(X.shape[0]):
        eta = np.dot(X[i], beta)
        probs = []
        for j in range(len(cutpoints) + 1):
            if j == 0:
                p = sigmoid(cutpoints[0] - eta)
            elif j == len(cutpoints):
                p = 1 - sigmoid(cutpoints[-1] - eta)
            else:
                p = sigmoid(cutpoints[j] - eta) - sigmoid(cutpoints[j - 1] - eta)
            probs.append(p)
        pred_class = np.argmax(probs) + categories[0]
        preds.append(pred_class)
    return np.array(preds)

# Kayıp fonksiyonu (negatif log likelihood)
def negative_log_likelihood(X, y, beta, cutpoints):
    ll = 0
    for i in range(X.shape[0]):
        eta = np.dot(X[i], beta)
        yi = y[i] - categories[0]
        if yi == 0:
            p = sigmoid(cutpoints[0] - eta)
        elif yi == n_classes - 1:
            p = 1 - sigmoid(cutpoints[-1] - eta)
        else:
            p = sigmoid(cutpoints[yi] - eta) - sigmoid(cutpoints[yi - 1] - eta)
        ll += np.log(p + 1e-9)
    return -ll

# 5. Gradient descent ile eğitim ⏱️
lr = 0.01
epochs = 300
start_train = time.time()

for epoch in range(epochs):
    grad_beta = np.zeros(n_features)
    grad_cuts = np.zeros(len(cutpoints))
    
    for i in range(X.shape[0]):
        eta = np.dot(X[i], beta)
        yi = y[i] - categories[0]
        
        if yi == 0:
            p1 = sigmoid(cutpoints[0] - eta)
            dp = p1 * (1 - p1)
            grad_beta -= (1 / (p1 + 1e-9)) * (-dp) * X[i]
            grad_cuts[0] += (1 / (p1 + 1e-9)) * dp
        elif yi == n_classes - 1:
            p2 = 1 - sigmoid(cutpoints[-1] - eta)
            dp = sigmoid(cutpoints[-1] - eta) * (1 - sigmoid(cutpoints[-1] - eta))
            grad_beta -= (1 / (p2 + 1e-9)) * (dp) * X[i]
            grad_cuts[-1] -= (1 / (p2 + 1e-9)) * dp
        else:
            s1 = sigmoid(cutpoints[yi] - eta)
            s0 = sigmoid(cutpoints[yi - 1] - eta)
            p = s1 - s0
            dp1 = s1 * (1 - s1)
            dp0 = s0 * (1 - s0)
            grad_beta -= (1 / (p + 1e-9)) * ((-dp1 + dp0) * X[i])
            grad_cuts[yi] += (1 / (p + 1e-9)) * dp1
            grad_cuts[yi - 1] -= (1 / (p + 1e-9)) * dp0

    beta -= lr * grad_beta
    cutpoints -= lr * grad_cuts
    cutpoints = np.sort(cutpoints)  # sıralı kalması şart

end_train = time.time()

# ⏱️ Tahmin süresi
start_pred = time.time()
y_pred = predict(X, beta, cutpoints)
end_pred = time.time()

# Confusion Matrix hesapla
cm = np.zeros((n_classes, n_classes), dtype=int)
for true, pred in zip(y, y_pred):
    i = np.where(categories == true)[0][0]
    j = np.where(categories == pred)[0][0]
    cm[i, j] += 1

# 🔍 Sonuçları yazdır
print("\n📊 Regresyon Katsayıları (Beta):")
for i, coef in enumerate(beta):
    print(f"{df.columns[i]}: {coef:.4f}")

print("\n📉 Cutpoint (Eşik) Değerleri:")
for i, cp in enumerate(cutpoints):
    print(f"Threshold {i+1}: {cp:.4f}")

print("\n⏱️ Eğitim süresi: {:.4f} saniye".format(end_train - start_train))
print("⏱️ Tahmin süresi: {:.4f} saniye".format(end_pred - start_pred))

# 🎯 Doğruluk (accuracy) hesapla
accuracy = np.mean(y_pred == y)
print("\n🎯 Accuracy (Doğruluk): {:.4f}".format(accuracy))




# 🎨 Confusion Matrix görselleştirme
# 🎨 Confusion Matrix görselleştirme (sayılarla birlikte)
plt.figure(figsize=(8, 6))
plt.imshow(cm, cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Tahmin Edilen")
plt.ylabel("Gerçek")
plt.xticks(ticks=np.arange(n_classes), labels=categories)
plt.yticks(ticks=np.arange(n_classes), labels=categories)
plt.colorbar()

# Her hücreye sayı yazdır
for i in range(n_classes):
    for j in range(n_classes):
        plt.text(j, i, str(cm[i, j]),
                 ha='center', va='center',
                 color='black', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()
