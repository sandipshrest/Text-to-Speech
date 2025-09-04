#!/usr/bin/env python3
"""
Test client for the TTS API Server.
This script demonstrates how to use the News Audio API.
"""

import sys
import requests
import argparse
import webbrowser
from urllib.parse import urljoin

def test_health(base_url):
    """Test the health endpoint."""
    health_url = urljoin(base_url, "api/health")
    response = requests.get(health_url)
    
    print(f"Health Check Response (Status {response.status_code}):")
    if response.status_code == 200:
        print(response.json())
        return True
    else:
        print(f"Error: {response.text}")
        return False

def get_news_audio(base_url, news_id):
    """Get audio for a specific news ID."""
    audio_url = urljoin(base_url, f"api/news-audio/{news_id}")
    print(f"Requesting audio for news ID: {news_id}")
    print(f"URL: {audio_url}")
    
    response = requests.get(audio_url)
    
    print(f"Response (Status {response.status_code}):")
    if response.status_code == 200:
        result = response.json()
        print(result)
        
        # Check if successful and audio URL is available
        if result.get("success") and "audio_url" in result.get("data", {}):
            audio_url = result["data"]["audio_url"]
            print(f"\nAudio URL: {audio_url}")
            
            # Ask if user wants to open in browser
            open_browser = input("Do you want to open the audio in your web browser? (y/n): ").lower()
            if open_browser == 'y':
                webbrowser.open(audio_url)
            
            # Download the file
            download = input("Do you want to download the audio file? (y/n): ").lower()
            if download == 'y':
                download_url = audio_url
                filename = download_url.split("/")[-1]
                
                print(f"Downloading to {filename}...")
                audio_response = requests.get(download_url)
                
                if audio_response.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(audio_response.content)
                    print(f"File downloaded: {filename}")
                else:
                    print(f"Error downloading file: {audio_response.status_code}")
        
        return True
    else:
        print(f"Error: {response.text}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test the TTS API Server')
    parser.add_argument('--url', default='http://localhost:5000/', help='Base URL of the API server')
    parser.add_argument('--news-id', help='News ID to convert to audio')
    parser.add_argument('--health', action='store_true', help='Check API server health')
    
    args = parser.parse_args()
    
    if args.health:
        test_health(args.url)
    elif args.news_id:
        get_news_audio(args.url, args.news_id)
    else:
        print("Please specify either --health or --news-id")
        parser.print_help()

if __name__ == "__main__":
    main()
