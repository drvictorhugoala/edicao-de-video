#!/bin/zsh
# Etapa 8: mede o ruído de fundo e limpa a voz do vídeo cortado (passa-alta, redução leve, compressão suave).
# Uso: limpar_voz.sh videos/<slug>  → 06_montagem/<slug>_cortado_limpo.mp4 e religa assets/video_cortado.mp4
set -euo pipefail
W="$1"; M="$W/06_montagem"; SLUG="${W:t}"; IN="$M/${SLUG}_cortado.mp4"
NOISE=$(ffmpeg -hide_banner -i "$W/01_transcricao/voz_16k.wav" -af "silencedetect=noise=-38dB:d=0.8" -f null - 2>&1 \
  | grep -oE "silence_start: [0-9.]+" | head -2 | tail -1 | awk '{print $2}')
if [[ -n "$NOISE" ]]; then
  ffmpeg -hide_banner -ss "$NOISE" -t 0.5 -i "$W/01_transcricao/voz_16k.wav" -af astats -f null - 2>&1 | grep -m1 "RMS level dB" | sed 's/.*RMS/ruído de fundo: RMS/'
fi
ffmpeg -v error -y -i "$IN" -vn -c:a pcm_s24le -ar 48000 "$M/voz.wav"
ffmpeg -v error -y -i "$M/voz.wav" -af "highpass=f=70,afftdn=nr=6:nf=-70,acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=2" \
  -c:a pcm_s24le "$M/voz_limpa.wav"
ffmpeg -v error -y -i "$IN" -i "$M/voz_limpa.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart "$M/${SLUG}_cortado_limpo.mp4"
for f in voz.wav voz_limpa.wav; do echo "$f: $(ffmpeg -hide_banner -i "$M/$f" -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|Peak):' | tr -s ' ' | tr '\n' ' ')"; done
rm "$M/voz.wav"
ln -sf "../../06_montagem/${SLUG}_cortado_limpo.mp4" "$W/04_motions/assets/video_cortado.mp4"
echo "assets/video_cortado.mp4 → ${SLUG}_cortado_limpo.mp4"
