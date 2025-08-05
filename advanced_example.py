#!/usr/bin/env python3
"""
Example script demonstrating the Advanced TTS Integration with various APIs.
"""

from advanced_tts_integration import AdvancedTTSIntegration

def main():
    """
    Main function demonstrating the Advanced TTS Integration with various APIs.
    """
    # Create an instance of the Advanced TTS Integration
    tts = AdvancedTTSIntegration(output_dir="audio_examples")
    
    print("\n=== Example 1: Using JSON Placeholder API ===")
    # Use JSONPlaceholder API to get a post
    post_audio = tts.process_pipeline(
        api_url="https://jsonplaceholder.typicode.com/posts/1",
        text_key="body",
        output_filename="json_placeholder_post",
        lang="en"
    )
    
    print("\n=== Example 2: Using JSONPlaceholder API with nested data ===")
    # Get user data and comments together
    user_comments_audio = tts.process_pipeline(
        api_url="https://jsonplaceholder.typicode.com/posts/1/comments",
        text_key="0.body",  # Get the first comment's body using dot notation
        output_filename="first_comment",
        lang="en"
    )
    
    print("\n=== Example 3: Using a custom text ===")
    # Directly convert text to speech without using an API
    custom_text = (
        "This is an example of the Advanced Text-to-Speech Integration. "
        "You can use this to convert any text to speech, in various languages "
        "and formats. It supports multiple TTS engines and can extract text "
        "from complex API responses."
    )
    
    custom_audio = tts.text_to_speech(
        text=custom_text,
        filename="custom_message",
        lang="en"
    )
    
    if custom_audio:
        print(f"Generated custom audio: {custom_audio}")
        print("Playing custom audio...")
        tts.play_audio(custom_audio)
    
    print("\n=== Example 4: Converting text to different audio formats ===")
    # Create a TTS instance with WAV as the output format
    tts_wav = AdvancedTTSIntegration(
        output_dir="audio_examples",
        audio_format="wav"
    )
    
    wav_audio = tts_wav.text_to_speech(
        text="This is an example of text converted to WAV format.",
        filename="wav_example",
        lang="en"
    )
    
    if wav_audio:
        print(f"Generated WAV audio: {wav_audio}")
        print("Playing WAV audio...")
        tts_wav.play_audio(wav_audio)
    
    print("\n=== Example 5: Using a different language ===")
    # Convert text to speech in Spanish
    spanish_text = "Hola, esto es un ejemplo de texto en español convertido a voz."
    
    spanish_audio = tts.text_to_speech(
        text=spanish_text,
        filename="spanish_example",
        lang="es"  # Spanish language code
    )
    
    if spanish_audio:
        print(f"Generated Spanish audio: {spanish_audio}")
        print("Playing Spanish audio...")
        tts.play_audio(spanish_audio)
    
    print("\nAll examples completed!")

if __name__ == "__main__":
    main()
