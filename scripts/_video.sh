#!/bin/zsh
# Funções compartilhadas por preparar.sh e cortar.sh.

# Filtro de rotação para vídeos do iPhone (metadado displaymatrix). Imprime "" quando não há rotação.
rotation_filter() {
  local rot
  rot=$(ffprobe -v error -select_streams v:0 -show_entries stream_side_data=rotation -of csv=p=0 "$1" | head -1)
  case "${rot%%.*}" in
    -90|270) echo ",transpose=clock" ;;
    90|-270) echo ",transpose=cclock" ;;
    180|-180) echo ",hflip,vflip" ;;
    *) echo "" ;;
  esac
}

# to_sdr_h264 <entrada> <saída> <crf> <args de áudio...>
# HDR (HLG/PQ) → SDR BT.709 pelo VideoToolbox, aplicando a rotação e zerando o metadado (senão gira duas vezes).
# SDR: só recodifica (o FFmpeg aplica a rotação sozinho).
to_sdr_h264() {
  local in="$1" out="$2" crf="$3"; shift 3
  local trc; trc=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$in")
  if [[ "$trc" == "arib-std-b67" || "$trc" == "smpte2084" ]]; then
    echo "HDR ($trc) → SDR BT.709 (VideoToolbox)"
    ffmpeg -v error -y -noautorotate -display_rotation:v:0 0 -hwaccel videotoolbox -hwaccel_output_format videotoolbox_vld \
      -i "$in" -map 0:v:0 -map 0:a:0 \
      -vf "scale_vt=color_matrix=bt709:color_primaries=bt709:color_transfer=bt709,hwdownload,format=p010le,format=yuv420p$(rotation_filter "$in")" \
      -r 30 -g 30 -c:v libx264 -preset medium -crf "$crf" -color_primaries bt709 -color_trc bt709 -colorspace bt709 "$@" "$out"
  else
    ffmpeg -v error -y -i "$in" -map 0:v:0 -map 0:a:0 -r 30 -g 30 -c:v libx264 -preset medium -crf "$crf" -pix_fmt yuv420p "$@" "$out"
  fi
}
