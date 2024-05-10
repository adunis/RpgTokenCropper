from PIL import Image, ImageDraw, ImageOps
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import psutil
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the directory containing the folders
directory_path = 'C:/Users/gobli/AppData/Local/FoundryVTT/Data/assets/token_images/rogue_pirate_swashbuckler'

def circular_crop_and_save(file_path, folder_name, file_number, total_files):  # Include total_files in the signature
    try:
        with Image.open(file_path) as img:
            # Calculate the size for the square
            size = min(img.size)
            # Create a mask
            mask = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            # Crop to square and apply mask
            img_cropped = img.crop((0, 0, size, size))
            result = ImageOps.fit(img_cropped, mask.size, centering=(0.5, 0.5))
            result.putalpha(mask)

            # Save the image with circular crop
            circular_filename = f"{folder_name}_{file_number}_circular.png"
            circular_file_path = os.path.join(os.path.dirname(file_path), circular_filename)
            result.save(circular_file_path)

        # Log progress and CPU usage
        progress = (file_number / total_files) * 100
        logging.info(f"Processed {file_number}/{total_files} images ({progress:.2f}%). CPU Usage: {psutil.cpu_percent()}%")

        # Delete the original file
        os.remove(file_path)

    except Exception as e:
        logging.error(f"Error for file {file_path}: {e}")

def process_folder(folder_path, folder_name):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'))]  # Include .webp files
    total_files = len(files)
    futures = []

    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        for file_number, file in enumerate(files, 1):
            file_path = os.path.join(folder_path, file)
            # Pass total_files to circular_crop_and_save
            futures.append(executor.submit(circular_crop_and_save, file_path, folder_name, file_number, total_files))

    # Wait for all futures to complete and log progress
    for future in as_completed(futures):
        pass  # Progress is logged in circular_crop_and_save, so nothing needed here

def process_directory(directory_path):
    # Process the images in the root directory first
    logging.info(f"Starting processing for root directory: {directory_path}")
    process_folder(directory_path, os.path.basename(directory_path))

    # Then process each sub-folder in the directory
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)
        if os.path.isdir(folder_path):
            logging.info(f"Starting processing folder: {folder_name}")
            process_folder(folder_path, folder_name)
            logging.info(f"Finished processing folder: {folder_name}")

if __name__ == "__main__":
    process_directory(directory_path)


# Path to the directory containing the folders
directory_path = 'C:/Users/gobli/AppData/Local/FoundryVTT/Data/assets/token_images'