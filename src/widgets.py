import ipywidgets as widgets
from IPython.display import display
from math import cos, sin, pi

from .geometry import axial_to_pixel


class MagicHexagonWidget:
    def __init__(self, hexagon):
        self.hexagon = hexagon
        self.background_image = "bg.jpg"

        self.board = widgets.HTML()
        self.status = widgets.HTML(layout=widgets.Layout(width="500px", margin="2px 12px 2px 2px"))
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
        if self.hexagon.validation_data is not None:
            self.status.value = self._render_status()

    def update_line_colours(self, validation_data=None):
        self.hexagon.validation_data = validation_data
        #self.redraw()

    def display(self):
        # Instancier les widgets
        display(self.ui)
        self.redraw()


    def _render_board(self):
        """Tracer des hexagones"""
        cells = self.hexagon.cells
        validation = self.hexagon.validation_data

        line_sums = []
        bad_lines = []
        good_lines = []
        line_indices = {}
        if validation is not None:
            for line, item in enumerate(validation):
                line_indices[line] = item.get("indices", [])
                somme = item.get("somme")
                is_good = (somme == 38)
                if is_good:
                    good_lines.append(line)
                elif somme is not None:
                    bad_lines.append(line)
                line_sums.append(somme)
        cell_fill = {}
        for c in cells:
            related_lines = [line for line, indices in line_indices.items() if c.indice in indices]
            if validation is not None and related_lines:
                if any(line in good_lines for line in related_lines):
                    cell_fill[c.indice] = "#1bc11b"
                else:
                    cell_fill[c.indice] = "#d51f1f"
            else:
                cell_fill[c.indice] = "#ffffff" if c.valeur is None else "#fff2b3"

        svg = ['<svg width="650" height="520" style="background:transparent">']
        for c in cells:
            # Tracer les polygones
            x, y = axial_to_pixel(c.q, c.r, size=60)
            x += 320
            y += 260
            fill = cell_fill.get(c.indice, "#ffffff")
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
        validation = self.hexagon.validation_data 
        bad_lines = []
        complete = False
        magic = False
        complete = all(item.get("somme") is not None for item in validation)
        magic = complete and all(
            item.get("correct") is not False and item.get("sum") == 38
            for item in validation
        )
        bad_lines = [
            item.get("indices")
            for item in validation
            if item.get("somme") is not None and item.get("somme") != 38
        ]
        html = "<div style='padding:16px; border:1px solid #dde2f0; border-radius:16px; background:#ffffff;'>"
        html += "<h3 style='margin:0 0 10px 0;'>Validation</h3>"
        #html += f"<div>Complète: <strong>{'oui' if complete else 'non'}</strong></div>"
        html += f"<div>L'hexagone est il Magique: <strong style='color:{'green' if magic else 'red'}'>{'oui' if magic else 'non'}</strong></div>"
        #if bad_lines:
        #    html += f"<div style='margin-top:8px; color:red;'>Lignes invalides: {', '.join(str(i + 1) for i in bad_lines)}</div>"
        #else:
        #    html += "<div style='margin-top:8px; color:green;'>Aucune ligne invalide</div>"
        html += "<div style='margin-top:12px; padding:8px; border:1px solid #ddd; border-radius:10px; background:#fafafa;'>"
        html += "<div style='margin-bottom:6px;'><span style='display:inline-block;width:16px;height:16px;background:#1bc11b;border:1px solid #9f9;vertical-align:middle;margin-right:6px;'></span> 😊 Somme à 38</div>"
        html += "<div><span style='display:inline-block;width:16px;height:16px;background:#d51f1f;border:1px solid #f99;vertical-align:middle;margin-right:6px;'></span> 😡 Ne Somme pas à 38, grrr...</div>"
        html += "</div></div>"
        return html


    def _render_history(self):
        return
        html = "<h3>Historique</h3>"

        for op in self.hexagon._history[-15:]:
            html += f"<div>{op}</div>"

        return html

# ça aide
def bool_to_french(value):
    return "Vrai" if value else "Faux"

def bool_color(value):
    return "green" if value else "red"
