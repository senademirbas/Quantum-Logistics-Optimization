# Proje Genel Bakış
[Türkçe] | [English](project_overview_en.md)
<!-- Bu dosya Antigravity'nin her oturumda projeyi anlaması için okunur -->

## Kimlik

- **Başvuru Sahibi:** Zeliha Baysan
- **Danışman:** Dr. Öğr. Üyesi Ensar Arif Sağbaş
- **Kurum:** Muğla Sıtkı Koçman Üniversitesi
- **Fon:** TÜBİTAK 2209-A

## Proje Başlığı

> Yapay zekâ destekli kuantum-hibrit lojistik optimizasyonu: QAOA simülasyon ve klasik yöntemlerin karşılaştırmalı analizi

## Problem

**Gezgin Satıcı Problemi (TSP)** — NP-zor, lojistik optimizasyonunun temel problemi.
Şehir sayısı: **N = 5, 6, 7** (sentetik, rasgele koordinatlar, Öklid mesafesi)

## Çift Planlı Yapı (Go/No-Go)

### Plan A — Kuantum-Hibrit (Birincil Hedef)
> Ay 4'te QAOA prototipi başarılı → Go kararı alınırsa aktif

| Model | Açıklama | Durum |
|-------|----------|-------|
| **GA-QAOA** | QAOA'nın β/γ parametrelerini GA ile optimize eden özgün hibrit model | ⬜ Yapılmadı |
| **Standart QAOA** | SPSA veya COBYLA optimizörlü kıyaslama modeli | ⬜ Yapılmadı |
| **GA** | Saf Genetik Algoritma | ✅ Tamamlandı |
| **SA** | Saf Simulated Annealing | ✅ Tamamlandı |

### Plan B — Kapsamlı Klasik Karşılaştırma (Yedek)
> Ay 4'te QAOA prototipi başarısız → No-Go kararı alınırsa aktif

| Model | Açıklama | Durum |
|-------|----------|-------|
| **GA** | Genetik Algoritma (hiper-parametre optimizasyonu yapılacak) | ✅ Temel Tamamlandı |
| **SA** | Simulated Annealing (hiper-parametre optimizasyonu yapılacak) | ✅ Temel Tamamlandı |
| **OR-Tools** | Google OR-Tools — endüstri standardı, deterministik | ✅ Tamamlandı |

> ⚠️ Plan B'de GA ve SA'nın **hiper-parametre optimizasyonu** yapılması bekleniyor (spec gereği). Mevcut parametreler varsayılan, optimize edilmemiş.

**Mevcut durum:** Hedef 1 tamamlandı ✅ — Go/No-Go kararı için **Hedef 2** bekleniyor (QAOA prototipi).

## Zaman Takvimi

| Dönem | Aşama | İçerik |
|-------|-------|--------|
| Ay 1-3 | Paralel Geliştirme | Klasik: GA + SA kodlama / Kuantum: QUBO + QAOA prototipi |
| **Ay 3 sonu – Ay 4 ilk yarı** | **Go/No-Go Kararı** | QAOA prototipi değerlendirme → Plan A mı B mi? |
| Ay 5-8 | Algoritmik Geliştirme | Plan A: GA-QAOA + Standart QAOA / Plan B: OR-Tools + hiper-param |
| Ay 9-10 | Veri Toplama | Tüm modeller × TSP setleri × 30 bağımsız çalıştırma |
| Ay 11-12 | Analiz & Raporlama | ANOVA, box plot, yakınsama grafikleri, rapor |

## Araştırma Soruları & Hipotezler

**H1 (Plan A):** GA'nın global arama yeteneği, QAOA'nın β/γ parametrelerini SPSA/COBYLA'ya göre daha verimli optimize eder → GA-QAOA, Standart QAOA'dan daha yüksek kalite ve düşük varyanslı sonuç üretir.

**H2 (Plan B):** GA popülasyon tabanlı arama sayesinde SA'dan daha iyi çözümler bulur; OR-Tools deterministik olduğu için hızlıdır ama GA küçük N'lerde (5-7) rekabetçi kalır.

## Performans Metrikleri

| Metrik | Ölçüm |
|--------|-------|
| Çözüm Kalitesi | Optimaliteye Yakınlık % = `(bulunan - optimal) / optimal * 100` |
| Çözüm İstikrarı | 30 bağımsız denemenin **varyansı** |
| Hesaplama Süresi | Milisaniye hassasiyetinde, saniye cinsinden float |

- Her algoritma × problem boyutu kombinasyonu: **30 bağımsız çalıştırma**
- Optimal referans: **Brute Force** (N=5,6,7 için uygulanabilir)

## Analiz Yöntemleri

- **ANOVA** (Tek Yönlü Varyans Analizi) — `scipy.stats.f_oneway`
- **Kutu grafikleri (box plot)** — performans dağılımı / istikrar
- **Yakınsama grafikleri** — nesil/iterasyon başına best_cost değişimi

## Anahtar Kelimeler

Kuantum Hesaplama, QAOA, QUBO, Hibrit Optimizasyon, Genetik Algoritma, Simulated Annealing, Gezgin Satıcı Problemi, OR-Tools, NISQ

## Literatür Referansları (Spec'te Geçenler)

- Lucas (2014) — TSP → QUBO formülasyonu
- Salehi, Glos ve Miszczak (2022) — QUBO dönüşümü
- Blekos vd. (2024) — QAOA parametre optimizasyonu, NISQ
- Preskill (2018) — NISQ dönemi
- Lo ve Shih (2021) — GA güçlü global arama
- Pihkakoski vd. (2025) — hibrit kuantum-klasik pratik değeri
- Padmasola vd. (2024) — hibrit iş akışları
- Fitzek vd. (2024) — QAOA araç rotalama
