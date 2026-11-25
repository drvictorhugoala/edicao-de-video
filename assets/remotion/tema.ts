// Tokens da marca Dr. Victor em escala 1080×1920. Espelham 01_MARCA/.../tokens.css: se o manual mudar, mude aqui.
import { continueRender, delayRender, staticFile } from "remotion";

export const cor = {
  azul: "#3b4259",
  azulMedio: "#5c6273",
  dourado: "#bf8e63", // só forma, régua, numeral, selo; nunca texto corrido
  douradoClaro: "#d2b093", // texto dourado pequeno sobre azul
  sobreDourado: "#262b38", // único texto sobre dourado
  offWhite: "#f2f2f2",
  branco: "#ffffff",
  sombra: "0 18px 48px rgba(20, 26, 46, .35)",
} as const;

export const fonte = {
  display: "Poppins, sans-serif",
  texto: "Inter, sans-serif",
} as const;

// Escala de texto do manual; nada abaixo de 28 px.
export const tamanho = { titulo: 58, subtitulo: 42, corpo: 38, numeral: 64, rodape: 28, kicker: 32 } as const;

// Layout 9:16 decidido pelo Dr. Victor: cartões na altura das mãos, longe do rosto e acima da interface das redes.
export const layout = { largura: 1080, altura: 1920, fps: 30, margemLateral: 120, larguraFaixa: 840, baseCartao: 440 } as const;

export const assinatura = "Dr. Victor Hugo Espíndola Ala · CRM-DF 18992 · RQE 14807/17941";

const arquivosFonte: Array<[string, string, string]> = [
  ["Poppins", "400", "fonts/Poppins-Regular.ttf"],
  ["Poppins", "500", "fonts/Poppins-Medium.ttf"],
  ["Poppins", "600", "fonts/Poppins-SemiBold.ttf"],
  ["Poppins", "700", "fonts/Poppins-Bold.ttf"],
  ["Inter", "100 900", "fonts/Inter-Variable.ttf"],
];

// Carrega as fontes de public/fonts antes do primeiro quadro (sem isso o render sai com a fonte do sistema).
export function carregarFontes(): void {
  if (typeof document === "undefined") {
    return;
  }
  const handle = delayRender("Fontes da marca");
  const carregamentos = arquivosFonte.map(([familia, peso, arquivo]) => {
    const face = new FontFace(familia, `url(${staticFile(arquivo)})`, { weight: peso });
    document.fonts.add(face);
    return face.load();
  });
  Promise.all(carregamentos).then(() => continueRender(handle));
}
