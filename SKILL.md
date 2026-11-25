---
name: edicao-de-video
description: Edita um vídeo do Dr. Victor Hugo falando para a câmera (Reels, Shorts, TikTok, YouTube) do arquivo bruto ao MP4 final — transcrição com tempo por palavra, mapa de cenas, escolha entre 6 estilos de edição (Clínico Sóbrio, Manchete com Fonte, Quadro Desenhado, Atlas em Corte, Dados em Frações, Artigo Destacado), motions no HyperFrames com o design system da marca, efeitos sonoros, corte de silêncios, SDR, −14 LUFS e ajustes por trecho. Motor padrão HyperFrames; Remotion como alternativa (vídeo inteiro ou cena de mapa/gráfico/Elements/legenda animada). Use sempre que a pessoa mandar um vídeo/arquivo .mov/.mp4 dela falando, pedir para "editar", "montar", "cortar silêncios", "colocar animações/motions", "legendar", "exportar para Reels" ou "refazer um trecho" de um vídeo já editado, mesmo sem dizer "skill" ou "HyperFrames".
---

# Edição de vídeo — Dr. Victor Hugo

Transforma um vídeo bruto do Dr. Victor falando para a câmera num vídeo vertical pronto para qualquer rede (Instagram, TikTok, YouTube Shorts), com motions da marca, efeitos sonoros e áudio no padrão das plataformas.

Exemplo completo já feito com esta skill: `videos/v1_drvictorresponde/` (estilo Clínico Sóbrio). Abra os arquivos dele quando precisar ver como uma etapa ficou na prática.

## Como trabalhar

- **Uma etapa por vez.** Mostre o resultado de cada etapa e espere o "ok" antes da próxima. A pessoa revisa conteúdo médico; pular etapas faz erro clínico chegar ao vídeo.
- Fale em português do Brasil, sem jargão técnico desnecessário.
- **Não baixe nada sem perguntar** (modelos, pacotes, músicas). Tudo que o fluxo precisa já existe nesta máquina — veja `references/ambiente.md`.
- Nunca altere o arquivo original da pessoa: trabalhe numa cópia.
- Telemetria do HyperFrames fica desligada (`DO_NOT_TRACK=1`); não rode o beacon `events`.

## Etapa 0 — Preparação (só na primeira vez da sessão)

Confira Node ≥ 22, FFmpeg, `whisper-cli`, o modelo Whisper e as skills do HyperFrames, e rode o doctor. Comandos e caminhos em `references/ambiente.md`. Se algo faltar, diga o que é e pergunte antes de instalar.

## Etapa 1 — Vídeo e pasta de trabalho

```bash
bash .claude/skills/edicao-de-video/scripts/preparar.sh "<caminho do vídeo>" <slug>
```

Cria `videos/<slug>/` com `00_original … 07_export`, copia o vídeo, gera a versão H.264 30 fps (o Chrome do render não lê HEVC), extrai o áudio 16 kHz e mede loudness. Mostre: duração, orientação (rotação do iPhone!), HDR ou não, LUFS, e um quadro para ver o enquadramento (onde ficam rosto, mãos e mesa).

## Etapa 2 — Transcrição

```bash
bash .claude/skills/edicao-de-video/scripts/transcrever.sh videos/<slug>
```

Gera `transcript_palavras.json` (tempo por palavra, formato HyperFrames), `segmentos.srt` e a lista de silêncios. Escreva `01_transcricao/transcricao.md`: tabela de trechos `mm:ss | ideia principal | fala`. Marque como duvidoso todo termo médico estranho (o Whisper troca "AVC" por "EVC", inventa palavras em trechos rápidos) e **pergunte ao Dr. Victor** o que foi dito — não adivinhe. Aplique as correções no JSON por palavra mantendo os tempos da palavra substituída.

## Etapa 3 — Mapa das cenas

Se a pessoa mandar anotações, organize-as; se pedir, proponha a partir da transcrição. Salve `02_mapa/mapa_cenas.md` com a tabela `# | tempo | o que é falado | tipo (animação / imagem / efeito) | o que aparece na tela`.

Regras do mapa:
- Uma ideia por cena; cena ancorada na palavra que a dispara.
- Os números e condutas na tela repetem **exatamente** o que ele falou. Não acrescente nuance de diretriz sem pedir — se achar que falta, aponte à parte.
- Cena 2 (ou a primeira oportunidade): faixa com nome, descritor e CRM/RQE. Última cena: CTA neutro de plataforma, parado ≥ 4 s, com a assinatura completa.
- Textos **multiplataforma**: nada de "YouTube", "canal", "link na bio" ou ícone de rede na tela. CTA padrão: "Deixe sua pergunta nos comentários."

