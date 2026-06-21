# CodeAlpha: AI Language Translation Tool

A clean, premium web interface for translating text across multiple languages. This project was developed as part of the CodeAlpha AI Internship program. It leverages python tools to provide instant text translations, clipboard utility integrations, and audio voice synthesis (text-to-speech) capabilities directly within the browser.

## Features

- 🌐 **Multi-Language Translation**: Supports over 100 languages powered by the `deep-translator` library (Google Translate engine).
- 🧠 **Auto Language Detection**: Automatically recognizes the source language.
- 🔊 **Text-to-Speech**: Listen to the pronunciation of translations with high-fidelity speech synthesis using `gTTS`.
- 📋 **Seamless Clipboard Copying**: Single-click "Copy Text" button featuring interactive feedback.
- 🎨 **Premium Aesthetic**: Responsive slate-dark theme designed with modern typography, smooth color gradients, and micro-interactions.
- ⚡ **Zero API Keys Required**: Fully functional out-of-the-box without requiring billing credentials or API keys.

---

## Tech Stack

- **Frontend / Web UI**: [Streamlit](https://streamlit.io/) (Python web framework)
- **Translation Engine**: [deep-translator](https://github.com/nidhaloff/deep-translator) (Google Translator API backend)
- **Speech Synthesis**: [gTTS](https://github.com/pndurette/gTTS) (Google Text-to-Speech API backend)
- **Interactivity**: HTML5, CSS3, and modern JavaScript (for clipboard integration)

---

## Project Structure

```text
CodeAlpha_LanguageTranslationTool/
│
├── .streamlit/
│   └── config.toml          # Custom theme configuration
│
├── utils/
│   ├── __init__.py          # Python package initializer
│   ├── translator.py        # Translation core logic
│   └── tts.py               # Text-to-Speech generator
│
├── app.py                   # Streamlit web application interface
├── requirements.txt         # Project dependencies
├── .gitignore               # Ignored files list
└── README.md                # Project documentation
```

---

## Installation & Setup

Follow these steps to run the application locally on your machine:

### Prerequisites
- Python 3.8 or higher installed. You can check your version by running:
  ```bash
  python --version
  ```

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<your-username>/CodeAlpha_LanguageTranslationTool.git
   cd CodeAlpha_LanguageTranslationTool
   ```

2. **Create a Virtual Environment**
   It is highly recommended to isolate your project dependencies:
   ```bash
   # Windows (PowerShell/CMD)
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   Install all the packages specified in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   Launch the Streamlit server locally:
   ```bash
   streamlit run app.py
   ```

5. **Access the App**
   Open your browser and navigate to:
   ```text
   http://localhost:8501
   ```

---

## Screenshots

*(Screenshots of the UI will be placed here)*

### Application Dashboard
![Language Translation Interface Placeholder](https://via.placeholder.com/800x450.png?text=Language+Translator+UI+Dashboard)

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
