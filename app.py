import yt_dlp
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DOWNLOAD_DIR = 'downloads'

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get('url')
    output_format = data.get('format', 'mp4')

    if not video_url:
        return jsonify({"error": "La URL del video es requerida"}), 400

    try:
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        # Opciones para descargar video MP4
        if output_format == 'mp4':
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'cookiefile': 'cookies.txt',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
            return jsonify({"message": "Video descargado exitosamente!", "file_path": filename})

        # Opciones para extraer audio MP3
        elif output_format == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'cookiefile': 'cookies.txt',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                # El nombre del archivo cambia a .mp3 después del procesamiento
                filename = os.path.splitext(ydl.prepare_filename(info))[0] + '.mp3'
            return jsonify({"message": "Audio MP3 creado exitosamente!", "file_path": filename})
        
        else:
            return jsonify({"error": "Formato no válido. Usa 'mp4' o 'mp3'."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')