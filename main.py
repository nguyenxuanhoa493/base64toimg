from flask import Flask, request, send_file, jsonify
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/decode_base64', methods=['POST'])
def decode_base64():
    data = request.get_json()
    if 'base64' not in data:
        return jsonify({'error': 'No base64 string provided'}), 400

    try:
        # Decode base64 string
        base64_str = data['base64']
        if base64_str.startswith('data:image'):
            base64_str = base64_str.split(',', 1)[1]

        image_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_data))

        # Save image to a temporary file
        temp_file = BytesIO()
        image.save(temp_file, format=image.format)
        temp_file.seek(0)

        return send_file(temp_file, mimetype=f'image/{image.format.lower()}')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=1000)
