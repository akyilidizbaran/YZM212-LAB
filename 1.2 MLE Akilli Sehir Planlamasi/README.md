# 1.2 MLE ile Akilli Sehir Planlamasi

Bu klasor, YZM212 Makine Ogrenmesi dersi 2. laboratuvar odevi icin hazirlanan Poisson dagilimi ve Maximum Likelihood Estimation (MLE) uygulamasini icerir. Senaryo, bir dakikada ana caddeden gecen arac sayilarini modelleyerek trafik yogunlugunu tahmin etmektir.

## Icerik

- `MLE_Akilli_Sehir_Planlamasi.ipynb`: Teorik turetme, sayisal MLE, gorsellestirme ve outlier analizi
- `requirements.txt`: Notebook icin gerekli kutuphaneler
- `figures/`: Notebook calistirildiginda uretilen grafikler

## Problem Tanimi

Verilen trafik verisinin Poisson dagilimi ile modellendigi varsayilir. Amaç:

1. Poisson olabilirlik ve log-olabilirlik fonksiyonunu turetmek
2. MLE tahmincisinin ornek ortalama oldugunu gostermek
3. Python ile negatif log-likelihood minimizasyonu yaparak ayni parametreyi sayisal olarak bulmak
4. Histogram ve Poisson PMF ile model uyumunu gorsellestirmek
5. Tek bir aykiri gozlemin MLE tahminini nasil bozdugunu yorumlamak

## Veri

Temiz trafik verisi:

```python
[12, 15, 10, 8, 14, 11, 13, 16, 9, 12, 11, 14, 10, 15]
```

## Yontem

- Teorik kisimda Poisson log-likelihood turevlenerek kapali form MLE sonucu elde edilir.
- Sayisal kisimda `scipy.optimize.minimize` ile negatif log-likelihood minimize edilir.
- `matplotlib` ile histogram ve Poisson PMF ayni grafikte karsilastirilir.
- Outlier senaryosunda veri setine `200` eklenerek MLE hassasiyeti analiz edilir.

## Temel Sonuclar

- Analitik MLE: `12.142857`
- Sayisal MLE: `12.142857` (optimizasyon sonucu analitik cozumle cakisir)
- Outlier sonrasi MLE: `24.666667`
- Tek bir aykiri deger, tahmini ortalamayi yaklasik `%103.24` artirmistir.

## Yorum / Tartisma

- Temiz veri icin Poisson modeli trafik akisinin merkezini makul bicimde temsil eder.
- Ornek varyans ortalamadan daha kucuk oldugu icin veri, ideal Poisson varsayimindan biraz daha duzenli gorunur.
- Tek bir ekstrem gozlem MLE tahminini ciddi bicimde saptirdigi icin belediye gibi karar vericiler aykiri deger temizligi yapmadan dogrudan altyapi karari vermemelidir.

## Calistirma

```bash
python3.11 -m pip install -r "1.2 MLE Akilli Sehir Planlamasi/requirements.txt"
python3.11 -m jupyter nbconvert --to notebook --execute --inplace "1.2 MLE Akilli Sehir Planlamasi/MLE_Akilli_Sehir_Planlamasi.ipynb"
```
