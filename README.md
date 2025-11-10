# CoquiTTS API

A Flask-based REST API for text-to-speech conversion using Coqui TTS. This service provides an easy-to-use endpoint to convert text into speech audio files.

## Features

- 🎤 Text-to-speech conversion using Coqui TTS
- 🌐 RESTful API with Flask
- 🐳 Docker containerization support
- 🔊 Returns audio files in WAV format
- 🧹 Automatic cleanup of temporary files

## Prerequisites

- Python 3.9 or higher
- Docker (optional, for containerized deployment)
- Git (for installing Coqui TTS)

## Installation

### Local Installation

1. Clone this repository:
```bash
git clone https://github.com/TharinduWijayarathna/CoquiTTS.git
cd CoquiTTS
```

2. Install system dependencies (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install -y git ffmpeg libsndfile1
```

3. Install Coqui TTS:
```bash
git clone https://github.com/coqui-ai/TTS.git
pip install -e TTS
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Docker Installation

1. Build the Docker image:
```bash
docker build -t coquitts-api .
```

2. Run the container:
```bash
docker run -p 5000:5000 coquitts-api
```

## Usage

### Starting the Server

**Local:**
```bash
python app.py
```

**Docker:**
```bash
docker run -p 5000:5000 coquitts-api
```

The API will be available at `http://localhost:5000`

### API Endpoints

#### GET `/`
Health check endpoint that returns the API status.

**Response:**
```json
{
  "message": "Coqui TTS API is running"
}
```

#### POST `/speak`
Converts text to speech and returns an audio file.

**Request Body:**
```json
{
  "text": "Hello, this is a test message."
}
```

**Response:**
- Success: Returns a WAV audio file (Content-Type: `audio/wav`)
- Error: Returns JSON with error message and status code 400

**Example using cURL:**
```bash
curl -X POST http://localhost:5000/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, world!"}' \
  --output output.wav
```

**Example using Python:**
```python
import requests

response = requests.post(
    'http://localhost:5000/speak',
    json={'text': 'Hello, this is a test message.'}
)

if response.status_code == 200:
    with open('output.wav', 'wb') as f:
        f.write(response.content)
    print("Audio file saved as output.wav")
else:
    print(f"Error: {response.json()}")
```

## Technical Details

- **TTS Model:** `tts_models/en/ljspeech/tacotron2-DDC`
- **Framework:** Flask
- **Python Version:** 3.9+
- **Port:** 5000
- **Audio Format:** WAV

## Notes

- The API automatically cleans up temporary audio files after sending the response
- The TTS model is loaded once at startup for better performance
- GPU support is disabled by default (can be enabled by modifying `gpu=False` in `app.py`)
