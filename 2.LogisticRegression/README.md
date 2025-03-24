# Logistic Regression ile İkili Sınıflandırma

Bu proje, logistic regression yöntemini kullanarak ikili sınıflandırma problemini çözmeyi amaçlamaktadır. Model hem `Scikit-learn` kütüphanesi ile hem de bu algoritmanın matematiksel temelini kullanarak sıfırdan Python ile manuel olarak uygulanmıştır.

## İçerik

- [Kullanılan Veri Seti](#kullanılan-veri-seti)
- [Kullanılan Yöntemler](#kullanılan-yöntemler)
- [Scikit-learn ile Model Eğitimi](#scikit-learn-ile-model-eğitimi)
- [Sıfırdan Logistic Regression Modeli](#sıfırdan-logistic-regression-modeli)
- [Karşılaştırma ve Sonuçlar](#karşılaştırma-ve-sonuçlar)
- [Nasıl Çalıştırılır](#nasıl-çalıştırılır)

## Kullanılan Veri Seti

Veri seti [Kaggle/UCI vb. kaynağın adı] üzerinden alınmıştır. Veri, ikili sınıflandırmaya uygun hale getirilmiş ve gerekli ön işleme adımlarından geçirilmiştir (eksik veri temizleme, normalizasyon vb.).

## Kullanılan Yöntemler

- **Logistic Regression:** Sınıflandırma algoritması olarak kullanıldı.
- **Cost Function:** Maksimum likelihood esaslı log-loss fonksiyonu.
- **Optimization:** Gradient descent algoritması kullanılarak modelin ağırlıkları güncellendi.
- **Evaluation Metrics:** Accuracy, precision, recall ve confusion matrix.

## Scikit-learn ile Model Eğitimi

Model `sklearn.linear_model.LogisticRegression` sınıfı kullanılarak eğitildi. Eğitim ve test setleri ayrıldıktan sonra model başarı oranı ölçüldü.

## Sıfırdan Logistic Regression Modeli

Scikit-learn dışında aynı veri seti ile sıfırdan logistic regression algoritması yazıldı:

- Sigmoid fonksiyonu
- Cost fonksiyonu (binary cross-entropy)
- Gradient descent ile ağırlıkların güncellenmesi
- Modelin eğitilmesi ve tahmin yapılması

## Karşılaştırma ve Sonuçlar

Her iki model de aynı eğitim ve test verisiyle test edildi. Performans karşılaştırmaları yapıldı ve benzer sonuçlar elde edildiği gözlemlendi.

## Nasıl Çalıştırılır

1. Python 3 yüklü olduğundan emin olun.
2. Gerekli kütüphaneleri yüklemek için:

```bash
pip install numpy pandas matplotlib scikit-learn

