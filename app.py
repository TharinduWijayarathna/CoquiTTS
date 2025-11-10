from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
import uuid
import os

app = Flask(__name__)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

@app.route("/speak", methods=["POST"])
def speak():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON or missing Content-Type: application/json"}), 400
        
        text = data.get("text")
        if not text:
            return jsonify({"error": "Missing 'text' in request body"}), 400

        output_path = f"output_{uuid.uuid4().hex}.wav"
        
        try:
            tts.tts_to_file(text=text, file_path=output_path)
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            return jsonify({"error": f"TTS generation failed: {str(e)}"}), 500
        
        response = send_file(output_path, mimetype="audio/wav", as_attachment=False)
        
        @response.call_on_close
        def cleanup():
            if os.path.exists(output_path):
                os.remove(output_path)

        return response
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Coqui TTS API is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
