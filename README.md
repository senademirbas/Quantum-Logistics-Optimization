# Quantum-Logistics-Optimization

# ⚛️ Yapay Zekâ Destekli Kuantum-Hibrit Lojistik Optimizasyonu

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)
![Qiskit](https://img.shields.io/badge/Quantum-Qiskit-purple?style=flat&logo=qiskit)
![OR-Tools](https://img.shields.io/badge/Solver-OR--Tools-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Hedef_1_Tamamlandı-brightgreen)

> **TÜBİTAK 2209-A Lisans Araştırma Projesi**  
> Muğla Sıtkı Koçman Üniversitesi  
> **Danışman:** Dr. Öğr. Üyesi Ensar Arif Sağbaş

---

## 📋 Proje Özeti

Bu proje, lojistik sektörünün temel NP-zor problemi olan **Gezgin Satıcı Problemi (TSP)** için yenilikçi bir hibrit çözüm geliştirmeyi amaçlamaktadır. Projenin özgün katkısı, **QAOA'nın β ve γ parametrelerini Genetik Algoritma** ile optimize eden bir **GA-QAOA hibrit modeli** önermesidir.

Proje, kuantum fizibilitesine bağlı **çift planlı** bir yapıya sahiptir: 
- **Plan A (Kuantum-Hibrit):** GA-QAOA modeli geliştirip Standart QAOA ve klasik yöntemlerle karşılaştırma
- **Plan B (Klasik):** GA, SA ve OR-Tools'un derinlemesine karşılaştırmalı analizi

---

## 📁 Proje Yapısı

```text
Quantum-Logistics-Optimization/
│
├── data/
│   ├── raw/                        ← TSP problem girdileri (seed=2026)
│   │   ├── tsp_n5.json
│   │   ├── tsp_n6.json
│   │   └── tsp_n7.json
│   │
│   ├── ground_truth/               ← Brute Force optimal çözümler (referans)
│   │   ├── tsp_n5_solution.json
│   │   ├── tsp_n6_solution.json
│   │   └── tsp_n7_solution.json
│   │
│   └── results/
│       ├── classical/
│       │   ├── ga/                 ← GA çıktıları
│       │   ├── sa/                 ← SA çıktıları
│       │   └── ortools/            ← OR-Tools çıktıları
│       └── quantum/                ← Plan A (gelecekte kullanılacak)
│           ├── qaoa_standard/
│           └── ga_qaoa/
│
├── src/
│   ├── common/
│   │   ├── utils.py                ← Path yardımcıları + veri yükleme
│   │   ├── tsp_generator.py        ← Sentetik TSP üreteci
│   │   └── brute_force_solver.py   ← Optimal çözüm üreteci (ground truth)
│   │
│   ├── classical/
│   │   ├── genetic_algo.py         ← ✅ Genetik Algoritma (OX crossover, tournament)
│   │   ├── sim_annealing.py        ← ✅ Simulated Annealing (2-opt, Metropolis)
│   │   └── or_tools_solver.py      ← ✅ Google OR-Tools (PATH_CHEAPEST_ARC)
│   │
│   └── quantum/                    ← ⏳ Plan A — Geliştirme bekliyor
│       ├── qubo_converter.py
│       ├── qaoa_standard.py
│       └── hybrid_ga_qaoa.py
│
├── notebooks/                      ← Jupyter deneyleri
├── reports/figures/                ← Box plot ve yakınsama grafikleri
├── .agent/memory/                  ← Proje belleği (geliştirici referansı)
├── requirements.txt
└── README.md
```

---

## 🚀 Kurulum

### 1. Repoyu Klonla
```bash
git clone https://github.com/senademirbas/Quantum-Logistics-Optimization.git
cd Quantum-Logistics-Optimization
```

### 2. Sanal Ortam Oluştur
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

> ⚠️ Python 3.12 kullanıyorsanız `ortools==9.11.4210` sürümü gereklidir.

---

## ▶️ Kullanım

### Adım 1 — TSP Verisi Üret
```bash
python src/common/tsp_generator.py
# Çıktı: data/raw/tsp_n{5,6,7}.json
```

### Adım 2 — Optimal Çözüm Üret (Ground Truth)
```bash
python src/common/brute_force_solver.py
# Çıktı: data/ground_truth/tsp_n{5,6,7}_solution.json
```

### Adım 3 — Klasik Algoritmaları Çalıştır
```bash
python src/classical/genetic_algo.py
# → data/results/classical/ga/tsp_n{N}_ga_solution.json

python src/classical/sim_annealing.py
# → data/results/classical/sa/tsp_n{N}_sa_solution.json

python src/classical/or_tools_solver.py
# → data/results/classical/ortools/tsp_n{N}_ortools_solution.json
```

---

## 📊 Metodoloji

### Araştırma Soruları

**Plan A (Kuantum odaklı):** GA-QAOA modeli, Standart QAOA ve klasik yöntemlere göre çözüm kalitesi ve istikrar açısından nasıl bir performans sergiler?

**Plan B (Klasik odaklı):** GA, SA ve OR-Tools; N=5, 6, 7 şehirli TSP'de çözüm kalitesi ve hız açısından nasıl karşılaştırılır?

### Performans Metrikleri
| Metrik | Açıklama |
|--------|----------|
| **Çözüm Kalitesi** | Optimaliteye yakınlık (%) |
| **Çözüm İstikrarı** | 30 bağımsız çalıştırmanın varyansı |
| **Hesaplama Süresi** | Saniye (milisaniye hassasiyeti) |

### Analiz Yöntemi
- **ANOVA** ile algoritmalar arası fark anlamlılık testi
- **Box plot** ile performans dağılımı görselleştirme
- **Yakınsama grafikleri** ile optimizasyon süreci analizi

---

## 📅 Proje Durumu

| Hedef | Açıklama | Durum |
|-------|----------|-------|
| Hedef 1 | Klasik algoritmaların temel implementasyonu | ✅ Tamamlandı |
| Hedef 2 | Go/No-Go karar aşaması (QAOA prototipi) | ⏳ Bekliyor |
| Hedef 3 | Seçilen plana göre geliştirme (A veya B) | ⏳ |
| Hedef 4 | 30 bağımsız çalıştırma benchmark'ı | ⏳ |
| Hedef 5 | ANOVA analizi + görselleştirme + rapor | ⏳ |

---

## 👥 Ekip

**Araştırmacılar:**
- Zeliha Baysan
- Şehri Sena Demirbaş
- Yaren Kaya

**Danışman:**
- Dr. Öğr. Üyesi Ensar Arif Sağbaş — Muğla Sıtkı Koçman Üniversitesi

---

## 📚 Anahtar Referanslar

- Blekos et al. (2024) — QAOA parametreleri ve sınırlamaları
- Lucas (2014) — TSP → QUBO formülasyonu
- Preskill (2018) — NISQ dönemi
- Pihkakoski et al. (2025) — Hibrit kuantum-klasik iş akışları
- Lo & Shih (2021) — GA ile karmaşık optimizasyon
