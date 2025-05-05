import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# 1) CSV dosya yolu
csv_path = r"C:\Users\Baran\OneDrive\Masaüstü\4.LinearRegression\LifeExpectancyData.csv"

# 2) Veri yükleme & sütun adlarından boşlukları kırpma
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# 3) Hedef ve sayısal özellikleri belirleme
target = 'Life expectancy'
numeric_cols = df.select_dtypes(include=[np.number]).columns.drop(target).tolist()

# 4) Eksik değer doldurma
for col in [target] + numeric_cols:
    df[col].fillna(df[col].median(), inplace=True)

# 5) Girdi (X) ve hedef (y)
X = df[numeric_cols].values
y = df[target].values.reshape(-1,1)

# 6) Eğitim/Test bölmesi
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# 7) Ölçeklendirme
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# 8) Model tanımlama ve eğitim
model = LinearRegression()
model.fit(X_train_s, y_train)

# 9) Tahminler
y_train_pred = model.predict(X_train_s)
y_test_pred  = model.predict(X_test_s)

# 10) Aynı cost fonksiyonunu kullanarak maliyet hesaplama
def compute_cost(y_true, y_pred):
    m = len(y_true)
    return (1/(2*m)) * np.sum((y_pred - y_true)**2)

print(f"SK Cost (Train): {compute_cost(y_train, y_train_pred):.4f}")
print(f"SK Cost (Test) : {compute_cost(y_test,  y_test_pred):.4f}")

# (Opsiyonel) R² skoru
print(f"R² Score (Train): {model.score(X_train_s, y_train):.4f}")
print(f"R² Score (Test) : {model.score(X_test_s,  y_test):.4f}")

# 11) Gerçek vs Tahmin grafiği (Test)
plt.figure(figsize=(6,6))
plt.scatter(y_test, y_test_pred, alpha=0.5)
lims = [y_test.min(), y_test.max()]
plt.plot(lims, lims, 'r--')
plt.xlabel("Gerçek Life Expectancy")
plt.ylabel("Predicted Life Expectancy")
plt.title("Gerçek vs Tahmin (scikit-learn, Test)")
plt.show()
