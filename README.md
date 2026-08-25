## Proje Mimarisi ve Dosya Sorumlulukları

```text
vehicle-statement/
├── src/
│   └── vehicle_simulator/
│       ├── __init__.py          # Paketi dışa aktarır ve modülleri erişilebilir kılar.
│       ├── constants.py         # Sinyal sınırları, eşik değerleri ve sabit tanımları tutar.
│       ├── exceptions.py        # Projeye özel hata sınıflarını (Custom Exceptions) barındırır.
│       ├── validation.py        # Gelen sinyal verilerinin geçerliliğini denetleyen kuralları içerir.
│       └── vehicle_state.py     # Aracın anlık durumunu temsil eden veri modelini yönetir.
├── tests/
│   └── test_vehicle_state.py    # Araç modeli ve validasyon kurallarının birim testlerini içerir.
├── requirements-dev.txt         # Geliştirme ve test araçlarını (pytest vb.) tanımlar.
├── .gitignore                   # Takip edilmeyecek dosya ve klasörleri (.venv vb.) filtreler.
└── README.md                    # Kurulum, test ve mimari dokümantasyonunu içerir.
```