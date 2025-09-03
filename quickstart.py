#!/usr/bin/env python3
"""
Quick Start Script for Gemini TTS.
This script provides an interactive way to test the Gemini TTS integration.
"""

import os
import sys
import readline  # For better input handling
from dotenv import load_dotenv
from gemini_tts_integration import GeminiTTSIntegration

def setup_gemini_api():
    """Check if Gemini API is configured and help set it up if not."""
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        print("No Gemini API key found in .env file.")
        setup_key = input("Would you like to set up a Gemini API key now? (y/n): ").lower()
        
        if setup_key == 'y':
            print("\nTo get a Gemini API key:")
            print("1. Go to https://ai.google.dev/ and sign in")
            print("2. Click on 'Get API key' in the top navigation")
            print("3. Create a new API key or use an existing one")
            
            new_key = input("\nEnter your Gemini API key: ").strip()
            
            if new_key:
                # Update .env file
                env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
                
                # Read existing .env content
                env_content = ""
                if os.path.exists(env_path):
                    with open(env_path, 'r') as f:
                        env_content = f.read()
                
                # Update or add the GEMINI_API_KEY
                if "GEMINI_API_KEY=" in env_content:
                    # Replace existing key
                    lines = env_content.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith("GEMINI_API_KEY="):
                            lines[i] = f"GEMINI_API_KEY={new_key}"
                    
                    env_content = '\n'.join(lines)
                else:
                    # Add new key
                    env_content += f"\nGEMINI_API_KEY={new_key}\n"
                
                # Write back to .env file
                with open(env_path, 'w') as f:
                    f.write(env_content)
                
                print("API key saved to .env file.")
                gemini_api_key = new_key
            else:
                print("No API key provided. Using Google TTS fallback.")
        else:
            print("Continuing without Gemini API. Using Google TTS fallback.")
    
    return gemini_api_key

def main():
    """Main function to test Gemini TTS."""
    print("===== Gemini TTS Quick Start =====")
    
    # Setup Gemini API
    gemini_api_key = setup_gemini_api()
    
    # Initialize TTS
    tts = GeminiTTSIntegration(
        output_dir="gemini_audio",
        gemini_api_key=gemini_api_key
    )
    
    # Check if Gemini is available
    if tts.gemini_available:
        print("\nGemini API is properly configured and working!")
    else:
        print("\nGemini API is not available. Using Google TTS fallback.")
    
    # Interactive loop
    while True:
        print("\nOptions:")
        print("1. Convert text to speech")
        print("2. Convert news to speech")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            text = input("\nEnter text to convert to speech: ")
            if text:
                filename = input("Enter output filename (leave empty for default): ")
                
                if not filename:
                    filename = "gemini_quickstart"
                
                print(f"\nConverting text to speech...")
                audio_file = tts.text_to_speech(text=text, filename=filename)
                
                if audio_file:
                    print(f"Generated audio file: {audio_file}")
                    play = input("Play the audio? (y/n): ").lower()
                    if play == 'y':
                        tts.play_audio(audio_file)
                else:
                    print("Failed to generate audio file.")
            else:
                print("No text provided.")
                
        elif choice == '2':
            print("\nFetching news data...")
            
            # Get API credentials from environment variables
            news_api_base_url = os.getenv("NEWS_API_BASE_URL")
            news_api_token = os.getenv("NEWS_API_TOKEN")
            
            if not news_api_base_url or not news_api_token:
                print("Error: Missing news API credentials in .env file.")
                print("Make sure NEWS_API_BASE_URL and NEWS_API_TOKEN are set.")
                continue
            
            # Set up headers with API token
            headers = {
                "Authorization": f"Bearer {news_api_token}",
                "Content-Type": "application/json"
            }
            
            # Fetch news data
            data = tts.fetch_data(
                api_url=f"{news_api_base_url}/news?pagination[page]=1&pagination[pageSize]=12&populate=*&sort[0][createdAt]=desc",
                method="GET",
                headers=headers
            )
            
            if not data or 'data' not in data or not isinstance(data['data'], list) or len(data['data']) == 0:
                print("No news data found.")
                continue
            
            # Display available news items
            print("\nAvailable news items:")
            for i, item in enumerate(data['data'][:5]):  # Show first 5 items
                if 'title' in item:
                    print(f"{i+1}. {item['title']}")
                else:
                    print(f"{i+1}. [Untitled news item]")
            
            # Select a news item
            selection = input("\nSelect a news item (1-5): ")
            try:
                index = int(selection) - 1
                if index < 0 or index >= len(data['data'][:5]):
                    print("Invalid selection.")
                    continue
                
                selected_news = data['data'][index]
                
                if 'short_description' in selected_news and selected_news['short_description']:
                    print(f"\nConverting news to speech: {selected_news['title']}")
                    audio_file = tts.text_to_speech(
                        text=selected_news['short_description'],
                        filename=f"news_item_{index+1}"
                    )
                    
                    if audio_file:
                        print(f"Generated audio file: {audio_file}")
                        play = input("Play the audio? (y/n): ").lower()
                        if play == 'y':
                            tts.play_audio(audio_file)
                    else:
                        print("Failed to generate audio file.")
                else:
                    print("No description available for this news item.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            
        elif choice == '3':
            print("\nExiting. Thank you for using Gemini TTS!")
            break
        
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting. Thank you for using Gemini TTS!")
        sys.exit(0)
