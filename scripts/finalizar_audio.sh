#!/bin/zsh
# Normaliza o render do HyperFrames para -14 LUFS / -1 dBTP (linear) e grava o MP4 final.
# Uso: ./finalizar_audio.sh <render_hyperframes.mp4> <saida.mp4>
set -e
IN="$1"; OUT="$2"; TMP="${OUT%.mp4}_audio_tmp.wav"
GAIN=$(ffmpeg -hide_banner -i "$IN" -af loudnorm=print_format=json -f null - 2>&1 | python3 -c "import sys,json;s=sys.stdin.read();print(round(-14-float(json.loads(s[s.rfind('{'):s.rfind('}')+1])['input_i']),2))")
ffmpeg -v error -y -i "$IN" -map 0:a -af "volume=${GAIN}dB,alimiter=limit=0.79:attack=3:release=60:level=disabled,aresample=48000" -c:a pcm_s24le "$TMP"
M=$(ffmpeg -hide_banner -i "$TMP" -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | python3 -c "import sys,json;s=sys.stdin.read();d=json.loads(s[s.rfind('{'):s.rfind('}')+1]);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -v error -y -i "$IN" -i "$TMP" -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-14:TP=-1:LRA=11:linear=true:$M,aresample=48000" -c:a aac -b:a 256k -ar 48000 -movflags +faststart "$OUT"
rm "$TMP"
ffmpeg -hide_banner -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|LRA|Peak):" | tr -s ' '
