# Ordinal Lojistik Regresyon ile Sınıflandırma

Bu proje, **Ordinal Lojistik Regresyon** yöntemini kullanarak sıralı kategorik verilerin sınıflandırılmasını amaçlamaktadır. Model, hem `scikit-learn` kütüphanesi kullanılarak hem de algoritmanın matematiksel temelleriyle sıfırdan Python dilinde manuel olarak uygulanmıştır.

## Proje İçeriği

- **OrdinalLogisticRegression_w_Sklearn.py**: `scikit-learn` kütüphanesi kullanılarak Ordinal Lojistik Regresyon modelinin uygulanmasını içeren Python dosyası.
- **OrdinaLogisticRegression.py**: Ordinal Lojistik Regresyon algoritmasının sıfırdan manuel olarak kodlandığı Python dosyası.
- **WineQT.xlsx**: Modelin eğitimi ve test edilmesi için kullanılan şarap kalitesi veri setini içeren Excel dosyası.
- **archive.zip**: Ham veri setini içeren sıkıştırılmış dosya.

## Veri Seti Özellikleri

**WineQT.xlsx** dosyası, şarap kalitesini belirleyen çeşitli kimyasal özellikleri içermektedir. Her bir örnek için aşağıdaki özellikler bulunmaktadır:

- **Sabit Asitlik (Fixed Acidity)**: Şarabın sabit asit içeriği.
- **Uçucu Asitlik (Volatile Acidity)**: Şarabın uçucu asit içeriği.
- **Sitrik Asit (Citric Acid)**: Sitrik asit miktarı.
- **Klorürler (Chlorides)**: Tuz içeriği.
- **Serbest Sülfür Dioksit (Free Sulfur Dioxide)**: Koruyucu olarak kullanılan serbest SO₂ miktarı.
- **Toplam Sülfür Dioksit (Total Sulfur Dioxide)**: Toplam SO₂ miktarı.
- **Yoğunluk (Density)**: Şarabın yoğunluğu.
- **pH**: Asitlik seviyesi.
- **Sülfatlar (Sulphates)**: Sülfat miktarı.
- **Alkol (Alcohol)**: Alkol oranı.
- **Kalite (Quality)**: 0 ile 10 arasında değişen ve şarabın kalitesini gösteren ordinal hedef değişken.

## Sonuçlar

- **Doğruluk Oranı (Accuracy)**: Scikit-learn ile yapılan uygulama %63.0, manuel uygulama ise %49.3 doğruluk oranına sahiptir. Aralarındaki fark fazlaca büyüktür. Bunun sebebi veri setinin yetersiz olması olabilir. Kütüphane ile yapılan uygulama çok daha fazla bir accuracy sağlamıştır.
- **Duyarlılık (Recall)**: Manuel modelde biraz daha yüksektir. Scikit-learn ile yapılan model %30.0 duyarlılığa sahipken, manuel model %32.9 duyarlılığa sahiptir. Bu, manuel modelin pozitif sınıfları biraz daha iyi tahmin ettiğini göstermektedir.
- **Çalışma Süresi**: Scikit-learn uygulaması 0,0310 saniyede eğitilip, 0,0010 saniyede tahmin ettirilmiştir. Manuel uygulama ise 3,6675 saniyede eğitilip, 0,0279 saniyede test edilmiştir. Kütüphaneli uygulamanın hız fakötrü çok daha yüksektir.

## Kişisel Yorum

- Scikit-learn kullanılarak yapılan uygulama, hız açısından daha avantajlıdır.
- Manuel olarak kodlanan model, pozitif sınıfı biraz daha iyi tahmin etmiş (Recall değeri daha yüksek) ancak çalıştırma süresi biraz daha uzundur.
- Sonuç olarak, Scikit-learn çözümü daha verimli ve pratik bir seçimdir. Ancak manuel uygulama, modelin işleyişini daha iyi anlamak açısından oldukça değerli bir çalışma olmuştur.

## Kaynakça

- [Ordinal Regression - Wikipedia](https://en.wikipedia.org/wiki/Ordinal_regression)
- [Ordinal Logistic Regression in Python - Medium](https://medium.com/@jumbongjunior1999/ordinal-logistic-regression-in-python-and-r-f6ee05d48d16)
- [Ordinal Regression - IBM Documentation](https://www.ibm.com/docs/en/spss-statistics/saas?topic=edition-ordinal-regression)
- [A Complete Tutorial on Ordinal Regression in Python](https://analyticsindiamag.com/ai-trends/a-complete-tutorial-on-ordinal-regression-in-python/)
- [Ordinal Regression Analysis in Python - YouTube](https://www.youtube.com/watch?v=ueh9UNEvN7w)
