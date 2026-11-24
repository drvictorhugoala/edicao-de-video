# Manchete com Fonte

**Essência:** dá para entender sem som. A legenda é a protagonista: frases grandes entram em blocos de 2–3 pedaços, uma palavra-chave ganha bloco dourado, e todo número chega com a etiqueta da fonte. Ideal para quem rola o feed no mudo.

**Use para:** estudo novo, notícia médica, "saiu uma diretriz", número que precisa de lastro. Combine com a skill `evidencia-clinica` para confirmar cada número e a fonte antes de pôr na tela.

## Peças
- **Legenda-manchete** (substitui a legenda comum): Poppins 700, 64–76 px, branco com sombra escura suave, na faixa y 1150–1400 (acima da interface, abaixo do rosto). Uma linha por vez; se não couber em 2 linhas, divida a frase em duas legendas. Paráfrase curta da fala, não transcrição literal.
- **Pedaços**: cada bloco entra 0,12 s depois do anterior (escala 1,25→1 em 0,13 s, `back.out(1.6)`).
- **Palavra-chave**: no máximo uma por legenda, bloco `--dourado` que varre da esquerda para a direita em 0,12 s atrás da palavra; texto vira `--sobre-dourado`.
- **Etiqueta de fonte**: pílula pequena (28 px) "Fonte: AHA/ASA 2021" ou "Fonte: NEJM, 2024" que desliza em 0,2 s junto do número. Sem fonte confirmada → o número não entra na tela.
- **Número que rola**: contador de 0 até o valor em ~0,6 s (`power2.out`), Poppins 600, 120+ px, `--dourado-claro` sobre um cartão azul.
- **Gancho**: o número mais forte do vídeo aparece nos primeiros 0,5 s.

## Ritmo
Legenda troca no máximo a cada ~2,5 s (tempo de leitura manda, não o corte). Pausa de respiração de 1–2 s depois da virada do argumento. Cortes secos; transição permitida: flash branco de 1–2 frames só na virada.

## Cuidados
Legenda grande disputa espaço com os cartões: neste estilo, cartões são raros (só número + fonte). Nunca cubra o rosto.
