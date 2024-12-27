from google.colab import drive
import zipfile
import os
from sklearn.model_selection import train_test_split
import shutil
from tensorflow.keras.preprocessing.image import ImageDataGenerator


drive.mount('/content/drive')

zip_path = "/content/drive/MyDrive/ColabVeriler/kitap_kapaklari.zip"
extract_path = "/content/kitap_kapaklari"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

base_path = os.path.join(extract_path, "kitap_kapaklari")
alt_klasorler = [
    folder for folder in os.listdir(base_path)
    if os.path.isdir(os.path.join(base_path, folder)) and folder != "kitap_kapaklari"
]
print(alt_klasorler)


train_dir = "/content/train_data"
test_dir = "/content/test_data"

if os.path.exists(train_dir):
    shutil.rmtree(train_dir)
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)

os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

def split_data(source_dir, train_dir, test_dir, test_size=0.2):
    for category in os.listdir(source_dir):
        category_path = os.path.join(source_dir, category)

        if not os.path.isdir(category_path) or category == "kitap_kapaklari":
            print(f"{category} klasörü atlandı.")
            continue

        train_category = os.path.join(train_dir, category)
        test_category = os.path.join(test_dir, category)
        os.makedirs(train_category, exist_ok=True)
        os.makedirs(test_category, exist_ok=True)

        images = [file for file in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, file))]

        train_images, test_images = train_test_split(images, test_size=test_size)

        for image in train_images:
            shutil.copy(os.path.join(category_path, image), os.path.join(train_category, image))

        for image in test_images:
            shutil.copy(os.path.join(category_path, image), os.path.join(test_category, image))

source_dir = base_path

split_data(source_dir, train_dir, test_dir)

for unwanted_dir in ["kitap_kapaklari"]:
    unwanted_train_dir = os.path.join(train_dir, unwanted_dir)
    unwanted_test_dir = os.path.join(test_dir, unwanted_dir)
    if os.path.exists(unwanted_train_dir):
        shutil.rmtree(unwanted_train_dir)
    if os.path.exists(unwanted_test_dir):
        shutil.rmtree(unwanted_test_dir)

print("Eğitim Klasörleri:", os.listdir(train_dir))
print("Test Klasörleri:", os.listdir(test_dir))

for category in os.listdir(train_dir):
    category_path = os.path.join(train_dir, category)
    print(f"Eğitim {category}: {len(os.listdir(category_path))} görsel")

for category in os.listdir(test_dir):
    category_path = os.path.join(test_dir, category)
    print(f"Test {category}: {len(os.listdir(category_path))} görsel")



train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(260, 400),
    batch_size=32,
    class_mode='categorical'
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(260, 400),
    batch_size=32,
    class_mode='categorical'
)

import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from transformers import DeiTForImageClassification, DeiTFeatureExtractor
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, precision_recall_fscore_support
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import time

class CustomDataset(Dataset):
    def __init__(self, file_paths, labels, transform):
        self.file_paths = file_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        image = Image.open(self.file_paths[idx]).convert("RGB")
        image = self.transform(image)
        label = self.labels[idx]
        return image, label


def prepare_dataset(directory, transform):
    file_paths = []
    labels = []
    class_to_idx = {}

    for idx, category in enumerate(sorted(os.listdir(directory))):
        category_path = os.path.join(directory, category)
        if os.path.isdir(category_path):
            class_to_idx[category] = idx
            for file_name in os.listdir(category_path):
                file_paths.append(os.path.join(category_path, file_name))
                labels.append(idx)

    dataset = CustomDataset(file_paths, labels, transform)
    return dataset, class_to_idx

feature_extractor = DeiTFeatureExtractor.from_pretrained("facebook/deit-base-distilled-patch16-224")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=feature_extractor.image_mean, std=feature_extractor.image_std),
])

train_dir = "/content/train_data"
test_dir = "/content/test_data"
train_dataset, class_to_idx = prepare_dataset(train_dir, transform)
test_dataset, _ = prepare_dataset(test_dir, transform)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

