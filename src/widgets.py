import ipywidgets as widgets
from IPython.display import display
from math import cos, sin, pi

from .geometry import axial_to_pixel


class MagicHexagonWidget:
    def __init__(self, hexagon):
        self.hexagon = hexagon

        self.board = widgets.HTML()
        self.status = widgets.HTML()
        self.history = widgets.HTML()

        self.ui = widgets.VBox([self.board, widgets.HBox([self.status, self.history])])

    # -------------------------
    # Rendering
    # -------------------------

    def redraw(self):
        self.board.value = self._render_board()
        self.status.value = self._render_status()
        self.history.value = self._render_history()

    def display(self):
        display(self.ui)
        self.redraw()

    # -------------------------
    # SVG BOARD
    # -------------------------

    def _render_board(self):

        cells = self.hexagon.cells

        svg = ['<svg width="650" height="520" style="background:#f7f7fb">']

        for c in cells:
            x, y = axial_to_pixel(c.q, c.r, size=25)
            x += 320
            y += 260

            fill = "#ffffff" if c.valeur is None else "#fff2b3"

            svg.append(f"""
                <polygon
                    points="{self._hex_points(x, y, 22)}"
                    fill="{fill}"
                    stroke="#444"
                    stroke-width="1.5"
                />
            """)

            svg.append(f"""
                <text x="{x}" y="{y - 8}" text-anchor="middle"
                      font-size="10" fill="#666">
                    {c.indice}
                </text>
            """)

            if c.valeur is not None:
                svg.append(f"""
                    <text x="{x}" y="{y + 10}" text-anchor="middle"
                          font-size="16" font-weight="bold"
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

    # -------------------------
    # STATUS PANEL
    # -------------------------

    def _render_status(self):
        v = self.hexagon.valider()

        filled = sum(x is not None for x in self.hexagon.valeurs)

        html = f"""
        <h3>Status</h3>
        Filled: {filled}/19<br>
        Magic: {v["magic"]}<br>
        <h4>Line sums</h4>
        """

        for i, s in enumerate(v["line_sums"]):
            if s is None:
                color = "gray"
            elif s == 38:
                color = "green"
            else:
                color = "red"

            html += f"<div style='color:{color}'>Line {i}: {s}</div>"

        return html

    # -------------------------
    # HISTORY PANEL
    # -------------------------

    def _render_history(self):
        html = "<h3>History</h3>"

        for op in self.hexagon._history[-15:]:
            html += f"<div>{op}</div>"

        return html
