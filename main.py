import random

from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert_audio', methods=['POST'])
def convert_audio():

    data = request.get_json()
    print(data)
    text = data.get('text')
    print(text)
    if not text:
        return jsonify({'success': False, 'message': 'Vui lòng cung cấp văn bản.'}), 400

    # try:
    # Thay thế 'https://maytinh.com' bằng URL thực tế của API chuyển văn bản sang âm thanh
    url = 'http://192.168.68.139:8848/api/v1/synthesise'
    # url = "http://localhost:8848/api/v1/synthesise"
    headers = {'Content-Type': 'application/json'}
    data = {"text": text}
    output_filename = "static/test.opus"

    try:
        response = requests.post(url, headers=headers, json=data, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Audio content saved to '{output_filename}'")

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return jsonify({'filepath':output_filename + "?rnd" + str(random.random())})
    # except requests.exceptions.RequestException as e:
    #     return jsonify({'success': False, 'message': f'Lỗi khi gọi API chuyển đổi âm thanh: {e}'}), 500
    # except ValueError:
    #     return jsonify({'success': False, 'message': 'Lỗi khi xử lý phản hồi JSON từ API.'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)