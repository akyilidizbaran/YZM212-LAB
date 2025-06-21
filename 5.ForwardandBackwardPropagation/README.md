# İleri/Geri Yayılım ile Sinir Ağı - Orman Örtüsü Sınıflandırması

## Veri Seti
- **Adı**: UCI Forest CoverType
- **Örnek Sayısı**: 581.012
- **Özellikler**: 54 sayısal ve ikili özellik (rakım, eğim, toprak türü, vb.)
- **Sınıflar**: 7 örtü tipi (1–7)
- **Kaynak**: UCI Machine Learning Repository  
  https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz

## Neden Bu Veri Seti?
Gerçek dünya çok sınıflı bir sınıflandırma problemi.  
- Yaklaşık 580.000 örnekle ölçeklenebilirlik test edilir.  
- Karmaşık arazi ilişkilerini modellemek için zengin özellikler.  
- İleri/geri yayılım performansını büyük veri üzerinde gösterir.

## Kod Özeti
- **Dosya**: `train_covtype_nn.py`  
- **Kütüphaneler**: NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn  
- **Adımlar**:
  1. Gzipped CSV indir ve yükle  
  2. Önişleme: X/y ayrımı, `float64` dönüşümü, etiketleri one-hot kodlama  
  3. Eğitim/test ayrımı  
  4. İki katmanlı sinir ağı sınıfı tanımı  
  5. İleri yayılım (linear → ReLU → linear → Softmax)  
  6. Geri yayılım (gradyan hesaplama ve güncelleme)  
  7. 100 epoch boyunca eğitim, her 10 epoch'ta loss yazdırma  
  8. Loss eğrisini çizme  
  9. Confusion matrix ve test doğruluğunu gösterme  

## Algoritma Detayları

### 1. İleri Yayılım (Forward Propagation)

- **Matematiksel İfade**  
  1. Katman (Gizli katman):  
     \[
       Z^{[1]} = X W^{[1]} + b^{[1]},\quad
       A^{[1]} = \mathrm{ReLU}\bigl(Z^{[1]}\bigr)
     \]
  2. Katman (Çıkış katmanı):  
     \[
       Z^{[2]} = A^{[1]} W^{[2]} + b^{[2]},\quad
       A^{[2]} = \mathrm{Softmax}\bigl(Z^{[2]}\bigr)
     \]

- **Türkçe Açıklama**  
  1. **Z¹ hesaplama**: Giriş verisine ağırlık matrisi ve bias eklenir.  
  2. **A¹ aktivasyonu**: ReLU fonksiyonu negatif değerleri sıfıra çevirerek gizli katman çıktısını oluşturur.  
  3. **Z² hesaplama**: Gizli katman çıktısı bir sonraki ağırlık matrisi ve bias ile çarpılır.  
  4. **A² aktivasyonu**: Softmax, son katman skorlarını olasılıklara dönüştürür, böylece her sınıfın tahmin olasılığı elde edilir.

### 2. Kayıp Fonksiyonu (Loss Function)

- **Matematiksel İfade**  
  \[
    L = -\frac{1}{m}\sum_{i=1}^{m} \sum_{k=1}^{C} y_{i,k}\,\log\bigl(\hat y_{i,k}\bigr)
  \]

- **Türkçe Açıklama**  
  - \(m\): eğitim örneği sayısı, \(C\): sınıf sayısı.  
  - Gerçek (one-hot) etiket \(y_{i,k}\) ile modelin tahmin olasılığı \(\hat y_{i,k}\) çarpılır ve logaritması alınır.  
  - Tüm örnekler ve sınıflar üzerinden toplanır, negatif işaretiyle ortalanır.  
  - Amaç, doğru sınıfın olasılığını maksimize edip loss’u minimize etmektir.

### 3. Geri Yayılım (Backward Propagation)

- **Matematiksel İfade**  

  1. Çıkış katmanı gradyanları:
     \[
       dZ^{[2]} = A^{[2]} - Y,\quad
       dW^{[2]} = \frac{1}{m}\,(A^{[1]})^T dZ^{[2]},\quad
       db^{[2]} = \frac{1}{m}\sum dZ^{[2]}
     \]
  2. Gizli katman gradyanları:
     \[
       dA^{[1]} = dZ^{[2]}\,(W^{[2]})^T,\quad
       dZ^{[1]} = dA^{[1]}\,\odot\,\mathrm{ReLU}'\bigl(Z^{[1]}\bigr)
     \]
     \[
       dW^{[1]} = \frac{1}{m}\,X^T dZ^{[1]},\quad
       db^{[1]} = \frac{1}{m}\sum dZ^{[1]}
     \]
  3. Ağırlık ve bias güncellemesi:
     \[
       W^{[l]} \leftarrow W^{[l]} - \alpha\,dW^{[l]},\quad
       b^{[l]} \leftarrow b^{[l]} - \alpha\,db^{[l]}
     \]

- **Türkçe Açıklama**  
  1. **Çıkış katmanı**: Tahmin olasılıkları ile gerçek etiketler farkı \(dZ^{[2]}\) olarak bulunur. Bu fark, ikinci katman ağırlık ve bias gradyanlarının hesaplanmasında kullanılır.  
  2. **Gizli katman**: Çıkış gradyanının bir önceki katmana aktarılması için ağırlıkların transpozu ile çarpılır. ReLU türevi ile eleman bazlı çarpılarak gerçek gizli birim gradyanı \(dZ^{[1]}\) elde edilir.  
  3. **Güncelleme**: Öğrenme oranı \(\alpha\) ile ağırlık ve bias gradyanları çarpılarak orijinal parametrelerden çıkarılır. Bu adım modelin hatayı azaltacak yönde kendini “ayarlamasını” sağlar.

---



## Sonuçlar ve Yorum
- **Loss Eğrisi**:  
   <img width="425" alt="1" src="https://github.com/user-attachments/assets/31519daf-693a-4b67-a720-f055f38e4469" />
  İlk epoch’lerde hızlı düşüş, 100. epoch’a ~1.38 civarında sabitlenme.  

- **Confusion Matrix**:  
  <img width="419" alt="2" src="https://github.com/user-attachments/assets/af1ec05e-cb2d-4da0-b988-5456d92d4c55" />

  Sınıf dengesizliği nedeniyle çoğunlukla tip 2 tahmin edilmiş.  

- **Test Doğruluğu**: `0.4876`  
  - Rastgele şansa (~14.3%) göre çok daha iyi performans.  
  - Daha derin ağlar veya düzenlileştirme ile iyileştirilebilir.

## Nasıl Çalıştırılır?
1. `train_covtype_nn.py` dosyasını proje köküne koyun.  
2. `data/` klasörü yoksa oluşturulur, veri otomatik indirilir.  
3. Bağımlılıkları yükleyin:  
   ```bash
   pip install numpy pandas matplotlib seaborn scikit-learn
   ```  
4. Çalıştırın:  
   ```bash
   python train_covtype_nn.py
   ```  
5. Çıktılar:  
   - `loss_curve.png`: epoch vs. loss eğrisi  
   - `confusion_matrix.png`: test confusion matrix  
   - Konsol: epoch’lara göre loss ve final doğruluk  

## Dosya Yapısı
```
forest-covertype-nn/
├── data/
│   └── covtype.data.gz
├── train_covtype_nn.py
├── loss_curve.png
├── confusion_matrix.png
├── README.md
└── Requirements.txt
```

*Sinir ağı NumPy ile baştan yazıldı.*
