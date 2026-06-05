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
    def __init__(self, radius=2, dessiner_hex=True):
        # Données internes
        self.radius = radius
        coords = generer_les_coordonnes_hex(radius)
        self.cells: List[Cellule] = [Cellule(i, q, r) for i, (q, r) in enumerate(coords)]
        # On laisse aux gens de décider des indexations
        self.valeurs = [None] * len(self.cells)
        self._history = []
        self.widget = None
        self.parcours = list(range(len(self.cells)))
        self.validation_data = None

        if dessiner_hex:
            self.dessiner_hex()        
    
    # propriéts
    # Est ce que les étudiants ont à coder cela aussi
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
        if self.valeurs[slot] is None:
            self.valeurs[slot] = valeur
            self.cells[slot].valeur = valeur
            self._log("mettre", slot, valeur)
            self._refresh()
        else:
            self.echanger(slot, self.valeurs.index(valeur))            

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
        
    def changer_parcours(self, list_des_indices: List):
        assert len(list_des_indices) == len(self.cells)
        for i,cell in enumerate(self.cells):
            cell.indice = list_des_indices[i]
        self._refresh()

    # Un vocabulaire plus experssif pour les opérations?
    def _log(self, op, a, b):
        self._history.append((op, a, b))

    def _refresh(self):
        return
        if self.widget:
            self.widget.redraw()


    def dessiner_hex(self):
        from .widgets import MagicHexagonWidget

        self.widget = MagicHexagonWidget(self)
        self.widget.display()
        return self.widget

