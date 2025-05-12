import streamlit as st
from openai import OpenAI
import os

# Inicializace OpenAI s klíčem z prostředí
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Nastavení aplikace
st.set_page_config(page_title="Mindset Coach", page_icon="🧠")
st.title("🧠 GPT Mindset Coach")

# Přepínač modelu
model_choice = st.selectbox(
    "🧠 Zvol model GPT", 
    ["gpt-3.5-turbo", "gpt-4"], 
    index=0,
    help="gpt-3.5 je rychlejší, gpt-4 je chytřejší (ale pomalejší)"
)

# Inicializace historie zpráv
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "Jsi Mindset Coach – digitální průvodce kurzem. Pomáháš studentům rozvíjet koučovací dovednosti, sebereflexi a emoční inteligenci."
        }
    ]

# Zobrazení historie zpráv
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Uživatelský vstup
if prompt := st.chat_input("Zeptej se na cokoliv z kurzu..."):
    # Uložení dotazu
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Zobrazení dotazu
    with st.chat_message("user"):
        st.markdown(prompt)

    # Odpověď od asistenta
    with st.chat_message("assistant"):
        try:
            response = openai.chat.completions.create(
                model=model_choice,
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ Chyba při dotazu na OpenAI: {str(e)}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
