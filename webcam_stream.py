import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

# Função para capturar o vídeo da webcam
def gen_frames():
    cap = cv2.VideoCapture(0)  # 0 para webcam padrão, altere se necessário
    while True:
        success, frame = cap.read()  # Capture frame da webcam
        if not success:
            break
        else:
            # Codifique o frame em formato JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Gere um stream de bytes para enviar para o navegador
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Rota para acessar o stream de vídeo
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Rota para a página principal
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
