# edicao-de-video

Skill do Claude Code que edita os vídeos do Dr. Victor Hugo Espíndola Ala falando para a câmera, do arquivo bruto ao MP4 final pronto para Instagram, TikTok e YouTube Shorts.

## O que faz

1. **Preparação**: confere Node, FFmpeg, Whisper e HyperFrames.
2. **Vídeo**: cria a pasta de trabalho e a versão H.264 SDR na vertical.
3. **Transcrição**: Whisper em português, com o tempo de cada palavra.
4. **Mapa das cenas**: tempo · fala · tipo · o que aparece na tela.
5. **Estilo**: escolha entre 6 estilos.
6. **Motions**: animações no HyperFrames com o design system da marca.
7. **Efeitos sonoros**: whoosh, pop e clique, bem abaixo da voz.
8. **Corte**: tira os silêncios e remapeia cenas e sons no novo tempo.
9. **Revisão e exportação**: voz limpa e MP4 em 1080×1920, 30 fps, −14 LUFS.

### Estilos

| Estilo | Para |
|---|---|
| Clínico Sóbrio | Pergunta de seguidor, conduta |
| Manchete com Fonte | Estudo novo, número com fonte |
| Quadro Desenhado | Como algo funciona |
| Atlas em Corte | Procedimentos e dispositivos |
| Dados em Frações | Riscos e comparações |
| Artigo Destacado | Artigo da semana, diretriz |

## Instalação

Copie a pasta para as skills do projeto (ou para `~/.claude/skills/`):

```bash
git clone https://github.com/drvictorhugoala/edicao-de-video.git .claude/skills/edicao-de-video
```

Outra opção é baixar o arquivo `edicao-de-video.skill` na página **Releases** do repositório.

Depois, no Claude Code, basta mandar o vídeo e pedir: "edita esse vídeo".

## Requisitos

- macOS (a conversão HDR→SDR usa o VideoToolbox)
- Node 22 ou mais novo, FFmpeg 7 ou mais novo, `whisper-cli` (whisper.cpp) e o modelo `ggml-large-v3-turbo`
- As skills do HyperFrames no projeto (`npx skills add heygen-com/hyperframes`)
- O design system da marca em `01_MARCA/MANUAL_IDENTIDADE_VISUAL_Dr-Victor_v1.0/`. Ele não está neste repositório

Caminhos e armadilhas conhecidas: [`references/ambiente.md`](references/ambiente.md).

## Créditos

- Os efeitos sonoros vêm do pacote do HyperFrames (Pixabay Content License).
- Os estilos foram escritos para esta skill. Eles se inspiram na linguagem visual de bibliotecas públicas de estilos de vídeo, sem reproduzir os textos delas.
