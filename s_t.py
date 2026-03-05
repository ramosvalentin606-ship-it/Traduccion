import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from gtts import gTTS
from googletrans import Translator


# 🎨 ESTILO VISUAL
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color: white;
}

h1, h2, h3 {
    color: #00e5ff;
}

section[data-testid="stSidebar"] {
    background-color: #111;
}

.stButton > button {
    background: linear-gradient(90deg,#ff4b2b,#ff416c);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px;
    font-size: 18px;
}

.stButton > button:hover {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color: white;
}

div[data-baseweb="select"] {
    background-color:#1e1e1e;
    border-radius:10px;
}

.stCheckbox {
    color:white;
}

audio {
    width:100%;
}

</style>
""", unsafe_allow_html=True)


st.title("🌍 TRADUCTOR DE VOZ")
st.subheader("Escucho lo que quieres traducir.")

image = Image.open('Ni Hao NIGGA.jpg')
st.image(image,width=300)

with st.sidebar:
    st.subheader("⚙️ Traductor")
    st.write(
        "Presiona el botón, cuando escuches la señal "
        "habla lo que quieres traducir y selecciona "
        "los idiomas."
    )

st.write("🎤 Presiona el botón y habla")

stt_button = Button(label="🎤 HABLA AHORA", width=300, height=50)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'es-ES';

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }

    recognition.onend = function() {
        console.log("Reconocimiento detenido");
    }

    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)


languages = {
    "Inglés": "en",
    "Español": "es",
    "Húngaro": "hu",
    "Polaco": "pl",
    "Checo": "cs",
    "Eslovaco": "sk",
    "Rumano": "ro",
    "Búlgaro": "bg",
    "Croata": "hr",
    "Serbio": "sr",
    "Esloveno": "sl",
    "Finlandés": "fi",
    "Sueco": "sv",
    "Danés": "da",
    "Noruego": "no",
    "Holandés": "nl",
    "Alemán": "de",
    "Francés": "fr",
    "Italiano": "it",
    "Portugués": "pt",
    "Griego": "el",
    "Turco": "tr",
    "Ruso": "ru",
    "Ucraniano": "uk",
    "Árabe": "ar",
    "Hindi": "hi",
    "Bengalí": "bn",
    "Coreano": "ko",
    "Mandarín": "zh-cn",
    "Japonés": "ja",
    "Islandés": "is",
    "Letón": "lv",
    "Lituano": "lt",
    "Maltés": "mt",
    "Estonio": "et",
    "Catalán": "ca",
    "Gallego": "gl",
    "Euskera": "eu"
}

if result:

    if "GET_TEXT" in result:
        st.success(result.get("GET_TEXT"))

    try:
        os.mkdir("temp")
    except:
        pass

    st.title("🔊 Texto a Audio")

    translator = Translator()
    text = str(result.get("GET_TEXT"))

    in_lang = st.selectbox(
        "🌍 Lenguaje de Entrada",
        list(languages.keys())
    )
    input_language = languages[in_lang]

    out_lang = st.selectbox(
        "🌎 Lenguaje de Salida",
        list(languages.keys())
    )
    output_language = languages[out_lang]

    english_accent = st.selectbox(
        "🗣 Acento",
        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canada",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )

    if english_accent == "Defecto":
        tld = "com"
    elif english_accent == "Español":
        tld = "com.mx"
    elif english_accent == "Reino Unido":
        tld = "co.uk"
    elif english_accent == "Estados Unidos":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Irlanda":
        tld = "ie"
    elif english_accent == "Sudáfrica":
        tld = "co.za"

    def text_to_speech(input_language, output_language, text, tld):

        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text

        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)

        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"

        tts.save(f"temp/{my_file_name}.mp3")

        return my_file_name, trans_text

    display_output_text = st.checkbox("📄 Mostrar texto traducido")

    if st.button("🚀 CONVERTIR"):

        result_audio, output_text = text_to_speech(
            input_language,
            output_language,
            text,
            tld
        )

        audio_file = open(f"temp/{result_audio}.mp3", "rb")
        audio_bytes = audio_file.read()

        st.markdown("## 🎧 Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("## 📜 Texto de salida:")
            st.write(output_text)

    def remove_files(n):

        mp3_files = glob.glob("temp/*mp3")

        if len(mp3_files) != 0:

            now = time.time()
            n_days = n * 86400

            for f in mp3_files:

                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)

    remove_files(7)

        
    


