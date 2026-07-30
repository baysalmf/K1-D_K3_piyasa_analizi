# ⚡ Zorlu Piyasa Analiz Raporu

EPİAŞ Şeffaflık Platformu üzerinden **K1+D** ve **K3** piyasa verilerini çeken, analiz eden ve raporlayan bir web uygulamasıdır.

---

## 📋 İçindekiler

- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Debug Mode](#debug-mode)
- [Çıktılar](#çıktılar)
- [Proje Yapısı](#proje-yapısı)

---

## ✨ Özellikler

- **K1+D Analizi** — 21 GTŞ için UECM ve EDM dengesizlik oranı hesaplama
- **K3 Analizi** — 21 GTŞ için MAPE hesaplama
- **Excel & CSV dışa aktarım** — Tek tıkla iki sayfalı Excel raporu veya birleşik CSV

---

## 🛠 Kurulum

### Gereksinimler

- Python 3.10+
- EPİAŞ Şeffaflık Platformu hesabı

### Adımlar

```bash
# 1. Depoyu klonlayın
git clone https://github.com/KULLANICI_ADI/zorlu-piyasa-analiz.git
cd zorlu-piyasa-analiz

# 2. Sanal ortam oluşturun (isteğe bağlı ama önerilir)
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Uygulamayı başlatın
streamlit run zorlu_piyasa_analiz_v2.py
```

Uygulama varsayılan olarak `http://localhost:8501` adresinde açılır.

---

## 🚀 Kullanım

1. Sol kenar çubuğundan **EPİAŞ kullanıcı adı** ve **şifrenizi** girin.
2. **Başlangıç** ve **Bitiş** tarihi seçin (varsayılan: bir önceki ay).
3. **Raporu Oluştur** butonuna tıklayın.
4. Uygulama sırasıyla K1+D ve K3 hesaplamalarını yapar; ilerleme çubuklarıyla takip edebilirsiniz.
5. İşlem tamamlandığında sonuçları tablo olarak inceleyin, ardından Excel veya CSV olarak indirin.

> ⚠️ Şifreniz hiçbir zaman kaydedilmez; yalnızca oturum boyunca bellekte tutulur.

---

## Debug Mode

Sol kenar çubuğundaki **Ayarlar** bölümünden **Debug Mode** checkbox'ını işaretleyin.

Aktif olduğunda tüm çıktılar Streamlit arayüzüne değil, uygulamayı başlattığınız **terminale** yazdırılır:

| Bilgi | Format |
|---|---|
| Her API POST isteğinin tam URL ve gövdesi | `[DEBUG] POST -> <url>` |
| Rate limit 429 uyarıları ve bekleme süresi | `[DEBUG] Rate limit (429) - Xs bekleniyor` |
| API yanıtının ilk 2 öğesi | `[DEBUG] Yanit - item sayisi: N, ilk 2: [...]` |
| Her şirket için hesaplanan ara sonuçlar | `[DEBUG] K1/K3 Sonuc — <şirket adı>` |

Debug Mode yalnızca geliştirme ve sorun giderme amaçlıdır; production ortamında kapalı bırakın.

---

## 📊 Çıktılar

### K1+D Tablosu

| Sütun | Açıklama |
|---|---|
| Şirket Adı | Dağıtım şirketi |
| UECM Toplam | Piyasa dengeleme miktarı toplamı (MWh) |
| EDM Toplam | Dengesizlik miktarı toplamı (MWh) |
| % (oran) | EDM / (UECM + EDM) × 100 |

### K3 Tablosu

| Sütun | Açıklama |
|---|---|
| Şirket Adı | Üretim organizasyonu |
| NET Toplam | Piyasalardaki net pozisyon toplamı (MWh) |
| UEVM Gerçek | Santral gerçekleşen üretim toplamı (MWh) |
| WMAPE (%) | Ağırlıklı mutlak yüzde hata |

---

## 📁 Proje Yapısı

```
zorlu-piyasa-analiz/
├── zorlu_piyasa_analiz_v2.py   # Ana uygulama
├── requirements.txt             # Python bağımlılıkları
└── README.md                    # Bu dosya
```

---

## 🔗 Kullanılan API Endpoint'leri

| Endpoint | Açıklama |
|---|---|
| `giris.epias.com.tr/cas/v1/tickets` | CAS TGT kimlik doğrulama |
| `.../markets/dam/data/clearing-quantity` | GÖP alış/satış miktarları |
| `.../markets/idm/data/matching-quantity` | GİP eşleşme miktarları |
| `.../markets/bilateral-contracts/data/...` | İkili anlaşma alış/satış |
| `.../markets/imbalance/data/dsg-imbalance-quantity` | DSG dengesizlik miktarı |
| `.../generation/data/injection-quantity` | UEVM santral üretim verisi |

---

## 📄 Lisans

Bu proje iş kullanım amacıyla geliştirilmiştir.
