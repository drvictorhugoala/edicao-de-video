# Ambiente desta máquina

Tudo abaixo foi verificado em 24/11/2026. Se algo não bater, confira antes de instalar.

| Item | Onde / como |
|---|---|
| Node | ≥ 22 (havia v24) |
| FFmpeg / FFprobe | `/opt/homebrew/bin` (versão 9.x) |
| Whisper | `whisper-cli` (whisper.cpp) em `/opt/homebrew/bin` |
| Modelo Whisper | `/Users/Shared/whisper-models/ggml-large-v3-turbo-q5_0.bin` (português bom; **não baixe outro**) |
| Alternativa | `/Users/Shared/whisper-flow/.venv` (openai-whisper, sem modelo em cache — usar só se pedirem) |
| Skills HyperFrames | `.claude/skills/hyperframes*`, `media-use` (instaladas no projeto) |
| Skills Remotion | globais em `~/.agents/skills/remotion-*` (links em `~/.claude/skills/`), versão 4.0.547; motor alternativo, ver `remotion.md` |
| claude-video-vision (revisão) | plugin v1.4.0, registrado em `~/.claude/settings.json` (`extraKnownMarketplaces`, tipo `directory`) apontando para a cópia já instalada em outro usuário deste Mac, sem duplicar arquivos. Config local em `~/.claude-video-vision/config.json` (whisper.cpp, `large-v3`, ~3,1 GB em `~/.claude-video-vision/models/ggml-large-v3.bin`, checksum conferido; o `large-v3-turbo` segue disponível como atalho para `/Users/Shared/whisper-models`). Não use os backends Gemini/OpenAI sem pedir: enviariam o áudio para fora |
| Design system da marca | `01_MARCA/MANUAL_IDENTIDADE_VISUAL_Dr-Victor_v1.0/` (tokens.css, fonts, assets/Logos) |

## Rodar o CLI do HyperFrames

Nunca `npx hyperframes` direto. Use o launcher da skill, a partir da pasta do projeto do vídeo:

```bash
L="<raiz do projeto>/.claude/skills/hyperframes/scripts/plugin-cli.mjs"
DO_NOT_TRACK=1 npm_config_cache="$HOME/.npm-cache-automacoes" node "$L" <comando>
```

- `npm_config_cache` alternativo: o `~/.npm` desta máquina tem arquivos de root e o npx falha com EACCES.
- `DO_NOT_TRACK=1`: telemetria desligada (regra do usuário: não enviar dados sem instrução).
- Doctor: `node "$L" doctor`. Kokoro, MusicGen e Docker aparecem como faltando — são opcionais, ignore.

## Armadilhas já encontradas

| Sintoma | Causa | Solução |
|---|---|---|
| `Unrecognized option 'filter_complex_script'` | FFmpeg 9 mudou a sintaxe | `-/filter_complex arquivo.txt` |
| Render sai HEVC Main10 BT.2020 | iPhone grava HDR (HLG); o render promove para HDR | converter para SDR antes (`cortar.sh`) e renderizar com `--sdr` |
| Vídeo lavado/acinzentado | conversão HLG→709 sem tonemap | VideoToolbox: `-hwaccel videotoolbox … scale_vt=color_matrix=bt709:color_primaries=bt709:color_transfer=bt709` |
| Vídeo deitado ou girado duas vezes | `.mov` do iPhone com rotação −90; o caminho VideoToolbox não aplica a rotação e copia o metadado | `scripts/_video.sh` aplica `transpose` e zera o metadado (`-display_rotation:v:0 0`); confirme 1080×1920 e sem `rotation` no ffprobe |
| Corte dessincroniza ~0,1 s no fim | concat estica cada trecho ao maior entre vídeo (frames) e áudio | `cortes.py` já calcula assim (`out_length`) |
| Plugin claude-video-vision não conecta (`Connection closed`) | o servidor dele sobe por `npx` e cai no EACCES do `~/.npm` | `"env": {"npm_config_cache": "<home>/.npm-cache-automacoes"}` no `~/.claude/settings.json`; vale a partir da sessão seguinte |
| Primeiras palavras da transcrição em 0–1 s, mas a fala começa depois | Whisper puxa o tempo das palavras para o início quando o vídeo abre em silêncio | o corte (silencedetect) está certo; `remotion_dados.py` encaixa essas palavras no trecho seguinte. Nas cenas, ancore na fala real, não no tempo dessas palavras |
| Render demora | ~12 min para 1:50 em 1080×1920 | rode em segundo plano e avise |
| `check` reprova `letterSpacing` animado | reflow de texto | anime opacidade/transform, não espaçamento |
