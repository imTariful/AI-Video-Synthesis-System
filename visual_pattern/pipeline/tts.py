import os
from gtts import gTTS
from mutagen.mp3 import MP3
import hashlib

TEXTS_DIR = "media/texts"
AUDIO_DIR = "media/audio"

def ensure_dirs():
    os.makedirs(TEXTS_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_voice(text: str, filename_prefix="tts") -> tuple[str, float]:
    """
    Generates an MP3 file from text.
    Returns: (file_path, duration_in_seconds)
    """
    ensure_dirs()
    
    # Create a unique filename based on text hash to avoid regeneration
    text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
    filename = f"{filename_prefix}_{text_hash}.mp3"
    file_path = os.path.join(AUDIO_DIR, filename)
    
    # Check if exists
    if not os.path.exists(file_path):
        print(f"Generating TTS for: '{text[:20]}...'")
        tts = gTTS(text=text, lang='en')
        tts.save(file_path)
    else:
        print(f"Using cached TTS for: '{text[:20]}...'")

    # Get duration
    try:
        audio = MP3(file_path)
        duration = audio.info.length
    except Exception as e:
        print(f"Error reading audio length: {e}")
        duration = 2.0 # Fallback

    return file_path, duration
