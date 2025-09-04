#!/usr/bin/env python3
"""
API Server for News Text-to-Speech Generation
Provides endpoints to convert news articles to speech using Gemini TTS.
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gemini_tts_integration import GeminiTTSIntegration

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tts_api_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TTSAPIServer")

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Gemini TTS
tts = GeminiTTSIntegration(
    output_dir="api_audio_output",
    gemini_api_key=os.getenv("GEMINI_API_KEY")
)

# Get API credentials from environment variables
NEWS_API_BASE_URL = os.getenv("NEWS_API_BASE_URL")
NEWS_API_TOKEN = os.getenv("NEWS_API_TOKEN")
PORT = os.getenv("PORT", 5000)

# Set up headers with API token
API_HEADERS = {
    "Authorization": f"Bearer {NEWS_API_TOKEN}",
    "Content-Type": "application/json"
}


@app.route('/api/news-audio/<news_id>', methods=['GET'])
def get_news_audio(news_id):
    """
    API endpoint to get audio for a specific news article by ID.
    
    Args:
        news_id: The ID of the news article
        
    Returns:
        JSON response with audio URL or error message
    """
    try:
        logger.info(f"Received request for news audio with ID: {news_id}")
        
        # Validate news_id
        if not news_id:
            return jsonify({
                "success": False,
                "error": "News ID is required"
            }), 400
        
        # Build API URL with all the required parameters
        api_url = f"{NEWS_API_BASE_URL}/news/{news_id}?populate[companies]=true&populate[categories]=true&populate[thumbnail]=true&sort[0][createdAt]=desc"
        
        logger.info(f"Fetching news data from: {api_url}")
        
        # Fetch news data
        news_data = tts.fetch_data(
            api_url=api_url,
            method="GET",
            headers=API_HEADERS
        )
        
        if not news_data:
            return jsonify({
                "success": False,
                "error": "Failed to fetch news data"
            }), 500
            
        # Check if data contains the necessary information
        if 'data' not in news_data or not news_data['data']:
            return jsonify({
                "success": False,
                "error": "News article not found"
            }), 404
        
        # Extract news content for TTS
        news_content = news_data['data']
        
        # Determine which field to use for TTS (prioritize content, then short_description, then title)
        tts_text = None
        content_source = None
        
        if 'attributes' in news_content:
            attributes = news_content['attributes']
            
            if 'content' in attributes and attributes['content']:
                tts_text = attributes['content']
                content_source = 'content'
            elif 'short_description' in attributes and attributes['short_description']:
                tts_text = attributes['short_description']
                content_source = 'short_description'
            elif 'title' in attributes and attributes['title']:
                tts_text = attributes['title']
                content_source = 'title'
        
        if not tts_text:
            return jsonify({
                "success": False,
                "error": "No content available for text-to-speech conversion"
            }), 404
            
        # Generate a unique filename based on news ID and content source
        filename = f"news_{news_id}_{content_source}"
        
        logger.info(f"Converting news to speech: {filename}")
        
        # Convert text to speech
        audio_file = tts.text_to_speech(
            text=tts_text,
            filename=filename,
            lang="en"  # You can make this configurable if needed
        )
        
        if not audio_file:
            return jsonify({
                "success": False,
                "error": "Failed to generate audio file"
            }), 500
            
        # Get the relative path from the output directory
        audio_filename = os.path.basename(audio_file)
        
        # Generate audio URL
        # In a production environment, you might want to use a CDN or cloud storage
        audio_url = request.url_root + f"api/audio/{audio_filename}"
        
        # Get information about the audio processing
        tts_engine = "Gemini API" if tts.gemini_available else "Google TTS (fallback)"
        
        # Return success response with audio URL
        return jsonify({
            "success": True,
            "data": {
                "news_id": news_id,
                "audio_url": audio_url,
                "content_source": content_source,
                "tts_engine": tts_engine,
                "news_title": news_content.get('attributes', {}).get('title', 'Untitled')
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


@app.route('/api/audio/<filename>', methods=['GET'])
def get_audio_file(filename):
    """
    Serve the generated audio files.
    
    Args:
        filename: The filename of the audio file
        
    Returns:
        Audio file as attachment
    """
    try:
        return send_from_directory(tts.output_dir, filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Error serving audio file: {e}")
        return jsonify({
            "success": False,
            "error": f"Audio file not found: {str(e)}"
        }), 404


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint.
    
    Returns:
        JSON response with server status
    """
    # Check if TTS engine is working
    tts_status = "operational" if tts is not None else "unavailable"
    
    # Check if Gemini API is available
    gemini_status = "available" if tts.gemini_available else "unavailable (using fallback)"
    
    # Check if news API is accessible
    news_api_status = "unknown"
    try:
        # Simple check to see if we can hit the news API
        test_response = tts.fetch_data(
            api_url=f"{NEWS_API_BASE_URL}/news?pagination[page]=1&pagination[pageSize]=1",
            method="GET",
            headers=API_HEADERS
        )
        news_api_status = "accessible" if test_response else "inaccessible"
    except Exception:
        news_api_status = "inaccessible"
    
    return jsonify({
        "status": "healthy",
        "services": {
            "tts_engine": tts_status,
            "gemini_api": gemini_status,
            "news_api": news_api_status
        },
        "version": "1.0.0"
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Resource not found"
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == "__main__":
    # Create output directory if it doesn't exist
    if not os.path.exists(tts.output_dir):
        os.makedirs(tts.output_dir)
        
    # Check if API credentials are available
    if not NEWS_API_BASE_URL or not NEWS_API_TOKEN:
        logger.error("Missing API credentials. Please set NEWS_API_BASE_URL and NEWS_API_TOKEN in .env file.")
        exit(1)
        
    logger.info("Starting TTS API Server...")
    logger.info(f"News API URL: {NEWS_API_BASE_URL}")
    logger.info(f"Gemini API available: {tts.gemini_available}")
    logger.info(f"Audio output directory: {tts.output_dir}")
    
    # Run the Flask app
    # In production, use a proper WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=PORT, debug=True)
