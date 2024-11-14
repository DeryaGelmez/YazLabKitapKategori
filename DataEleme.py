import os
from PIL import Image
import imagehash
import shutil

main_folder_path = "C:\\Users\\derya\\PycharmProjects\\YazLab\\İndirilenler"
duplicates_main_folder = os.path.join(main_folder_path, 'Tekrarlayan Görseller')

if not os.path.exists(duplicates_main_folder):
    os.makedirs(duplicates_main_folder)
    print(f"{duplicates_main_folder} oluşturuldu.")

subfolders = ['Çizgi Roman', 'Çocuk', 'Kişisel Gelişim', 'Polisiye', 'Polisiye2', 'Tarih']

for subfolder in subfolders:
    folder_path = os.path.join(main_folder_path, subfolder)
    duplicates_folder = os.path.join(duplicates_main_folder, subfolder)

    if not os.path.exists(duplicates_folder):
        os.makedirs(duplicates_folder)
        print(f"{subfolder} kategorisinin tekrarlayan görselleri için klasör oluşturuldu.")

    hashes = {}
    duplicate_count = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            file_path = os.path.join(folder_path, filename)
            image = Image.open(file_path)


            img_hash = imagehash.phash(image)

            if img_hash in hashes:
                duplicate_path = os.path.join(duplicates_folder, filename)
                shutil.move(file_path, duplicate_path)
                duplicate_count += 1
            else:
                hashes[img_hash] = file_path

    print(
        f"{subfolder} kategorisi için {duplicate_count} adet tekrarlayan görsel {duplicates_folder} klasörüne taşındı.")

print("Tüm alt klasörlerdeki tekrarlayan görseller ilgili klasörlere taşındı.")
