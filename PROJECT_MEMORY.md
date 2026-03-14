# PROJECT_MEMORY

## 0) TL;DR (En guncel durum)

* Su an YZM212-LAB deposuna 2. laboratuvar icin MLE tabanli akilli sehir planlamasi notebook'u ekleniyor.
* Son degisiklik: Notebook calistirildi; analitik ve sayisal MLE degeri `12.142857` olarak dogrulandi, outlier sonrasi MLE `24.666667` seviyesine cikti ve grafikler uretildi.
* Bir sonraki net adim: Degisiklikleri commit edip GitHub'a pushlamak.

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
* `README.md`: Repo genelinde laboratuvarlarin ozet listesi
* Veri akisi:
* Notebook, sabit trafik verisini kullanir; analitik ve sayisal MLE hesaplar; gorseller uretir; outlier etkisini raporlar.
* Onemli dizinler/moduller:
* `1.2 MLE Akilli Sehir Planlamasi/MLE_Akilli_Sehir_Planlamasi.ipynb`
* `1.2 MLE Akilli Sehir Planlamasi/README.md`

## 4) Konvansiyonlar ve Standartlar

* Kod stili / lint / format: Aciklayici degisken isimleri, yorum satirlari ve notebook icinde bolumlere ayrilmis hucreler.
* Branch/commit yaklasimi: Kullanici istedigi zaman anlamli bir commit mesaji ile `main` uzerinden guncelleme.
* Isimlendirme/klasor duzeni: Her laboratuvar ayri klasorde tutulur.

## 5) Kurulum & Calistirma

* Gereksinimler:
* Python 3.11+
* NumPy, SciPy, Matplotlib, Jupyter
* Komutlar:
* `python3.11 -m pip install -r "1.2 MLE Akilli Sehir Planlamasi/requirements.txt"`
* `python3.11 -m jupyter nbconvert --to notebook --execute --inplace "1.2 MLE Akilli Sehir Planlamasi/MLE_Akilli_Sehir_Planlamasi.ipynb"`
* Ortam degiskenleri (sadece ISIMLER):
* Yok
* Lokal gelistirme notlari:
* Notebook calistiktan sonra grafikler `figures/` altina kaydedilir.

## 6) Decision Log (append-only)

* 2026-03-14 — Karar: 2. laboratuvar odevi icin notebook tabanli bir cozum eklenecek. | Gerekce: PDF talimati Jupyter Notebook'u oneriyor ve hucre bazli ayrim istiyor. | Etki: Cozum `.ipynb` olarak teslim edilmeye uygun hale geldi. | Alternatifler: Tek `.py` dosyasi yazmak.
* 2026-03-14 — Karar: Cekirdek veri icin Poisson MLE analitik ve sayisal olarak ayni notebook'ta gosterilecek, outlier etkisi ayrica gorsellestirilecek. | Gerekce: Odev hem teorik kanit hem sayisal optimizasyon hem de yorum talep ediyor. | Etki: Notebook tek basina raporlanabilir hale geldi. | Alternatifler: Teori ve kodu ayri dosyalara bolmek.

## 7) Milestones / Donum Noktalari (append-only)

* 2026-03-14 — Milestone: 1.2 MLE klasoru olusturuldu. | Sonuc: Notebook, README ve requirements taslagi eklendi.
* 2026-03-14 — Milestone: Notebook yurutuldu ve sonuclar dogrulandi. | Sonuc: MLE ve outlier etkisi beklenen ciktlari verdi; grafikler olusturuldu.

## 8) Yapilanlar

* [x] PDF talimatlari extract edildi.
* [x] Repo klonlandi.
* [x] `1.2 MLE Akilli Sehir Planlamasi` klasoru olusturuldu.
* [x] Notebook taslagi yazildi.
* [x] Notebook yurutuldu ve sonuc hucreleri kaydedildi.
* [x] `poisson_fit.png` ve `outlier_impact.png` grafikleri uretildi.
* [x] Root README'ye yeni laboratuvar eklendi.

## 9) Yapilacaklar (Next)

* [ ] Commit ve push yap.

## 10) Bilinen Sorunlar / Teknik Borc / Riskler

* Push asamasinda git kimligi veya erisim yetkisi sorunu cikabilir.
* Notebook yurutme sirasinda kutuphane uyumsuzlugu yasanirsa requirements genisletilebilir.
* Ilk notebook calistirmasindan kalan hatali ic ice `figures/` klasoru izlenmeyen dosya olarak duruyor; commit asamasinda yalnizca dogru dosyalar stage edilmeli.

## 11) Notlar ve Tuzaklar (Pitfalls)

* Aykiri deger analizi raporda yalnizca sayisal degil, sehir planlamasi acisindan da yorumlanmali.
* MLE ile ortalamanin esitligi hem teorik hem sayisal olarak gosterilmeli.

### Guncelleme Kaydi

* Son guncelleme: 2026-03-14
