from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
import uuid
import os

app = Flask(__name__)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    output_path = f"output_{uuid.uuid4().hex}.wav"
    tts.tts_to_file(text=text, file_path=output_path)
    
    response = send_file(output_path, mimetype="audio/wav")
    
    @response.call_on_close
    def cleanup():
        os.remove(output_path)

    return response

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Coqui TTS API is running"}), 200
