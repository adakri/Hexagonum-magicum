import ipywidgets as widgets
from IPython.display import display
from math import cos, sin, pi

from .geometry import axial_to_pixel


class MagicHexagonWidget:
    def __init__(self, hexagon):
        self.hexagon = hexagon
        self.background_image = "bg.jpg"

        self.board = widgets.HTML()
        self.status = widgets.HTML(layout=widgets.Layout(width="320px", margin="2px 12px 2px 2px"))
        self.history = widgets.HTML(layout=widgets.Layout(width="320px"))

        self.ui = widgets.VBox([
            self.board,
            widgets.HBox(
                [self.status, self.history],
                layout=widgets.Layout(justify_content="flex-start", align_items="flex-start", width="100%"),
            ),
        ])

    def redraw(self):
        board_html = self._render_board()
        # Magie de copilot
        self.board.value = f"""
            <div style="position:relative; width:650px; height:520px;">
                <div style="position:absolute; inset:0; z-index:0;">
                    {self._render_background_svg()}
                </div>
                <div style="position:absolute; inset:0; z-index:1;">
                    {board_html}
                </div>
            </div>
        """

        self.status.value = self._render_status()
        self.history.value = self._render_history()

    def display(self):
        # Instancier les widgets
        display(self.ui)
        self.redraw()


    def _render_board(self):
        """Tracer des hexagones"""
        cells = self.hexagon.cells
        svg = ['<svg width="650" height="520" style="background:transparent">']
        for c in cells:
            # Tracer les polygones
            x, y = axial_to_pixel(c.q, c.r, size=60)
            x += 320
            y += 260
            fill = "#ffffff" if c.valeur is None else "#fff2b3"
            svg.append(f"""
                <polygon
                    points="{self._hex_points(x, y, 55)}"
                    fill="{fill}"
                    stroke="#444"
                    stroke-width="1.5"
                />
            """)
            # Ajouter les indices si le tracé est décidé
            if c.indice is not None:
                svg.append(f"""
                    <text x="{x}" y="{y - 25}" text-anchor="middle"
                        font-size="15" fill="#666">
                        {c.indice}
                    </text>
                """)
            else:
                svg.append(f"""
                    <text x="{x}" y="{y - 8}" text-anchor="middle"
                        font-size="20" fill="#666">
                        {"?"}
                    </text>
                """)
            # Ajouter les valeurs si y'en a
            if c.valeur is not None:
                svg.append(f"""
                    <text x="{x}" y="{y + 10}" text-anchor="middle"
                          font-size="30" font-weight="bold"
                          fill="#1f3c88">
                        {c.valeur}
                    </text>
                """)
        svg.append("</svg>")
        return "".join(svg)
    
    def _render_board_trace_indices(self):
        """Tracer des lignes pour trouver les lignes etc"""
        return

    def _hex_points(self, cx, cy, r):
        pts = []
        for i in range(6):
            angle = pi / 3 * i + pi / 6
            x = cx + r * cos(angle)
            y = cy + r * sin(angle)
            pts.append(f"{x},{y}")
        return " ".join(pts)

    def _render_background_svg(self):
        return f"""
            <svg width="650" height="520" viewBox="0 0 650 520" preserveAspectRatio="xMidYMid slice">
                <image
                    href="{self.background_image}"
                    x="0" y="0"
                    width="650" height="520"
                    preserveAspectRatio="xMidYMid slice"
                />
            </svg>
        """

    def _render_status(self):
        html = f"""
            <div style="padding:16px; border:1px solid #dde2f0; border-radius:16px; background:#ffffff; box-shadow:0 8px 20px rgba(0,0,0,0.08); width:100%; box-sizing:border-box;">
                <h3 style="margin:0 0 10px 0; font-size:1.1rem;">Comment ça se passe?</h3>
                <div style="margin-bottom:8px;">Est ce que c'est rempli? <strong style='color:{bool_color(self.hexagon.rempli)}'>{bool_to_french(self.hexagon.rempli)}</strong></div>
                <div style="margin-bottom:8px;">Est ce que c'est valide? <strong style='color:{bool_color(self.hexagon.valide)}'>{bool_to_french(self.hexagon.valide)}</strong></div>
                <div>Est ce un hexagone magique? <strong style='color:{bool_color(self.hexagon.gagné)}'>{bool_to_french(self.hexagon.gagné)}</strong></div>
            </div>
            """
        if self.hexagon.rempli or self.hexagon.valide:
            v = self.hexagon.valider()
            html += "<div style='margin-top:12px;'>"
            for i, s in enumerate(v["line_sums"]):
                if s is None:
                    color = "gray"
                elif s == 38:
                    color = "green"
                else:
                    color = "red"

                html += f"<div style='color:{color}; margin-bottom:4px;'>Line {i}: {s}</div>"
            html += "</div>"
        return html

    def _render_history(self):
        html = "<h3>Historique</h3>"

        for op in self.hexagon._history[-15:]:
            html += f"<div>{op}</div>"

        return html

# ça aide
def bool_to_french(value):
    return "Vrai" if value else "Faux"

def bool_color(value):
    return "green" if value else "red"
