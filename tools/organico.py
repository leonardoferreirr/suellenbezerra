"""Desenhos da capa: a forma orgânica atrás dela e o ramo de folhas em traço (na linha da folha dos posts dela).
O build.py importa daqui; para mexer no desenho, ajuste os números e rode o build de novo."""
import math, json, sys

def blob(n=9, amp=((3, .07, .4), (2, .05, 1.7), (5, .025, .9)), r0=100, cx=100, cy=100):
    pts = []
    for i in range(n):
        th = 2 * math.pi * i / n
        r = r0 * (1 + sum(a * math.sin(k * th + f) for k, a, f in amp))
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
    # Catmull-Rom fechado -> Bézier
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d + "Z"

def bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    u = 1 - t
    x = u**3*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t**3*x3
    y = u**3*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t**3*y3
    dx = 3*u*u*(x1-x0) + 6*u*t*(x2-x1) + 3*t*t*(x3-x2)
    dy = 3*u*u*(y1-y0) + 6*u*t*(y2-y1) + 3*t*t*(y3-y2)
    return x, y, math.degrees(math.atan2(dy, dx))

def folha(L, w, k=1):
    """folha comprida, levemente curvada para o lado k (1 ou -1), base em (0,0); contorno + nervura."""
    tx = k * L * .1
    c = (f"M0 0C{w*1.1:.1f} {-L*.2:.1f} {w*.95+tx:.1f} {-L*.68:.1f} {tx:.1f} {-L:.1f}"
         f"C{-w*.75+tx:.1f} {-L*.7:.1f} {-w*.95:.1f} {-L*.28:.1f} 0 0Z")
    n = f"M0 {-L*.03:.1f}Q{tx*.3+w*.1:.1f} {-L*.55:.1f} {tx*.92:.1f} {-L*.9:.1f}"
    return c, n

def ramo():
    # caule: de baixo à direita subindo para a esquerda, curva suave
    P = ((150, 430), (160, 300), (128, 160), (70, 20))
    caule = f"M{P[0][0]} {P[0][1]}C{P[1][0]} {P[1][1]} {P[2][0]} {P[2][1]} {P[3][0]} {P[3][1]}"
    partes = [caule]
    folhas = [(.1, 1, 104), (.2, -1, 100), (.31, 1, 94), (.42, -1, 88), (.53, 1, 80), (.64, -1, 72), (.75, 1, 62), (.85, -1, 52)]
    for t, lado, L in folhas:
        x, y, ang = bez(P, t)
        rot = ang + 90 + lado * 34          # folha sai do caule inclinada para o lado
        c, n = folha(L, L * .2, lado)
        partes.append(f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.1f})"><path d="{c}"/><path d="{n}"/></g>')
    x, y, ang = bez(P, 1)
    c, n = folha(48, 10, 1)
    partes.append(f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang + 90:.1f})"><path d="{c}"/><path d="{n}"/></g>')
    return partes

if __name__ == "__main__":
    print(json.dumps({"blob1": blob(), "blob2": blob(amp=((3, .06, 2.2), (2, .06, .3), (4, .03, 1.1))), "ramo": ramo()}))
