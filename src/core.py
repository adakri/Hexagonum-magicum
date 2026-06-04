from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from .geometry import generer_les_coordonnes_hex

MAGIC_SUM_ORDER_3 = 38

# ça fait double mias je dois avoir un système pour ordonner les choses dans un premier temps
@dataclass
class Cellule:
    indice: int # à remplir par les étudiants
    q: int
    r: int
    valeur: Optional[int] = None


class HexagoneMagique:
    def __init__(self, radius=2, show_widget=True):
        self.radius = radius
        coords = generer_les_coordonnes_hex(radius)
        self.cells: List[Cellule] = [
            Cellule(i, q, r) for i, (q, r) in enumerate(coords)
        ]
        # On laisse aux gens de décider des indexations
        self.valeurs = [None] * len(self.cells)
        self._history = []
        self.widget = None
        self.parcours = list(range(len(self.cells)))
        if show_widget:
            self.show_widget()        
    
    # propriéts
    @property
    def rempli(self) -> bool:
        """True si toutes les cellules sont remplies (aucune valeur None)."""
        return all(v is not None for v in self.valeurs)

    @property
    def valide(self) -> bool:
        """True si toutes les valeurs sont des entiers entre 1 et 19 (inclus)."""
        return all(isinstance(v, int) and 1 <= v <= 19 for v in self.valeurs)

    @property
    def gagné(self) -> bool:
        """True si la grille est magique (utilise la méthode `valider`)."""
        try:
            return bool(self.valider().get("magic", False))
        except Exception:
            return False

    # Opérations sur la struct
    def mettre(self, slot: int, valeur: int):
        self.valeurs[slot] = valeur
        self.cells[slot].valeur = valeur
        self._log("mettre", slot, valeur)
        self._refresh()

    def vider(self, slot: int):
        old = self.valeurs[slot]
        self.valeurs[slot] = None
        self.cells[slot].valeur = None
        self._log("vider", slot, old)
        self._refresh()

    def echanger(self, a: int, b: int):
        self.valeurs[a], self.valeurs[b] = self.valeurs[b], self.valeurs[a]
        self.cells[a].valeur = self.valeurs[a]
        self.cells[b].valeur = self.valeurs[b]
        self._log("echanger", a, b)
        self._refresh()

    def remplir(self, valeurs):
        if len(valeurs) != len(self.cells):
            raise ValueError("Wrong number of values")
        for i, v in enumerate(valeurs):
            self.valeurs[i] = v
            self.cells[i].valeur = v

        self._log("remplir", None, None)
        self._refresh()
        
    def fixer_parcours(self, list_des_indices: List):
        assert len(list_des_indices) == len(self.cells)
        for i,cell in enumerate(self.cells):
            cell.indice = list_des_indices[i]
        self._refresh()

    # -------------------------
    # Trucs à faire par eux?
    # -------------------------

    def lignes(self):
        return self._compute_lines()


    def valider(self):        
        lines = self._compute_lines()
        sums = []
        for line in lines:
            vals = [self.valeurs[i] for i in line]
            if None in vals:
                sums.append(None)
            else:
                sums.append(sum(vals))
        complete = all(v is not None for v in self.valeurs)
        magic = (
            complete
            and sorted(self.valeurs) == list(range(1, 20))
            and all(s == MAGIC_SUM_ORDER_3 for s in sums)
        )
        bad_lines = [
            i for i, s in enumerate(sums) if s is not None and s != MAGIC_SUM_ORDER_3
        ]
        return {
            "magic": magic,
            "line_sums": sums,
            "bad_lines": bad_lines,
            "complete": complete,
        }

    def _compute_lines(self):
        coord_to_i = {(c.q, c.r): c.indice for c in self.cells}
        lines = []
        for q in range(-2, 3):
            line = [coord_to_i[(q, r)] for r in range(-2, 3) if (q, r) in coord_to_i]
            if len(line) >= 3:
                lines.append(line)
        for r in range(-2, 3):
            line = [coord_to_i[(q, r)] for q in range(-2, 3) if (q, r) in coord_to_i]
            if len(line) >= 3:
                lines.append(line)
        for s in range(-2, 3):
            line = []
            for q in range(-2, 3):
                r = -s - q
                if (q, r) in coord_to_i:
                    line.append(coord_to_i[(q, r)])
            if len(line) >= 3:
                lines.append(line)

        return lines


    # Un vocabulaire plus experssif pour les opérations?
    def _log(self, op, a, b):
        self._history.append((op, a, b))

    def _refresh(self):
        if self.widget:
            self.widget.redraw()


    def show_widget(self):
        from .widgets import MagicHexagonWidget

        self.widget = MagicHexagonWidget(self)
        self.widget.display()
        return self.widget
