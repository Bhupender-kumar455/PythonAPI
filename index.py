from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/remove-bg": {
        "origins": ["http://localhost:5173", "https://your-frontend-domain.vercel.app"],  # Add production frontend URL later
        "methods": ["POST", "OPTIONS"],  # Include OPTIONS for preflight
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return {'error': 'No image provided'}, 400

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

# Remove or comment out for Vercel
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
