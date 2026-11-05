"""IndicXlit adapter with a local demonstration fallback.
Set USE_HF_MODELS=1 and HF_TOKEN (if required) to load the AI4Bharat checkpoint.
"""
import os, re

MODEL_ID = os.getenv("INDICXLIT_MODEL", "ai4bharat/indicxlit")
PIPELINE = None

def _load_model():
    global PIPELINE
    if PIPELINE is not None: return PIPELINE
    if os.getenv("USE_HF_MODELS") != "1": return None
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
        token = os.getenv("HF_TOKEN")
        tok = AutoTokenizer.from_pretrained(MODEL_ID, token=token, trust_remote_code=True)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID, token=token, trust_remote_code=True)
        PIPELINE = pipeline("text2text-generation", model=model, tokenizer=tok)
        return PIPELINE
    except Exception:
        return None

# Small transparent transliteration lexicon for offline demo mode.
LEXICON = {
 "Kannada": {"namaskara":"ನಮಸ್ಕಾರ","naanu":"ನಾನು","nanna":"ನನ್ನ","college":"ಕಾಲೇಜು","assignment":"ಅಸೈನ್‌ಮೆಂಟ್","complete":"ಪೂರ್ಣ","maaduttiddene":"ಮಾಡುತ್ತಿದ್ದೇನೆ","dayavittu":"ದಯವಿಟ್ಟು","nanage":"ನನಗೆ","help":"ಸಹಾಯ","maadi":"ಮಾಡಿ","hege":"ಹೇಗೆ","idira":"ಇದ್ದೀರಾ","dhanyavada":"ಧನ್ಯವಾದ","ivattu":"ಇವತ್ತು","chennagide":"ಚೆನ್ನಾಗಿದೆ"},
 "Hindi": {"namaste":"नमस्ते","kal":"कल","mera":"मेरा","exam":"एग्ज़ाम","hai":"है","mujhe":"मुझे","notes":"नोट्स","chahiye":"चाहिए","madad":"मदद","karo":"करो","dhanyavaad":"धन्यवाद","aap":"आप","kaise":"कैसे","ho":"हो"},
 "Tamil": {"vanakkam":"வணக்கம்","naan":"நான்","en":"என்","ungal":"உங்கள்","nandri":"நன்றி","udhavi":"உதவி","seiyungal":"செய்யுங்கள்","naalai":"நாளை","thervu":"தேர்வு","irukirathu":"இருக்கிறது"}
}

def get_backend():
    return "AI4Bharat IndicXlit (configured)" if _load_model() else "Offline demo lexicon (IndicXlit adapter ready)"

def convert_text(text, language):
    if not text.strip(): return "Please enter some text first."
    model = _load_model()
    if model:
        try:
            result = model(text, max_new_tokens=256)
            if result and isinstance(result, list): return result[0].get("generated_text", str(result[0]))
        except Exception:
            pass
    mapping = LEXICON.get(language, {})
    tokens = re.findall(r"[A-Za-zÀ-ÿ0-9]+|[^A-Za-zÀ-ÿ0-9]+", text)
    converted = []
    for token in tokens:
        key = token.lower()
        value = mapping.get(key, token)
        if token[:1].isupper() and value != token:
            value = value
        converted.append(value)
    return "".join(converted)
