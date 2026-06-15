from pathlib import Path
from PIL import Image
import pillow_heif


pillow_heif.register_heif_opener()

image_dir = Path("images/multi")
output_dir = Path("images/multi_fixed")

output_dir.mkdir(exist_ok=True)

image_files = []

for suffix in ["*.jpg", "*.jpeg", "*.png", "*.heic", "*.heif", "*.JPG", "*.JPEG", "*.PNG", "*.HEIC", "*.HEIF"]:
    image_files.extend(image_dir.glob(suffix))

image_files = sorted(image_files)

print(f"Found {len(image_files)} image files.")

success_count = 0
fail_count = 0

for index, image_path in enumerate(image_files, start=1):
    try:
        image = Image.open(image_path).convert("RGB")

        new_path = output_dir / f"test_{index:03d}.jpg"
        image.save(new_path, "JPEG", quality=95)

        print(f"OK: {image_path.name} -> {new_path.name}")
        success_count += 1

    except Exception as error:
        print(f"FAILED: {image_path.name} | {error}")
        fail_count += 1

print("=" * 50)
print(f"Success: {success_count}")
print(f"Failed: {fail_count}")
print(f"Output directory: {output_dir}")