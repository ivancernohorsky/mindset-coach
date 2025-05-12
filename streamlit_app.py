
import streamlit as st
from openai import OpenAI
import os

# Načteme obsah kurzu (moduly s kontextem)
from kurz_data import kurz_content

# Inicializace OpenAI
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Mindset Coach", page_icon="🧠")
st.title("🧠 GPT Mindset Coach")

# Výběr tématu kurzu
selected_topic = st.selectbox(
    "📚 Vyber téma kurzu, ke kterému máš otázku:",
    options=list(kurz_content.keys()),
    format_func=lambda key: kurz_content[key]["label"]
)

# Výběr modelu GPT
model_choice = st.selectbox(
    "🤖 Zvol model GPT", 
    ["gpt-3.5-turbo", "gpt-4"], 
    index=0,
    help="gpt-3.5 je rychlejší, gpt-4 je chytřejší (ale pomalejší)"
)

# Inicializace konverzace
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": f"Jsi digitální kouč Mindset Coach. Pomáháš studentům s tématem: {kurz_content[selected_topic]['label']}. Kontext: {kurz_content[selected_topic]['context']}"
        }
    ]

# Zobrazení dosavadní konverzace
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Uživatelský vstup
if prompt := st.chat_input("Zeptej se na cokoliv z vybraného tématu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Vložení aktuálního kontextu znovu do system promptu při každé nové otázce
            system_prompt = {
                "role": "system",
                "content": f"Jsi digitální kouč Mindset Coach. Pomáháš studentům s tématem: {kurz_content[selected_topic]['label']}. Kontext: {kurz_content[selected_topic]['context']}"
            }

            response = openai.chat.completions.create(
                model=model_choice,
                messages=[system_prompt] + st.session_state.messages[1:]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ Chyba při dotazu na OpenAI: {str(e)}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
