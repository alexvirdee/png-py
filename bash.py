# Use this file to convert without UI client (keeping for reference)
import os 
from pdf2image import convert_from_path

def pdf_to_png(input_path, output_path):
    pages = convert_from_path(input_path)
    for i, page in enumerate(pages):
        global_page_number = pdf_to_png.page_counter + i + 1
        page.save(f"{output_path}/page_{global_page_number}.png", "PNG")
        pdf_to_png.page_counter += len(pages)

pdf_to_png.page_counter = 0

def convert_folder(folder_path):
    output_path = os.path.join(folder_path, 'png-images')  # Specify the output folder
    os.makedirs(output_path, exist_ok=True)
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            input_path = os.path.join(folder_path, filename)
            pdf_to_png(input_path, output_path)

if __name__ == '__main__':
    folder_path = input("Enter the folder path: ")
    convert_folder(folder_path)
