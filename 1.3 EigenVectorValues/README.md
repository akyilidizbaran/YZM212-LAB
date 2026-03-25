# 1.3 EigenVectorValues

Bu klasor, 2025-2026 Bahar Donemi YZM212 Makine Ogrenmesi dersi III. laboratuvar PDF'inde istenen ozdeger-ozvektor calismasini repo icinde paylasilabilir hale getirir. Teslim, rapor niteligindeki bu `README.md` dosyasini ve 3. soru icin calistirilabilir uygulamayi (`EigenVectorValues.ipynb` + `eigenvector_values_analysis.py`) birlikte sunar.

## Icerik

- `EigenVectorValues.ipynb`: 3. soru icin notebook tabanli tekrar uygulama
- `eigenvector_values_analysis.py`: LucasBN karakteristik polinom yaklasimi ile NumPy karsilastirmasi
- `requirements.txt`: Bu klasor icin gerekli temel kutuphaneler
- `README.md`: PDF sorularina kaynakli cevaplar

## 1. Matris, ozdeger ve ozvektorlerin makine ogrenmesi ile iliskisi

- **Matris:** Veri tablosu, agirlik matrisi, kovaryans matrisi ve lineer donusumlerin standart gosterimidir. Makine ogrenmesi boru hatlarinda ozellikler ve parametreler genellikle matrisler halinde tutulur.
- **Ozdeger:** Bir kare matrisin belirli yonlerde ne kadar olcekleme yaptigini gosteren skaler degerdir. `A v = lambda v` esitligindeki `lambda`, ozdegerdir.
- **Ozvektor:** Matriste uygulanan lineer donusum sonrasi yonunu koruyup yalnizca buyuklugu degisen sifirdan farkli vektordur.

Makine ogrenmesindeki temel kullanim alanlari:

1. **PCA / boyut indirgeme:** `sklearn.decomposition.PCA` dokumani, PCA'nin veriyi daha az boyutlu bir uzaya tasidigi ve bunu ana bilesenler uzerinden yaptigini aciklar. Pratikte bu bilesenler kovaryans yapisinin baskin yonlerini temsil eder ve ozdeger-ozvektor analiziyle dogrudan iliskilidir.
2. **Spektral kumeleme:** scikit-learn clustering dokumani, Spectral Clustering'i duz olmayan geometriye sahip veri yapilarinda faydali bir yontem olarak konumlar. Bu ailede benzerlik/graph yapisindan uretilen matrislerin ozvektorleri kume yapisini ayristirmakta kullanilir.
3. **Genel lineer donusum analizi:** Jason Brownlee'nin ozdeger-ozvektor girisi, eigendecomposition'in bir matrisi daha karmasik islemleri sadeleştirecek bilesenlere ayirdigini ve PCA gibi yontemlerde kullanildigini vurgular.

Bu nedenle ozdegerler "hangi yonlerin baskin oldugunu", ozvektorler ise "bu yonlerin hangileri oldugunu" gosterir. Veri sikistirma, yapisal desen analizi ve lineer cebir tabanli pek cok ML yonteminde bu ikili birlikte kullanilir.

## 2. NumPy `linalg.eig` fonksiyonu nasil calisir?

NumPy dokumanina gore `numpy.linalg.eig(a)`:

- kare bir matrisin **ozdegerlerini** ve **sag (right) ozvektorlerini** hesaplar,
- ozvektorleri sutun bazli dondurur; yani `eigenvectors[:, i]`, `eigenvalues[i]` degerine karsilik gelir,
- gerekirse kompleks sayi dondurebilir,
- sayisal hesaplamayi LAPACK'in `_geev` rutinleri uzerinden yapar.

Kaynak kodu incelendiginde `numpy/linalg/_linalg.py` icinde `eig` fonksiyonunun girisi once kare matris dogrulamasindan gecer, sonra uygun veri tipine gore `_umath_linalg.eig(...)` cagirilir. Resmi dokuman ayrica `a @ eigenvectors[:, i] = eigenvalues[i] * eigenvectors[:, i]` iliskisini acikca verir ve simetrik/Hermitian yapilar icin `eig` yerine `eigh` kullanmanin daha uygun oldugunu belirtir.

Ozetle:

