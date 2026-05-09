import streamlit as st
import google.generativeai as genai
import os

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-3.1-flash-lite')

st.set_page_config(
    page_title="PetMed AI - Virtual Vet",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #F0F2F6; }
    .block-container { max-width: 900px; padding-bottom: 8rem; }

    [data-testid="stChatMessage"] { background-color: transparent; padding: 0.8rem 0rem; }
    [data-testid="stChatMessageContent"] {
        padding: 1.2rem;
        border-radius: 20px;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    [data-testid="stChatMessageUser"] [data-testid="stChatMessageContent"] {
        background-color: #1E2631;
        border: 1px solid #36414F;
    }

    [data-testid="stChatMessageAssistant"] [data-testid="stChatMessageContent"] {
        background-color: #1A1C1E;
        border: 1px solid #C0392B;
    }

    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 80% !important;
        max-width: 750px;
        background-color: #1E2631 !important;
        border-radius: 50px !important;
        border: 1px solid #455364 !important;
        z-index: 1000;
    }

    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='color:#C0392B;'>👨‍⚕️ PetMed AI</h1>", unsafe_allow_html=True)
    st.caption("2026 Clinical Intelligence Edition")
    st.markdown("---")

    st.markdown("### 🐾 Patient Details")
    pet_name = st.text_input("Pet Name", value="My Pet")
    species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Exotic/Reptile", "Equine"])
    breed = st.text_input("Breed", placeholder="e.g. Beagle")
    age = st.number_input("Age (Years)", min_value=0.0, step=0.5)
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)

    st.markdown("---")
    if st.button("🗑️ Clear Consultation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("Virtual Vet Consultation")
with col2:
    if st.button("⚙️ Edit Pet"):
        st.info("The sidebar is on the left. If it's closed, click the > arrow at the top left.")
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.info(f"Ready to assist with **{pet_name}**. Use the sidebar to update details.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div style='background-color:#1E2631; padding:15px; border-radius:10px;'><b>Symptoms?</b><br>Ask about vomiting, limping, or skin issues.</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='background-color:#1E2631; padding:15px; border-radius:10px;'><b>Diet?</b><br>Ask about food allergies or toxic ingredients.</div>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

SYSTEM_PROMPT = f"""
You are an expert veterinarian AI trained on clinical documentations.
PATIENT: {pet_name} ({species}), Breed: {breed}, Age: {age}yrs, Weight: {weight}kg.
GOAL: Provide clinical, evidence-based advice.
EMERGENCY CHECK: If symptoms involve difficulty breathing, seizures, heavy bleeding, or poisoning, tell them to visit an emergency clinic NOW.
Always speak to the user as a professional vet.
"""

if prompt := st.chat_input(f"How can I help {pet_name} today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Analyzing clinical data..."):
        try:
            full_context = f"{SYSTEM_PROMPT}\n\nQuestion: {prompt}"
            response = model.generate_content(full_context)

            st.session_state.messages.append({"role": "assistant", "content": response.text})
            with st.chat_message("assistant"):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Connection Error: {e}")
