## Proje Özeti
Bu proje, belirli kitap kategorilerine ait görselleri çeşitli sitelerden toplar, ardından toplanan görselleri işlemlerden geçirir. İlk adımda web scraping ile kitap kapak görselleri indirilir, ikinci adımda tekrarlayan görseller tespit edilerek taşınır, piksel bozukluğu olan ve kategoriye uygun olmayan görseller manuel şekilde tekrardan elenir; üçüncü adımda ise her görselin parlaklık, kontrast ve döndürme işlemleri ile zenginleştirilmiş varyantları oluşturulur. Bu sayede, görüntü işleme ve makine öğrenmesi projelerinde kullanılmak üzere çeşitli görsel veriler elde edilmiş olur.

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

![Veri kazımanın yapılacağı URL'ye giriş](https://github.com/DeryaGelmez/YazLabKitapKategori/blob/main/Screenshot%20(24).png) 
![Kitap içeriğinin farklı URL'de açılması](https://github.com/DeryaGelmez/YazLabKitapKategori/blob/main/Screenshot%20(27).png)
![Veri arttırma sonucu klasörden bir kesit](https://github.com/DeryaGelmez/YazLabKitapKategori/blob/main/Screenshot%20(26).png)
![Tüm işlemler sonucunda açılan klasörler](https://github.com/DeryaGelmez/YazLabKitapKategori/blob/main/Screenshot%20(23).png)

