from flask import Flask, request, send_file
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/decode_base64', methods=['POST'])
def decode_base64():
    data = request.json
    if 'base64' not in data:
        return {'error': 'No base64 string provided'}, 400

    try:
        # Decode base64 string
        image_data = base64.b64decode(data['base64'])
        image = Image.open(BytesIO(image_data))

        # Save image to a temporary file
        temp_file = BytesIO()
        image.save(temp_file, format=image.format)
        temp_file.seek(0)

        return send_file(temp_file, mimetype='image/jpeg')

    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