## Etapa 4 — Estilo e referências

Escolha **um** estilo do menu (tabela abaixo). Recomende o que combina com o assunto, explique em uma linha por quê e ofereça os outros como alternativa. Se a pessoa mandar prints de referência (Pinterest, YouTube), descreva cores, fontes, movimento e ritmo, e adapte ao estilo escolhido sem sair da marca.

| Estilo | Quando usar | Arquivo |
|---|---|---|
| **Clínico Sóbrio** (padrão) | Pergunta de seguidor, conduta, "quando operar" | `references/estilos/clinico-sobrio.md` |
| **Manchete com Fonte** | Estudo novo, notícia, número que precisa de fonte | `references/estilos/manchete-com-fonte.md` |
| **Quadro Desenhado** | Explicar como algo funciona (aneurisma, AVC, fluxo) | `references/estilos/quadro-desenhado.md` |
| **Atlas em Corte** | Procedimento: vaso em corte, cateter, stent, coil | `references/estilos/atlas-em-corte.md` |
| **Dados em Frações** | Risco, chance, comparação de números | `references/estilos/dados-em-fracoes.md` |
| **Artigo Destacado** | Artigo da semana (L2), diretriz, citação de estudo | `references/estilos/artigo-destacado.md` |

Leia só o arquivo do estilo escolhido. Todos herdam a marca e o layout de `references/marca-e-layout.md` — leia sempre — e passam pelo checklist de `references/proibidos.md`.

Escolha também o **layout** (padrão: sobreposição):
- **Sobreposição** — cartões sobre o vídeo, na altura das mãos.
- **Tela dividida** — vídeo na metade de cima, gráfico na de baixo, para cenas de muita informação.
- **Inserção em tela cheia** — o gráfico cobre o vídeo por 3–6 s (a voz continua), para um desenho que precisa de espaço.

E o **motor** (padrão: HyperFrames):
- **HyperFrames** — o fluxo abaixo, com `remapear.py`.
- **Remotion** — quando a pessoa pedir, ou quando o vídeo pedir Elements prontos, mapas, gráficos complexos ou legenda animada palavra a palavra. Pode ser o vídeo inteiro ou só uma cena dentro do HyperFrames. Leia `references/remotion.md` e pergunte antes de instalar (pacotes npm, navegador de render, licença).

## Etapa 5 — Criação dos motions (HyperFrames)

Com o motor Remotion, siga `references/remotion.md` nesta etapa e na exportação; o resto do fluxo é igual.

Antes de escrever composição, invoque a skill `/hyperframes` e siga o contrato dela. Depois:

1. `npx hyperframes init videos/<slug>/04_motions --skip-skills --skill=hyperframes` (via launcher, `references/ambiente.md`).
2. Copie de `assets/`: `dv-video.css` e `index-base.html` (já tem os helpers `DV.enter/exit/words/rule` e o rig de câmera para punch-in). Copie do design system (`01_MARCA/MANUAL_IDENTIDADE_VISUAL_Dr-Victor_v1.0/`): `tokens.css` → `assets/`, `fonts/*.ttf` → `assets/fonts/`, `assets/Logos/*.svg` → `assets/logos/`. Ligue o vídeo de trabalho: `ln -s ../../00_original/<slug>_h264.mp4 assets/video.mp4`.
3. Uma cena por arquivo em `compositions/`, transparente, com entrada e saída suaves e texto curto. Monte na **linha do tempo original** primeiro; o corte vem na Etapa 7 e o `remapear.py` move tudo.
4. Gere as cenas por um script (`tools/gen_scenes.py`, como no exemplo v1) quando houver componentes repetidos: facilita ajustes globais (ex.: descer todos os cartões) sem editar 14 arquivos à mão.
5. `npx hyperframes check --json`: zero erros. Os avisos `outside_safe_zone` abaixo de y 1248 são esperados (decisão da marca, ver `marca-e-layout.md`); `line_unread` em selos curtos presos à fala pode ser aceito — diga ao usuário.
6. Prévia: `snapshot --at <um instante por cena, já pousado>` → mostre as folhas de contato; depois um render `-q draft` do vídeo inteiro e abra com `open`.

Olhe os quadros antes de mostrar: rótulo cortado na borda, cartão cobrindo boca/queixo e texto encostando na interface da rede são os erros que mais aparecem.

## Etapa 6 — Efeitos sonoros

