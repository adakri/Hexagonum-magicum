import math

# Comment traverser une grille hexagonale?
# https://www.redblobgames.com/grids/hexagons/

# La pièce centrale est placée au centre de l'hexagone
# Trois axes sont définis sur les axes principaux de l'hexa
# Marcher dans le sens de l'axe c'est de garder une corrdonée nulle" Tourner à gauche est -1, à droite +1
def generer_les_coordonnes_hex(radius):
    coords = []
    for q in range(-radius, radius + 1):
        r1 = max(-radius, -q - radius)
        r2 = min(radius, -q + radius)
        for r in range(r1, r2 + 1):
            coords.append((q, r))
    coords.sort(key=lambda x: (x[1], x[0]))
    return coords


def axial_to_pixel(q, r, size=1.0):
    x = size * math.sqrt(3) * (q + r / 2)
    y = size * 3/2 * r
    return x, y