# 4. Laboratuvar: Lineer Regresyon – Yaşam Beklentisi Veri Seti

Bu proje, Dünya Sağlık Örgütü’nün “Life Expectancy” veri seti kullanılarak iki farklı yaklaşım ile lineer regresyon modellerinin kurulması, maliyet fonksiyonlarının hesaplanması ve karşılaştırılmasını içerir:

1. **From-Scratch (Least Squares)  
2. **Scikit-Learn `LinearRegression`**

---

## Dosya Yapısı

```
4.LinearRegression/
├── data/
│   └── LifeExpectancyData.csv    # Yaşam beklentisi veri seti
├── LinearRegression_LS.ipynb      # Analitik çözüm (normal equation)
├── LinearRegression_SK.ipynb      # scikit-learn ile uygulama
└── README.md                      # Proje dökümantasyonu
```

---

## Kullanım

1. Bu repoyu klonlayın:
   ```bash
   git clone https://github.com/KULLANICIADI/4.LinearRegression.git
   cd 4.LinearRegression
   ```

2. Gerekli Python paketlerini yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Jupyter Notebook’u başlatın:
   ```bash
   jupyter notebook
   ```
   - `LinearRegression_LS.ipynb` ve `LinearRegression_SK.ipynb` dosyalarını sırasıyla çalıştırın.

---

## Sonuçlar ve Karşılaştırma

Aşağıdaki tabloda eğitim ve test setleri için her iki yöntemde hesaplanan maliyet (cost) değerleri yer almaktadır:

| Model                                | Train Cost | Test Cost  |
|--------------------------------------|------------|------------|
| Least Squares (from scratch)         | 8.1999     | 8.4441     |
| scikit-learn `LinearRegression`      | 8.1999     | 8.4441     |

---

## Model Performansı (R² Skorları)

Aşağıdaki tabloda eğitim ve test setleri için hesaplanan R² skorları gösterilmektedir:

| Model                                | R² Score (Train) | R² Score (Test) |
|--------------------------------------|------------------|-----------------|
| Least Squares (from scratch)         | 0.8157           | 0.8194          |
| scikit-learn `LinearRegression`      | 0.8157           | 0.8194          |

**Yorum:**
- Eğitim setindeki verinin yaklaşık %81.6’sını model açıklayabiliyor.
- Test setinde yaklaşık %81.9’unu açıklayarak güçlü bir genelleme performansı gösteriyor.
- Model under-/over-fitting yapmıyor; eğitim ve test skorlarının yakınlığı bu durumu doğruluyor.
- Daha yüksek performans için özellik mühendisliği ve düzenlileştirme yöntemleri (Ridge, Lasso) düşünebilirsiniz.

---

## Maliyet (Cost) Fonksiyonu

Kullandığımız ortalama kare hatayı (MSE) baz alan maliyet fonksiyonu:

```python
def compute_cost(y_true, y_pred):
    m = len(y_true)
    return (1/(2*m)) * np.sum((y_pred - y_true)**2)
```

---

## Görselleştirme

Her iki yöntemde de “Gerçek vs Tahmin” grafiklerini oluşturabilir, 45° çizgisi etrafında ne kadar toplandığına bakarak görsel performans analizi yapabilirsiniz.

---

## Lisans & Katkılar

- Kodlar açık kaynaklıdır; çekinmeden forklayıp geliştirebilirsiniz.  
- Herhangi bir katkı, sorun bildirimi veya öneri için “Issues” sekmesini kullanabilirsiniz.
