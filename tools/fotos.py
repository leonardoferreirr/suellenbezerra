#!/usr/bin/env python3
"""Fotos do site a partir do Instagram dela (assets/src/instagram/, fora do git).

    python3 tools/fotos.py

Cada foto: (arquivo, nome no site, recorte (x0, y0, x1, y1) em fração ou None, larguras).
A capa usa o recorte sem fundo (hero-recorte.png, Vision da Apple via lift.swift).
Gera também a og-image (os ícones saem do tools/marca.py).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
SRC = RAIZ / "assets/src/instagram"
OUT = RAIZ / "assets/img/fotos"
FONTE = Path.home() / "Library/Fonts/Poppins-Light.ttf"
FONTE_M = Path.home() / "Library/Fonts/Poppins-Medium.ttf"

FOTOS = [
    ("sb-114.jpg", "cuidado", (0, .02, 1, .77), (800, 1200)),       # mão no queixo (a pose do post dela)
    ("sb-120.jpg", "sobre", (0, 0, 1, .75), (800, 1200)),           # jaleco, olhar direto
    ("sb-122.jpg", "formatura", (.03, 0, .97, 1), (600, 900)),      # formatura, nome no telão
    # de branco com café: recortada abaixo do texto do post e com o topo refeito no Firefly (espaço acima da cabeça)
    ("frase-expandida.png", "frase-v2", None, (800, 1200, 1600)),
    ("sb-125.jpg", "final", (0, 0, 1, .82), (800, 1200, 1600)),     # jaleco e planta
    # seção 2 no celular continua com o retrato; no computador, a versão com o fundo estendido (Firefly)
    ("cuidado-expandida.png", "cuidado-larga", (0, .014, 1, 1), (1200, 1800, 2400)),
    # carrossel do "Prazer, sou a Suéllen" (4:5)
    ("sb-118.jpg", "slide-jaleco", ("45", .05), (600, 900)),
    ("sb-060.jpg", "slide-corrida", ("45", .5), (600, 900)),
    # frames dos reels de treino (DcPlichN-DD e DbYW6TxMqOP), recortados longe da legenda queimada no vídeo
    ("frame-academia-branca.jpg", "slide-academia", (0, 0, 1, .703), (600, 900)),
    ("frame-academia-rosa.jpg", "slide-treino", (.0556, .229, .9444, .854), (600, 900)),
    ("sb-corrida-pos.jpg", "slide-pos-corrida", ("45", .1), (600, 900)),   # 2ª foto do post DMyOTw0SLtg
    ("sb-119.jpg", "slide-jardim", ("45", .5), (600, 900)),
]


def salvar(im, nome, larguras, q=78):
    for w in larguras:
        alvo = w                              # o nome segue a largura pedida (o img lê o tamanho real)
        w = min(w, im.width)
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(OUT / f"{nome}-{alvo}.webp", "WEBP", quality=q, method=6)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # capa: recorte sem fundo, aparado ao contorno
    rec = Image.open(SRC / "hero-recorte.png").convert("RGBA")
    rec = rec.crop(rec.getbbox())
    salvar(rec, "hero", (700, 1100), q=82)
    for arq, nome, caixa, larguras in FOTOS:
        im = Image.open(SRC / arq).convert("RGB")
        if caixa and caixa[0] == "45":           # 4:5 exato, âncora vertical caixa[1] (0 = topo)
            W, H = im.size
            w, h = (W, round(W * 1.25)) if W * 1.25 <= H else (round(H * .8), H)
            x0, y0 = (W - w) // 2, round((H - h) * caixa[1])
            im = im.crop((x0, y0, x0 + w, y0 + h))
        elif caixa:
            W, H = im.size
            im = im.crop((round(caixa[0] * W), round(caixa[1] * H), round(caixa[2] * W), round(caixa[3] * H)))
        salvar(im, nome, larguras)
    # os ícones da aba saem do monograma SB: tools/marca.py
    # compartilhamento: a frase é o destaque; a marca entra pequena, na horizontal, no canto (como no cabeçalho)
    og = Image.new("RGB", (1200, 630), (251, 246, 241)); d = ImageDraw.Draw(og)
    d.ellipse((660, 70, 1240, 650), fill=(237, 213, 203))
    r = rec.copy(); r.thumbnail((540, 600), Image.LANCZOS)
    og.paste(r, (1200 - r.width - 24, 630 - r.height), r)
    x0, y0 = 72, 58
    mono = RAIZ / "assets/src/marca/sb-og.png"           # gerado pelo tools/marca.py
    if mono.exists():
        m = Image.open(mono).convert("RGBA"); m = m.crop(m.getbbox()); m.thumbnail((48, 56), Image.LANCZOS)
        og.paste(m, (x0, y0), m)
        x_txt = x0 + m.width + 16
    else:
        x_txt = x0
    d.text((x_txt, y0 + 2), "Suéllen Bezerra", font=ImageFont.truetype(str(FONTE_M), 24), fill=(59, 38, 34))
    d.text((x_txt, y0 + 32), "NUTRICIONISTA · CRN 11028", font=ImageFont.truetype(str(FONTE), 14), fill=(125, 103, 98))
    fr = ImageFont.truetype(str(FONTE), 86)
    for i, (linha, cor) in enumerate((("Emagreça", (59, 38, 34)), ("sem dieta", (59, 38, 34)), ("restritiva.", (163, 90, 71)))):
        d.text((x0 - 4, 178 + i * 102), linha, font=fr, fill=cor)
    og.save(RAIZ / "assets/img/og-image-v2.jpg", quality=86)
    print("ok:", sorted(p.name for p in OUT.glob("*.webp")))


if __name__ == "__main__":
    main()
