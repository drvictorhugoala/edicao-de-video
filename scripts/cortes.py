"""Etapa 7: detecta as pausas e calcula os trechos mantidos e o mapa de tempo original → cortado.

Uso: python3 cortes.py videos/<slug> [--min 0.45] [--fim <segundos>]
Grava videos/<slug>/06_montagem/cortes.json. Também é importado por remapear.py (make_mapper).
"""
import argparse
import json
import math
import pathlib
import re
import subprocess

TAIL, HEAD = 0.12, 0.13   # respiro mantido depois e antes da fala (pausa final ≈ 0,25 s)
START_HEAD = 0.15         # respiro antes da primeira palavra
FPS = 30


def detect_silences(wav, min_gap):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af", f"silencedetect=noise=-38dB:d={min_gap}",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    merged = []
    for a, b in zip(starts, ends):  # um estalo de < 0,15 s entre dois silêncios não é fala
        if merged and a - merged[-1][1] < 0.15:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged


def keep_segments(silences, video_end, end):
    """Trechos mantidos. O silêncio inicial some; o final fica até `end` (fica sob o CTA)."""
    first_speech = silences[0][1] if silences and silences[0][0] < 0.05 else 0.0
    inner = [s for s in silences if s[0] >= 0.05 and s[1] < video_end - 0.05]
    segs, cursor = [], max(0.0, first_speech - START_HEAD)
    for a, b in inner:
        segs.append((round(cursor, 3), round(a + TAIL, 3)))
        cursor = b - HEAD
    segs.append((round(cursor, 3), round(end, 3)))
    return segs


def out_length(s, e, fps=FPS):
    """Duração real do trecho no arquivo cortado: o concat estica cada trecho ao maior entre vídeo (frames) e áudio."""
    frames = math.ceil(e * fps - 1e-9) - math.ceil(s * fps - 1e-9)
    return max(frames / fps, e - s)


def make_mapper(segs):
    def to_cut(t):
        acc = 0.0
        for s, e in segs:
            if t < s:
                return round(acc, 3)
            if t <= e:
                return round(acc + t - s, 3)
            acc += out_length(s, e)
        return round(acc, 3)
    return to_cut


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_dir")
    ap.add_argument("--min", type=float, default=0.45, help="pausa mínima a encurtar (s)")
    ap.add_argument("--fim", type=float, help="onde o vídeo termina (padrão: última fala + 0,8 s)")
    a = ap.parse_args()
    w = pathlib.Path(a.video_dir)
    wav = w / "01_transcricao" / "voz_16k.wav"
    duration = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)],
                                    capture_output=True, text=True).stdout)
    silences = detect_silences(wav, a.min)
    last_speech = silences[-1][0] if silences and silences[-1][1] >= duration - 0.05 else duration
    end = min(duration, a.fim if a.fim else last_speech + 0.8)
    segs = keep_segments(silences, duration, end)
    total = sum(out_length(s, e) for s, e in segs)
    (w / "06_montagem").mkdir(exist_ok=True)
    json.dump({"segments": segs, "duration": round(total, 3), "source_duration": duration},
              open(w / "06_montagem" / "cortes.json", "w"), indent=1)
    print(f"{len(segs)} trechos · {total:.2f} s (de {duration:.2f} s) · {len(segs) - 1} pausas encurtadas")


if __name__ == "__main__":
    main()
