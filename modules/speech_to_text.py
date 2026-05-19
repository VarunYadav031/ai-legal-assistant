# modules/speech_to_text.py

import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment


def transcribe_audio(audio_file):
    """
    Convert audio file to text.

    Supports:
    - webm (streamlit-mic-recorder output)
    - wav
    - mp3
    - m4a
    """

    recognizer = sr.Recognizer()
    temp_wav_path = None

    try:
        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp_wav:
            temp_wav_path = temp_wav.name

        # Convert input audio to WAV
        audio = AudioSegment.from_file(audio_file)
        audio.export(temp_wav_path, format="wav")

        # Read WAV using SpeechRecognition
        with sr.AudioFile(temp_wav_path) as source:
            audio_data = recognizer.record(source)

        # Convert speech to text
        text = recognizer.recognize_google(audio_data)

        return text

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        return "Speech recognition service unavailable."

    except Exception as e:
        return f"Speech recognition error: {e}"

    finally:
        # Delete temporary WAV file
        if temp_wav_path and os.path.exists(temp_wav_path):
            try:
                os.remove(temp_wav_path)
            except Exception:
                pass