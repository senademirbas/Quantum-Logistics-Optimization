## 1. Temel Kavramlar

### 🗺️ TSP (Traveling Salesperson Problem) - "Soru"

Gezgin Satıcı Problemi, bir kuryenin belirli sayıdaki noktayı (şehri) ziyaret edip, başladığı yere en kısa yoldan dönme problemidir.

* **Projedeki Rolü:** Kuantum simülasyonuna verilecek "Girdi" (Input) verisidir.
* **İçerik:** Şehir koordinatları ve şehirler arası mesafe matrisi.

### 🔐 Brute Force (Kaba Kuvvet) - "Cevap Anahtarı"

Olası tüm rotaların tek tek hesaplanıp en kısasının seçildiği yöntemdir.

* **Neden Kullanıyoruz?** Şehir sayısı az olduğunda (), bu yöntem bize %100 kesinlikte **en iyi sonucu (Ground Truth)** verir.
* **Projedeki Rolü:** Kuantum algoritmasının bulduğu sonucun doğruluğunu ölçmek için referans noktasıdır. Kuantum sonucu bu değere ne kadar yakınsa, o kadar başarılıdır.

---

## 2. Kullanılan Dosyalar ve Yapı

Bu süreçte projenin şu dosyaları aktif rol oynar:

* `src/common/tsp_generator.py`: Rastgele harita üreten sınıf.
* `src/common/brute_force_solver.py`: Haritayı çözüp en kısa yolu bulan sınıf.
* `notebooks/01_data_generation.ipynb`: Süreci yöneten ana notebook.
* `data/`: Oluşturulan `.json` veri setlerinin kaydedildiği klasör.

---

## 3. Adım Adım Uygulama (`01_data_generation.ipynb`)

Veri üretmek ve çözümlemek için aşağıdaki adımları takip edin:

1. **Notebook'u Açın:** `notebooks/01_data_generation.ipynb` dosyasını çalıştırın.
2. **Parametreleri Kontrol Edin:**
* `N_VALUES = [5, 6, 7]`: Kaç şehirli haritalar üretileceğini belirler.
* `SEED = 42`: Her çalıştırışta aynı haritaların üretilmesi için sabittir.


3. **Tüm Hücreleri Çalıştırın (Run All):**
* Script önce `TSPGenerator` ile şehirleri saçar.
* Hemen ardından `BruteForceSolver` ile en kısa yolu hesaplar.
* Sonuçları tek bir pakette birleştirir.


4. **Çıktıları İnceleyin:**
* **Veriler:** `data/` klasöründe `tsp_n5.json`, `tsp_n6.json` vb. oluşur.
* **Görseller:** `reports/figures/` klasöründe `tsp_n5_ground_truth.png` vb. oluşur.



---

## 4. Çıktı Dosyası Analizi (`tsp_nX.json`)

Oluşturulan JSON dosyaları iki ana bölümden oluşur: **Soru (Input)** ve **Cevap (Meta)**.

Örnek bir `tsp_n5.json` yapısı ve anlamı:

```json
{
    "meta": {
        // --- CEVAP ANAHTARI (Ground Truth) ---
        // Bu kısım Kuantum algoritmasına verilmez, sadece kontrol için saklanır.
        
        "n_cities": 5,
        "optimal_cost": 227.34,         // Matematiksel olarak mümkün olan en kısa mesafe.
        "optimal_path": [0, 3, 2, 1, 4, 0] // Bu mesafeyi sağlayan mükemmel rota.
    },
    
    "input": {
        // --- SORU (Problem Sahası) ---
        // Kuantum Simülasyonuna beslenecek olan ham veriler.
        
        "coordinates": [                // Şehirlerin (x, y) konumları.
            [37.4, 95.0], 
            [73.1, 59.8], ...
        ],
        "distance_matrix": [            // Şehirler arası mesafeler.
            [0.0, 50.1, ...],
            [50.1, 0.0, ...], ...
        ]
    }
}

```

### Nasıl Okunmalı?

1. **Simülasyon Aşaması:** `input` bloğundaki `distance_matrix` verisini alıp kuantum devresine (QAOA) vereceğiz.
2. **Değerlendirme Aşaması:** Kuantum devresi bize bir rota ve maliyet verecek (Örn: 230.5).
3. **Karşılaştırma:** Kuantumun bulduğu 230.5 değerini, `meta` bloğundaki `optimal_cost` (227.34) ile kıyaslayacağız. Fark ne kadar az ise başarı o kadar yüksektir.

---

## 5. Görsel Çıktı

`reports/figures/` klasöründeki görseller, hesaplanan "En İyi Rota"nın görsel kanıtıdır. Rota çizgileri birbiriyle kesişmemelidir (dış bükey bir rota izler).

---
