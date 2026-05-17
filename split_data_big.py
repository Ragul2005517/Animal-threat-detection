import os
import shutil
import random

print("🚀 Starting split_data_big.py script...")

# Source folders
all_calm = "all_calm_dogs"
all_aggressive = "all_aggressive_dogs"

# Destination folders
dest_folders = {
    "train_calm": "data/train/calm_dog",
    "val_calm": "data/val/calm_dog",
    "test_calm": "data/test/calm_dog",
    "train_agg": "data/train/aggressive_dog",
    "val_agg": "data/val/aggressive_dog",
    "test_agg": "data/test/aggressive_dog",
}

def split_images(src_folder, train_folder, val_folder, test_folder):
    print(f"\n📂 Processing folder: {src_folder}")

    if not os.path.exists(src_folder):
        print(f"⚠️ Source folder does not exist: {src_folder}")
        return

    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)

    images = [f for f in os.listdir(src_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"🔹 Found {len(images)} images in {src_folder}")

    if len(images) == 0:
        print(f"⚠️ No images found in {src_folder}! Check folder and image extensions.")
        return

    random.shuffle(images)

    total = len(images)
    train_end = int(total * 0.7)
    val_end = train_end + int(total * 0.2)

    for i, img in enumerate(images):
        src_path = os.path.join(src_folder, img)
        if i < train_end:
            shutil.copy(src_path, train_folder)
        elif i < val_end:
            shutil.copy(src_path, val_folder)
        else:
            shutil.copy(src_path, test_folder)

    print(f"✅ Split complete for {src_folder}:")
    print(f"   Train: {train_end} images")
    print(f"   Val:   {val_end - train_end} images")
    print(f"   Test:  {total - val_end} images")

# Run splits
split_images(all_calm, dest_folders["train_calm"], dest_folders["val_calm"], dest_folders["test_calm"])
split_images(all_aggressive, dest_folders["train_agg"], dest_folders["val_agg"], dest_folders["test_agg"])

print("\n🎉 All data splitting finished successfully!")
