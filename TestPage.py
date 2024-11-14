#İlk web kazıma test (Öğrenilenlerin bir kategoride uygulanması)
import os
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.dr.com.tr/kategori/Kitap/Egitim-Basvuru/Kisisel-Gelisim/grupno=00179'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.get(url)

sayfa_no = 1
image_urls = []

with open(r'C:\Users\derya\Desktop\kisiselgelisim_urls.txt', 'w', encoding='utf-8') as file:
    while True:
        print(f'sayfa: --> {sayfa_no}')
        sayfa_url = f'https://www.dr.com.tr/kategori/Kitap/Egitim-Basvuru/Kisisel-Gelisim/grupno=00179?Page={sayfa_no}&ShowNotForSale=false'

        driver.get(sayfa_url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div.prd-main-wrapper')))
        kitaplar = driver.find_elements(By.CSS_SELECTOR, 'div.prd-main-wrapper')

        for kitap in kitaplar:
            img = kitap.find_element(By.CSS_SELECTOR, 'a img')
            src = img.get_attribute('src')
            data_src = img.get_attribute('data-src')
            if data_src:
                file.write(data_src + '\n')
                image_urls.append(data_src)
            else:
                file.write(src + '\n')
                image_urls.append(src)


        try:
            ileri_butonu = driver.find_element(By.CSS_SELECTOR, 'li.pagination-next')
            if ileri_butonu is None:
                break
            else:
                sayfa_no += 1
        except Exception:
            break

print("Görsel URL'leri text dosyasına başarıyla kaydedildi.")

download_folder = os.path.join(os.path.expanduser("~"), "Desktop", "kisisel_gelisim")
os.makedirs(download_folder, exist_ok=True)

for index, url in enumerate(image_urls, start=1):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_path = os.path.join(download_folder, f"{index}.jpg")


            img = Image.open(BytesIO(response.content))
            img = img.resize((200, 300), Image.LANCZOS)
            img.save(image_path)

            print(f"{index}.jpg başarıyla indirildi ve boyutlandırıldı.")
        else:
            print(f"{url} adresinden resim indirilemedi.")
    except Exception as e:
        print(f"Hata: {e}")

driver.quit()