# News Text-to-Speech API Server

This API server provides endpoints to convert news articles to speech using Gemini TTS integration.

## Features

- **News Audio Endpoint**: Get audio for a specific news article by ID
- **Audio Serving**: Serve generated audio files
- **Health Check**: Monitor the health of the API server and its dependencies
- **Fallback Mechanisms**: Automatically falls back to Google TTS if Gemini API is unavailable

## Prerequisites

- Python 3.6+
- News API credentials
- Gemini API key (optional, falls back to Google TTS if not available)
- Flask and Flask-CORS

## Installation

1. Ensure you have installed the required packages:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in your `.env` file:
```
NEWS_API_BASE_URL="https://news.peridot.com.np/api"
NEWS_API_TOKEN="your_news_api_token"
GEMINI_API_KEY="your_gemini_api_key"
```

## Running the Server

Start the API server:

```bash
./tts_api_server.py
```

The server will run on `http://localhost:5000` by default.

## API Endpoints

### 1. Get News Audio

**Endpoint**: `/api/news-audio/<news_id>`

**Method**: GET

**Parameters**:
- `news_id`: The ID of the news article to convert to speech

**Response**:
```json
{
  "success": true,
  "data": {
    "news_id": "123",
    "audio_url": "http://localhost:5000/api/audio/news_123_content.mp3",
    "content_source": "content",
    "tts_engine": "Gemini API",
    "news_title": "Sample News Title"
  }
}
```

### 2. Get Audio File

**Endpoint**: `/api/audio/<filename>`

**Method**: GET

**Parameters**:
- `filename`: The filename of the audio file to retrieve

**Response**: Audio file download

### 3. Health Check

**Endpoint**: `/api/health`

**Method**: GET

**Response**:
```json
{
  "status": "healthy",
  "services": {
    "tts_engine": "operational",
    "gemini_api": "available",
    "news_api": "accessible"
  },
  "version": "1.0.0"
}
```

## Testing the API

Use the provided test client:

```bash
# Check API health
./test_api_client.py --health

# Get audio for a news article
./test_api_client.py --news-id 123
```

## Integration Example

```python
import requests

# Get audio for a news article
response = requests.get("http://localhost:5000/api/news-audio/123")

if response.status_code == 200:
    result = response.json()
    if result["success"]:
        audio_url = result["data"]["audio_url"]
        print(f"Audio URL: {audio_url}")
```

## Deployment Considerations

For production deployment:

1. Use a production WSGI server like Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 tts_api_server:app
```

2. Set `debug=False` in the Flask app

3. Consider using a reverse proxy like Nginx

4. Implement proper authentication for the API

5. Use a CDN or cloud storage for serving audio files
