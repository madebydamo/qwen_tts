# AGENTS.md

This file contains guidelines and conventions for agents working on this Qwen3 TTS codebase. Follow these rules to maintain consistency and quality.

## Build/Lint/Test Commands

### Running the Application

**Generate audio from text with voice cloning:**
```bash
./run.sh --text "Your text here" [--ref-audio trump.mp3] [--ref-text "ref"] [--language en] [--name custom]
# Example: ./run.sh --text "Hello world" --ref-audio trump.mp3
```

**Python CLI:**
```bash
python generate.py --text "Your sentence here" --ref-audio trump.mp3
```

**Download models:**
```bash
./download.sh
```

**Run with Docker:**
```bash
docker compose up
# Or:
docker compose run --rm qwen-tts ./run.sh --text "Hello world"
```

### Testing

**Manual testing of audio generation:**
- Test with different audio formats (mp3, wav, ogg)
- Test with various text lengths (short phrases to full sentences)
- Test voice cloning quality with different reference audio files
- Verify output audio file is created and playable

**Model loading tests:**
- Test local model loading vs HuggingFace download (cached in /app/models/)
- Test with different reference audio files

### Linting and Code Quality

**Python code style (PEP 8):**
```bash
pip install flake8 black isort mypy
flake8 generate.py  # Check for style issues
black generate.py   # Auto-format code
isort generate.py   # Sort imports
mypy generate.py    # Type checking
```

**Recommended pre-commit checks:**
- Run black/isort before committing
- Check for syntax errors with python -m py_compile
- Verify imports work with python -c "import generate"

## Code Style Guidelines

### Imports

**Standard library imports first:**
```python
import sys
import os
import torch
import soundfile as sf
from pathlib import Path
```

**Third-party imports second:**
```python
from qwen_tts import Qwen3TTSModel
```

**Local imports last:**
```python
# (none in this codebase currently)
```

**Import organization:**
- Group imports by type with blank lines between groups
- Use absolute imports
- Avoid wildcard imports (`from module import *`)

### Formatting

**Line length:** Maximum 88 characters (Black default)

**Indentation:** 4 spaces (PEP 8 standard)

**String quotes:** Use double quotes for consistency with existing code

**Trailing commas:** Include in multi-line structures for cleaner diffs

**Example:**
```python
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--ref-audio", default="trump.mp3")
    args = parser.parse_args()
```

### Naming Conventions

**Variables:**
- `snake_case` for variables and functions
- `ref_audio`, `text`, `model_path` (descriptive names)

**Constants:**
- `UPPER_SNAKE_CASE` for constants
- `DEFAULT_MODEL_PATH = "/app/models/Qwen3-TTS-12Hz-1.7B-Base"`

**Functions:**
- `snake_case` with descriptive names
- `generate_audio()`, `load_model()`, `validate_input()`

**Files:**
- `snake_case` for Python files: `generate.py`, `download.py`
- `kebab-case` for shell scripts: `run.sh`, `download.sh`

### Types and Type Hints

**Use type hints for function parameters and return values:**
```python
from typing import Optional

def main() -> None:
    # Function body

def load_model(model_path: str, use_gpu: bool = True) -> Qwen3TTSModel:
    # Function body
```

**Common types to import:**
```python
from typing import List, Dict, Tuple, Optional, Union
```

### Error Handling

**Use try/except blocks for external operations:**
```python
try:
    model = Qwen3TTSModel.from_pretrained(model_path)
except Exception as e:
    print(f"Failed to load model: {e}")
    sys.exit(1)
```

**Validate inputs early:**
```python
def validate_audio_file(file_path: str) -> bool:
    if not os.path.exists(file_path):
        print(f"Audio file not found: {file_path}")
        return False
    # Additional validation...
    return True
```

**Handle file operations safely:**
```python
try:
    with open(audio_file, 'rb') as f:
        # Process file
        pass
except IOError as e:
    print(f"Error reading audio file: {e}")
    sys.exit(1)
```

