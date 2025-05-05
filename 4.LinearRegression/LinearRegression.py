import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1) CSV dosya yolu
csv_path = r"C:\Users\Baran\OneDrive\Masaüstü\4.LinearRegression\LifeExpectancyData.csv"

# 2) Veri yükleme ve sütun adlarını kırpma
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# 3) Hedef değişken ve sayısal özellikleri belirleme
target = 'Life expectancy'
# Tüm sayısal sütunlardan hedefi çıkarıp X’e alıyoruz
numeric_cols = df.select_dtypes(include=[np.number]).columns.drop(target).tolist()

# 4) Eksik değer doldurma (medyan ile)
for col in [target] + numeric_cols:
    df[col].fillna(df[col].median(), inplace=True)

# 5) Girdi (X) ve hedef (y) matrisi
X = df[numeric_cols].values
y = df[target].values.reshape(-1,1)

# 6) Eğitim/Test bölmesi
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# 7) Ölçeklendirme
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# 8) En küçük kareler (Normal Equation) için intercept ekleme
m, _ = X_train_s.shape
Xb_train = np.hstack([np.ones((m,1)), X_train_s])

# θ = (XᵀX)⁻¹Xᵀy
theta = np.linalg.inv(Xb_train.T.dot(Xb_train)).dot(Xb_train.T).dot(y_train)

# 9) Tahmin ve cost fonksiyonları
def predict(X_s, theta):
    Xb = np.hstack([np.ones((X_s.shape[0],1)), X_s])
    return Xb.dot(theta)

def compute_cost(y_true, y_pred):
    m = len(y_true)
    return (1/(2*m)) * np.sum((y_pred - y_true)**2)

# 10) Maliyetleri yazdır
train_pred = predict(X_train_s, theta)
test_pred  = predict(X_test_s,  theta)

print(f"LS Cost (Train): {compute_cost(y_train, train_pred):.4f}")
print(f"LS Cost (Test) : {compute_cost(y_test,  test_pred):.4f}")

# --- (Opsiyonel) Gerçek vs Tahmin Grafiği ---
plt.figure(figsize=(6,6))
plt.scatter(y_test, test_pred, alpha=0.5)
lims = [y_test.min(), y_test.max()]
plt.plot(lims, lims, 'r--')
plt.xlabel("Gerçek Life Expectancy")
plt.ylabel("Predicted Life Expectancy")
plt.title("Gerçek vs Tahmin (Test Seti)")
plt.show()
