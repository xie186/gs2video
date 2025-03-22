# GS2Video

GS2Video is a Python tool that converts Google Slides presentations into videos. It uses Google Slides API to fetch the presentation content, generates audio using Google Text-to-Speech (gTTS) and Kokoro TTS, and creates a video with transitions between slides.

## Features

- Convert Google Slides presentations to videos
- Generate audio using Google Text-to-Speech (gTTS) and Kokoro TTS
- Add custom background color and duration for slide transitions
- Keep or remove intermediate files (mp3 and png files)
- Force overwrite existing output video files

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/gs2video.git
    cd gs2video
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up Google API credentials:
    - Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
    - Enable the Google Slides API for your project.
    - Create OAuth 2.0 credentials and download the JSON file.
    - Save the JSON file as `gs2slide-1eb92b075bce.json` in the project directory.

## Usage

### Command Line Interface (CLI)

The CLI allows you to convert Google Slides presentations to videos with various options.

#### Example Command

```bash
python -m gs2slide.cli -p <presentation_id> -o output.mp4 --fps 24 --language en --keep --force --duration 1 --bg_color 0,0,0
```

#### Arguments

- `-p`, `--presentation_id`: The ID of the Google Slides presentation (required).
- `-f`, `--fps`: Frames per second (FPS) for the output video (default: 24).
- `-l`, `--language`: Language for the text-to-speech (default: 'en').
- `--keep`: Keep intermediate files (mp3 and png files).
- `--force`: Force generate the output video even if it already exists.
- `--duration`: Duration of each slide in seconds (default: 0.5).
- `--bg_color`: Background color during transitions (RGB values as comma-separated integers, default: (0, 0, 0)).
- `-o`, `--output`: Output video file (default: "Output_file.mp4").

### Example

```bash
python -m gs2slide.cli -p 1A2B3C4D5E6F7G8H9I0J -o my_presentation.mp4 --fps 30 --language en --keep --force --duration 2 --bg_color 255,255,255
```

## Design

### Project Structure

```
gs2video/
├── gs2slide/
│   ├── __init__.py
│   ├── cli.py
│   ├── core.py
│   └── utils.py
├── .gitignore
├── README.md
└── requirements.txt
```

### Core Components

- **`gs2slide/core.py`**: Contains the `GS2Video` class that handles the conversion of Google Slides presentations to videos.
- **`gs2slide/cli.py`**: Provides the command line interface for the tool.
- **`gs2slide/utils.py`**: Contains utility functions, including the `credential` function for Google API authentication.

### GS2Video Class

The `GS2Video` class is responsible for:

- Initializing with credentials, output file, language, FPS, and other options.
- Fetching the presentation content using Google Slides API.
- Generating audio for each slide using gTTS and Kokoro TTS.
- Creating video clips for each slide and concatenating them with transitions.
- Saving the final video to the specified output file.

#### Methods

- `__init__(self, credentials, output, language='en', fps=24, keep=False, force=False, duration=1, bg_color=(0, 0, 0))`: Initializes the `GS2Video` object.
- `check_output(self)`: Checks if the output file already exists and exits if it does, unless the `force` option is set.
- `prep_cache_dir(self)`: Prepares the cache directory based on the output file name.
- `generate_hash(self, content)`: Generates an MD5 hash for the given content.
- `rmtem(self)`: Removes temporary files.
- `to_video(self, presentation_id)`: Converts the Google Slides presentation to a video.
- `process_slide(self, slide, video_hash, index, presentation_id)`: Processes each slide to generate audio and image clips.
- `process_audio(self, text, text_hash, index)`: Generates audio for the given text using gTTS.
- `process_image(self, slide, video_hash, index, presentation_id)`: Downloads the slide image and saves it to the cache.
- `process_audio_kokoro(self, text, text_hash, index)`: Generates audio for the given text using Kokoro TTS.
- `extract_terms_and_ipa(self, presentation_id)`: Extracts terms and their IPA pronunciations from the slide notes.
- `replace_terms_with_ipa(self, text, terms_ipa)`: Replaces terms in the text with their IPA pronunciations.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [Google Slides API](https://developers.google.com/slides)
- [gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS/)
- [Kokoro TTS](https://github.com/yourusername/kokoro-tts)
- [MoviePy](https://zulko.github.io/moviepy/)
- [Misaki G2P](https://github.com/yourusername/misaki-g2p)



