# EigenVectorsValues

## 1. Matris, Özdeğer ve Özvektör Tanımları

### 1.1 Tanımlar
- **Matris:** Satır ve sütunlardan oluşan iki boyutlu sayısal veri yapısıdır. Veri dönüşümleri ve lineer cebirsel işlemler makine öğrenmesinde sıklıkla matrisler üzerinden gerçekleştirilir.
- **Özdeğer (Eigenvalue):** \(A\) kare matrisinin \(v\neq0\) vektörü için \(Av = \lambda v\) eşitliğini sağlayan scalardır. Burada \(\lambda\) matrisin özdeğeridir.
- **Özvektör (Eigenvector):** \(A\) matrisine etki ettiğinde yönü değişmeyen, sadece ölçeklenen vektördür; yani \(v\) vektörüdür.

### 1.2 Makine Öğrenmesi ile İlişki
- **Temel Bileşen Analizi (PCA):** Veri boyutunu azaltmak için kovaryans matrisinin özdeğerleri ve özvektörleri kullanılır. En büyük özdeğere sahip özvektörler, verinin varyansını en çok tutan eksenleri belirler.
- **Spektral Kümeleme:** Graf tabanlı yöntemlerde, graf Laplasyanı matrisinin özdeğerleri ve özvektörleri küme yapılarını ortaya çıkarır.
- **Diğer Yaklaşımlar:** Yansıtmalı yöntemler, titreşim analizi ve Latent Semantic Analysis (LSA) gibi tekniklerde de özdeğer–özvektör ayrıştırması kritik rol oynar.

**Kaynakça:**
1. Brownlee, J. "Introduction to Matrices for Machine Learning." Machine Learning Mastery. Erişim: 
2. Brownlee, J. "Introduction to Eigendecomposition, Eigenvalues and Eigenvectors." Machine Learning Mastery. 

## 2. NumPy `linalg.eig` Fonksiyonu

NumPy’ın `numpy.linalg.eig` fonksiyonu, bir kare matrisin özdeğerlerini ve özvektörlerini bulmak için optimize edilmiş bir C/Fortran altyapısı kullanır. İşleyiş adımları:

1. **Giriş Validasyonu:** Matrisin kare olması kontrol edilir.
2. **Atama ve Depolama:** Veriler C dizilerine dönüştürülüp bellek bloklarına yerleştirilir.
3. **Algoritma:** QR ayrıştırması gibi sayısal yaklaşım kullanılarak özdeğerler ve isteğe bağlı olarak özvektörler bulunur.
4. **Çıktı:** Python dizileri (NumPy `ndarray`) biçiminde döndürülür.

**Referanslar:**
- NumPy Documentation, "numpy.linalg.eig", NumPy 2.1 Reference. Erişim: 7 Nisan 2025.
- NumPy Source Code, `numpy/linalg` modülü, GitHub. Erişim: 7 Nisan 2025.

## 3. Manuel Özdeğer Hesaplama ve Karşılaştırma

LucasBN tarafından sunulan "Eigenvalues-and-Eigenvectors" GitHub deposunda verilen karakteristik polinom üzerinden Laplace açılımı ile özdeğer hesaplama algoritmasını kullanarak:

- `det_poly` fonksiyonu matrisin karakteristik polinomunu oluşturur.
- `numpy.roots` ile polinom kökleri (özdeğerler) bulunur.
- Aynı matris için `numpy.linalg.eig` çıktısı ile sonuçlar karşılaştırılır.

**Karşılaştırma Örnekleri:**
- 3×3 ve 4×4 matrislerde NumPy yöntemi, manuel yönteme göre çok daha hızlıdır.

**Kaynak:**
- LucasBN, "Eigenvalues-and-Eigenvectors", GitHub Repository. Erişim: 7 Nisan 2025.

## 4. Sonuç

Manuel Laplace açılımı algoritması eğitim ve deneyim amaçlı faydalı iken, üretim ortamı ve büyük boyutlu matris işlemleri için NumPy’ın `linalg.eig` fonksiyonu performans ve doğruluk açısından tercih edilmelidir.

---

*Bu rapor, YZM212 Makine Öğrenmesi III. Laboratuvar değerlendirmesi için hazırlanmıştır.*
