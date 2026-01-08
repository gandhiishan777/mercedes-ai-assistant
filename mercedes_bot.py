import streamlit as st
from firecrawl import FirecrawlApp
from openai import OpenAI

# =========================================================
# 1. PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Mercedes-Benz AI Showroom",
    page_icon="🚙",
    layout="centered",
)

# =========================================================
# 2. PREMIUM UI / CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background: radial-gradient(
        circle at top,
        #1a1f2b 0%,
        #0b0e14 45%,
        #000000 100%
    );
    color: white;
}

/* Hide Streamlit chrome */
header, footer, .stDeployButton {
    visibility: hidden;
}

/* Glassmorphism cards */
.glass {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 18px;
    padding: 26px;
    border: 1px solid rgba(255,255,255,0.14);
    box-shadow: 0 25px 60px rgba(0,0,0,0.55);
    margin-bottom: 20px;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.14),
        rgba(255,255,255,0.04)
    );
    border: 1px solid rgba(255,255,255,0.25);
    color: white;
    border-radius: 14px;
    padding: 14px 22px;
    font-weight: 500;
    letter-spacing: 0.4px;
    transition: all 0.25s ease;
    width: 100%;
}

div.stButton > button:hover {
    background: white;
    color: black;
    transform: translateY(-2px);
    box-shadow: 0 14px 34px rgba(255,255,255,0.3);
}

/* Chat bubbles */
.stChatMessage {
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 14px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Chat input */
.stChatInput textarea {
    border-radius: 18px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.18);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. API SETUP
# =========================================================
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    firecrawl = FirecrawlApp(api_key=st.secrets["FIRECRAWL_API_KEY"])
except Exception:
    st.error("⚠️ API keys missing. Set them in `.streamlit/secrets.toml`.")
    st.stop()

# =========================================================
# 4. DATA
# =========================================================
MODELS = {
    "GLC SUV": "https://www.mbusa.com/en/vehicles/class/glc/suv",
    "GLE SUV": "https://www.mbusa.com/en/vehicles/class/gle/suv",
    "C-Class Sedan": "https://www.mbusa.com/en/vehicles/class/c-class/sedan",
    "E-Class Sedan": "https://www.mbusa.com/en/vehicles/class/e-class/sedan",
    "S-Class Sedan": "https://www.mbusa.com/en/vehicles/class/s-class/sedan",
    "G-Class SUV": "https://www.mbusa.com/en/vehicles/class/g-class/suv",
    "GLS SUV": "https://www.mbusa.com/en/vehicles/class/gls/suv",
    "EQS Sedan": "https://www.mbusa.com/en/vehicles/class/eqs/sedan",
}

# =========================================================
# 5. SESSION STATE
# =========================================================
if "current_model" not in st.session_state:
    st.session_state.current_model = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""

# =========================================================
# 6. HELPERS
# =========================================================
def get_car_context(url: str) -> str:
    with st.spinner("Accessing Mercedes-Benz vehicle intelligence…"):
        try:
            data = firecrawl.scrape_url(url, params={"formats": ["markdown"]})
            return data["markdown"]
        except Exception as e:
            return f"Error retrieving data: {e}"

# =========================================================
# 7. HEADER / HERO
# =========================================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Mercedes-Benz_silver_star_logo.svg/1024px-Mercedes-Benz_silver_star_logo.svg.png",
        use_container_width=True
    )

st.markdown("""
<div class="glass" style="text-align:center;">
    <h1 style="font-weight:300;">Mercedes-Benz AI Showroom</h1>
    <p style="color:#bbb; font-size:16px;">
        A private, intelligent vehicle consultation experience
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 8. SHOWROOM VIEW
# =========================================================
if st.session_state.current_model is None:
    st.markdown(
        "<p style='text-align:center; color:#aaa;'>Select a vehicle to begin.</p>",
        unsafe_allow_html=True
    )

    cols = st.columns(2)
    model_names = list(MODELS.keys())

    for i, model in enumerate(model_names):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="glass">
                <h3>{model}</h3>
                <p style="color:#aaa; font-size:14px;">
                    Design · Performance · Technology
                </p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Enter Experience →", key=model):
                st.session_state.current_model = model
                st.session_state.context = get_car_context(MODELS[model])
                st.session_state.messages = [{
                    "role": "assistant",
                    "content": (
                        f"Welcome to the **{model}**.\n\n"
                        "I’m your Mercedes-Benz product specialist. "
                        "What would you like to explore?"
                    )
                }]
                st.rerun()

# =========================================================
# 9. CONSULTATION VIEW
# =========================================================
else:
    with st.sidebar:
        st.markdown(f"""
        <div class="glass">
            <h3>Currently Viewing</h3>
            <h2>{st.session_state.current_model}</h2>
            <p style="color:#aaa;">Live vehicle data enabled</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("← Return to Showroom"):
            st.session_state.current_model = None
            st.session_state.messages = []
            st.session_state.context = ""
            st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about pricing, features, performance…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a Mercedes-Benz product specialist. "
                            "Your tone is calm, refined, and confident. "
                            "Never sound like a chatbot. "
                            "Be concise, precise, and premium.\n\n"
                            f"Vehicle context:\n{st.session_state.context}"
                        )
                    },
                    *st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
