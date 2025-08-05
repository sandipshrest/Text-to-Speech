#!/usr/bin/env python3
"""
Text-to-Speech Integration Script
Fetches data from an API, extracts text, and converts it to speech.
"""

import requests
import json
import os
from gtts import gTTS  # Google Text-to-Speech
import pygame  # For audio playback
from pydub import AudioSegment  # For audio file manipulation
import time

class TTSIntegration:
    def __init__(self, api_url=None, output_dir="audio_output"):
        """
        Initialize the TTS Integration class.
        
        Args:
            api_url (str): URL to fetch text data from
            output_dir (str): Directory to save audio files
        """
        self.api_url = api_url
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
    
    def fetch_data(self, api_url=None):
        """
        Fetch data from the specified API.
        
        Args:
            api_url (str): URL to fetch data from (overrides instance variable if provided)
            
        Returns:
            dict: JSON response from the API
        """
        url = api_url or self.api_url
        
        if not url:
            raise ValueError("API URL must be provided")
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return None
    
    def extract_text(self, data, text_key='text'):
        """
        Extract text from the data.
        
        Args:
            data (dict): Data containing text
            text_key (str): Key to extract text from
            
        Returns:
            str: Extracted text
        """
        if not data:
            return ""
        
        # Handle different data structures
        if isinstance(data, dict):
            # If text_key exists in the data, return its value
            if text_key in data:
                return data[text_key]
            
            # Recursive search in nested dictionaries
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    result = self.extract_text(value, text_key)
                    if result:
                        return result
                elif key == text_key:
                    return value
        
        # Handle list type data
        elif isinstance(data, list):
            # Concatenate all text items in the list
            all_text = []
            for item in data:
                extracted = self.extract_text(item, text_key)
                if extracted:
                    all_text.append(extracted)
            
            return " ".join(all_text)
        
        return ""
    
    def text_to_speech(self, text, filename=None, lang='en'):
        """
        Convert text to speech and save as an audio file.
        
        Args:
            text (str): Text to convert to speech
            filename (str): Output filename (without extension)
            lang (str): Language code
            
        Returns:
            str: Path to the saved audio file
        """
        if not text:
            print("No text provided for conversion")
            return None
        
        # Generate filename if not provided
        if not filename:
            timestamp = int(time.time())
            filename = f"tts_output_{timestamp}"
        
        # Add extension if not present
        if not filename.endswith('.mp3'):
            filename += '.mp3'
        
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            # Convert text to speech
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(output_path)
            print(f"Text converted to speech and saved as '{output_path}'")
            return output_path
        except Exception as e:
            print(f"Error converting text to speech: {e}")
            return None
    
    def play_audio(self, audio_file):
        """
        Play the audio file.
        
        Args:
            audio_file (str): Path to the audio file
        """
        if not os.path.exists(audio_file):
            print(f"Audio file not found: {audio_file}")
            return
        
        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def process_pipeline(self, api_url=None, text_key='text', output_filename=None, lang='en'):
        """
        Run the complete pipeline: fetch data, extract text, convert to speech, and play.
        
        Args:
            api_url (str): API URL to fetch data from
            text_key (str): Key to extract text from the data
            output_filename (str): Output audio filename
            lang (str): Language code for TTS
            
        Returns:
            str: Path to the generated audio file
        """
        # Fetch data from API
        data = self.fetch_data(api_url)
        
        if not data:
            print("No data fetched from API")
            return None
        
        # Extract text from data
        text = self.extract_text(data, text_key)
        
        if not text:
            print("No text extracted from data")
            return None
        
        print(f"Extracted text: {text[:100]}..." if len(text) > 100 else f"Extracted text: {text}")
        
        # Convert text to speech
        audio_file = self.text_to_speech(text, output_filename, lang)
        
        if audio_file and os.path.exists(audio_file):
            # Play the audio
            self.play_audio(audio_file)
        
        return audio_file


# Example usage
if __name__ == "__main__":
    # Example API URL (replace with your actual API)
    API_URL = "https://jsonplaceholder.typicode.com/posts/1"
    
    # Create TTS integration instance
    tts_integration = TTSIntegration(api_url=API_URL)
    
    # Run the complete pipeline
    audio_file = tts_integration.process_pipeline(text_key='body')
    
    if audio_file:
        print(f"Generated audio file: {audio_file}")
    else:
        print("Failed to generate audio file")
