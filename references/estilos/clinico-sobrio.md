# Clínico Sóbrio (padrão)

**Essência:** o médico fala, o cartão confirma. Cartões compactos sobre o tronco, uma ideia por vez, ritmo calmo. A credibilidade vem do rosto dele; os cartões só organizam o raciocínio.

**Use para:** pergunta de seguidor, "quando operar", sinais de alerta, conduta explicada. Exemplo pronto: `videos/v1_drvictorresponde/` (gerador em `04_motions/tools/gen_scenes.py`).

## Peças
- **Selo de abertura** (acima da cabeça): cartão azul "Dr. Victor Responde · suas perguntas, respondidas" ou o tema do vídeo.
- **Faixa de nome** (componente Assinatura): régua dourada + nome + descritor + CRM/RQE + ícone dourado.
- **Kicker + número**: "#1 · Pergunta de um seguidor".
- **Comentário**: cartão branco com "Comentário de um seguidor" e a pergunta, palavras acendendo no ritmo da fala (opacidade 0,12→1).
- **Ilustração simples** num cartão branco (vaso com placa, barra de porcentagem): SVG com cores da marca, uma forma que cresce no momento do número.
- **Metáfora visual** (ex.: balança risco × benefício) que reaparece e muda de estado quando a conclusão chega — é a jogada nativa.
- **Frase-chave**: cartão azul, título 66 px, palavras uma a uma, 1–2 palavras em `--dourado-claro`.
- **Selos de decisão**: pílula dourada "Tratar" com ✓; pílula contorno "Sem indicação" com ✕.
- **Resumo**: cartão azul com os casos em linhas (✓/✕); destaque com borda dourada no caso da pergunta.
- **CTA**: tela azul, logo completo dourado, pergunta-condição ("Tem estenose de carótida?"), "Deixe sua pergunta nos comentários.", @ e assinatura. ≥ 4 s parado.

## Ritmo
Um cartão a cada 6–10 s; cada cartão entra na palavra-gatilho e sai antes do próximo. Entradas variadas: deslize + blur, régua que cresce, palavras uma a uma, forma que cresce, selo com leve overshoot (`back.out(1.4)`).
