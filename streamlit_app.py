
import streamlit as st
from openai import OpenAI
import os
from kurz_data import kurz_content

# Inicializace OpenAI
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Mindset Coach", page_icon="🧠")
st.title("🧠 GPT Mindset Coach")

# Získání všech kategorií
categories = sorted(set([item["category"] for item in kurz_content.values()]))

# Výběr kategorie
selected_category = st.selectbox(
    "📚 Vyber oblast rozvoje:",
    options=categories
)

# Filtrování témat podle vybrané kategorie
available_topics = {
    key: val for key, val in kurz_content.items() if val["category"] == selected_category
}

# Výběr tématu
selected_topic = st.selectbox(
    "📖 Vyber konkrétní modul:",
    options=list(available_topics.keys()),
    format_func=lambda key: available_topics[key]["label"]
)

# Výběr modelu GPT
model_choice = st.selectbox(
    "🤖 Zvol model GPT", 
    ["gpt-3.5-turbo", "gpt-4"], 
    index=0,
    help="gpt-3.5 je rychlejší, gpt-4 je chytřejší (ale pomalejší)"
)

# System prompt připravíme, ale nenačteme do historie
system_prompt = {
    "role": "system",
    "content": f"Jsi digitální kouč Mindset Coach. Pomáháš studentům s tématem: {kurz_content[selected_topic]['label']}. Kontext: {kurz_content[selected_topic]['context']}"
}

# Přátelské přivítání – zobrazí se jako první zpráva asistenta
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ahoj, já jsem Mindset Coach, odborný AI asistent pro účastníky Online kurzu koučinku Mindset Coaching®\n\nNapiš mi, ve které části kurzu se právě nacházíš, nebo s čím ti mohu pomoci?"
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
            response = openai.chat.completions.create(
                model=model_choice,
                messages=[system_prompt] + st.session_state.messages
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ Chyba při dotazu na OpenAI: {str(e)}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
