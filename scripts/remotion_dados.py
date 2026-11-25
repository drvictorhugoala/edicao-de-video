"""Motor Remotion: exporta o mapa do corte e as legendas para dentro do projeto Remotion.

Uso: python3 remotion_dados.py videos/<slug> [--projeto 04_remotion]

Escreve em <projeto>/src/dados/:
- cortes.json   {fps, duracao, trechos: [{inicio, fim, saida}]}. O tempo.ts usa isso para levar um instante
                da fala original para o vídeo cortado. Sem 06_montagem/cortes.json, o mapa é a identidade.
- legendas.json Caption[] do @remotion/captions (ms, já no tempo do vídeo cortado). Palavras que o Whisper
                marcou dentro de um corte são encaixadas no começo do trecho seguinte, sem sair da ordem.
"""
import argparse
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from cortes import FPS, make_mapper, out_length  # noqa: E402


def video_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def cut_map(video_dir, slug):
    cortes = video_dir / "06_montagem" / "cortes.json"
    if cortes.exists():
        data = json.loads(cortes.read_text())
        return data["segments"], data["duration"]
    duration = video_duration(video_dir / "00_original" / f"{slug}_h264.mp4")
    return [[0.0, duration]], duration


def build_segments(segments):
    result, start_out = [], 0.0
    for start, end in segments:
        result.append({"inicio": start, "fim": end, "saida": round(start_out, 3)})
        start_out += out_length(start, end)
    return result


MIN_WORD = 0.12  # duração mínima (s) de uma palavra empurrada para fora de um corte


def build_captions(words, segments):
    """O corte vem do áudio real (silencedetect); palavra que cai num corte é erro de tempo do Whisper
    (comum no silêncio inicial). Em vez de sumir com ela, encaixa no começo do trecho seguinte, em ordem."""
    to_cut = make_mapper(segments)
    captions, previous_end = [], 0.0
    for word in words:
        start = max(to_cut(word["start"]), previous_end)
        end = max(to_cut(word["end"]), start + MIN_WORD)
        previous_end = end
        captions.append({"text": " " + word["text"].strip(), "startMs": round(start * 1000),
                         "endMs": round(end * 1000), "timestampMs": round(start * 1000), "confidence": None})
    return captions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video_dir")
    parser.add_argument("--projeto", default="04_remotion")
    args = parser.parse_args()
    video_dir = pathlib.Path(args.video_dir)
    segments, duration = cut_map(video_dir, video_dir.name)
    words = json.loads((video_dir / "01_transcricao" / "transcript_palavras.json").read_text())

    destination = video_dir / args.projeto / "src" / "dados"
    destination.mkdir(parents=True, exist_ok=True)
    mapa = {"fps": FPS, "duracao": duration, "trechos": build_segments(segments)}
    (destination / "cortes.json").write_text(json.dumps(mapa, ensure_ascii=False, indent=1))
    captions = build_captions(words, segments)
    (destination / "legendas.json").write_text(json.dumps(captions, ensure_ascii=False, indent=1))
    print(f"{len(mapa['trechos'])} trechos, {duration:.3f} s, {len(captions)} palavras → {destination}")


if __name__ == "__main__":
    main()
