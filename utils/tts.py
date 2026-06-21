from gtts import gTTS
import io

def text_to_speech(text: str, lang_code: str) -> bytes:
    """
    Generates speech audio from text using gTTS and returns raw audio bytes.
    """
    if not text or not text.strip():
        raise ValueError("Input text is empty.")
    
    try:
        # gTTS works with standard language codes. E.g. 'en', 'es', 'fr', 'zh-CN'.
        tts = gTTS(text=text, lang=lang_code, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp.getvalue()
    except Exception as e:
        raise RuntimeError(f"Text-to-speech failed: {str(e)}")
