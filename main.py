import os
import shutil
import zipfile
from pdf2image import convert_from_path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, expose_headers='Content-Disposition')

def convert_to_png(input_path, output_path, pdf_filename):
    images = convert_from_path(input_path)
    for i, image in enumerate(images):
        page_number = i + 1
        image_name = f"page_{page_number}_{pdf_filename}.png"
        image_path = os.path.join(output_path, image_name)
        image.save(image_path, "PNG")

@app.route('/convert', methods=['POST'])
def convert_files():
    files = request.files.getlist('files')
    print('files', files)
    output_path = os.path.join(os.getcwd(), 'converted_to_png')
    
    # Clean up previous converted files
    shutil.rmtree(output_path, ignore_errors=True)
    
    # Create the output folder
    os.makedirs(output_path, exist_ok=True)

    try:
        for file in files:
            if file.filename.endswith('.pdf'):
                pdf_filename = os.path.splitext(file.filename)[0]
                input_path = os.path.join(output_path, file.filename)
                file.save(input_path)
                convert_to_png(input_path, output_path, pdf_filename)

        return jsonify({'message': 'Conversion successful!'})

    except Exception as e:
        return jsonify({'message': f'Conversion failed: {str(e)}'}), 500

@app.route('/download', methods=['GET'])
def download_images():
    output_path = os.path.join(os.getcwd(), 'converted_to_png')
    zip_filename = os.path.join(os.getcwd(), 'converted_to_png.zip')

    try:
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            files_added = 0
            for root, dirs, files in os.walk(output_path):
                for file in files:
                    if file.endswith('.png'):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, output_path)
                        zipf.write(file_path, arcname=os.path.join('converted_to_png', arcname))
                        files_added += 1

            app.logger.debug(f"Files added to ZIP: {files_added}")

        return send_file(zip_filename, as_attachment=True)

    except Exception as e:
        app.logger.error(f"Error occurred during ZIP creation: {e}")

    finally:
        if os.path.exists(zip_filename):
            os.remove(zip_filename)

    return jsonify({'message': 'Failed to create ZIP file.'})


if __name__ == '__main__':
    app.run(port=5001)