1. Girdi `(..., M, M)` seklinde kare matris yiginlari olabilir.
2. Sayisal rutin, ozdeger ve sag ozvektorleri uretir.
3. Sonuc `ndarray` olarak geri doner.
4. Sonuclar teorik esitligi sayisal tolerans dahilinde saglar; bu nedenle kalan hata normu (`||Av - lambda v||`) cok kucuk olur.

## 3. LucasBN referans deposunun tekrar uygulanmasi ve NumPy karsilastirmasi

PDF'nin 3. sorusu icin [LucasBN/Eigenvalues-and-Eigenvectors](https://github.com/LucasBN/Eigenvalues-and-Eigenvectors) deposundaki fikir yeniden uygulandi. Kullanilan cekirdek mantik:

1. Matrisin karakteristik matrisi `A - lambda I` olusturulur.
2. Laplace acilimi ile determinant polinomu recursive sekilde hesaplanir.
3. Polinom kokleri `numpy.roots` ile bulunur ve manuel ozdegerler elde edilir.
4. Ayni matrisler icin `numpy.linalg.eig` calistirilir.
5. Elde edilen ozdegerler tolerans dahilinde karsilastirilir, ayrica NumPy'nin verdigi ozvektorler icin `Av - lambda v` artik normu kontrol edilir.

Uygulama dosyasi: `eigenvector_values_analysis.py`

### Ornek sonuc ozeti

Bu makinede alinan ornek benchmark sonucunda:

- 3x3 referans matriste manuel ve NumPy ozdegerleri `[3.000000, 5.000000, 7.000000]` olarak ayni cikti.
- 4x4 ornek matriste iki kompleks eslenik kok de dahil olmak uzere sonuclar sayisal tolerans icinde eslesti.
- 5x5 yogun matriste de maksimum mutlak fark `5.684e-14` seviyesinde kaldi.
- Ortalama sure karsilastirmasinda manuel yontem tum testlerde daha yavas kaldi. Ornek calismalarda 3x3 icin yaklasik `2-3x`, 4x4 icin `6-8x`, 5x5 icin ise cift haneli katsayilara kadar daha yavas oldugu goruldu. Milisaniye seviyesindeki sureler donanima ve tekrar sayisina gore degisebilir.

Bu sonuclar iki seyi gosteriyor:

1. Karakteristik polinom yaklasimi egitsel olarak dogrudur ve manuel mantigi aciklar.
2. Uretim kullanimi icin `numpy.linalg.eig`, hem daha hizli hem de dogrudan ozvektor dondurdugu icin daha pratiktir.

## Sonuc

III. laboratuvar PDF'inde istenen uc gorev bu klasorde birlikte karsilanmistir:

1. Matris, ozdeger ve ozvektorlerin makine ogrenmesindeki rolu aciklandi.
2. `numpy.linalg.eig` fonksiyonu resmi dokuman ve kaynak kod uzerinden ozetlendi.
3. LucasBN referansi tekrar uygulanarak ayni fikir NumPy ile karsilastirildi.

Kisaca, manuel cozum kavramsal anlayis icin faydali; ancak dogruluk, hiz ve hazir ozvektor uretimi nedeniyle pratikte tercih edilmesi gereken yontem NumPy'nin LAPACK tabanli `eig` fonksiyonudur.

## Kaynaklar

- NumPy `eig` dokumani: [numpy.org/doc/2.1/reference/generated/numpy.linalg.eig.html](https://numpy.org/doc/2.1/reference/generated/numpy.linalg.eig.html)
- NumPy kaynak kodu: [github.com/numpy/numpy/blob/v2.1.3/numpy/linalg/_linalg.py](https://github.com/numpy/numpy/blob/v2.1.3/numpy/linalg/_linalg.py)
- LucasBN referans deposu: [github.com/LucasBN/Eigenvalues-and-Eigenvectors](https://github.com/LucasBN/Eigenvalues-and-Eigenvectors)
- Machine Learning Mastery ozdeger/ozvektor yazisi: [machinelearningmastery.com/introduction-to-eigendecomposition-eigenvalues-and-eigenvectors](https://machinelearningmastery.com/introduction-to-eigendecomposition-eigenvalues-and-eigenvectors/)
- scikit-learn PCA dokumani: [scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
- scikit-learn clustering dokumani: [scikit-learn.org/stable/modules/clustering.html#spectral-clustering](https://scikit-learn.org/stable/modules/clustering.html#spectral-clustering)
