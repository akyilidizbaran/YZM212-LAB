# PROJECT_MEMORY

## 0) TL;DR (En guncel durum)

* Su an YZM212-LAB deposuna 4. laboratuvar icin `1.4 BayesianBrightnessInference` klasoru eklendi.
* Son degisiklik: Bayesian MCMC notebook'u, helper module, PNG figure'lar ve ayri PDF raporu uretildi.
* Bir sonraki net adim: Gerekirse repo baglantisini dersin Google Sheet teslim listesine eklemek ve son teslim kontrolunu yapmak.

## 1) Proje Amaci ve Kapsam

* Amac: YZM212 laboratuvar odevi cozumlerini duzenli klasorler halinde saklamak ve her laboratuvar icin calisir kod/dokumantasyon sunmak.
* Kapsam ici: Notebook, README, gorseller, gereksinim dosyalari ve odev ciktlari.
* Kapsam disi: Ders disi deneyler, gereksiz gecici dosyalar ve ilgisiz global konfigurasyonlar.

## 2) Non-negotiables / Kirmizi Cizgiler

* Notebook calisir olmali.
* README problem tanimi, veri, yontem, sonuc ve yorum kisimlarini acikca icermeli.
* Grafiklerde eksen, baslik ve legend bulunmali.
* Kod ve yorumlar odev talimatlarina uygun olmali.

## 3) Mimari Ozet

* Bilesenler:
* `1.2 MLE Akilli Sehir Planlamasi/`: 2. laboratuvar odevi icin notebook ve dokumantasyon
* `1.3 EigenVectorValues/`: III. laboratuvar odevi icin notebook, manuel ozdeger karsilastirma script'i ve kaynakli rapor
* `1.4 BayesianBrightnessInference/`: 4. laboratuvar odevi icin notebook, MCMC helper module, figure'lar ve PDF raporu
* `README.md`: Repo genelinde laboratuvarlarin ozet listesi
* Veri akisi:
* Notebook, sabit trafik verisini kullanir; analitik ve sayisal MLE hesaplar; gorseller uretir; outlier etkisini raporlar.
* Eigenvalue calismasi, verilen matrisleri once LucasBN karakteristik polinom yaklasimiyla, sonra `numpy.linalg.eig` ile analiz eder; ozdeger farki ve residual normlari raporlar.
* Bayesian parlaklik calismasi, sentetik astronomi verisi uretir; `emcee` ile posterior ornekler; PNG figure'lar ve programatik PDF raporu uretir.
* Onemli dizinler/moduller:
* `1.2 MLE Akilli Sehir Planlamasi/MLE_Akilli_Sehir_Planlamasi.ipynb`
* `1.2 MLE Akilli Sehir Planlamasi/README.md`
* `1.3 EigenVectorValues/EigenVectorValues.ipynb`
* `1.3 EigenVectorValues/eigenvector_values_analysis.py`
* `1.4 BayesianBrightnessInference/Bayesian_Brightness_Inference.ipynb`
* `1.4 BayesianBrightnessInference/bayesian_brightness_analysis.py`
* `1.4 BayesianBrightnessInference/report/generate_report.py`

## 4) Konvansiyonlar ve Standartlar

* Kod stili / lint / format: Aciklayici degisken isimleri, kisa yorumlar ve notebook icinde bolumlere ayrilmis hucreler.
* Branch/commit yaklasimi: Kullanici istedigi zaman anlamli bir commit mesaji ile `main` uzerinden guncelleme.
* Isimlendirme/klasor duzeni: Her laboratuvar ayri klasorde tutulur; PDF'ye bagli ara projeler `1.1`, `1.2`, `1.3`, `1.4` gibi numaralandirilir.

## 5) Kurulum & Calistirma

