# Qwen3 TTS Voice Cloning

Generate high-quality speech with voice cloning using Qwen3-TTS model.

## Quick Start

### Prerequisites
- Docker (recommended)
- Or Python 3.12+ with dependencies

### Download Models (first time)
```bash
./download.sh
```

### Generate Audio
```bash
# Using run.sh (recommended)
./run.sh --text "Hello, this is a test of the voice cloning system."

# With custom voice
./run.sh --ref-audio trump.mp3 --text "I will make America great again."

# All parameters
./run.sh --ref-audio trump.mp3 --text "Your text here" --language en --ref-text "Reference text for better cloning" --name myoutput
```

### Python directly
```bash
python generate.py --text "Hello world" --ref-audio trump.mp3 --language en
```

## Parameters
- `--ref-audio`: Reference audio file for voice cloning (default: `trump.mp3`)
- `--text`: Text to synthesize (required)
- `--ref-text`: Optional reference text from the audio for improved cloning
- `--language`: Language code (default: `en`, supports en, de, etc.)
- `--name`: Custom output filename (without path/extension, stored in `/app/`)

## Output
- Saved as `/app/<timestamp>_<sanitized_text[:20]>.wav` or `/app/<name>.wav`
- Filename: lowercase, `_` separators, timestamp prefixed

## Docker
```bash
docker compose up
# Or
docker compose run --rm qwen-tts ./run.sh --text "Test audio"
```

## Model
- Uses `Qwen/Qwen3-TTS-12Hz-1.7B-Base`
- Automatically downloaded and cached in `./models/Qwen3-TTS-12Hz-1.7B-Base`

## Testing
- Test with different voices: `trump.mp3`, `heyjessi.mp3`, etc.
- Verify output WAV files are generated and playable

See `AGENTS.md` for development guidelines.
