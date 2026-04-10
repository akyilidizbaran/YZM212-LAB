# 1.4 BayesianBrightnessInference

Bu klasor, YZM212 Makine Ogrenmesi dersi 4. laboratuvar odevi icin hazirlanan Bayesyen parlaklik analizi teslimini icerir. Gorev, gurultulu astronomi gozlemlerinden bir gok cisminin gercek parlakligini (`mu`) ve olcum belirsizligini (`sigma`) Bayesyen cikarim ile tahmin etmektir.

## Icerik

- `Bayesian_Brightness_Inference.ipynb`: ana notebook teslimi
- `bayesian_brightness_analysis.py`: veri uretimi, MCMC, posterior ozetleri ve figure uretimi
- `requirements.txt`: klasor-ici bagimliliklar
- `figures/`: kaydedilen grafikler
- `report/`: `bayesian_brightness_report.pdf` ve rapor uretim scripti

## Problem Tanimi

PDF'de verilen senaryo, laboratuvarda yeniden uretilemeyen astronomi gozlemlerini Bayes Teoremi ile yorumlamayi istiyor. Bu teslimde:

1. Gaussian gozlem modeli ile `mu` ve `sigma` icin posterior tanimlandi.
2. `emcee` kutuphanesi ile MCMC orneklemesi yapildi.
3. Prior etkisi ve veri miktari etkisi ayrica test edildi.
4. Corner plot, trace plot ve karsilastirma grafigi uretildi.
5. Sonuclar notebook, README ve ayri PDF raporu olarak teslim edildi.

## Veri

Temel veri, PDF'deki ile ayni sabitlerle sentetik olarak uretildi:

- `true_mu = 150.0`
- `true_sigma = 10.0`
- `n_obs = 50`
- `seed = 42`

Kod, PDF'deki veri uretimini birebir izleyerek `np.random.seed(42)` ve `np.random.randn(50)` kullaniyor. Uretilen temel veri setinin ornek ortalamasi `147.745`, ornek standart sapmasi `9.243` oldu. Ek analizlerde:

- ayni veri ile dar `mu` prior'i (`100 < mu < 110`) denendi
- ayni rastgele serinin ilk 5 gozlemi kullanilarak `n_obs = 5` senaryosu kuruldu

## Yontem

- Log-likelihood, Gaussian gozlem modeli ile tanimlanir.
- Prior iki bicimde kullanilir: genis prior ve dar `mu` prior'i.
- Posterior, `emcee.EnsembleSampler` ile orneklenir.
- Sonuclar median, `%16`, `%84`, mutlak hata ve guven araligi genisligi ile raporlanir.
- MCMC sabitleri: `initial=[140, 5]`, `n_walkers=32`, `n_steps=2000`, `burn_in=500`, `thin=15`
- Dar prior senaryosunda sampler'in prior icinde baslayabilmesi icin walker merkezi `mu=105` civarina cekildi.

## Sonuclar

Temel senaryoda elde edilen tablo:

| Degisken | Gercek Deger | Tahmin Edilen (Median) | Alt Sinir (%16) | Ust Sinir (%84) | Mutlak Hata |
| --- | ---: | ---: | ---: | ---: | ---: |
| mu (Parlaklik) | 150.000 | 147.750 | 146.374 | 149.122 | 2.250 |
| sigma (Hata Payi) | 10.000 | 9.487 | 8.626 | 10.484 | 0.513 |

Ek senaryo bulgulari:

- Temel senaryoda acceptance fraction `0.709` oldu.
- Dar prior senaryosunda `mu` mediani `109.441` seviyesine cekildi ve `sigma` mediani `40.266` seviyesine siserek modeli telafi etmeye calisti.
- `n_obs=5` senaryosunda `mu` mediani `154.625`, `sigma` mediani `9.038` oldu; belirsizlikler belirgin bicimde genisledi.
- Uretilen figure dosyalari:
  - `figures/base_corner_plot.png`
  - `figures/base_trace_plot.png`
  - `figures/prior_effect_corner_plot.png`
  - `figures/sample_size_effect_corner_plot.png`
  - `figures/comparison_summary.png`

## Yorum / Tartisma

- **Accuracy:** Temel senaryoda `mu` icin mutlak hata `2.250`, `sigma` icin `0.513`. Posterior merkezleri, gercek parametrelerden cok veri setinin gozlenen ortalama ve sacilim degerlerine yaklasti; bu Bayesyen modelin sonlu gozleme uygun davrandigini gosteriyor.
- **Prior etkisi:** Dar `mu` prior'i, posterior'u veri yerine prior bandina cekti. Sonuc olarak `mu` temel senaryoya gore `38.308` birim sola kaydi ve `sigma` yanlis merkezlenmis modeli telafi etmek icin `40` civarina buyudu.
- **Veri miktari etkisi:** `n_obs=5` durumunda `mu` icin guven araligi temel senaryoya gore `3.05x`, `sigma` icin `4.91x` genisledi. Veri azaldikca posterior dogal olarak daha yayvan hale geliyor.
- **Precision:** Mutlak CI genisligi yerine goreli belirsizlige bakildiginda `mu` icin CI genisligi `%1.83`, `sigma` icin `%18.58`. Bu nedenle ortalama tahmini goreli olarak cok daha kesin.
- **Korelasyon:** Temel corner plot icin ornek korelasyon katsayisi `0.023`. Elips neredeyse dik oldugu icin `mu` ve `sigma` arasinda guclu bir korelasyon yok.

## Calistirma

```bash
python3 -m pip install -r "1.4 BayesianBrightnessInference/requirements.txt"
python3 -m jupyter nbconvert --to notebook --execute --inplace "1.4 BayesianBrightnessInference/Bayesian_Brightness_Inference.ipynb"
python3 "1.4 BayesianBrightnessInference/report/generate_report.py"
```

Teslim dosyalari:

- Notebook: `1.4 BayesianBrightnessInference/Bayesian_Brightness_Inference.ipynb`
- PDF raporu: `1.4 BayesianBrightnessInference/report/bayesian_brightness_report.pdf`