* Gereksinimler:
* Python 3.11+
* NumPy, SciPy, Matplotlib, Jupyter
* Komutlar:
* `python3.11 -m pip install -r "1.2 MLE Akilli Sehir Planlamasi/requirements.txt"`
* `python3.11 -m jupyter nbconvert --to notebook --execute --inplace "1.2 MLE Akilli Sehir Planlamasi/MLE_Akilli_Sehir_Planlamasi.ipynb"`
* `python3 -m pip install -r Requirements.txt`
* `python3 "1.3 EigenVectorValues/eigenvector_values_analysis.py"`
* `python3 -m jupyter nbconvert --to notebook --execute --inplace "1.4 BayesianBrightnessInference/Bayesian_Brightness_Inference.ipynb"`
* `python3 "1.4 BayesianBrightnessInference/report/generate_report.py"`
* Ortam degiskenleri (sadece ISIMLER):
* Yok
* Lokal gelistirme notlari:
* Notebook calistiktan sonra grafikler `figures/` altina kaydedilir.
* `1.3 EigenVectorValues` altindaki notebook, ayni klasorde bulunan `eigenvector_values_analysis.py` dosyasini import eder.
* `1.4 BayesianBrightnessInference` hem notebook hem PDF raporu icin ayni helper module'u kullanir.

## 6) Decision Log (append-only)

* 2026-03-14 — Karar: 2. laboratuvar odevi icin notebook tabanli bir cozum eklenecek. | Gerekce: PDF talimati Jupyter Notebook'u oneriyor ve hucre bazli ayrim istiyor. | Etki: Cozum `.ipynb` olarak teslim edilmeye uygun hale geldi. | Alternatifler: Tek `.py` dosyasi yazmak.
* 2026-03-14 — Karar: Cekirdek veri icin Poisson MLE analitik ve sayisal olarak ayni notebook'ta gosterilecek, outlier etkisi ayrica gorsellestirilecek. | Gerekce: Odev hem teorik kanit hem sayisal optimizasyon hem de yorum talep ediyor. | Etki: Notebook tek basina raporlanabilir hale geldi. | Alternatifler: Teori ve kodu ayri dosyalara bolmek.
* 2026-03-25 — Karar: III. laboratuvar odevi `1.3 EigenVectorValues` klasoru olarak, notebook + helper script + README uclusuyle sunulacak. | Gerekce: PDF hem rapor hem de 3. soru icin tekrar uygulanabilir kod bekliyor; repo naming'i `1.1` ve `1.2` ile uyumlu tutulmak istendi. | Etki: Eski `3.EigenVectorsValues` klasoru yeni numaralandirmaya tasindi ve kapsam genisletildi. | Alternatifler: Eski klasoru oldugu gibi korumak.
* 2026-03-25 — Karar: Manuel ozdeger hesabinda LucasBN karakteristik polinom yaklasimi baz alinacak, dogrulama ise NumPy `linalg.eig`, ozdeger farki ve residual normlari ile yapilacak. | Gerekce: PDF dogrudan bu depoyu referans veriyor ve resmi NumPy dokumani/kaynak kodu ile karsilastirma istiyor. | Etki: Cozum hem kaynakli hem de olculebilir hale geldi. | Alternatifler: Tamamen yeni bir manuel algoritma yazmak.
* 2026-04-10 — Karar: 4. laboratuvar odevi `1.4 BayesianBrightnessInference` klasoru olarak notebook + helper module + programatik PDF raporu ile sunulacak. | Gerekce: PDF hem notebook hem grafik yorumlariyla birlikte ayri bir PDF artifact'i istiyor. | Etki: Tek kaynaktan hem notebook hem rapor ureten bir akis kuruldu. | Alternatifler: Sadece notebook teslim etmek.
* 2026-04-10 — Karar: PDF'deki sentetik veri uretimi birebir taklit edilerek `np.random.seed(42)` ve `np.random.randn` akisi korunacak. | Gerekce: Farkli RNG uygulamalari farkli ozet istatistikler ureterek rapor tablosunu degistiriyordu. | Etki: Sonuclar PDF'deki beklenen kurgu ile daha uyumlu ve tekrar uretilebilir hale geldi. | Alternatifler: `default_rng` kullanmak.

## 7) Milestones / Donum Noktalari (append-only)

