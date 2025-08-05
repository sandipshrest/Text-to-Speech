# Text-to-Speech Integration

This project provides tools for integrating text-to-speech capabilities with various APIs, allowing you to fetch data, extract text, and convert it to speech.

## Features

### Basic TTS Integration (`tts_integration.py`)
- Fetch data from API endpoints
- Extract text from JSON responses
- Convert text to speech using Google TTS
- Play audio using pygame
- Save audio files for later use

### Advanced TTS Integration (`advanced_tts_integration.py`)
- Support for multiple TTS engines
- Multiple audio formats (MP3, WAV, OGG)
- Enhanced API data extraction with path navigation
- Improved error handling and logging
- Support for different HTTP methods (GET, POST)
- Audio file format conversion
- Various playback options

## Requirements

- Python 3.6+
- Internet connection (for API access and Google TTS)

## Installation

1. Clone this repository or download the files
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   # On Linux/macOS
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```
4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the basic script with default settings:

```bash
python tts_integration.py
```

Or run the example script:

```bash
python example.py
```

### Advanced Usage

Run the advanced script:

```bash
python advanced_tts_integration.py
```

Or run the advanced example script:

```bash
python advanced_example.py
```

### Integration in Your Own Code

#### Basic TTS Integration

```python
from tts_integration import TTSIntegration

# Initialize with custom API URL and output directory
tts = TTSIntegration(
    api_url="https://your-api-endpoint.com/data",
    output_dir="custom_audio_folder"
)

# Run the complete pipeline with custom parameters
audio_file = tts.process_pipeline(
    text_key='content',      # The key to extract text from in the JSON response
    output_filename='my_audio',  # Custom filename for the output audio
    lang='fr'                # Language code (default is 'en' for English)
)

# Or run individual steps
data = tts.fetch_data()
text = tts.extract_text(data, text_key='body')
audio_file = tts.text_to_speech(text, filename='speech_output')
tts.play_audio(audio_file)
```

#### Advanced TTS Integration

```python
from advanced_tts_integration import AdvancedTTSIntegration

# Initialize with custom settings
tts = AdvancedTTSIntegration(
    api_url="https://your-api-endpoint.com/data",
    output_dir="custom_audio_folder",
    tts_engine="gtts",       # TTS engine to use
    audio_format="wav"       # Output audio format
)

# Run the complete pipeline with custom parameters
audio_file = tts.process_pipeline(
    method="POST",           # HTTP method
    headers={"Authorization": "Bearer YOUR_TOKEN"},  # Custom headers
    params={"param1": "value1"},  # URL parameters
    json_data={"key": "value"},  # JSON data for POST requests
    text_key='content',      # The key to extract text from in the JSON response
    output_filename='my_audio',  # Custom filename for the output audio
    lang='fr',               # Language code (default is 'en' for English)
    max_length=1000,         # Maximum text length to process
    auto_play=True           # Whether to automatically play the audio
)
```

## Customization

### Basic TTS Integration
- Change the API URL in the script to fetch data from different sources
- Modify the `text_key` parameter to extract text from different fields in the API response
- Change the language using the `lang` parameter (e.g., 'en' for English, 'fr' for French)

### Advanced TTS Integration
- Choose different TTS engines (currently supports Google TTS)
- Select output audio formats (MP3, WAV, OGG)
- Use dot notation to extract text from complex nested structures
- Set maximum text length for processing
- Configure HTTP request parameters (headers, method, etc.)
- Enable/disable auto-playback of generated audio

## Supported TTS Engines

Currently, the following TTS engines are supported:

- `gtts`: Google Text-to-Speech (default)

## Supported Audio Formats

- MP3: MPEG Audio Layer III (default)
- WAV: Waveform Audio File Format
- OGG: Ogg Vorbis Audio

## Supported Languages

The script uses Google TTS which supports multiple languages. Use the appropriate language code:

- English: 'en'
- French: 'fr'
- Spanish: 'es'
- German: 'de'
- Italian: 'it'
- And many more...

## Troubleshooting

- Ensure you have an active internet connection
- Check that the API URL is correct and accessible
- Make sure the required packages are installed
- Verify that your system has audio capabilities for playback
- Check the log file (`tts_integration.log`) for detailed error information in the advanced version

## License

This project is licensed under the MIT License.
