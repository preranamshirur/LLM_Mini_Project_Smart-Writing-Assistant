# BhashaFlow — Hinglish Smart Writing Assistant

CS3235 mini-project prototype using the AI4Bharat / BharatGen ecosystem.

## Features
- Roman Hinglish input with Kannada, Hindi and Tamil output.
- IndicXlit model adapter (checkpoint: `ai4bharat/indicxlit`) with an offline lexicon fallback for a quick demo.
- Optional writing/translation adapters for BharatGen Param1 and AI4Bharat IndicTrans2.
- Streamlit frontend.

## Run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Enable model-backed inference
Set `USE_HF_MODELS=1` and `HF_TOKEN` if the selected Hugging Face checkpoints require access.
The IndicXlit adapter is configured with `ai4bharat/indicxlit`. Review the current model card, language codes,
input/output conventions, license and hardware requirements before a full deployment. The example adapter
is intentionally isolated in `transliteration.py` so checkpoint-specific preprocessing can be adjusted.

## Evaluation
`python evaluate.py` computes character error rate (CER) and word accuracy on the included small sample set.
The bundled samples are illustrative smoke tests, not a statistically valid benchmark. Expand to 30–50
representative user-validated examples and report language-wise results and failure categories.

## Architecture
Roman Hinglish → text normalization/tokenization → IndicXlit adapter → native-script text → optional
Param1 phrasing / IndicTrans2 translation → Streamlit output.

## Important
The offline fallback uses a small hand-curated lexicon and preserves unknown tokens. It is included so the UI
works immediately without downloading large model weights. Do not report fallback output as pretrained-model
performance. Model-based results should be measured separately.
