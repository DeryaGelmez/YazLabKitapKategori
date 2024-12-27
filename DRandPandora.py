#Gereken kütüphanelerin içe aktarımı
import os #Dosya ve klosör işlemlerini yürütmek için
import requests #Web istekleri göndermek ve yanıt almak için
from io import BytesIO #İnternetten indirdiğimiz görselleri bellekte tutmak için
from PIL import Image #Görselleri açıp işlemek için (Boyutlandırma, döndürme, ışık ayarı vs. için) (Pillow kütüphanesi)
#Selenium kütüphanesinin farklı bileşenlerini içe aktarma
from selenium import webdriver #Web sayfalarına doğrudan erişim için
from selenium.webdriver.common.by import By #Web kazıma yaparken Selenium'da HTML elementini seçerken hangi kriterin kullanılacağını By sınıfı ile belirleriz. Ör; By.CSS_SELECTOR/By.ID)
from selenium.webdriver.support.ui import WebDriverWait #Sayfada istenen içeriğin yüklenmesi için bekleme süresini belirlerken kullanıyoruz.
from selenium.webdriver.support import expected_conditions as EC #expected_conditions modülü EC olarak içe aktarılır. Bu modül ile sayfanın yüklenmesi, bir öğenin görünmesi veya tıklanabilir olması gibi durumlar kontrol edilir. (Koşullu bekleme tanımlama)
from selenium.common.exceptions import TimeoutException, NoSuchElementException #Selenium kütüphanesinin belirli hata türlerini içe aktarmak için
#TimeoutException: Belirtilen süre içinde öğe yüklenmezse tetiklenir.
#NoSuchElementException: Belirtilen HTML öğesi sayfada bulunamazsa tetiklenir.

# Web sürücüsünü başlatma ayarları
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)

main_folder = os.path.join(os.getcwd(), "İndirilenler")
os.makedirs(main_folder, exist_ok=True)

#Görsel URL'lerini kaydetmek için bir fonksiyon
def save_url(url, folder, max_image=6000):
    page_no = 1
    max_page=4
    image_urls = []
    downloaded_count = 0

    while page_no<max_page and downloaded_count < max_image:
        driver.get(f"{url}?Page={page_no}&ShowNotForSale=false")

        try:
            books = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'div.prd-main-wrapper')))



            for book in books:
                book_link = book.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                driver.execute_script("window.open(arguments[0]);", book_link)
                driver.switch_to.window(driver.window_handles[1])

                img=WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.swiper-slide-active img.js-prd-first-image')))
                img_url = img.get_attribute('src')

                if img_url:
                        image_urls.append(img_url)
                        downloaded_count += 1

                if downloaded_count >= max_image:
                        break

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            try:
                    ileri_butonu = driver.find_element(By.CSS_SELECTOR, 'li.pagination-next a')
                    if downloaded_count < max_image:
                        page_no += 1
                    else:
                        break
            except NoSuchElementException:
                    break

        except TimeoutException:
            print("Zaman aşımı")
            break

    url_file_path = os.path.join(folder, "image_urls.txt")
    with open(url_file_path, "w") as file:
        for img_url in image_urls:
            file.write(img_url + "\n")
    print(f"*****\n{len(image_urls)} URL kaydedildi: {url_file_path}")


def download_images(folder, max_image=6000):
    url_file_path = os.path.join(folder, "image_urls.txt")
    downloaded_count = 0

    with open(url_file_path, "r") as file:
        for line in file:
            img_url = line.strip()
            if downloaded_count >= max_image:
                break

            try:
                response = requests.get(img_url)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    img = img.convert("RGB")
                    img=img.resize((260,400))
                    img.save(os.path.join(folder, f"{downloaded_count + 1}.jpg"), "JPEG")
                    downloaded_count += 1
                    print(f"{downloaded_count}.jpg başarıyla boyutlandırıldı ve indirildi.")
                else:
                    print("Resim indirilemedi.")

            except Exception as e:
                print(f"Resim indirilirken hata oluştu: {e}")


categories = [
    {"name": "Kişisel Gelişim",
     "url": "https://www.dr.com.tr/kategori/Kitap/Egitim-Basvuru/Kisisel-Gelisim/grupno=00179"},
    {"name": "Çocuk", "url": "https://www.dr.com.tr/kategori/Kitap/Cocuk-ve-Genclik/Okul-Cagi-6-10-Yas/grupno=00886"},
    {"name": "Tarih", "url": "https://www.dr.com.tr/kategori/Kitap/Arastirma-Tarih/Tarih/grupno=00226"},
    {"name": "Çizgi Roman", "url": "https://www.dr.com.tr/kategori/Kitap/Cizgi-Roman/grupno=00053"},
    {"name": "Polisiye", "url": "https://www.dr.com.tr/kategori/Kitap/Edebiyat/Roman/Polisiye/grupno=00497"}
]

for category in categories:
    folder = os.path.join(main_folder, category["name"])
    os.makedirs(folder, exist_ok=True)

    save_url(category["url"], folder, max_image=6000)
    download_images(folder, max_image=6000)

print("D&R'daki tüm indirme işlemleri tamamlandı.")

url = 'https://www.pandora.com.tr/urunler/polisiye/10/Turkce_Kitaplar'

image_urls = []
indirilenler_klasor = os.path.join(os.getcwd(), 'İndirilenler')
polisiye2_klasor = os.path.join(indirilenler_klasor, 'Polisiye2')
image_urls_file_path = os.path.join(polisiye2_klasor, 'image_urls.txt')

os.makedirs(polisiye2_klasor, exist_ok=True)

with open(image_urls_file_path, 'w', encoding='utf-8') as file:
    sayfa_no = 1
    while True:
        sayfa_url = f'{url}?sayfa={sayfa_no}'
        driver.get(sayfa_url)

        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.col-xs-12.col-sm-6.col-md-4.col-lg-3'))
        )

        kitaplar = driver.find_elements(By.CSS_SELECTOR, 'li.col-xs-12.col-sm-6.col-md-4.col-lg-3')

        if not kitaplar:
            print(f"{sayfa_no}. sayfada kitap bulunamadı, işlem sonlandırılıyor.")
            break

        for kitap in kitaplar:
            img = kitap.find_element(By.CSS_SELECTOR, 'div.coverWrapper img')
            src = img.get_attribute('src')
            data_src = img.get_attribute('data-src')
            if data_src:
                file.write(data_src + '\n')
                image_urls.append(data_src)
            else:
                file.write(src + '\n')
                image_urls.append(src)

        try:
            ileri_butonu = driver.find_element(By.CSS_SELECTOR, 'span.glyphicon.glyphicon-step-forward')
            if ileri_butonu is None:
                break
            else:
                sayfa_no += 1
        except Exception:
            break

print(f"*****\n{len(image_urls)} URL kaydedildi: {image_urls_file_path}")

for index, url in enumerate(image_urls, start=1):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_path = os.path.join(polisiye2_klasor, f"{index}.jpg")

            img = Image.open(BytesIO(response.content))
            img = img.resize((260, 400), Image.LANCZOS)
            img.save(image_path)

            print(f"{index}.jpg başarıyla boyutlandırıldı ve indirildi.")
        else:
            print(f"{url} adresinden resim indirilemedi, durum kodu: {response.status_code}")
    except Exception as e:
        print(f"Hata: {e}")

print("Pandora'daki tüm indirme işlemleri tamamlandı.")

driver.quit()
