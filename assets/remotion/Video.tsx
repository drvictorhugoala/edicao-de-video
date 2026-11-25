// Composição modelo: vídeo cortado + cenas do mapa + efeitos sonoros. Copie para src/ e troque a lista de cenas.
// Os tempos (s) são os da transcrição original; quadro() leva para o vídeo cortado.
import React from "react";
import { AbsoluteFill, Html5Audio, OffthreadVideo, Sequence, staticFile } from "remotion";
import { Cartao } from "./Cartao";
import { carregarFontes } from "./tema";
import { quadro } from "./tempo";

carregarFontes();

type Cena = { id: string; inicio: number; fim: number; kicker?: string; titulo: string; apoio?: string; variante?: "azul" | "destaque" };
type Efeito = { arquivo: string; em: number; db: number };

const cenas: Cena[] = [
  { id: "s03", inicio: 12.4, fim: 17.8, kicker: "Pergunta", titulo: "Quando operar a carótida?" },
];

const efeitos: Efeito[] = [{ arquivo: "sfx/whoosh.mp3", em: 12.4, db: -17 }];

const volume = (db: number) => Math.pow(10, db / 20);

export const Video: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    <OffthreadVideo src={staticFile("video_cortado.mp4")} />
    {cenas.map((cena) => (
      <Sequence key={cena.id} name={cena.id} from={quadro(cena.inicio)} durationInFrames={Math.max(1, quadro(cena.fim) - quadro(cena.inicio))}>
        <Cartao kicker={cena.kicker} titulo={cena.titulo} apoio={cena.apoio} variante={cena.variante} />
      </Sequence>
    ))}
    {efeitos.map((efeito) => (
      <Sequence key={`${efeito.arquivo}@${efeito.em}`} from={quadro(efeito.em)}>
        <Html5Audio src={staticFile(efeito.arquivo)} volume={volume(efeito.db)} />
      </Sequence>
    ))}
  </AbsoluteFill>
);
