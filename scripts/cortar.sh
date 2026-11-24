#!/bin/zsh
# Etapa 7: converte para SDR (tonemap do VideoToolbox se for HDR) e corta conforme cortes.json, com micro-fades no áudio.
# Uso: cortar.sh videos/<slug>   → videos/<slug>/06_montagem/<slug>_cortado.mp4
set -euo pipefail
W="$1"; M="$W/06_montagem"; SLUG="${W:t}"
ORIG=$(ls "$W"/00_original/"$SLUG".* | grep -v _h264 | head -1)
FULL="$M/sdr_full.mov"

source "${0:A:h}/_video.sh"
to_sdr_h264 "$ORIG" "$FULL" 16 -c:a pcm_s16le

python3 - "$M" <<'EOF'
import json, sys, pathlib
m = pathlib.Path(sys.argv[1]); segs = json.load(open(m / "cortes.json"))["segments"]; F = 0.012
v = [f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{i}]" for i, (s, e) in enumerate(segs)]
a = [f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d={F},afade=t=out:st={e - s - F:.3f}:d={F}[a{i}]" for i, (s, e) in enumerate(segs)]
cat = "".join(f"[v{i}][a{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[v][a]"
(m / "cortes_filtro.txt").write_text(";".join(v + a + [cat]))
EOF

# FFmpeg 9: o filtro vem de arquivo com "-/filter_complex"
ffmpeg -v error -y -i "$FULL" -/filter_complex "$M/cortes_filtro.txt" -map "[v]" -map "[a]" \
  -c:v libx264 -crf 16 -preset medium -g 30 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:a aac -b:a 256k -movflags +faststart "$M/${SLUG}_cortado.mp4"
rm "$FULL"
ffprobe -v error -show_entries format=duration:stream=codec_name,color_transfer -of csv=p=0 "$M/${SLUG}_cortado.mp4"
echo "Esperado (cortes.json): $(python3 -c "import json;print(json.load(open('$M/cortes.json'))['duration'])") s"
