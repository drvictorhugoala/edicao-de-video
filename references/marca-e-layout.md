# Marca e layout (vale para todos os estilos)

Fonte de verdade: `01_MARCA/MANUAL_IDENTIDADE_VISUAL_Dr-Victor_v1.0/` (design system em HTML/CSS) e o PDF do manual. Use os tokens do `tokens.css`; não digite cores à mão. O PDF da MED Magno em `Refs/` é a marca da comunidade, **não** a do Dr. Victor.

## Cores

| Token | Hex | Uso no vídeo |
|---|---|---|
| `--azul` | #3B4259 | Cartões escuros, fundo do CTA |
| `--dourado` | #BF8E63 | Acento: régua, diagonal, números grandes, selo. Nunca texto corrido |
| `--dourado-claro` | #D2B093 | Texto dourado pequeno sobre azul (palavra-chave, 50%, CRM) |
| `--off-white` / `--branco` | #F2F2F2 / #FFF | Cartões claros, texto sobre azul |
| `--azul-medio` | #5C6273 | Texto secundário sobre claro |
| `--sobre-dourado` | #262B38 | Único texto permitido sobre dourado |

Contraste: dourado sobre claro só em formas; branco sobre dourado nunca.

## Tipografia (escala 1080 px)

Poppins (títulos, números, kicker em caixa alta com tracking 0,14em) e Inter (apoio, rodapé). Título 58 · subtítulo 42 · corpo 38 · numeral 64+ · rodapé 28. **Nada abaixo de 28 px** (piso de leitura no celular).

## Sinais da marca

1. Diagonal dourada (~33° da vertical) — abertura/fechamento.
2. Régua dourada 72–96 × 6 px abaixo do kicker.
3. Card de destaque: branco, raio 20, filete esquerdo dourado de 8 px.
4. Selo de ação: pílula dourada, texto `--sobre-dourado` em Poppins 600.
5. Assinatura: "Dr. Victor Hugo Espíndola Ala · CRM-DF 18992 · RQE 14807/17941" — obrigatória (CFM 2.336/2023) na faixa de nome e no cartão final.

Logo só pelos SVGs (sobre azul: dourado ou branco; sobre o vídeo: branco). Sem sombra, brilho, contorno.

Voz: educativo, acolhedor, sóbrio. Evite "excelência", "referência", "mais seguro", promessa, comparação com colegas. Descritor por extenso: "neurocirurgião vascular e neurorradiologista intervencionista".

## Layout 9:16 (1080×1920)

Decisão do Dr. Victor (24/11/2026): **cartões na altura das mãos**, nunca na frente do rosto, e acima da faixa de interface das redes.

| Zona | y | Uso |
|---|---|---|
| Topo da interface | 0–270 | nada |
| Acima da cabeça | ~280–440 | selo de abertura curto |
| Rosto | ~440–830 | **livre** |
| Tronco/mãos | ~830–1480 | cartões (ancorar pela base: `bottom: 440px`) |
| Legenda/@/botões das redes | 1500–1920 | nada |
| Laterais | x 120–888 | coluna de texto (fora da barra de ícones à direita) |

Confirme no quadro de cada vídeo: se ele estiver mais perto da câmera, o rosto desce — ajuste o `bottom` para o cartão não tocar o queixo.

O `check` do HyperFrames usa a faixa conservadora do Reels (até y 1248) e vai avisar `outside_safe_zone`: é esperado.

### Tela dividida
Vídeo reposicionado na metade de cima (wrapper `#cam` com `y` negativo e leve zoom, transição 0,6 s `power2.inOut` num intervalo entre cartões), gráfico ocupando y 980–1480. Volte o vídeo ao quadro cheio quando a cena acabar.

### Inserção em tela cheia
Fundo `--azul` ou `--off-white` cobre o vídeo (fade 0,3 s), 3–6 s, voz continua. Use para desenhos que precisam de espaço (Atlas em Corte, Quadro Desenhado). No máximo 2 por vídeo — o rosto do médico é o que gera confiança.
