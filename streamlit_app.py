import streamlit as st
from openai import OpenAI
import os

# Zadej svůj OpenAI klíč – nebo použij .env
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Mindset Coach", page_icon="🧠")
st.title("🧠 GPT Mindset Coach")

# Inicializace historie
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Jsi Mindset Coach – digitální průvodce kurzem. Pomáháš studentům rozvíjet koučovací dovednosti, sebereflexi a emoční inteligenci."}
    ]

# Zobrazení historie konverzace
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Uživatelský vstup
if prompt := st.chat_input("Zeptej se na cokoliv z kurzu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ Chyba: {str(e)}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
