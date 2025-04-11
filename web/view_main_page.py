from flask import render_template, url_for, request, jsonify
from .data_models.models import *

from .excel_data_handler import extract_categories_from_excel
from .data_models.utils import load_sub_categories
# from .data_models.utils_v2 import load_sub_categories_v2

@app.route('/')
@app.route('/main')
def main():
    objects = SubCategory.query
    return render_template('main.html', objects = objects)


@app.route('/upload', methods=['POST'])
def upload():
    # Проверяем, есть ли файл в запросе
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Если файл не выбран
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    excel_data = extract_categories_from_excel(file)
    load_sub_categories(excel_data)
    # load_sub_categories_v2(excel_data)
    # print(excel_data)
    # Здесь можно добавить другие операции с файлом

    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename}), 200
