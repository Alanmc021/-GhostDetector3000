from IPython.display import Javascript
from google.colab import output
import cv2
import numpy as np
from google.colab.patches import cv2_imshow
import io
import base64
from PIL import Image

# Código JavaScript para capturar a imagem
def take_photo(filename='photo.jpg'):
    js = Javascript('''
    async function takePhoto() {
        const video = document.createElement('video');
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        document.body.appendChild(video);
        video.srcObject = stream;
        await new Promise(resolve => video.onloadedmetadata = resolve);
        video.play();
        await new Promise(resolve => setTimeout(resolve, 2000)); // Espera 2 segundos
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        stream.getTracks().forEach(track => track.stop());
        video.remove();
        return canvas.toDataURL('image/jpeg');
    }
    takePhoto().then(data => google.colab.kernel.invokeFunction('notebook.save_photo', [data], {}));
    ''')
    display(js)

def save_photo(data):
    """ Salva a imagem capturada """
    image_bytes = base64.b64decode(data.split(',')[1])
    image = Image.open(io.BytesIO(image_bytes))
    image.save('photo.jpg')
    print("📸 Imagem capturada com sucesso!")

output.register_callback('notebook.save_photo', save_photo)

print("📷 Olhe para a câmera, capturando imagem...")
take_photo()

# ================================
# PROCESSAMENTO DA IMAGEM
# ================================

# Carregar imagem
image_path = "photo.jpg"
image = cv2.imread(image_path)

humanLabel, ghotLabel = "Humano idade: 192", "Humano idade: 39"

if image is None:
    print("Erro ao carregar a imagem.")
else:
    height, width, _ = image.shape

    # Ajustando as dimensões para cobrir melhor as áreas
    ghost_x, ghost_y = 40, 50
    ghost_w, ghost_h = 150, 220  # Aumentei a largura

    human_x, human_y = 300, 100
    human_w, human_h = 200, 260  # Aumentei a largura

    # Desenhar retângulo do fantasma
    cv2.rectangle(image, (ghost_x, ghost_y), (ghost_x + ghost_w, ghost_y + ghost_h), (255, 0, 255), 1)  # Roxo
    cv2.putText(image, humanLabel, (ghost_x, ghost_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

    # Desenhar retângulo fixo para humano
    cv2.rectangle(image, (human_x, human_y), (human_x + human_w, human_y + human_h), (0, 255, 0), 1)  # Verde
    cv2.putText(image, ghotLabel, (human_x, human_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Exibir imagem processada
    cv2_imshow(image)
