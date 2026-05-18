import speech_recognition as sr


def transcribe_audio(audio_file):
    """
    Convert uploaded audio file to text.
    Supports WAV format reliably.
    """
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except Exception:
        return ""