# Qwen3 TTS Voice Cloning

Generate high-quality speech with voice cloning using Qwen3-TTS model.

## Quick Start

### Prerequisites

- Docker

### Generate Audio

```bash
# Using run.sh (recommended)
./run.sh --text "Hello, this is a test of the voice cloning system."

# With custom voice
./run.sh --ref-audio trump.mp3 --text "I will make America great again."

# All parameters
./run.sh --ref-audio trump.mp3 --text "Your text here" --language english --ref-text "Reference text for better cloning" --name myoutput
```

## Parameters

- `--ref-audio`: Reference audio file for voice cloning (default: `trump.mp3`, must be present in repository)
- `--text`: Text to synthesize (required)
- `--ref-text`: Optional reference text from the audio for improved cloning
- `--language`: Language code (default: `english`, supports auto, chinese, english, french, german, italian, japanese, korean, portuguese, russian, spanish)
- `--name`: Custom output filename (without path/extension, stored in `/app/`)

## Output

- Saved as `/app/<timestamp>_<sanitized_text[:20]>.wav` or `/app/<name>.wav`
- Filename: lowercase, `_` separators, timestamp prefixed

## Model

- Uses `Qwen/Qwen3-TTS-12Hz-1.7B-Base`
- Automatically downloaded and cached in `./models/Qwen3-TTS-12Hz-1.7B-Base`

See `AGENTS.md` for development guidelines.
