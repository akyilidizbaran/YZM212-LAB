# 1.1 HMM Speech Recognition

Bu depo, YZM212 Makine Ogrenmesi dersi birinci laboratuvar odevinin cozumunu icerir. Gorev, HMM ile izole kelime tanima mantigini gostermek ve iki farkli kelime icin basit bir siniflandirici kurmaktir.

## Problem Tanimi

Odev iki bolumden olusur:

1. `EV` kelimesi icin verilen HMM parametreleriyle `[High, Low]` gozlem dizisinde Viterbi algoritmasini adim adim uygulamak.
2. Python ve `hmmlearn` kullanarak `EV` ve `OKUL` kelimeleri icin iki farkli HMM modeli kurup, yeni bir gozlem dizisini daha yuksek log-likelihood veren modele atamak.

## Dizin Yapisi

```text
data/
src/
report/
requirements.txt
README.md
```

## Veri

`data/sample_data.json` dosyasinda:

- `High` ve `Low` gozlemlerinin sayisal eslemesi,
- `EV` ve `OKUL` icin temsili egitim dizileri,
- ornek test dizileri

yer alir.

## Yontem

- Ayrik gozlemler icin `hmmlearn.hmm.CategoricalHMM` kullanildi.
- `EV` modeli 2 gizli durum (`e`, `v`) ile tanimlandi.
- `OKUL` modeli 4 gizli durum (`o`, `k`, `u`, `l`) ile tanimlandi.
- Siniflandirma, ayni gozlem dizisinin her iki model altindaki `score()` sonucunu karsilastirarak yapilir.

## Sonuclar

Teorik bolumde `[High, Low]` gozlem dizisi icin Viterbi sonucu:

- En olasi yol: `e -> v`
- Nihai olasilik: `0.252`

Kod tarafinda ornek test dizileri icin `EV` benzeri kisa diziler `EV`, `OKUL` benzeri uzun ve degisen diziler `OKUL` olarak etiketlenir.

## Yorum / Tartisma

- Gurultu, emisyon olasiliklarini dagitarak dogru durum ile yanlis durum arasindaki ayrimi azaltir.
- Kelime sayisi buyudukce HMM tabanli ayrik modelleme hem temsil gucu hem de olceklenebilirlik acisindan zorlanir.
- Derin ogrenme tabanli sistemler, daha zengin ozellik ogrenimi ve uzun baglam modellemesi sundugu icin gercek sistemlerde daha yaygindir.

## Calistirma

```bash
python -m pip install -r requirements.txt
python src/recognizer.py
python src/generate_report.py
```

## Cikti

- Kaynak kod: `src/recognizer.py`
- Rapor PDF: `report/cozum_anahtari.pdf`
