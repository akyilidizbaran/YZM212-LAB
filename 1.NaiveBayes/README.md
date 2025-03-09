# Bernoulli Naive Bayes Sınıflandırıcı Uygulaması

Bu proje, **Bernoulli Naive Bayes** algoritmasını hem `scikit-learn` kütüphanesi kullanarak hem de manuel olarak Python dilinde uygulamayı amaçlamaktadır. Bernoulli Naive Bayes, özellikle ikili (binary) verilerle çalışmak üzere tasarlanmış, basit ve etkili bir olasılıksal makine öğrenmesi algoritmasıdır.

## Proje İçeriği

- **Bernoulli Naive Bayes w Sklearn.py**: Bernoulli Naive Bayes algoritmasının `scikit-learn` kütüphanesi ile uygulanmasını içeren python dosyası.
- **Bernoulli Naive Bayes.py**: Bernoulli Naive Bayes algoritmasının sıfırdan manuel olarak kodlandığı python dosyası.
- **archive.zip**: Modelin eğitimi ve test edilmesi için kullanılan ham veri setini içeren sıkıştırılmış dosya.
- **Veri.xlsx**: Önişleme adımlarından geçirilmiş ve Bernoulli Naive Bayes algoritmasına uygun hale getirilmiş veri setini içeren Excel dosyası.

## Veri Seti Özellikleri

**archive.zip** dosyası içerisinde yer alan ham veri seti, metin belgelerinden oluşmaktadır. Bu belgeler, aşağıdaki önişleme adımlarından geçirilerek Bernoulli Naive Bayes algoritmasına uygun hale getirilmiştir:

1. **Metin Temizleme**: Noktalama işaretleri, sayılar ve özel karakterler metinlerden çıkarılmıştır.
2. **Küçük Harfe Dönüştürme**: Tüm metinler küçük harfe dönüştürülerek tutarlılık sağlanmıştır.
3. **Gereksiz Kelimelerin Kaldırılması**: "ve", "bir", "bu" gibi anlamsız kelimeler metinlerden çıkarılmıştır.
4. **Köklerine Ayırma (Stemming)**: Kelimeler kök hallerine indirgenmiştir.

Bu işlemler sonucunda, veri setindeki her bir belge, en çok kullanılan 20 kelimenin varlığı veya yokluğuna göre ikili (binary) özelliklerle temsil edilmiştir. Örneğin, bir kelime belgede mevcutsa 1, değilse 0 olarak kodlanmıştır. Bu sayede, Bernoulli Naive Bayes algoritmasının gerektirdiği ikili özellikler elde edilmiştir. 

**Veri.xlsx** dosyası, projenin temelini oluşturan veri setini içermektedir. Bu veri seti aşağıdaki özelliklere sahiptir:

1. Özellikler (Features): Her bir satır, belirli özelliklere sahip bir örneği temsil eder. Örneğin, metin verileri için kelimelerin belgede bulunup bulunmadığını belirten ikili değerler (0 veya 1) kullanılabilir.

2. Hedef Değişken (Target Variable): Her bir örneğin ait olduğu sınıfı gösteren ikili bir değişken. Örneğin, bir e-postanın spam olup olmadığını belirten 0 veya 1 değeri.

Veri setinin yapısı, Bernoulli Naive Bayes algoritmasının gereksinimlerine uygun olarak ikili (binary) özelliklerden oluşmaktadır.

## Sonuçlar

Bu çalışmada, Bernoulli Naive Bayes algoritması iki farklı yöntemle uygulanmış ve sonuçları karşılaştırılmıştır:

Confusion Matrix Değerleri:

Scikit-learn ile yapılan uygulamada:

954 doğru negatif (True Negative)

11 yanlış pozitif (False Positive)

105 yanlış negatif (False Negative)

45 doğru pozitif (True Positive)

Kodun çalışma süresi: 1.4630 saniye

Manuel olarak kodlanan uygulamada:

954 doğru negatif (True Negative)

12 yanlış pozitif (False Positive)

100 yanlış negatif (False Negative)

49 doğru pozitif (True Positive)

Kodun çalışma süresi: 1.5344 saniye

Performans Karşılaştırması:

Doğruluk (Accuracy) açısından bakıldığında, sklearn ile yapılan uygulama %90.0, manuel uygulama ise %90.3 doğruluk oranına sahiptir. Aralarındaki fark oldukça küçük olup manuel model biraz daha yüksek doğruluk sağlamıştır.

Hassasiyet (Precision) (Pozitif sınıf için) iki modelde de aynıdır ve %80.3 olarak hesaplanmıştır.

Duyarlılık (Recall) (Pozitif sınıf için) manuel modelde biraz daha yüksektir. Sklearn ile yapılan model %30.0 duyarlılığa sahipken, manuel model %32.9 duyarlılığa sahiptir. Bu, manuel modelin pozitif sınıfları biraz daha iyi tahmin ettiğini göstermektedir.
Kod Çalışma Süresi açısından bakıldığında, sklearn uygulaması 1.4630 saniyede, manuel uygulama ise 1.5344 saniyede çalışmıştır. Sklearn daha optimize olduğu için daha hızlıdır.

## Kişisel Yorum

Scikit-learn kullanılarak yapılan uygulama, hız açısından daha avantajlıdır.
Manuel olarak kodlanan model, pozitif sınıfı biraz daha iyi tahmin etmiş (Recall değeri daha yüksek) ancak çalıştırma süresi biraz daha uzundur.
Genel doğruluk farkı çok küçük olduğu için (~%0.3), manuel uygulama daha fazla zaman harcamasına rağmen büyük bir iyileştirme sunmamaktadır.
Sonuç olarak, sklearn çözümü daha verimli ve pratik bir seçimdir. Ancak manuel uygulama, modelin işleyişini daha iyi anlamak açısından oldukça değerli bir çalışma olmuştur.

## Kaynaklar

- [Bernoulli Naive Bayes - GeeksforGeeks](https://www.geeksforgeeks.org/bernoulli-naive-bayes/)
- [Naive Bayes Sınıflandırıcı - Vikipedi](https://tr.wikipedia.org/wiki/Naive_Bayes_s%C4%B1n%C4%B1fland%C4%B1r%C4%B1c%C4%B1s%C4%B1)
- [Naive Bayes - Ultralytics](https://www.ultralytics.com/tr/glossary/naive-bayes)
- [SMS Spam Collection Dataset - Kaggle](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset?resource=download)



Baran Akyıldız 23290910 
