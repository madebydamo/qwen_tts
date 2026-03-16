import sys
import os
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: python generate.py <ref_audio> 'Your sentence here' [optional ref_text]"
        )
        sys.exit(1)

    ref_audio = "/app/" + sys.argv[1]
    text = sys.argv[2]
    ref_text = sys.argv[3] if len(sys.argv) > 3 else None

    model_path = "/app/models/Qwen3-TTS-12Hz-1.7B-Base"
    # model_path = "/app/models/Qwen3-TTS-12Hz-1.7B-CustomVoice"
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}. Downloading...")
        model = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
            device_map="auto",
            dtype=torch.bfloat16,
            # attn_implementation="flash_attention_2",  # Uncomment if flash-attn is installed
        )
    else:
        print("Loading local model...")
        model = Qwen3TTSModel.from_pretrained(
            model_path,
            device_map="auto",
            dtype=torch.bfloat16,
            # attn_implementation="flash_attention_2",  # Uncomment if flash-attn is installed
        )

    print("Generating audio...")
    if ref_text:
        wavs, sr = model.generate_voice_clone(
            text=text,
            language="German",  # Adjust if needed
            ref_audio=ref_audio,
            ref_text=ref_text,
            x_vector_only_mode=True,
        )
    else:
        wavs, sr = model.generate_voice_clone(
            text=text,
            language="German",
            ref_audio=ref_audio,
            x_vector_only_mode=True,
        )

    output_file = "/app/output.wav"
    sf.write(output_file, wavs[0], sr)
    print(f"Audio saved to {output_file}")


if __name__ == "__main__":
    main()