* 2026-03-14 — Milestone: 1.2 MLE klasoru olusturuldu. | Sonuc: Notebook, README ve requirements taslagi eklendi.
* 2026-03-14 — Milestone: Notebook yurutuldu ve sonuclar dogrulandi. | Sonuc: MLE ve outlier etkisi beklenen ciktlari verdi; grafikler olusturuldu.
* 2026-03-25 — Milestone: `1.3 EigenVectorValues` klasoru olusturuldu. | Sonuc: Notebook, helper script, README ve klasor-ici requirements dosyasi eklendi.
* 2026-03-25 — Milestone: NumPy ve LucasBN referansli ozdeger karsilastirmasi dogrulandi. | Sonuc: Script ve notebook hucre kodu calistirildi; ozdegerler sayisal tolerans icinde eslesti.
* 2026-04-10 — Milestone: `1.4 BayesianBrightnessInference` klasoru olusturuldu. | Sonuc: Notebook, helper module, figure'lar ve PDF raporu eklendi.
* 2026-04-10 — Milestone: Bayesian MCMC sonuclari dogrulandi. | Sonuc: Temel posterior tablosu dolduruldu, prior ve veri miktari analizleri tamamlandi.

## 8) Yapilanlar

* [x] PDF talimatlari extract edildi.
* [x] Repo klonlandi.
* [x] `1.2 MLE Akilli Sehir Planlamasi` klasoru olusturuldu.
* [x] Notebook taslagi yazildi.
* [x] Notebook yurutuldu ve sonuc hucreleri kaydedildi.
* [x] `poisson_fit.png` ve `outlier_impact.png` grafikleri uretildi.
* [x] Root README'ye yeni laboratuvar eklendi.
* [x] III. laboratuvar PDF'i sayfa bazli incelendi ve render dogrulamasi yapildi.
* [x] `3.EigenVectorsValues` klasoru `1.3 EigenVectorValues` olarak yeniden yapilandirildi.
* [x] `EigenVectorValues.ipynb`, `eigenvector_values_analysis.py` ve yeni README eklendi.
* [x] Root `Requirements.txt` ve `.gitignore` dosyalari eklendi.
* [x] Notebook JSON dogrulandi ve kod hucreleri calistirildi.
* [x] 4. odev PDF'i extract edildi ve maddeler cikarildi.
* [x] `1.4 BayesianBrightnessInference` klasoru ve dosya iskeleti olusturuldu.
* [x] `emcee`, `corner`, `matplotlib` ve `reportlab` ile MCMC/figure/PDF akisi kuruldu.
* [x] Notebook, PNG figure'lar ve PDF raporu uretildi.

## 9) Yapilacaklar (Next)

* [ ] Gerekirse repo baglantisini teslim listesine ekle.

## 10) Bilinen Sorunlar / Teknik Borc / Riskler

* Push asamasinda git kimligi veya erisim yetkisi sorunu cikabilir.
* Notebook yurutme sirasinda kutuphane uyumsuzlugu yasanirsa requirements genisletilebilir.
* Ilk notebook calistirmasindan kalan hatali ic ice `figures/` klasoru izlenmeyen dosya olarak duruyor; commit asamasinda yalnizca dogru dosyalar stage edilmeli.
* Ozdeger benchmark sureleri milisaniye seviyesinde oldugu icin farkli makinelerde oranlar degisebilir; raporda egilim odakli yorum yapmak daha sagliklidir.
* MCMC sonuc tablosu sabit tohumla tekrar uretilebilir, ancak emcee veya numpy surumu degisirse ufak oynamalar olabilir.
* Dar prior senaryosu bilerek yanli bir posterior uretiyor; README ve raporda bunun bir hata degil deneysel analiz oldugu acik yazilmali.

## 11) Notlar ve Tuzaklar (Pitfalls)

* Aykiri deger analizi raporda yalnizca sayisal degil, sehir planlamasi acisindan da yorumlanmali.
* MLE ile ortalamanin esitligi hem teorik hem sayisal olarak gosterilmeli.
* `1.3 EigenVectorValues` notebook'u ayni klasorden import yaptigi icin notebook baska bir cwd ile kosulursa import yolu ayarlanmalidir.
* Bosluk iceren klasor adlari nedeniyle terminal komutlarinda yolun tirnak icinde verilmesi gerekir.
* `1.4 BayesianBrightnessInference` notebook'u ve rapor script'i ayni helper module'u import eder; yol baglaminin bozulmamasi icin komutlar proje klasoru icinden veya tam path ile verilmelidir.

### Guncelleme Kaydi

* Son guncelleme: 2026-04-10
