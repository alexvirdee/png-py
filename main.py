import os from pdf2image import convert_from_path

def pdf_to_png(input_path, output_path):
    pages = convert_from_path(input_path)
    for i, page in enumerate(pages):
        page.save(f"{output_path}/page_{i+1}.png", "PNG")

def convert_folder(folder_path):
    output_path = os.path.join(folder_path, 'output')  # Specify the output folder for PNG files
    os.makedirs(output_path, exist_ok=True)
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            input_path = os.path.join(folder_path, filename)
            pdf_to_png(input_path, output_path)

if __name__ == '__main__':
    folder_path = input("Enter the folder path: ")
    convert_folder(folder_path)

    