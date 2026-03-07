# 1.1 - YZM212 Makine Ogrenmesi Laboratuvar Raporu

## 1. Teorik Temeller

Verilen HMM parametreleri:

- Durumlar: `S = {e, v}`
- Gozlemler: `O = {High, Low}`
- Baslangic: `P(e)=1.0`, `P(v)=0.0`
- Gecisler:
  - `P(e->e)=0.6`, `P(e->v)=0.4`
  - `P(v->e)=0.2`, `P(v->v)=0.8`
- Emisyonlar:
  - `P(High|e)=0.7`, `P(Low|e)=0.3`
  - `P(High|v)=0.1`, `P(Low|v)=0.9`

Gozlem dizisi: `[High, Low]`

### Viterbi Hesabi

Ilk adim:

- `delta1(e) = P(e) * P(High|e) = 1.0 * 0.7 = 0.7`
- `delta1(v) = P(v) * P(High|v) = 0.0 * 0.1 = 0.0`

Ikinci adim:

- `delta2(e) = max(0.7 * 0.6, 0.0 * 0.2) * 0.3 = 0.42 * 0.3 = 0.126`
- `delta2(v) = max(0.7 * 0.4, 0.0 * 0.8) * 0.9 = 0.28 * 0.9 = 0.252`

Sonuc:

- En yuksek olasilik `0.252`
- En olasi fonem dizisi: `e -> v`

## 2. Uygulama

Bu calismada `hmmlearn` kutuphanesinin `CategoricalHMM` sinifi kullanilmistir. Gozlemler `High=0` ve `Low=1` olarak kodlanmistir.

- `EV` icin 2 durumlu HMM
- `OKUL` icin 4 durumlu HMM

Temsili egitim verileri `data/sample_data.json` icinde tutulmustur. Bu veriler, kelimelerin beklenen akustik akislarini basit sekilde temsil eder.

Siniflandirma mantigi:

1. Gozlem dizisini sayisal forma donustur.
2. Diziyi hem `EV` hem `OKUL` modeli ile skorla.
3. Daha yuksek log-likelihood veren modeli sec.

## 3. Analiz ve Yorumlama

### 3.1 Noise etkisi

Ses verisindeki gurultu, dogru fonemin tipik akustik izini bozar. Bunun sonucu olarak:

- dogru duruma ait emisyon olasiligi azalir,
- yanlis duruma ait emisyon olasiligi goreli olarak artar,
- modelin ayirt ediciligi duser.

Bu durum Viterbi yolunu da degistirebilir; yani sistem yanlis fonem dizisini daha olasi gorebilir.

### 3.2 Neden daha karmasik yontemler?

Gercek sistemlerde binlerce kelime, farkli konusmaci profilleri, hiz, vurgu ve ortam gurultusu bulunur. Klasik HMM tabanli sistemler:

- ozellik cikarimina daha cok bagimlidir,
- uzun baglamlari sinirli temsil eder,
- buyuk veri ustunde temsil gucu bakimindan yetersiz kalabilir.

Derin ogrenme tabanli yontemler, ham veya zenginlestirilmis akustik ozelliklerden daha guclu temsiller ogrenebilir ve buyuk kelime dagarciginda daha yuksek basari saglar.
