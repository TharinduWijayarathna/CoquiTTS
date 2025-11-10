FROM python:3.9-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y git ffmpeg libsndfile1 && \
    apt-get clean

# Set workdir
WORKDIR /app

# Install Coqui TTS
RUN git clone https://github.com/coqui-ai/TTS.git /app/TTS && \
    pip install -e /app/TTS

# Copy app files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Expose port
EXPOSE 5000

CMD ["python", "app.py"]
