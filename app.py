import streamlit as st
from transliteration import convert_text, get_backend
from writing import improve_text, translate_to_english

st.set_page_config(page_title="BhashaFlow | Smart Writing", page_icon="✍️", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(135deg,#f8f9ff 0%,#f4f7fb 55%,#f9f5ff 100%);}
.block-container {max-width:1180px;padding-top:2.2rem;}
.hero {background:linear-gradient(110deg,#20275c,#493c91 65%,#7255ad);padding:30px 34px;border-radius:22px;color:white;margin-bottom:22px;box-shadow:0 14px 35px #33305a22;}
.hero h1 {font-family:'Plus Jakarta Sans';font-size:34px;margin:0 0 8px 0;color:white;}
.hero p {color:#e5e4ff;font-size:15px;margin:0;}
.panel {background:white;border:1px solid #e8eaf2;border-radius:18px;padding:20px 22px;box-shadow:0 8px 24px #22224408;}
.eyebrow {color:#6e63a8;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;}
.result {background:#f7f6ff;border:1px solid #e5e0ff;border-radius:14px;padding:18px;font-size:23px;line-height:1.65;color:#26264b;min-height:130px;}
.metric {background:#fff;border:1px solid #e9eaf2;border-radius:14px;padding:14px 16px;}
.metric b {font-size:21px;color:#25265a;}
.stButton>button {border-radius:11px;font-weight:700;height:44px;}
div[data-testid="stTextArea"] textarea {border-radius:12px;}
footer {visibility:hidden;}
</style>
<div class="hero">
  <div style="font-size:12px;letter-spacing:2px;font-weight:700;color:#c9c3ff;">INDIC LANGUAGE AI • CS3235 MINI PROJECT</div>
  <h1>✍️ BhashaFlow</h1>
  <p>Your Hinglish, in your script. Write naturally in Roman Hinglish and convert it into Kannada, Hindi or Tamil.</p>
</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns([1.45,1], gap="large")
with col_a:
    st.markdown('<div class="panel"><div class="eyebrow">01 / YOUR MESSAGE</div>', unsafe_allow_html=True)
    language = st.selectbox("Choose output language", ["Kannada", "Hindi", "Tamil"], index=0)
    source = st.text_area("Type in Roman Hinglish", value="Namaskara! Naanu nanna college assignment complete maaduttiddene. Dayavittu nanage help maadi.", height=155, placeholder="Example: kal mera exam hai, mujhe notes chahiye...")
    st.caption("Tip: Type the way you speak. You can mix English words with Indian-language words.")
    c1,c2 = st.columns(2)
    with c1: convert = st.button("Convert to native script  →", type="primary", use_container_width=True)
    with c2: clear = st.button("Clear text", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if clear:
        st.session_state["source"] = ""
        st.rerun()

with col_b:
    st.markdown('<div class="panel"><div class="eyebrow">02 / NATIVE SCRIPT OUTPUT</div>', unsafe_allow_html=True)
    st.markdown(f"**{language}**")
    if convert:
        st.session_state["converted"] = convert_text(source, language)
        st.session_state["last_source"] = source
        st.session_state["last_language"] = language
    output = st.session_state.get("converted", "Your converted text will appear here.")
    st.markdown(f'<div class="result">{output}</div>', unsafe_allow_html=True)
    if "converted" in st.session_state:
        st.button("Copy output", on_click=lambda: st.toast("Select and copy the text above."))
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
st.markdown('<div class="eyebrow">03 / WRITING TOOLS</div>', unsafe_allow_html=True)
x,y,z = st.columns(3)
with x:
    st.markdown('<div class="metric"><b>अ / ಅ / அ</b><br><span style="color:#666">Native-script conversion</span></div>', unsafe_allow_html=True)
with y:
    st.markdown('<div class="metric"><b>AI4Bharat</b><br><span style="color:#666">IndicXlit integration</span></div>', unsafe_allow_html=True)
with z:
    st.markdown('<div class="metric"><b>3 languages</b><br><span style="color:#666">Kannada · Hindi · Tamil</span></div>', unsafe_allow_html=True)

with st.expander("✨ Improve phrasing / translate to English"):
    st.caption("Optional BharatGen Param1 / IndicTrans2 integration can be enabled with a Hugging Face token. The demo includes a safe local fallback.")
    mode = st.radio("Action", ["Improve phrasing", "Translate to English"], horizontal=True)
    if st.button("Run writing assistant"):
        if mode == "Improve phrasing":
            st.info(improve_text(source))
        else:
            st.info(translate_to_english(source))

st.caption(f"Engine status: {get_backend()}  ·  Prototype build | Model checkpoints are loaded only when configured.")
