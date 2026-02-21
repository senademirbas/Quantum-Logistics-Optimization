# Proje Genel Bakış
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
> Ay 4'te Kuantum Ekibi prototipi başarılıysa aktif olur

| Model | Açıklama | Durum |
|-------|----------|-------|
| **GA-QAOA** | QAOA parametrelerini GA ile optimize eden özgün hibrit model | ⬜ Yapılmadı |
| **Standart QAOA** | SPSA/COBYLA optimizörlü kıyaslama modeli | ⬜ Yapılmadı |
| **GA** | Saf Genetik Algoritma | ✅ Tamamlandı |
| **SA** | Saf Simulated Annealing | ✅ Tamamlandı |

### Plan B — Kapsamlı Klasik Karşılaştırma (Yedek)
> QAOA prototipi başarısız olursa aktif olur

| Model | Açıklama | Durum |
|-------|----------|-------|
| **GA** | Genetik Algoritma | ✅ Tamamlandı |
| **SA** | Simulated Annealing | ✅ Tamamlandı |
| **OR-Tools** | Google OR-Tools (endüstri standardı) | ✅ Tamamlandı |

**Mevcut durum:** Plan A/B henüz karar verilmedi → Go/No-Go aşamasındayız.

## Araştırma Soruları & Hipotezler

**H1 (Plan A):** GA'nın global arama yeteneği QAOA parametrelerini SPSA/COBYLA'ya göre daha verimli optimize eder → GA-QAOA, Standart QAOA'dan daha yüksek kalite ve düşük varyanslı sonuç üretir.

**H2 (Plan B):** GA popülasyon tabanlı arama sayesinde SA'dan iyi çözümler bulur; OR-Tools deterministik olduğu için daha hızlıdır ama GA küçük N'lerde (5-7) rekabetçi kalır.

## Performans Metrikleri

| Metrik | Açıklama |
|--------|----------|
| Çözüm Kalitesi | Optimaliteye Yakınlık % = `(bulunan - optimal) / optimal * 100` |
| Çözüm İstikrarı | 30 bağımsız denemenin varyansı |
| Hesaplama Süresi | Milisaniye hassasiyetinde saniye cinsinden |

Her algoritma × problem boyutu kombinasyonu: **30 bağımsız çalıştırma**

## Analiz Yöntemleri

- **ANOVA** (Tek Yönlü Varyans Analizi) — çözüm kaliteleri arasındaki fark anlamlı mı?
- **Kutu grafikleri (box plot)** — performans dağılımı / istikrar
- **Yakınsama grafikleri** — algoritmaların yakınsama süreci

## Anahtar Kelimeler

Kuantum Hesaplama, QAOA, QUBO, Hibrit Optimizasyon, Genetik Algoritma, Simulated Annealing, Gezgin Satıcı Problemi, OR-Tools, NISQ