model = DeiTForImageClassification.from_pretrained(
    "facebook/deit-base-distilled-patch16-224",
    num_labels=len(class_to_idx),
    ignore_mismatched_sizes=True
)

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def train_model_with_early_stopping(model, train_loader, test_loader, optimizer, epochs=20, patience=3):
    model.train()
    loss_fn = torch.nn.CrossEntropyLoss()
    train_losses = []
    val_losses = []
    best_val_loss = float('inf')
    patience_counter = 0
    start_time = time.time()

    for epoch in range(epochs):
        total_loss = 0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images).logits
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            preds = torch.argmax(outputs, dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        accuracy = correct / total
        train_losses.append(total_loss / len(train_loader))
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss:.4f}, Accuracy: {accuracy:.4f}")

        val_loss, val_metrics = evaluate_model(model, test_loader, loss_fn)
        val_losses.append(val_loss)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            print(f"Validation loss improved to {val_loss:.4f}. Resetting patience counter.")
        else:
            patience_counter += 1
            print(f"Validation loss did not improve. Patience counter: {patience_counter}/{patience}")

        if patience_counter >= patience:
            print("Early stopping triggered. Stopping training.")
            break

    end_time = time.time()
    training_time = end_time - start_time
    print(f"Total Training Time: {training_time:.2f} seconds")

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(train_losses) + 1), train_losses, label='Train Loss', marker='o')
    plt.plot(range(1, len(val_losses) + 1), val_losses, label='Validation Loss', marker='x')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('Training and Validation Loss')
    plt.show()

    return training_time

def evaluate_model(model, test_loader, loss_fn=None):
    model.eval()
    correct = 0
    total = 0
    all_preds = []
    all_labels = []
    val_loss = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images).logits
            preds = torch.argmax(outputs, dim=1)

            if loss_fn:
                val_loss += loss_fn(outputs, labels).item()

            correct += (preds == labels).sum().item()
            total += labels.size(0)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    accuracy = correct / total
    precision, recall, fscore, _ = precision_recall_fscore_support(all_labels, all_preds, average='weighted')
    cm = confusion_matrix(all_labels, all_preds)
    sensitivity = cm[1, 1] / (cm[1, 1] + cm[1, 0]) if cm.shape[0] > 1 else 0
    specificity = cm[0, 0] / (cm[0, 0] + cm[0, 1]) if cm.shape[0] > 1 else 0

    print(f"Validation Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F-Score: {fscore:.4f}")
    print(f"Sensitivity: {sensitivity:.4f}")
    print(f"Specificity: {specificity:.4f}")

    print("Classification Report:")
    print(classification_report(all_labels, all_preds))

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=list(class_to_idx.keys()), yticklabels=list(class_to_idx.keys()))
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()

    y_true_bin = np.eye(len(class_to_idx))[all_labels]
    y_pred_bin = np.eye(len(class_to_idx))[all_preds]

    fpr, tpr, _ = roc_curve(y_true_bin.ravel(), y_pred_bin.ravel())
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f}')
    plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()

    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'fscore': fscore,
        'sensitivity': sensitivity,
        'specificity': specificity,
        'auc': roc_auc
    }

    return val_loss / len(test_loader) if loss_fn else 0, metrics

def inference_time(model, test_loader):
    model.eval()
    start_time = time.time()

    with torch.no_grad():
        for images, _ in test_loader:
            images = images.to(device)
            _ = model(images)

    end_time = time.time()
    inference_duration = end_time - start_time
    print(f"Inference Time: {inference_duration:.2f} seconds")
    return inference_duration

training_time = train_model_with_early_stopping(model, train_loader, test_loader, optimizer, epochs=20, patience=3)

inference_duration = inference_time(model, test_loader)

print(f"Training Time: {training_time:.2f} seconds")
print(f"Inference Time: {inference_duration:.2f} seconds")
print("Training Completed.")