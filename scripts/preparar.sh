#!/bin/zsh
# Etapa 1: cria a pasta de trabalho do vídeo, copia o original e prepara as versões de trabalho.
# Uso: preparar.sh "<vídeo original>" <slug>   (rodar na raiz do projeto)
set -euo pipefail
SRC="$1"; SLUG="$2"; W="videos/$SLUG"
[[ -f "$SRC" ]] || { echo "Arquivo não encontrado: $SRC" >&2; exit 1; }
mkdir -p "$W"/{00_original,01_transcricao,02_mapa,03_referencias,05_sfx,06_montagem,07_export}
EXT="${SRC##*.}"; ORIG="$W/00_original/${SLUG}.${EXT:l}"
[[ -f "$ORIG" ]] || cp -p "$SRC" "$ORIG"

# Versão de trabalho H.264 30 fps, já em SDR e em pé (o Chrome do render não lê HEVC; HDR deixaria as prévias em HDR).
source "${0:A:h}/_video.sh"
to_sdr_h264 "$ORIG" "$W/00_original/${SLUG}_h264.mp4" 18 -c:a aac -b:a 192k -movflags +faststart
ffmpeg -v error -y -i "$ORIG" -vn -ac 1 -ar 16000 -c:a pcm_s16le "$W/01_transcricao/voz_16k.wav"
ffmpeg -v error -y -ss 5 -i "$W/00_original/${SLUG}_h264.mp4" -frames:v 1 -vf scale=540:-1 "$W/00_original/quadro_5s.jpg"

echo "== Ficha"
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate,color_transfer:stream_side_data=rotation \
  -of default=nw=1 "$ORIG"
ffprobe -v error -show_entries format=duration -of default=nw=1 "$ORIG"
echo "(color_transfer arib-std-b67 = HDR HLG do iPhone; rotation -90 = vertical)"
ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$W/00_original/${SLUG}_h264.mp4" | head -1 | sed 's/^/versão de trabalho: /'
ffmpeg -hide_banner -i "$ORIG" -af loudnorm=print_format=summary -f null - 2>&1 | grep -E "Input (Integrated|True Peak|LRA)"
echo "Quadro para enquadramento: $W/00_original/quadro_5s.jpg"
