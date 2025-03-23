# GS2Video

GS2Video is a Python tool that converts Google Slides presentations into videos. It uses Google Slides API to fetch the presentation content, generates audio using Kokoro TTS, and creates a video with transitions between slides.

## Features

- Convert Google Slides presentations to videos
- Generate audio using Kokoro TTS
- Add custom background color and duration for slide transitions
- Keep or remove intermediate files (mp3 and png files)
- Force overwrite existing output video files

## Support Me
Like what I do, Please consider supporting me.

<a href="https://coindrop.to/xie186" target="_blank"><img src="https://coindrop.to/embed-button.png" style="border-radius: 10px;" alt="Coindrop.to me" style="height: 57px !important;width: 229px !important;" ></a>

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
    pip install -r .devcontainer/requirements.txt
    ```

4. Set up Google API credentials:
    - Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
    - Enable the Google Slides API for your project.
    - Create OAuth 2.0 credentials and download the JSON file.
    - Save the JSON file as `gs2slide-credential.json` in the project directory.

## Usage

### Command Line Interface (CLI)

The CLI allows you to convert Google Slides presentations to videos with various options.

#### Example Command

```bash
python -m gs2video.cli -p <presentation_id> -o output.mp4 --fps 24 --language en --keep --force --duration 1 --bg_color 0,0,0
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
python -m gs2video.cli -p 1A2B3C4D5E6F7G8H9I0J -o my_presentation.mp4 --fps 30 --language en --keep --force --duration 2 --bg_color 255,255,255
```

## Design

### Project Structure

```
gs2video/
├── gs2video/
│   ├── __init__.py
│   ├── cli.py
│   ├── core.py
│   └── utils.py
├── .gitignore
├── README.md
└── requirements.txt
```

### Core Components

- **`gs2video/core.py`**: Contains the `GS2Video` class that handles the conversion of Google Slides presentations to videos.
- **`gs2video/cli.py`**: Provides the command line interface for the tool.
- **`gs2video/utils.py`**: Contains utility functions, including the `credential` function for Google API authentication.

### GS2Video Class

The `GS2Video` class is responsible for:

- Initializing with credentials, output file, language, FPS, and other options.
- Fetching the presentation content using Google Slides API.
- Generating audio for each slide using Kokoro TTS.
- Creating video clips for each slide and concatenating them with transitions.
- Saving the final video to the specified output file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [Google Slides API](https://developers.google.com/slides)
- [Kokoro TTS](https://github.com/yourusername/kokoro-tts)
- [MoviePy](https://zulko.github.io/moviepy/)
- [Misaki G2P](https://github.com/yourusername/misaki-g2p)



