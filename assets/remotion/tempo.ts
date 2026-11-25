// Leva instantes da fala original (segundos, como na transcrição e no mapa das cenas) para o vídeo cortado.
// O mapa vem de scripts/remotion_dados.py → src/dados/cortes.json. Assim as cenas são escritas no tempo
// original e o corte pode mudar sem reescrever nenhuma cena: basta rodar o script de novo.
import mapa from "./dados/cortes.json";

type Trecho = { inicio: number; fim: number; saida: number };

const trechos: Trecho[] = mapa.trechos;

export const fps: number = mapa.fps;
export const duracaoEmQuadros: number = Math.round(mapa.duracao * mapa.fps);

// Instante dentro de um corte vai para o começo do trecho seguinte (mesma regra do cortes.py).
export function noCorte(segundosOriginais: number): number {
  for (const trecho of trechos) {
    if (segundosOriginais < trecho.inicio) {
      return trecho.saida;
    }
    if (segundosOriginais <= trecho.fim) {
      return trecho.saida + segundosOriginais - trecho.inicio;
    }
  }
  return mapa.duracao;
}

export function quadro(segundosOriginais: number): number {
  return Math.round(noCorte(segundosOriginais) * fps);
}
