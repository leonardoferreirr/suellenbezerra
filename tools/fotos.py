#!/usr/bin/env python3
"""Fotos do site a partir do Instagram dela (assets/src/instagram/, fora do git).

    python3 tools/fotos.py

Cada foto: (arquivo, nome no site, recorte (x0, y0, x1, y1) em fração ou None, larguras).
A capa usa o recorte sem fundo (hero-recorte.png, Vision da Apple via lift.swift).
Gera também favicon, apple-touch-icon e og-image.
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
    ("sb-047.jpg", "frase", (0, .24, 1, 1), (800, 1200, 1600)),     # de branco com café, sem o texto do post
    ("sb-125.jpg", "final", (0, 0, 1, .82), (800, 1200, 1600)),     # jaleco e planta
]


def salvar(im, nome, larguras, q=78):
    for w in larguras:
        if w > im.width:
            w = im.width
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(OUT / f"{nome}-{w}.webp", "WEBP", quality=q, method=6)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # capa: recorte sem fundo, aparado ao contorno
    rec = Image.open(SRC / "hero-recorte.png").convert("RGBA")
    rec = rec.crop(rec.getbbox())
    salvar(rec, "hero", (700, 1100), q=82)
    for arq, nome, caixa, larguras in FOTOS:
        im = Image.open(SRC / arq).convert("RGB")
        if caixa:
            W, H = im.size
            im = im.crop((round(caixa[0] * W), round(caixa[1] * H), round(caixa[2] * W), round(caixa[3] * H)))
        salvar(im, nome, larguras)
    # ícones: iniciais em terracota sobre creme
    for lado, arq in ((64, "favicon.png"), (180, "apple-touch-icon.png")):
        ic = Image.new("RGB", (lado, lado), (163, 90, 71)); d = ImageDraw.Draw(ic)
        f = ImageFont.truetype(str(FONTE_M), round(lado * .42))
        d.text((lado / 2, lado / 2), "SB", font=f, fill=(251, 246, 241), anchor="mm")
        ic.save(RAIZ / "assets/img" / arq)
    # compartilhamento: foto à direita, nome e promessa à esquerda
    og = Image.new("RGB", (1200, 630), (251, 246, 241)); d = ImageDraw.Draw(og)
    d.ellipse((640, 60, 1240, 660), fill=(237, 213, 203))
    r = rec.copy(); r.thumbnail((560, 620), Image.LANCZOS)
    og.paste(r, (1200 - r.width - 20, 630 - r.height), r)
    d.text((70, 170), "Suéllen Bezerra", font=ImageFont.truetype(str(FONTE_M), 58), fill=(59, 38, 34))
    d.text((72, 250), "Nutricionista · CRN 11028", font=ImageFont.truetype(str(FONTE), 28), fill=(125, 103, 98))
    d.text((70, 330), "Emagrecer sem\ndieta restritiva.", font=ImageFont.truetype(str(FONTE), 52), fill=(163, 90, 71), spacing=10)
    og.save(RAIZ / "assets/img/og-image.jpg", quality=86)
    print("ok:", sorted(p.name for p in OUT.glob("*.webp")))


if __name__ == "__main__":
    main()
