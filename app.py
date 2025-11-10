from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
import uuid
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize TTS model
logger.info("Loading TTS model...")
try:
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
    logger.info("TTS model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load TTS model: {e}")
    raise

@app.route("/speak", methods=["POST"])
def speak():
    try:
        logger.info("Received /speak request")
        data = request.get_json()
        if not data:
            logger.warning("Invalid JSON or missing Content-Type")
            return jsonify({"error": "Invalid JSON or missing Content-Type: application/json"}), 400
        
        text = data.get("text")
        if not text:
            logger.warning("Missing 'text' in request body")
            return jsonify({"error": "Missing 'text' in request body"}), 400

        logger.info(f"Generating TTS for text: {text[:50]}...")
        output_path = f"output_{uuid.uuid4().hex}.wav"
        
        try:
            tts.tts_to_file(text=text, file_path=output_path)
            logger.info(f"TTS generated successfully: {output_path}")
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            if os.path.exists(output_path):
                os.remove(output_path)
            return jsonify({"error": f"TTS generation failed: {str(e)}"}), 500
        
        response = send_file(output_path, mimetype="audio/wav", as_attachment=False)
        
        @response.call_on_close
        def cleanup():
            if os.path.exists(output_path):
                os.remove(output_path)
                logger.info(f"Cleaned up: {output_path}")

        return response
    except Exception as e:
        logger.error(f"Internal server error: {e}", exc_info=True)
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def index():
    logger.info("Health check request received")
    return jsonify({"message": "Coqui TTS API is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
