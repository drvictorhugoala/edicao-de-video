# Quadro Desenhado

**Essência:** o desenho nasce enquanto ele explica. Traço azul sobre papel off-white, como um médico rabiscando para o paciente no consultório: o vaso, o fluxo, a dilatação aparecem traço a traço, na velocidade da fala.

**Use para:** "como funciona" — aneurisma, AVC isquêmico × hemorrágico, fluxo no vaso, pressão intracraniana.

## Peças
- **Folha**: cartão `--off-white` (raio 20) na faixa das mãos, ou inserção em tela cheia quando o desenho precisa de espaço.
- **Traço**: SVG `path` com `stroke-dasharray`/`stroke-dashoffset` animado (desenho progressivo), `--azul`, 6–8 px, pontas arredondadas, leve irregularidade (caminhos desenhados à mão, não formas perfeitas).
- **Destaque**: área pintada em `--dourado` a 35–60% de opacidade que "preenche" depois do contorno (a parte doente: aneurisma, placa, sangramento).
- **Rótulos**: Inter 500, 30–34 px, `--azul-medio`, com seta fina desenhada até o ponto.
- **Setas de fluxo**: pequenas setas que percorrem o vaso (movimento constante, linear, é o único caso de animação contínua aceito).
- **Jogada nativa**: o desenho se transforma (o vaso normal ganha a dilatação; o fluxo para atrás do coágulo) na palavra-chave.

## Ritmo
Traço leva 0,8–2 s por elemento; nunca desenhe mais rápido que a fala. Um desenho por ideia; ao trocar de ideia, a folha vira (deslize lateral de 0,4 s) ou se apaga (opacidade + blur 0,25 s).

## Cuidados
Anatomia simplificada, mas correta — se a simplificação puder induzir a erro, rotule. Peça validação do Dr. Victor no mapa de cenas.
