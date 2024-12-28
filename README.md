# Kitap Kapaklarının Görsel Sınıflandırması - Yapay Zeka Modelleri ile

Bu proje, kitap kapak görsellerini farklı kategorilere ayırmak için web kazıma (web scraping), veri ön işleme, veri artırma ve yapay zeka model eğitimi süreçlerini kapsar. DeiT, BEiT, Swin Transformer, ViT ve EfficientNet modelleri kullanılarak görsel sınıflandırma performansı değerlendirilmiştir. Çalışma, kitap kapaklarının doğru bir şekilde sınıflandırılması için kapsamlı bir veri hazırlama ve modelleme sürecini içerir.

---

## 📖 Proje Hedefi
Kitap kapaklarını, kişisel gelişim, çocuk kitapları, tarih, çizgi roman ve polisiye gibi kategorilere ayırmak için verimli ve doğru çalışan bir yapay zeka sistemi geliştirmek. Projede şu hedefler gerçekleştirilmiştir:
- İnternet sitelerinden kitap kapak görsellerinin otomatik olarak toplanması.
- Toplanan görsellerin kalite kontrolü ve işlenmesi.
- Veri setinin veri artırma teknikleriyle genişletilmesi.
- Transformer tabanlı ve CNN tabanlı modellerle sınıflandırma performansının karşılaştırılması.
- Model sonuçlarının analiz edilerek en iyi modeli belirlemek.

---

## 🛠️ Kullanılan Yöntemler ve Teknolojiler
### 1. **Veri Toplama**
- **Web Scraping**: Python `Selenium` ve `Requests` kütüphaneleri kullanılarak D&R ve Pandora gibi web sitelerinden kitap kapak görselleri toplanmıştır.
- **Kaydetme Süreci**: Her kategoriye ait görseller, kategori isimlerine göre ayrılarak ilgili dizinlerde saklanmıştır.
- **Zorluklar**: İnternet bağlantı kesintileri, site engellemeleri ve veri çekim hatalarıyla başa çıkmak için tekrar eden işlemler optimize edilmiştir.

### 2. **Veri Eleme**
- **Perceptual Hashing (phash)**: Görsellerin tekrarlayan versiyonları, `imagehash` kütüphanesi kullanılarak tespit edilmiş ve klasörlere taşınmıştır.
- **Manuel Eleme**: Piksel bozulmaları olan ve kategoriyle uyumsuz görseller elenmiştir.

### 3. **Veri Artırma**
- **Parlaklık ve Kontrast Değişikliği**: Görsellerin parlaklık ve kontrast değerleri rastgele değiştirilmiştir.
- **Döndürme İşlemleri**: Görseller, sabit ve rastgele açılarla döndürülerek farklı varyantlar oluşturulmuştur.

### 4. **Model Eğitimi**
- **Kullanılan Modeller**:
  - DeiT
  - BEiT
  - Swin Transformer
  - ViT
  - EfficientNet
- **Veri Hazırlığı**: Görseller, modellerin gereksinimlerine uygun şekilde normalize edilerek boyutlandırılmıştır.
- **Eğitim Süreci**: Google Colab üzerinde GPU kullanılarak eğitim gerçekleştirilmiştir. Early stopping tekniğiyle aşırı öğrenme önlenmiştir.
- **Performans Değerlendirme**: Doğruluk (Accuracy), F1-Skor, Duyarlılık (Sensitivity) ve Özgüllük (Specificity) gibi metrikler hesaplanmıştır.

---

## 🔑 Elde Edilen Sonuçlar
- **En İyi Model**: 
  - **Swin Transformer**: %98.54 doğruluk oranıyla en iyi sonucu vermiştir.
- **Diğer Modellerin Performansı**:
  - DeiT: %96.8 doğruluk
  - BEiT: %97.0 doğruluk
  - EfficientNet: %96.0 doğruluk
  - ViT: %96.35 doğruluk

| Model            | Doğruluk (%) | Precision (%) | Recall (%) | F1-Skor (%) | Sensitivity (%) | Specificity (%) |
|-------------------|--------------|---------------|------------|-------------|------------------|------------------|
| DeiT             | 96.8         | 96.7          | 96.6       | 96.7        | 98.6            | 99.1            |
| BEiT             | 97.0         | 97.0          | 97.0       | 97.0        | 99.0            | 98.6            |
| EfficientNet     | 96.0         | 96.0          | 96.0       | 96.0        | 97.9            | 98.5            |
| ViT              | 96.35        | 96.41         | 96.35      | 96.37       | 98.98           | 98.52           |
| Swin Transformer | 98.54        | 98.54         | 98.54      | 98.54       | 98.91           | 99.30           |


## Geliştirme Ortamı
- **Python Sürümü:** Python 3.8 veya üzeri
- **Gerekli Kütüphaneler:**
  - `selenium` (Web scraping işlemleri için)
  - `Pillow` (Görsel işleme işlemleri için)
  - `requests` (HTTP isteklerini yönetmek için)
  - `imagehash` (Tekrarlayan görselleri tespit etmek için)
  - `shutil` (Dosya taşıma işlemleri için)
  - `random` ve `os` (Dosya ve klasör işlemleri için)
  - `io.BytesIO` (İndirilen görüntü verilerini bellekten okumak ve işlemek için)
- **Tarayıcı ve Web Driver:** Google Chrome ve chromedriver (selenium ile birlikte)

## Projenin Yüklenmesi
1. **Gerekli Bağımlılıkların Yüklenmesi**  
   Projeyi çalıştırmadan önce gerekli Python kütüphanelerinin yüklenmesi gereklidir.
2. **ChromeDriver'ın Kurulumu**  
   Google Chrome'un versiyonuna uygun chromedriver indirilip PATH değişkenine eklenmelidir.

## Projenin Çalıştırılması
Bu projede üç ana Python dosyası bulunmaktadır:
1. **Web Scraping ve Görsel İndirme**  
   Bu dosya, `selenium` ve `requests` kütüphanelerini kullanarak belirli kategorilere ait görselleri D&R ve Pandora gibi sitelerden toplar. Web sayfalarında gezinerek her görselin bağlantısını bir dosyaya kaydeder ve ardından bu görselleri indirir.

2. **Tekrarlayan Görsellerin Tespiti ve Taşınması**  
   İndirilen görsellerin `imagehash` kullanılarak hash değerleri hesaplanır ve tekrarlayan görseller "Tekrarlayan Görseller" klasörüne taşınır. Pikseli bozuk olan görseller manuel şekilde elenir.

3. **Görsel Zenginleştirme ve Çoğaltma**  
   Her görsel üzerinde döndürme, parlaklık ve kontrast ayarları gibi veri çoklama işlemleri yapılarak yeni varyantlar oluşturulur. Bu, makine öğrenmesi projeleri için daha geniş bir veri kümesi elde etmeye yardımcı olur.

## Proje Raporu
[Proje Raporunu Görüntüle](https://github.com/DeryaGelmez/YazLabKitapKategori/blob/main/Rapor.pdf)

## Projede Oluşturulan Veri Setlerine Erişim
[Data Setlerini Görüntüle](https://drive.google.com/drive/folders/1O9yWV-ZxrSfPuyDPSKedRyI7kGMchwL4?usp=drive_link)
[Colab Verilerini Görüntüle](https://drive.google.com/drive/folders/1eOJyz8F48Ggs20mL9bRbRBxzcCB3iOy-)

----
