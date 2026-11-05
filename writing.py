"""Optional LLM writing adapters. These functions clearly label local fallback behavior."""
import os

def _generate(prompt, model_id):
    if os.getenv("USE_HF_MODELS") != "1": return None
    try:
        from transformers import pipeline
        gen = pipeline("text-generation", model=model_id, token=os.getenv("HF_TOKEN"))
        out = gen(prompt, max_new_tokens=180, do_sample=False)
        return out[0]["generated_text"][len(prompt):].strip()
    except Exception:
        return None

def improve_text(text):
    if not text.strip(): return "Enter text to improve."
    answer = _generate("Rewrite this Hinglish message clearly without changing its meaning:\n"+text+"\nImproved version:", "bharatgenai/Param1-2.9B-Instruct")
    return answer or "Demo fallback: Your original message is preserved. Configure the BharatGen Param1 checkpoint to enable AI-powered phrasing suggestions."

def translate_to_english(text):
    if not text.strip(): return "Enter text to translate."
    answer = _generate("Translate this Hinglish text into natural English:\n"+text+"\nEnglish translation:", "ai4bharat/indictrans2-indic-en-1B")
    return answer or "Demo fallback: Configure AI4Bharat IndicTrans2 to enable model-based English translation."
