#!/usr/bin/env python3
"""
Example script showing how to use the TTS Integration with a custom API.
"""

from tts_integration import TTSIntegration

def main():
    """
    Main function demonstrating TTS integration with a custom API.
    """
    # Define your API URL
    # This is just an example API that returns JSON data with text
    # Replace with your actual API endpoint
    news_api_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY"
    
    # Weather API example
    weather_api_url = "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"
    
    # Using the placeholder API for demonstration
    placeholder_api = "https://jsonplaceholder.typicode.com/posts/1"
    
    # Initialize the TTS Integration
    tts = TTSIntegration(output_dir="custom_audio")
    
    print("=== Example 1: Using News API ===")
    print("(Commented out - replace YOUR_API_KEY with your actual API key to use)")
    # Uncomment and replace YOUR_API_KEY with your actual API key to use
    # news_audio = tts.process_pipeline(
    #     api_url=news_api_url,
    #     text_key='articles', 
    #     output_filename='latest_news',
    #     lang='en'
    # )
    
    print("\n=== Example 2: Using Placeholder API ===")
    placeholder_audio = tts.process_pipeline(
        api_url=placeholder_api,
        text_key='body',
        output_filename='placeholder_post',
        lang='en'
    )
    
    print("\n=== Example 3: Custom Text ===")
    # Example of directly converting text to speech without API
    custom_text = "This is a demonstration of the Text-to-Speech integration. " \
                 "You can use this to convert any text to speech."
    
    custom_audio = tts.text_to_speech(
        text=custom_text,
        filename='custom_message',
        lang='en'
    )
    
    if custom_audio:
        print(f"Generated custom audio: {custom_audio}")
        print("Playing custom audio...")
        tts.play_audio(custom_audio)

if __name__ == "__main__":
    main()
