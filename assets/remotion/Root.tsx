// Registra a composição 1080×1920, 30 fps, com a duração do vídeo cortado (src/dados/cortes.json).
import React from "react";
import { Composition } from "remotion";
import { layout } from "./tema";
import { duracaoEmQuadros, fps } from "./tempo";
import { Video } from "./Video";

export const RemotionRoot: React.FC = () => (
  <Composition id="Video" component={Video} durationInFrames={duracaoEmQuadros} fps={fps} width={layout.largura} height={layout.altura} />
);
