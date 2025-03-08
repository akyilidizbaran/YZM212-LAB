# Bernoulli Naive Bayes Sınıflandırıcı Uygulaması

Bu proje, **Bernoulli Naive Bayes** algoritmasını hem `scikit-learn` kütüphanesi kullanarak hem de manuel olarak Python dilinde uygulamayı amaçlamaktadır. Bernoulli Naive Bayes, özellikle ikili (binary) verilerle çalışmak üzere tasarlanmış, basit ve etkili bir olasılıksal makine öğrenmesi algoritmasıdır. :contentReference[oaicite:2]{index=2}

## Proje İçeriği

- **NaiveBayes.ipynb**: Bernoulli Naive Bayes algoritmasının `scikit-learn` kütüphanesi ile uygulanmasını içeren Jupyter Notebook dosyası.
- **ManualBernoulliNB.ipynb**: Bernoulli Naive Bayes algoritmasının sıfırdan manuel olarak kodlandığı Jupyter Notebook dosyası.
- **archive.zip**: Modelin eğitimi ve test edilmesi için kullanılan ham veri setini içeren sıkıştırılmış dosya.
- **Veri.xlsx**: Önişleme adımlarından geçirilmiş ve Bernoulli Naive Bayes algoritmasına uygun hale getirilmiş veri setini içeren Excel dosyası.

## Veri Seti Özellikleri

**archive.zip** dosyası içerisinde yer alan ham veri seti, metin belgelerinden oluşmaktadır. Bu belgeler, aşağıdaki önişleme adımlarından geçirilerek Bernoulli Naive Bayes algoritmasına uygun hale getirilmiştir:

1. **Metin Temizleme**: Noktalama işaretleri, sayılar ve özel karakterler metinlerden çıkarılmıştır.
2. **Küçük Harfe Dönüştürme**: Tüm metinler küçük harfe dönüştürülerek tutarlılık sağlanmıştır.
3. **Gereksiz Kelimelerin Kaldırılması**: "ve", "bir", "bu" gibi anlamsız kelimeler metinlerden çıkarılmıştır.
4. **Köklerine Ayırma (Stemming)**: Kelimeler kök hallerine indirgenmiştir.

Bu işlemler sonucunda, veri setindeki her bir belge, en çok kullanılan 20 kelimenin varlığı veya yokluğuna göre ikili (binary) özelliklerle temsil edilmiştir. Örneğin, bir kelime belgede mevcutsa 1, değilse 0 olarak kodlanmıştır. Bu sayede, Bernoulli Naive Bayes algoritmasının gerektirdiği ikili özellikler elde edilmiştir. 

**Veri.xlsx** dosyası, bu önişleme adımlarından geçirilmiş ve ikili özelliklerle temsil edilen nihai veri setini içermektedir.

## Sonuçlar

Her iki yaklaşım da (kütüphane kullanarak ve manuel) Bernoulli Naive Bayes algoritmasının performansını değerlendirmeyi amaçlamaktadır. Sonuçlar, modelin doğruluğu, kesinliği ve hatırlama oranı gibi metriklerle analiz edilmiştir.

## Kaynaklar

- [Bernoulli Naive Bayes - GeeksforGeeks](https://www.geeksforgeeks.org/bernoulli-naive-bayes/)
- [Naive Bayes Sınıflandırıcı - Vikipedi](https://tr.wikipedia.org/wiki/Naive_Bayes_s%C4%B1n%C4%B1fland%C4%B1r%C4%B1c%C4%B1s%C4%B1)
- [Naive Bayes - Ultralytics](https://www.ultralytics.com/tr/glossary/naive-bayes)