Use os efeitos que já vêm com o HyperFrames (Pixabay, uso livre). Detalhes, níveis e variações em `references/movimento-e-som.md`. Em resumo: um efeito por entrada (whoosh em cartão, pop em selo/número, clique em frase-chave), pico 1 frame depois da imagem, ~15–19 dB abaixo da voz. Mostre uma prévia só de áudio (`m4a`) e registre a tabela em `05_sfx/efeitos.md`. Diga que os níveis foram medidos, não ouvidos.

## Etapa 7 — Corte e montagem

```bash
python3 .claude/skills/edicao-de-video/scripts/cortes.py videos/<slug>          # detecta pausas e calcula trechos
bash   .claude/skills/edicao-de-video/scripts/cortar.sh videos/<slug>           # HDR→SDR + corte com micro-fades
python3 .claude/skills/edicao-de-video/scripts/remapear.py videos/<slug>        # move cenas, sons e zoom para o corte
```

- Pausas ≥ 0,45 s viram ~0,25 s; pausas curtas e palavras de ligação ficam (fala picotada soa artificial).
- Frases repetidas (ele recomeçou a frase): procure na transcrição palavras/trechos duplicados próximos; proponha o corte e confirme antes de aplicar — corte de conteúdo é decisão dele.
- `cortar.sh` converte HDR (HLG do iPhone) para SDR pelo VideoToolbox; a conversão "ingênua" deixa o vídeo lavado.
- `remapear.py` guarda a montagem original em `06_montagem/linha_original/` e reescreve o projeto. Para mudar uma cena depois, edite/regere na linha original e rode `remapear.py` de novo.
- Render `-q draft --sdr`, confira quadros-chave (texto sincronizado com a palavra) e abra o vídeo.

## Etapa 8 — Revisão e exportação

Antes de exportar, confira e relate:
- **Voz**: meça o ruído de fundo num silêncio; aplique `scripts/limpar_voz.sh` (passa-alta 70 Hz, redução leve, compressão 2,5:1). Lapela costuma vir limpa — não exagere.
- **Textos**: leia todas as strings das cenas; erro de grafia é bloqueio. Fala coloquial citada fica como ele disse (aponte a forma culta à parte).
- **Ritmo**: nenhuma emenda estalando, nenhum cartão aparecendo antes da palavra.

Exporte:
```bash
npx hyperframes render -q delivery --sdr -f 30 -o videos/<slug>/07_export/render_hyperframes.mp4
bash .claude/skills/edicao-de-video/scripts/finalizar_audio.sh videos/<slug>/07_export/render_hyperframes.mp4 videos/<slug>/07_export/<slug>_FINAL_9x16.mp4
```
Saída: 1080×1920 (ou 1920×1080 se pedirem 16:9), 30 fps, H.264 SDR BT.709, −14 LUFS, pico ≤ −1 dBTP.

**Assista ao vídeo final antes de entregar** com o plugin `claude-video-vision` (ferramentas `video_info`, `video_watch` e `video_detail`, configurado para rodar local; ver `references/ambiente.md`):
1. `video_info` no MP4 final: confira duração, 1080×1920 e presença de áudio.
2. `video_watch` com `fps: "auto"` e `resolution: 768` para o vídeo inteiro (para vídeos acima de 2 min, segmentos com fps baixo nas falas e mais alto nas entradas de cena).
3. Compare com o mapa das cenas e a transcrição:
   - cada cartão entra junto da palavra que o dispara e sai antes do próximo;
   - nenhum cartão cobre boca ou queixo; nada encosta na interface das redes;
   - a transcrição do áudio final não perdeu palavras nos cortes, sem emenda estalando;
   - o CTA final fica parado ≥ 4 s com a assinatura completa.
4. Onde houver dúvida, `video_detail` no trecho com `resolution: 1024` para ler o texto da tela.

Liste o que encontrou com o tempo (mm:ss) e corrija antes de entregar. Se o plugin não estiver disponível, faça a mesma conferência com quadros do `ffmpeg` e diga que a revisão foi por quadros soltos. Escreva `07_export/REVISAO.md` (inclua o resultado dessa conferência) e abra o vídeo com `open`.

## Ajustes depois da entrega

"Refaça só aquele trecho": mude apenas a cena citada (na linha original + `remapear.py`), confira os quadros dela com `snapshot --at` (e, no render, `video_detail` só nesse trecho), renderize e normalize de novo. Se a mudança for global (posição de todos os cartões, um texto que aparece em várias cenas), faça no gerador e diga que afeta o vídeo todo. Salve a nova versão como `_v2`, `_v3` — nunca sobrescreva a entrega anterior.

Arquivos intermediários grandes (renders sem normalização, versões antigas): ofereça apagar, não apague sozinho.
