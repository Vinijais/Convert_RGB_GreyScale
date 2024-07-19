import zipfile
import os
from PIL import Image

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def convert_images_to_grayscale(input_paths, output_directory, size=(800,800)):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for image_path in input_paths:
        try:
            # Load the image
            img = Image.open(image_path)

            # Resize the image
            img_resized = img.resize(size)

            # Convert the image to grayscale
            img_gray = img_resized.convert("L")

            # Define the output path
            base_name = os.path.basename(image_path)
            output_path = os.path.join(output_directory,base_name)

            # Save the grayscale image
            img_gray.save(output_path)

            print(f'Successfully processed: {image_path}')

        except Exception as e:
            print(f'Error processing {image_path}: {e}')

def create_zip_from_directory(directory, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))

def process_zip_file(zip_file_path, output_zip_file):
    # Create a temporary directory to extract the zip file
    temp_extract_dir = 'temp_extracted_images'
    temp_output_dir = 'temp_output_grayscale_images'
    
    # Extract the zip file
    extract_zip(zip_file_path, temp_extract_dir)
    
    # Collect all image paths from the extracted files
    image_paths = []
    for root, _, files in os.walk(temp_extract_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_paths.append(os.path.join(root, file))
    
    # Convert images to grayscale
    convert_images_to_grayscale(image_paths, temp_output_dir)
    
    # Create output zip file with grayscale images
    create_zip_from_directory(temp_output_dir, output_zip_file)
    
    # Clean up temporary directories
    for root, _, files in os.walk(temp_extract_dir):
        for file in files:
            os.remove(os.path.join(root, file))
    os.rmdir(temp_extract_dir)

    for root, _, files in os.walk(temp_output_dir):
        for file in files:
            os.remove(os.path.join(root, file))
    os.rmdir(temp_output_dir)

zip_file_path = '11July.zip'  
# Replace with your zip file path
output_zip_file = '11Julyg.zip'  # Replace with your desired output zip file path

process_zip_file(zip_file_path, output_zip_file)
