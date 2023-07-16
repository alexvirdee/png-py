import os 
from flask import Flask, request, jsonify
from pdf2image import convert_from_path
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def pdf_to_png(input_path, output_path):
    pages = convert_from_path(input_path)
    for i, page in enumerate(pages):
        global_page_number = pdf_to_png.page_counter + i + 1
        page.save(f"{output_path}/page_{global_page_number}.png", "PNG")
        pdf_to_png.page_counter += len(pages)

pdf_to_png.page_counter = 0

@app.route('/convert', methods=['POST'])
def convert_folder():
    request_data = request.form # Access the form data from the request
    folder_path = request_data.get('fodler_path') # Extract the folder_path from the form data
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            input_path = os.path.join(folder_path, filename)
            pdf_to_png(input_path, output_path)

    return jsonify({ 'message': 'Conversion successful!' })

if __name__ == '__main__':
    app.run()