from gtts import gTTS
import tempfile


def speak_text(text, lang="english"):

    lang_map = {
        "english": "en",
        "hindi": "hi",
        "hinglish": "en"
    }

    tts = gTTS(text=text, lang=lang_map.get(lang, "en"))

    file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(file.name)

    return file.name