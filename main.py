from flask import Flask, request
import base64
from PIL import Image
from io import BytesIO
from local_stable_diffusion import image_pipeline

app = Flask(__name__)


@app.route('/process_image', methods=['POST'])
def process_image():
    # Gelen veriyi Base64'ten çöz
    image_data = request.form['image']
    prompt = request.form['prompt']

    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image.save('downloads/gelen_resim.png', 'PNG')
    # image.save(os.path.join("downloads", "gelen_resim.png"))

    # Burada resim üzerinde istediğin değişiklikleri yap
    image_path = BytesIO(base64.b64decode(image_data))
    processed_image = image_pipeline.generate_image(prompt=prompt,
                                                    image_path=image_path)

    # İşlenmiş resmi bir BytesIO nesnesine kaydet
    processed_image_data = BytesIO()
    processed_image.save(processed_image_data, format='JPEG')
    processed_image_data.seek(0)

    # İşlenmiş resmi Base64 kodlayarak string'e çevir
    encoded_processed_image = base64.b64encode(processed_image_data.getvalue()).decode('utf-8')

    # İşlenmiş resmi istemciye geri gönder
    return {'processed_image': encoded_processed_image}


if __name__ == '__main__':
    app.run(host='192.168.84.106', port=8000, debug=True)
