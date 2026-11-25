// Cartão da marca na altura das mãos, com entrada e saída suaves (opacidade + deslocamento, nunca espaçamento).
// Use dentro de <Sequence from={quadro(inicio)} durationInFrames={quadro(fim) - quadro(inicio)}>.
import React from "react";
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { cor, fonte, layout, tamanho } from "./tema";

type Variante = "azul" | "destaque";

type Props = {
  kicker?: string;
  titulo: string;
  apoio?: string;
  variante?: Variante;
  entrada?: number; // quadros
  saida?: number; // quadros
};

const suave = Easing.bezier(0.22, 1, 0.36, 1);

function useEntradaSaida(entrada: number, saida: number) {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const fimEntrada = interpolate(frame, [0, entrada], [0, 1], { easing: suave, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const inicioSaida = interpolate(frame, [durationInFrames - saida, durationInFrames], [1, 0], { easing: Easing.in(Easing.cubic), extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const visivel = Math.min(fimEntrada, inicioSaida);
  return { opacity: visivel, transform: `translateY(${(1 - visivel) * 48}px)` };
}

function estiloVariante(variante: Variante): React.CSSProperties {
  if (variante === "destaque") {
    return { background: cor.branco, color: cor.azul, borderRadius: 20, borderLeft: `8px solid ${cor.dourado}`, padding: "36px 40px 36px 48px" };
  }
  return { background: cor.azul, color: cor.branco, borderRadius: 24, padding: "36px 40px" };
}

export const Cartao: React.FC<Props> = ({ kicker, titulo, apoio, variante = "azul", entrada = 12, saida = 9 }) => {
  const movimento = useEntradaSaida(entrada, saida);
  const corKicker = variante === "azul" ? cor.douradoClaro : cor.azul;
  return (
    <div style={{ position: "absolute", left: layout.margemLateral, width: layout.larguraFaixa, bottom: layout.baseCartao, boxShadow: cor.sombra, ...estiloVariante(variante), ...movimento }}>
      {kicker ? (
        <div style={{ font: `500 ${tamanho.kicker}px/1.2 ${fonte.display}`, letterSpacing: "0.14em", textTransform: "uppercase", color: corKicker }}>
          {kicker}
          <div style={{ height: 6, width: 96, background: cor.dourado, borderRadius: 3, margin: "16px 0 20px" }} />
        </div>
      ) : null}
      <div style={{ font: `600 ${tamanho.titulo}px/1.18 ${fonte.display}` }}>{titulo}</div>
      {apoio ? <div style={{ font: `400 ${tamanho.corpo}px/1.45 ${fonte.texto}`, marginTop: 16 }}>{apoio}</div> : null}
    </div>
  );
};
