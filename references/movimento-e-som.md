# Movimento e som (padrão de todos os estilos)

Cada estilo pode trocar valores, mas parte daqui.

## Movimento

- Entrada 0,45–0,6 s, `expo.out` (chega devagar, cauda longa); deslize curto de 24–40 px + blur 8→0. Helper: `DV.enter`.
- Saída 0,25–0,3 s, `power3.in`, um movimento só. Helper: `DV.exit`.
- Palavras escalonadas 60–120 ms; itens de lista 40–80 ms.
- Texto pousado fica **parado** (nada de flutuar, pulsar, crescer devagar).
- Leitura: 0,5 s + 0,3 s por palavra antes de sair. A última tela ≥ 4 s.
- Use sempre `fromTo` dentro das cenas (o runtime re-busca a cena).
- Ancore cada elemento na palavra da fala (tempo do `transcript_palavras.json`).
- Uma "jogada nativa" por vídeo, no ponto alto (ex.: a balança que pesa quando ele diz "é menor"). Não espalhe efeito em toda cena.
- Punch-in no rosto: wrapper `#cam`, 1,00→1,08 em 0,6 s `power2.inOut`, origem no rosto (`transform-origin: 50% 32%`). No máximo 2–3 por vídeo.

## Efeitos sonoros

Origem: pacote do HyperFrames, licença Pixabay (uso comercial livre, sem atribuição). Pasta:
`~/.npm-cache-automacoes/_npx/*/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx/`
(se o caminho mudar: `find ~/.npm-cache-automacoes -path "*media-use/audio/assets/sfx" -type d`).

| Som | Quando | Volume (`data-volume`) | Pico no arquivo |
|---|---|---|---|
| whoosh (a/b/c) | cartão entrando | 0,08 | ~0,16 s |
| pop (a/b) | selo, número, badge pousando | 0,18 | ~0,12 s |
| click | frase-chave, destaque | 0,20 | ~0,07 s |

- Crie variações de tom para não repetir o mesmo som: `ffmpeg -i whoosh.mp3 -af "asetrate=44100*0.88,aresample=44100" whoosh-b.mp3` (0,88 e 1,12).
- Posição: `data-start = momento_da_imagem + 1/30 − pico`. Meça o pico com `hyperframes audio <arquivo> --json` (`moments.peak`).
- Todos na mesma faixa (`data-track-index="3"`), cada `<audio>` com `id`.
- Meta medida no exemplo v1: efeitos ~19 dB abaixo da voz mais alta e ~12–15 dB abaixo do pico. Meça com `ebur128` (momentânea máx.) voz × efeitos isolados.
- Sem trilha musical por padrão (vídeo de autoridade médica, voz é o centro). Se pedirem música, ela fica ~0,14 de volume sob a voz e precisa de fonte com licença clara.
- Sem tons sintetizados, sinos ou "ding".
