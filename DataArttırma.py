import os
import random
from PIL import Image, ImageEnhance

categories = [
    "Çizgi Roman",
    "Çocuk",
    "Kişisel Gelişim",
    "Tarih",
    "Polisiye"
]

base_path = "C:\\Users\\derya\\PycharmProjects\\YazLab\\İndirilenler"

def brightness_contrast(img):
    brightness_factor = random.uniform(0.5, 1.5)
    contrast_factor = random.uniform(0.5, 1.5)

    enhancer = ImageEnhance.Brightness(img)
    bright_img = enhancer.enhance(brightness_factor)

    enhancer = ImageEnhance.Contrast(bright_img)
    contrast_img = enhancer.enhance(contrast_factor)

    return contrast_img

def rotate_image(image_path, save_path):
    try:
        with Image.open(image_path) as img:
            img.save(save_path)

            for angle in [90, 180, 270]:
                rotated_img = img.rotate(angle, expand=True, resample=Image.BICUBIC)
                enhanced_img = brightness_contrast(rotated_img)
                enhanced_img.save(f"{save_path}_{angle}_gelistirilmis.jpg")

            for _ in range(2):
                random_angle = random.randint(1, 360)
                rotated_img = img.rotate(random_angle, expand=True, resample=Image.BICUBIC)
                enhanced_img = brightness_contrast(rotated_img)
                enhanced_img.save(f"{save_path}_random_{random_angle}_gelistirilmis.jpg")

    except Exception as e:
        print(f"Resim işlenirken hata meydana geldi > {image_path}: {e}")

def process_category(category_name):
    category_path = os.path.join(base_path, category_name)
    if not os.path.exists(category_path):
        print(f"Klasör bulunamadı: {category_path}")
        return

    new_folder = os.path.join(base_path, f"{category_name} Çoklama")
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    for file_name in os.listdir(category_path):
        file_path = os.path.join(category_path, file_name)

        if file_name.lower().endswith('.jpg'):
            new_image_path = os.path.join(new_folder, file_name)
            rotate_image(file_path, new_image_path)

def main():
    for category in categories:
        process_category(category)
    print("İşlem tamamlandı.")

if __name__ == "__main__":
    main()
