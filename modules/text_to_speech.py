from gtts import gTTS
import tempfile
import os


def generate_audio(text, lang="en"):
    """
    Convert text to speech and return path to mp3 file.
    """

    lang_map = {
        "english": "en",
        "hindi": "hi",
        "hinglish": "hi"
    }

    tts_lang = lang_map.get(lang, "en")

    tts = gTTS(text=text, lang=tts_lang)

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    tts.save(temp_file.name)

    return temp_file.name