#!/usr/bin/env python3
"""
Example script demonstrating how to use environment variables with the Advanced TTS Integration.
This example shows how to fetch news from a custom API using credentials from .env file.
"""

import os
from advanced_tts_integration import AdvancedTTSIntegration
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """
    Main function demonstrating the Advanced TTS Integration with environment variables.
    """
    # Get API credentials from environment variables
    news_api_base_url = os.getenv("NEWS_API_BASE_URL")
    news_api_token = os.getenv("NEWS_API_TOKEN")
    
    if not news_api_base_url or not news_api_token:
        print("Error: Missing API credentials in .env file")
        print("Make sure NEWS_API_BASE_URL and NEWS_API_TOKEN are set in the .env file")
        return
    
    print(f"Using News API URL: {news_api_base_url}")
    print(f"API Token (first 10 chars): {news_api_token[:10]}...")
    
    # Create an instance of the Advanced TTS Integration
    tts = AdvancedTTSIntegration(output_dir="news_audio")
    
    # Set up headers with API token
    headers = {
        "Authorization": f"Bearer {news_api_token}",
        "Content-Type": "application/json"
    }
    
    print("\n=== Example: Fetching Latest News Headline ===")
    
    # This is just an example - you'll need to adjust the API endpoint and parameters
    # based on your actual API structure
    try:
        # First fetch the data to inspect its structure
        print("Fetching data from API...")
        data = tts.fetch_data(
            api_url=f"{news_api_base_url}/news?pagination[page]=1&pagination[pageSize]=12&populate=*&sort[0][createdAt]=desc",
            method="GET",
            headers=headers
        )
        
        if data:
            print("API response received successfully.")
            print(f"Response structure: {list(data.keys())}")
            
            # Check if 'data' key exists and is a list
            if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
                print(f"Found {len(data['data'])} news items.")
                
                # Get first news item
                first_news = data['data'][0]
                print(f"First news item structure: {list(first_news.keys()) if isinstance(first_news, dict) else 'Not a dictionary'}")
                
                # Check for news content fields
                if isinstance(first_news, dict):
                    # Check for short_description
                    if 'short_description' in first_news:
                        print(f"Short description found: {first_news['short_description'][:100]}..." if len(first_news['short_description']) > 100 else f"Short description found: {first_news['short_description']}")
                    elif 'title' in first_news:
                        print(f"Title found: {first_news['title']}")
        
        # Only convert short_description field from the first news item
        news_audio = tts.process_pipeline(
            api_url=f"{news_api_base_url}/news?pagination[page]=1&pagination[pageSize]=12&populate=*&sort[0][createdAt]=desc",
            method="GET",
            headers=headers,
            text_key="data.0.short_description",  # Only use short_description from first item in data array
            output_filename="latest_news",
            lang="en"
        )
        
        if news_audio:
            print(f"Generated news audio: {news_audio}")
        else:
            print("Failed to generate news audio with description. Trying with title...")
            
            # Try with title as fallback
            title_audio = tts.process_pipeline(
                api_url=f"{news_api_base_url}/news?pagination[page]=1&pagination[pageSize]=12&populate=*&sort[0][createdAt]=desc",
                method="GET",
                headers=headers,
                text_key="data.0.title",  # Try title as fallback
                output_filename="latest_news_title",
                lang="en"
            )
            
            if title_audio:
                print(f"Generated news audio using title: {title_audio}")
            else:
                print("Failed to generate news audio. Check the log for details.")
                
                # As a fallback, let's use a custom text
                print("\n=== Fallback: Using custom text ===")
                custom_text = "This is a fallback message since we couldn't fetch the latest news."
            
            custom_audio = tts.text_to_speech(
                text=custom_text,
                filename="fallback_message",
                lang="en"
            )
            
            if custom_audio:
                print(f"Generated fallback audio: {custom_audio}")
                print("Playing fallback audio...")
                tts.play_audio(custom_audio)
                
    except Exception as e:
        print(f"Error fetching news: {e}")
        
    print("\nDemo completed!")

if __name__ == "__main__":
    main()
