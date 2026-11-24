# Dados em Frações

**Essência:** número que se vê, não que se lê. Riscos e chances viram pessoas, pontos ou barras que se contam — "1 em cada 50" em vez de "2%", como o manual da marca pede para pacientes.

**Use para:** risco de ruptura, chance de complicação, comparação entre tratar × observar, antes × depois.

## Peças
- **Grade de pessoas**: 10×10 ícones simples de pessoa (SVG, `--azul-medio` a 35%); os afetados acendem em `--dourado` um a um ou em bloco, no momento do número.
- **Barra comparativa**: duas barras horizontais lado a lado (tratar × não tratar), crescendo da esquerda em 0,8 s `power3.out`, valor em Poppins 600 no fim da barra.
- **Fração grande**: "1 em cada 50" em Poppins 600, o "1" em `--dourado-claro`, sobre cartão azul.
- **Linha do tempo**: eixo fino com marcos (5 anos, 10 anos) quando o risco é acumulado.
- **Etiqueta de fonte** (mesma do estilo Manchete) em todo dado.
- **Jogada nativa**: a grade se reorganiza — os pontos de um grupo migram para mostrar a diferença entre os cenários.

## Ritmo
Um dado por cartão. Segure o resultado ≥ 2,5 s depois que tudo pousou. Contraste: comparações sempre lado a lado, mesma escala.

## Cuidados
Frações exatas no cartão só com fonte; arredondamento declarado ("cerca de 1 em 50"). Nunca escala enganosa (eixo cortado, área desproporcional). Confirme números com a skill `evidencia-clinica`.
