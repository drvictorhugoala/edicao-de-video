#!/bin/zsh
# Etapa 2: transcreve em português com tempo por palavra e lista os silêncios.
# Uso: transcrever.sh videos/<slug> ["vocabulário extra para o prompt"]
set -euo pipefail
W="$1"; T="$W/01_transcricao"
MODEL="${WHISPER_MODEL:-/Users/Shared/whisper-models/ggml-large-v3-turbo-q5_0.bin}"
[[ -f "$MODEL" ]] || { echo "Modelo não encontrado: $MODEL (não baixe sem perguntar)" >&2; exit 1; }
PROMPT="Dr. Victor Hugo, neurocirurgião vascular. Aneurisma cerebral, AVC, carótida, estenose, stent, embolização. ${2:-}"

whisper-cli -m "$MODEL" -f "$T/voz_16k.wav" -l pt --prompt "$PROMPT" -oj -osrt -of "$T/segmentos" -np >/dev/null 2>&1
whisper-cli -m "$MODEL" -f "$T/voz_16k.wav" -l pt --prompt "$PROMPT" -ml 1 -sow -oj -of "$T/palavras" -np >/dev/null 2>&1

python3 - "$T" <<'EOF'
import json, sys, pathlib
t = pathlib.Path(sys.argv[1])
raw = json.load(open(t / "palavras.json"))["transcription"]
words = [{"text": x["text"].strip(), "start": round(x["offsets"]["from"] / 1000, 3), "end": round(x["offsets"]["to"] / 1000, 3)}
         for x in raw if x["text"].strip() and not x["text"].strip().startswith("[")]
json.dump(words, open(t / "transcript_palavras.json", "w"), ensure_ascii=False, indent=1)
print(len(words), "palavras ·", words[0]["start"], "→", words[-1]["end"], "s")
EOF

echo "== Silêncios (−38 dB, ≥ 0,45 s)"
ffmpeg -hide_banner -i "$T/voz_16k.wav" -af silencedetect=noise=-38dB:d=0.45 -f null - 2>&1 \
  | grep -oE "silence_(start|end): [0-9.]+" | paste - - | awk '{printf "%.2f–%.2f  ", $2, $4} END {print ""}'
echo "== Texto por frase"; cat "$T/segmentos.srt"
