from flask import Flask, request, jsonify, send_from_directory
import qrcode
import os
from flask_cors import CORS  # Import CORS
from flask import send_file

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app

# Set up a route to serve static files (QR codes)
@app.route('/qrcodes/<filename>')
def serve_qrcode(filename):
    return send_from_directory('qrcodes', filename)


# Set up a route to generate QR codes for URLs
@app.route('/generate_qr_code', methods=['POST'])
def generate_qr_code():
    data = request.json.get('data')
    if data:
        # Sanitize the URL to create a valid filename
        sanitized_data = data.replace("://", "_").replace("/", "_")
        filename = '{sanitized_data}.png'

        # Check if the file already exists
        if os.path.exists(os.path.join('qrcodes', filename)):
            return jsonify({'message': 'QR code already exists', 'filename': filename})

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image
        img.save(os.path.join('qrcodes', filename))
        return jsonify({'message': 'QR code generated successfully', 'filename': filename})
    else:
        return jsonify({'error': 'No data provided'})
    

@app.route('/download_qr_code/<filename>', methods=['GET'])
def download_qr_code(filename):
    file_path = os.path.join('qrcodes', filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run()
