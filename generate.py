import os
import torch
import soundfile as sf
import argparse
from datetime import datetime
import re
from huggingface_hub import snapshot_download
from qwen_tts import Qwen3TTSModel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref-audio", default="trump.mp3")
    parser.add_argument("--text", required=True)
    parser.add_argument("--ref-text", default=None)
    parser.add_argument("--language", default="english")
    parser.add_argument("--name", default=None)
    args = parser.parse_args()

    ref_audio = "/app/" + args.ref_audio
    text = args.text
    ref_text = args.ref_text
    language = args.language

    model_path = "/app/models/Qwen3-TTS-12Hz-1.7B-Base"
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}. Downloading...")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        snapshot_download("Qwen/Qwen3-TTS-12Hz-1.7B-Base", local_dir=model_path)
    print("Loading local model...")
    model = Qwen3TTSModel.from_pretrained(
        model_path,
        device_map="auto",
        dtype=torch.bfloat16,
    )

    print("Generating audio...")
    if ref_text:
        wavs, sr = model.generate_voice_clone(
            text=text,
            language=language,
            ref_audio=ref_audio,
            ref_text=ref_text,
            x_vector_only_mode=True,
        )
    else:
        wavs, sr = model.generate_voice_clone(
            text=text,
            language=language,
            ref_audio=ref_audio,
            x_vector_only_mode=True,
        )

    if args.name:
        base_name = args.name
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean = re.sub(r"[^a-z0-9]+", "_", text.lower())
        clean = clean.strip("_")[:20]
        base_name = timestamp + "_" + clean
    output_file = "/app/" + base_name + ".wav"
    sf.write(output_file, wavs[0], sr)
    print(f"Audio saved to {output_file}")


if __name__ == "__main__":
    main()
