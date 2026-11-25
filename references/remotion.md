# Motor Remotion (alternativa ao HyperFrames)

O HyperFrames continua sendo o motor padrão: é o que o exemplo v1 usa e o que o `remapear.py` entende. O Remotion (vídeo em React) entra em dois casos:

| Caso | Como usar |
|---|---|
| **Vídeo inteiro em Remotion** — a pessoa pede, ou o vídeo depende de Elements prontos, mapas, gráficos ou legendas animadas palavra a palavra | Projeto em `videos/<slug>/04_remotion/`, com o vídeo cortado ao fundo |
| **Uma cena só** (mapa, gráfico complexo) dentro da montagem HyperFrames | Renderize a cena transparente em WebM e use como `<video>` na composição HyperFrames |

Para a parte técnica do Remotion, invoque as skills dele (instaladas globalmente em `~/.agents/skills/`): `remotion-best-practices` (roteador), `remotion-create`, `remotion-markup`, `remotion-captions`, `remotion-elements`, `remotion-maps`, `remotion-render`, `remotion-studio`. Esta página só diz como encaixá-lo no fluxo e na marca.

## Antes de começar: pergunte

- **Instalação**: `create-video` instala pacotes npm, e o primeiro render baixa o Chrome Headless Shell (cerca de 140 MB). Pela regra do Dr. Victor, peça autorização antes.
- **Licença**: o Remotion é gratuito para pessoa física e empresas pequenas, e pago para empresas maiores. Confira com a skill `remotion-license` e pergunte ao Dr. Victor em qual caso ele se encaixa. Só passe `--license-key` com o ok dele: a chave faz o Remotion registrar os renders no servidor da empresa.
- Use o cache alternativo do npm: `npm_config_cache="$HOME/.npm-cache-automacoes"` (ver `ambiente.md`).

## Vídeo inteiro em Remotion

As etapas 1 a 4 e 6 não mudam. Na Etapa 7, rode `cortes.py` e `cortar.sh` **antes** de montar as cenas: o Remotion trabalha direto sobre o vídeo cortado.

1. Projeto: `npx create-video@latest --yes --blank --no-tailwind videos/<slug>/04_remotion`.
2. Copie `assets/remotion/*.tsx|ts` da skill para `04_remotion/src/` (substitua o `Root.tsx` do modelo; o `index.ts` com `registerRoot` continua).
3. `public/`:
   - `fonts/*.ttf` do design system (`01_MARCA/.../fonts/`), `logos/*.svg`, `sfx/*.mp3` (os do HyperFrames, ver `movimento-e-som.md`).
   - O vídeo cortado como **link físico ou cópia**, nunca link simbólico (o bundler não segue symlink e o render dá 404):
     `ln videos/<slug>/06_montagem/<slug>_cortado.mp4 videos/<slug>/04_remotion/public/video_cortado.mp4`
4. Dados do corte e legendas:
   ```bash
   python3 .claude/skills/edicao-de-video/scripts/remotion_dados.py videos/<slug>
   ```
   Gera `src/dados/cortes.json` (mapa original → cortado) e `src/dados/legendas.json` (`Caption[]` do `@remotion/captions`, já no tempo cortado). Rode de novo sempre que o corte mudar.
5. Escreva as cenas em `Video.tsx` (lista `cenas` e `efeitos`) **no tempo original** da transcrição: `quadro(s)` em `tempo.ts` converte para o vídeo cortado. É o equivalente do `remapear.py`.
6. Componentes: `Cartao` (azul ou destaque, na altura das mãos, `bottom: 440`). Novos componentes usam só `tema.ts`: cores, escala de texto (nada abaixo de 28 px), `layout.baseCartao`. Anime opacidade e transform, com `interpolate` e easing suave; nunca anime espaçamento de letras.
7. Prévia: Remotion Studio (`npx remotion studio --no-open`, servidor de longa duração, então peça antes) ou quadros soltos:
   ```bash
   npx remotion still src/index.ts Video out/cena.png --frame=<quadro>
   ```
   Confira os mesmos erros de sempre: texto cortado na borda, cartão cobrindo boca ou queixo.

### Exportação

```bash
npx remotion render src/index.ts Video ../07_export/render_remotion.mp4 \
  --codec=h264 --crf=16 --color-space=bt709 --pixel-format=yuv420p
bash .claude/skills/edicao-de-video/scripts/finalizar_audio.sh videos/<slug>/07_export/render_remotion.mp4 videos/<slug>/07_export/<slug>_FINAL_9x16.mp4
```

A voz limpa (`limpar_voz.sh`) e a normalização −14 LUFS são as mesmas do HyperFrames.

## Uma cena em Remotion dentro do HyperFrames

1. Crie a composição só da cena, com fundo transparente (sem `OffthreadVideo`, sem cor de fundo) e duração da cena.
2. Renderize em WebM com alfa (o Chrome do HyperFrames lê VP9 com transparência; não lê ProRes):
   ```bash
   npx remotion render src/index.ts Cena out/cena.webm --codec=vp9 --image-format=png --pixel-format=yuva420p
   ```
3. Copie para `04_motions/assets/` e coloque como `<video muted playsinline>` na composição da cena. O tempo dela segue o `remapear.py` como qualquer outra.

## Armadilhas

| Sintoma | Causa | Solução |
|---|---|---|
| `404 … public/video_cortado.mp4` no render | vídeo em `public/` é link simbólico | link físico (`ln` sem `-s`) ou cópia |
| Texto na fonte do sistema | fontes não carregadas antes do quadro | `carregarFontes()` do `tema.ts` no topo do `Video.tsx` |
| Cenas fora de sincronia após mudar o corte | `cortes.json` antigo | rode `remotion_dados.py` de novo |
| Render lavado | vídeo HDR no fundo | use o vídeo cortado em SDR do `cortar.sh`, nunca o `.mov` original |
