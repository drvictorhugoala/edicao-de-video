"""Etapa 7: leva a montagem da linha do tempo original para o vídeo cortado.

Uso: python3 remapear.py videos/<slug> [--cta s15] [--cta-dur 5.2]

Na primeira execução copia 04_motions/index.html e compositions/ para 06_montagem/linha_original/ (a montagem no tempo
original). Depois, sempre lê de linha_original/ e reescreve 04_motions/: hosts das cenas, efeitos sonoros (mantendo o pico
1 frame após a imagem), o zoom do #cam e os tempos internos de cada cena. Para mudar uma cena, edite/regere em
linha_original/ e rode de novo.

Convenções esperadas nas cenas (as do exemplo v1 e do index-base.html):
- clip raiz:   class="clip v-layer" data-start="0" data-duration="N"
- posições:    DV.enter/exit/rule/words(tl, "#id", N ...)  e  tl.fromTo/to(..., { ... }, N);
- vetor de tempos: const t = [a, b, ...]
- vídeo:       <video id="footage" ... src="assets/<algo>.mp4" ...> ; efeitos: src="assets/sfx/<nome>.mp3"
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import json

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from cortes import make_mapper  # noqa: E402

FRAME = 1 / 30


def fmt(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


def sfx_peak(path, cache={}):
    """Pico do efeito (s), medido uma vez por arquivo com astats por janelas de 10 ms."""
    if path in cache:
        return cache[path]
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af",
                          "asetnsamples=n=441,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.Peak_level",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    levels = [float(x) for x in re.findall(r"Peak_level=(-?[\d.]+|-inf)", out.replace("-inf", "-999"))]
    cache[path] = round(levels.index(max(levels)) * 0.01, 3) if levels else 0.1
    return cache[path]


def remap_scene(src, dst, start, to_cut):
    new_start = to_cut(start)
    m = lambda local: max(0.0, to_cut(start + local) - new_start)  # noqa: E731
    text = src.read_text(encoding="utf-8")
    text = re.sub(r'(class="clip v-layer" data-start="0" data-duration=")([\d.]+)"', lambda g: f'{g[1]}{fmt(m(float(g[2])))}"', text)
    text = re.sub(r'(DV\.(?:enter|exit|rule|words)\(tl, [^,]+, )([\d.]+)', lambda g: g[1] + fmt(m(float(g[2]))), text)
    text = re.sub(r'(\}, )([\d.]+)(\);)', lambda g: g[1] + fmt(m(float(g[2]))) + g[3], text)
    text = re.sub(r'const t = \[([\d., ]+)\]', lambda g: "const t = [" + ", ".join(fmt(m(float(x))) for x in g[1].split(",")) + "]", text)
    dst.write_text(text, encoding="utf-8")


def remap_index(orig, proj, to_cut, video_name, video_dur, cta_id, cta_dur):
    html = (orig / "index.html").read_text(encoding="utf-8")
    hosts = dict(re.findall(r'<div id="(s\d+)" data-composition-id="[^"]+" data-composition-src="compositions/([^"]+)"', html))
    starts = {}

    def host(g):
        sid, mid, start, dur = g[1], g[2], float(g[3]), float(g[4])
        starts[sid] = start
        ns = to_cut(start)
        nd = cta_dur if sid == cta_id else to_cut(start + dur) - ns
        return f'<div id="{sid}"{mid}data-start="{fmt(ns)}" data-duration="{fmt(nd)}"'
    html = re.sub(r'<div id="(s\d+)"( data-composition-id="[^"]+" data-composition-src="[^"]+" )data-start="([\d.]+)" data-duration="([\d.]+)"', host, html)

    def sfx(g):
        peak = sfx_peak(proj / "assets" / "sfx" / f"{g[2]}.mp3")
        hit = float(g[3]) - FRAME + peak
        return f'{g[1]}{g[2]}.mp3" data-start="{fmt(max(0.0, to_cut(hit) + FRAME - peak))}"'
    html = re.sub(r'(src="assets/sfx/)([\w-]+)\.mp3" data-start="([\d.]+)"', sfx, html)
    html = re.sub(r'(tl\.(?:fromTo|to)\("#cam".*?\}, )([\d.]+)(\);)', lambda g: g[1] + fmt(to_cut(float(g[2]))) + g[3], html)
    html = re.sub(r'(<video id="footage"[^>]*?src=")[^"]+(" data-start="0" data-duration=")[\d.]+"',
                  lambda g: f'{g[1]}assets/{video_name}{g[2]}{fmt(video_dur - 0.02)}"', html)
    cta_start = to_cut(starts[cta_id]) if cta_id in starts else video_dur
    html = re.sub(r'(data-composition-id="main" data-start="0" data-duration=")[\d.]+"', lambda g: f'{g[1]}{fmt(max(video_dur, cta_start + cta_dur))}"', html)
    (proj / "index.html").write_text(html, encoding="utf-8")
    return {sid: (hosts[sid], starts[sid]) for sid in starts}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_dir")
    ap.add_argument("--cta", default=None, help="id da cena final (padrão: a última sNN)")
    ap.add_argument("--cta-dur", type=float, default=None, help="duração do CTA (padrão: a do index original)")
    a = ap.parse_args()
    w = pathlib.Path(a.video_dir); slug = w.name
    proj, mont = w / "04_motions", w / "06_montagem"
    orig = mont / "linha_original"
    if not orig.exists():
        orig.mkdir(parents=True)
        shutil.copy(proj / "index.html", orig / "index.html")
        shutil.copytree(proj / "compositions", orig / "compositions")
        print("linha do tempo original guardada em", orig)
    cortes = json.load(open(mont / "cortes.json"))
    to_cut = make_mapper(cortes["segments"])
    cut_video = mont / f"{slug}_cortado.mp4"
    link = proj / "assets" / "video_cortado.mp4"
    if link.exists() or link.is_symlink():
        link.unlink()
    link.symlink_to(pathlib.Path("../../06_montagem") / cut_video.name)

    html = (orig / "index.html").read_text(encoding="utf-8")
    ids = re.findall(r'<div id="(s\d+)" data-composition-id', html)
    cta = a.cta or ids[-1]
    cta_dur = a.cta_dur or float(re.search(rf'<div id="{cta}"[^>]*data-duration="([\d.]+)"', html)[1])
    scenes = remap_index(orig, proj, to_cut, link.name, cortes["duration"], cta, cta_dur)
    for sid, (name, start) in scenes.items():
        src, dst = orig / "compositions" / name, proj / "compositions" / name
        if sid == cta:  # o CTA fica depois da última fala: tempos internos não mudam
            shutil.copy(src, dst)
        else:
            remap_scene(src, dst, start, to_cut)
    print(f"remapeado: {len(scenes)} cenas · vídeo cortado {cortes['duration']} s · CTA {cta} {cta_dur} s")


if __name__ == "__main__":
    main()
