from flask import Flask, request, send_file, make_response
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

# Manually handle CORS for all responses
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'  # Update for production later
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Max-Age'] = '86400'  # Cache preflight for 24 hours
    return response

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        response = make_response({'error': 'No image provided'}, 400)
        return response

    file = request.files['image']
    input_image = Image.open(file.stream)
    output_image = remove(input_image)

    output_buffer = io.BytesIO()
    output_image.save(output_buffer, format='PNG')
    output_buffer.seek(0)

    return send_file(
        output_buffer,
        mimetype='image/png',
        as_attachment=True,
        download_name='output.png'
    )

@app.route('/remove-bg', methods=['OPTIONS'])
def handle_options():
    response = make_response({}, 200)
    return response