### Documentation

**Add docstrings to functions:**
```python
def generate_audio(ref_audio: str, text: str, ref_text: Optional[str] = None) -> str:
    """
    Generate audio using voice cloning.

    Args:
        ref_audio: Path to reference audio file
        text: Text to synthesize
        ref_text: Optional reference text for better cloning

    Returns:
        Path to generated audio file

    Raises:
        FileNotFoundError: If reference audio doesn't exist
        RuntimeError: If model fails to generate audio
    """
```

**Comment complex logic:**
```python
# Load model with GPU acceleration if available
model = Qwen3TTSModel.from_pretrained(
    model_path,
    device_map="auto",  # Automatically choose best device
    dtype=torch.bfloat16,  # Use bfloat16 for memory efficiency
)
```

### Security Best Practices

**Input validation:**
- Validate file paths exist before use
- Sanitize command line arguments
- Check file extensions for audio files

**Resource management:**
- Close files properly
- Handle GPU memory cleanup
- Limit concurrent operations

**Secrets and credentials:**
- Never hardcode API keys or tokens
- Use environment variables for sensitive configuration
- Avoid logging sensitive information

### Performance Considerations

**GPU usage:**
- Use `device_map="auto"` for automatic device placement
- Prefer `torch.bfloat16` for memory efficiency
- Enable FlashAttention when available

**Memory management:**
- Load models only when needed
- Clear GPU cache after operations
- Use streaming for large files when possible

### File Organization

**Project structure:**
```
/
├── models/                 # Downloaded model files
├── generate.py            # Main generation script
├── run.sh                # Shell wrapper
├── download.sh           # Model download script
├── Dockerfile            # Container definition
├── docker-compose.yml    # Container orchestration
├── README.md             # Usage documentation
└── AGENTS.md             # This file
```

**Model file organization:**
- Keep downloaded models in `models/` directory
- Use consistent naming: `Qwen3-TTS-{freq}-{size}-{variant}`

### Docker and Containerization

**Build context:**
- Use multi-stage builds for smaller images
- Install only necessary system dependencies
- Create non-root user for security

**Volume mounting:**
- Mount source code for development
- Mount model directory for persistence
- Use consistent working directory (`/app`)

### Testing and Validation

**Audio output validation:**
- Check generated files exist and are playable
- Verify audio duration matches expected length
- Test with various input formats and languages

**Model compatibility:**
- Test different model variants
- Verify FlashAttention compatibility
- Check memory requirements

### Git and Version Control

**Commit messages:**
- Use imperative mood: "Add voice cloning feature"
- Include component name: "generate.py: Add error handling"
- Keep first line under 50 characters

**File patterns to ignore:**
```
# Audio output files
output*.wav
*.mp3
*.ogg

# Python cache
__pycache__/
*.pyc

# Model cache (if not committed)
models/*/cache/
```

### Language and Localization

**Supported languages:**
- Chinese, English, Japanese, Korean, German, French, Russian, Portuguese, Spanish, Italian
- Use "Auto" for automatic language detection when supported
- Specify language explicitly for best results

**Text encoding:**
- Use UTF-8 encoding for all text files
- Handle Unicode characters properly in audio generation

### Dependencies and Environment

**Python version:** 3.12+ (matches Dockerfile)

**Key dependencies:**
- torch: Deep learning framework
- qwen-tts: TTS library
- soundfile: Audio file handling
- huggingface-hub: Model downloading

**Virtual environment:**
- Use isolated environments (conda/virtualenv)
- Pin dependency versions in requirements.txt (create if missing)
- Install FlashAttention separately for GPU optimization

### Continuous Integration

**Automated checks:**
- Run linting on all Python files
- Test basic functionality with sample inputs
- Verify Docker builds successfully
- Check model downloads work

**Quality gates:**
- All linting passes
- Basic generation test succeeds
- No syntax errors
- Type checking passes

This document should be updated as the codebase evolves and new patterns emerge.