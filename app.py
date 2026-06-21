import streamlit as st
import streamlit.components.v1 as components
from utils.translator import get_languages, translate_text, detect_language
from utils.tts import text_to_speech
from gtts.lang import tts_langs

# Set up page configurations
st.set_page_config(
    page_title="AI Language Translation Tool",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom premium CSS styling
st.markdown("""
    <style>
    /* Hide top header and main menu for clean professional look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main body background overlay for custom aesthetic */
    .stApp {
        background-color: #0f172a;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Title typography */
    .app-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        text-align: center;
    }
    .app-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Segment headings */
    .section-title {
        font-size: 1.25rem;
        color: #f8fafc;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Custom container cards styling for Streamlit bordered containers */
    div[data-testid="stVerticalBlockBorder"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        margin-bottom: 1.5rem !important;
    }
    
    .translation-output-box {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        color: #f8fafc;
        font-size: 1.05rem;
        min-height: 120px;
        white-space: pre-wrap;
        margin-bottom: 1rem;
    }
    
    /* Footer credit */
    .internship-badge {
        text-align: center;
        margin-top: 3rem;
        font-size: 0.85rem;
        color: #64748b;
        letter-spacing: 0.05em;
    }
    .internship-badge a {
        color: #6366f1;
        text-decoration: none;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="app-title">🌐 AI Language Translator</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Translate text seamlessly across languages. Powered by CodeAlpha.</div>', unsafe_allow_html=True)

# Fetch supported languages
languages_dict = get_languages()

# Initialize Session State variables to store state across re-runs
if 'source_lang_selection' not in st.session_state:
    st.session_state.source_lang_selection = "Auto Detect"
if 'was_auto_detected' not in st.session_state:
    st.session_state.was_auto_detected = False
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'translation_performed' not in st.session_state:
    st.session_state.translation_performed = False
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None
if 'audio_lang' not in st.session_state:
    st.session_state.audio_lang = ""

# Read the text area value from session state
typed_text = st.session_state.get("input_text_val", "")

if typed_text.strip():
    # Detect language if "Auto Detect" is active or it was previously auto-detected
    if st.session_state.source_lang_selection == "Auto Detect" or st.session_state.was_auto_detected:
        detected_code = detect_language(typed_text)
        if detected_code != "auto":
            code_to_name = {code: name for name, code in languages_dict.items()}
            detected_name = code_to_name.get(detected_code, "Unknown")
            if detected_name in languages_dict:
                st.session_state.source_lang_selection = detected_name
                st.session_state.was_auto_detected = True
else:
    # Reset back to "Auto Detect" if input is cleared and it was auto-detected
    if st.session_state.was_auto_detected:
        st.session_state.source_lang_selection = "Auto Detect"
        st.session_state.was_auto_detected = False

def on_source_lang_change():
    # If user manually changes the selection, stop auto-detect overrides
    st.session_state.was_auto_detected = False

# Prepare selection lists
source_options = ["Auto Detect"] + list(languages_dict.keys())
target_options = list(languages_dict.keys())

# Default values
default_target_idx = target_options.index("Spanish") if "Spanish" in target_options else 0

# Main Content Card
with st.container(border=True):
    
    # 1. Language Selectors
    col1, col2 = st.columns(2)
    with col1:
        source_lang_name = st.selectbox(
            "Source Language",
            options=source_options,
            key="source_lang_selection",
            on_change=on_source_lang_change,
            help="Select the language of your input text or choose 'Auto Detect' for automatic recognition."
        )
    with col2:
        target_lang_name = st.selectbox(
            "Target Language",
            options=target_options,
            index=default_target_idx,
            help="Select the language you want to translate the text into."
        )
    
    # Map selection names to codes
    source_code = "auto" if source_lang_name == "Auto Detect" else languages_dict[source_lang_name]
    target_code = languages_dict[target_lang_name]
    
    # 2. Text Input Area
    input_text = st.text_area(
        "Enter text to translate",
        placeholder="Type or paste your text here (maximum 5000 characters)...",
        height=150,
        max_chars=5000,
        key="input_text_val"
    )
    
    # Character count layout
    st.caption(f"Character count: {len(input_text)} / 5000")
            
    # 3. Translate Button Action
    if st.button("Translate", type="primary", use_container_width=True):
        if not input_text.strip():
            st.error("⚠️ Please enter some text to translate.")
        else:
            with st.spinner("Translating text..."):
                try:
                    translated = translate_text(input_text, source_code, target_code)
                    st.session_state.translated_text = translated
                    st.session_state.translation_performed = True
                    # Reset audio cache if translation changes
                    st.session_state.audio_bytes = None
                    st.session_state.audio_lang = ""
                except Exception as e:
                    st.error(f"❌ Translation failed: {str(e)}")
                    st.session_state.translation_performed = False
                    
# 4. Translation Output Display
if st.session_state.translation_performed:
    with st.container(border=True):
        st.markdown('<div class="section-title">Translation Output</div>', unsafe_allow_html=True)
    
    # Render translation text
    st.markdown(
        f'<div class="translation-output-box">{st.session_state.translated_text}</div>',
        unsafe_allow_html=True
    )
    
    # Row for interactive components: Copy button and Text-to-Speech
    col_copy, col_tts = st.columns([1, 1])
    
    with col_copy:
        # Embed custom Copy component inside iframe to bypass sandbox restrictions using fallback
        escaped_text = st.session_state.translated_text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "")
        copy_button_html = f"""
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: transparent;
            }}
        </style>
        <button id="copyBtn" style="
            background-color: #6366f1;
            color: white;
            border: none;
            padding: 8px 16px;
            font-size: 14px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            width: 100%;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.2);
        ">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            Copy Text
        </button>
        <script>
            const text = "{escaped_text}";
            const btn = document.getElementById('copyBtn');
            
            btn.addEventListener('click', () => {{
                if (navigator.clipboard && navigator.clipboard.writeText) {{
                    navigator.clipboard.writeText(text).then(onSuccess).catch(onFallback);
                }} else {{
                    onFallback();
                }}
            }});
            
            function onSuccess() {{
                btn.style.backgroundColor = '#10b981'; // Emerald Green
                btn.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                    Copied!
                `;
                setTimeout(() => {{
                    btn.style.backgroundColor = '#6366f1';
                    btn.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        Copy Text
                    `;
                }}, 2000);
            }}
            
            function onFallback() {{
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                try {{
                    const successful = document.execCommand('copy');
                    if (successful) {{
                        onSuccess();
                    }} else {{
                        btn.style.backgroundColor = '#ef4444'; // Error Red
                        btn.innerText = 'Failed to Copy';
                    }}
                }} catch (err) {{
                    btn.style.backgroundColor = '#ef4444';
                    btn.innerText = 'Failed to Copy';
                }}
                document.body.removeChild(textarea);
            }}
        </script>
        """
        components.html(copy_button_html, height=38)
        
    with col_tts:
        # Check if target language is supported by gTTS
        try:
            supported_tts = tts_langs()
        except Exception:
            supported_tts = {}
            
        if target_code in supported_tts:
            if st.button("🔊 Text to Speech", use_container_width=True, help="Convert the translated text into spoken audio."):
                with st.spinner("Generating speech..."):
                    try:
                        st.session_state.audio_bytes = text_to_speech(st.session_state.translated_text, target_code)
                        st.session_state.audio_lang = target_code
                    except Exception as e:
                        st.error(f"Speech synthesis error: {str(e)}")
        else:
            st.info("ℹ️ Audio playback not supported for this language.")
            
    # Render audio player if cached and matches target language
    if st.session_state.audio_bytes is not None and st.session_state.audio_lang == target_code:
        st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
        st.audio(st.session_state.audio_bytes, format="audio/mp3")



# Footer credits
st.markdown("""
    <div class="internship-badge">
        Developed for the <strong>CodeAlpha AI Internship</strong> | 
        <a href="https://github.com/CodeAlpha" target="_blank">CodeAlpha GitHub</a>
    </div>
""", unsafe_allow_html=True)
