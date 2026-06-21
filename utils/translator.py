from deep_translator import GoogleTranslator
from typing import Dict

def get_languages() -> Dict[str, str]:
    """
    Returns a dictionary of supported languages mapping language names (capitalized) to language codes.
    """
    try:
        raw_langs = GoogleTranslator().get_supported_languages(as_dict=True)
        # Format keys nicely (title case)
        return {name.title(): code for name, code in raw_langs.items()}
    except Exception as e:
        # Fallback dictionary in case of network issue or API changes
        return {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Italian": "it",
            "Portuguese": "pt",
            "Russian": "ru",
            "Chinese (Simplified)": "zh-CN",
            "Chinese (Traditional)": "zh-TW",
            "Japanese": "ja",
            "Korean": "ko",
            "Arabic": "ar",
            "Hindi": "hi",
            "Turkish": "tr",
            "Dutch": "nl",
            "Polish": "pl"
        }

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translates text from source_lang to target_lang.
    source_lang and target_lang should be language codes.
    """
    if not text or not text.strip():
        raise ValueError("Input text is empty.")
    
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text)
        if not translated:
            raise RuntimeError("Translation returned empty result.")
        return translated
    except Exception as e:
        raise RuntimeError(f"Translation failed: {str(e)}")
