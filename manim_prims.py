# Prim's Minimum Spanning Tree Visualization
# Run: manim -pql manim_prims.py PrimsVisualization
# Run (high quality): manim -pqh manim_prims.py PrimsVisualization

from manim import *
import numpy as np
import heapq
from collections import defaultdict


# ── Node layout ──────────────────────────────────────────────────────────────
# Scene coordinate space: x ∈ [-7.1, 7.1], y ∈ [-4, 4]
# Graph occupies x ∈ [-6.5, 3.0] — PQ panel sits on the right
NODE_XY = [
    (-5.0,  1.2),   # 0  ← source
    (-3.0,  1.7),   # 1
    (-1.0,  1.4),   # 2
    ( 1.2,  1.6),   # 3
    ( 3.0,  1.0),   # 4
    (-4.0, -0.5),   # 5
    (-1.8, -0.2),   # 6
    ( 1.0, -0.8),   # 7
    (-3.0, -2.2),   # 8
    ( 0.0, -2.5),   # 9
]
START_NODE = 0


# ── Graph helpers ─────────────────────────────────────────────────────────────

def euc(a, b):
    """Euclidean distance rounded to 1 decimal."""
    return round(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5, 1)


def build_graph(positions, connect_radius=3.2, k_nearest=2):
    """
    Build undirected graph: connect every pair within connect_radius,
    and guarantee at least k_nearest edges per node regardless of radius.
    """
    n = len(positions)
    adj = defaultdict(dict)

    for i in range(n):
        by_dist = sorted(
            [(euc(positions[i], positions[j]), j) for j in range(n) if j != i]
        )
        # k nearest neighbors (unconditional)
        for d, j in by_dist[:k_nearest]:
            adj[i][j] = d
            adj[j][i] = d
        # all within radius
        for d, j in by_dist:
            if d > connect_radius:
                break
            adj[i][j] = d
            adj[j][i] = d

    seen = set()
    edges = []
    for i in adj:
        for j, w in adj[i].items():
            ekey = (min(i, j), max(i, j))
            if ekey not in seen:
                seen.add(ekey)
                edges.append((ekey[0], ekey[1], w))
    return adj, sorted(edges)


# ── Scene ─────────────────────────────────────────────────────────────────────

class PrimsVisualization(Scene):

    # ── color palette ──────────────────────────────────────────────────────
    C_NODE_FILL     = "#1a3a6e"
    C_NODE_STROKE   = "#3a7fdd"
    C_CURRENT_FILL  = "#c8900a"   # yellow-gold  — node being added to MST
    C_VISITED_FILL  = "#1a5e28"   # green        — in MST
    C_NEIGHBOR_FILL = "#7a3a00"   # orange-brown — neighbor being inspected
    C_EDGE          = "#444444"   # default edge
    C_ACTIVE_EDGE   = "#ddaa00"   # edge currently being considered
    C_RELAXED_EDGE  = "#22bb44"   # edge that improved a key value
    C_PANEL_BG      = "#06060f"
    C_PANEL_BORDER  = "#223355"

    NODE_R  = 0.35   # node circle radius
    PANEL_X = 5.4    # x-centre of PQ panel

    def construct(self):
        n   = len(NODE_XY)
        pos = [np.array([x, y, 0]) for x, y in NODE_XY]
        adj, edges = build_graph(NODE_XY)

        # ── node visuals ───────────────────────────────────────────────────
        circles, c_labels = [], []
        for i, p in enumerate(pos):
            c = Circle(
                radius=self.NODE_R,
                fill_color=self.C_NODE_FILL, fill_opacity=0.7,
                stroke_color=self.C_NODE_STROKE, stroke_width=2,
            ).move_to(p)
            lbl = Text(str(i), font_size=27, color=WHITE).move_to(p)
            circles.append(c)
            c_labels.append(lbl)

        # ── edge visuals ───────────────────────────────────────────────────
        e_lines, e_wlbls = {}, {}
        for i, j, w in edges:
            ekey  = (i, j)
            d_vec = pos[j] - pos[i]
            d_hat = d_vec / np.linalg.norm(d_vec)
            # start/end at circle boundary instead of centre
            p_start = pos[i] + d_hat * self.NODE_R
            p_end   = pos[j] - d_hat * self.NODE_R
            line = Line(p_start, p_end, stroke_color=self.C_EDGE, stroke_width=2)
            mid  = (pos[i] + pos[j]) / 2
            # perpendicular offset so weight label doesn't sit on the line
            perp = np.array([-d_vec[1], d_vec[0], 0])
            norm = np.linalg.norm(perp)
            off  = perp / norm * 0.22 if norm > 0 else np.array([0, 0.22, 0])
            wlbl = Text(str(w), font_size=20, color="#888888").move_to(mid + off)
            e_lines[ekey]  = line
            e_wlbls[ekey]  = wlbl

        # ── key labels (cheapest edge to MST, shown above each node) ───────
        # In Prim's, key[v] = cheapest edge weight connecting v to the MST.
        INF      = float("inf")
        key_vals = [INF] * n
        key_vals[START_NODE] = 0.0
        key_lbls = []
        for i, p in enumerate(pos):
            txt = "0.0" if i == START_NODE else "∞"
            col = WHITE if i == START_NODE else "#cc3333"
            key_lbls.append(
                Text(txt, font_size=23, color=col).move_to(p + UP * 0.58)
            )

        # ── priority queue panel (right side) ─────────────────────────────
        panel = Rectangle(
            width=3.2, height=5.8,
            fill_color=self.C_PANEL_BG, fill_opacity=0.92,
            stroke_color=self.C_PANEL_BORDER, stroke_width=1.5,
        ).move_to([self.PANEL_X, -0.9, 0])
        pq_title  = Text("Priority Queue", font_size=32, color=YELLOW) \
                        .next_to(panel, UP, buff=0.06)
        pq_header = Text("(key,  node)", font_size=21, color="#666666") \
                        .move_to([self.PANEL_X, 1.82, 0])

        # mutable list tracking which Text mobjects are live in the panel
        pq_items: list = []

        def refresh_pq(heap_snap, highlight_top=False):
            """Return animations that swap the PQ display to match heap_snap."""
            outs = [FadeOut(m) for m in pq_items]
            pq_items.clear()
            ins = []
            for idx, (kv, nd) in enumerate(sorted(heap_snap)[:8]):
                color = YELLOW if (highlight_top and idx == 0) else WHITE
                t = Text(f"({kv:.1f},  {nd})", font_size=26, color=color)
                t.move_to([self.PANEL_X, 1.3 - idx * 0.72, 0])
                pq_items.append(t)
                ins.append(FadeIn(t))
            return outs + ins

        def exp(txt, color=WHITE):
            """One-line explanation text near the top of the screen."""
            t = Text(txt, font_size=29, color=color, line_spacing=1.2)
            t.to_edge(UP, buff=0.50)
            return t

        # ══════════════════════════════════════════════════════════════════
        #  INTRO
        # ══════════════════════════════════════════════════════════════════
        self.next_section("Intro")

        title = Text("Prim's Minimum Spanning Tree Algorithm", font_size=48, color=YELLOW)
        sub = Text(
            "Finds the minimum spanning tree of a weighted graph.\n"
            "Greedily adds the cheapest edge connecting an unvisited node to the MST.",
            font_size=30, line_spacing=1.4,
        )
        VGroup(title, sub).arrange(DOWN, buff=0.4).center()
        self.play(Write(title, run_time=3.75))
        self.play(FadeIn(sub, run_time=3.75))
        self.wait(6.0)
        self.play(FadeOut(title), FadeOut(sub))

        # ══════════════════════════════════════════════════════════════════
        #  DRAW GRAPH
        # ══════════════════════════════════════════════════════════════════
        self.next_section("Draw Graph")

        e1 = exp("10-node graph — edge weights are Euclidean distances.", WHITE)
        self.play(Write(e1, run_time=1.875))
        self.play(
            *[Create(l) for l in e_lines.values()],
            *[FadeIn(w) for w in e_wlbls.values()],
        )
        self.play(
            *[Create(c) for c in circles],
            *[Write(l) for l in c_labels],
        )
        self.play(*[Write(d) for d in key_lbls])
        self.play(FadeIn(panel), Write(pq_title), Write(pq_header))
        self.wait(1.55)
        self.play(FadeOut(e1))

        # ══════════════════════════════════════════════════════════════════
        #  PRIM'S ALGORITHM
        # ══════════════════════════════════════════════════════════════════
        self.next_section("Algorithm")

        heap    = [(0.0, START_NODE)]
        in_mst  = set()
        prev    = [None] * n

        # ── initialization ─────────────────────────────────────────────
        e2 = exp(
            f"Initialize: key[{START_NODE}] = 0, all others = ∞.  "
            f"Push node {START_NODE} onto the PQ.",
            YELLOW,
        )
        self.play(
            Write(e2, run_time=1.875),
            circles[START_NODE].animate
                .set_fill(color=self.C_CURRENT_FILL, opacity=0.9)
                .set_stroke(color=YELLOW, width=3),
            *refresh_pq(heap, highlight_top=True),
        )
        self.wait(2.25)
        self.play(FadeOut(e2))

        # ── main loop ──────────────────────────────────────────────────
        while heap:
            k_u, u = heapq.heappop(heap)

            # skip stale entries (node already added to MST)
            if u in in_mst:
                e = exp(f"Pop ({k_u:.1f}, {u}) — node {u} already in MST, skip.", "#888888")
                self.play(Write(e, run_time=1.875), *refresh_pq(heap))
                self.wait(1.35)
                self.play(FadeOut(e))
                continue

            in_mst.add(u)

            # ── pop minimum ───────────────────────────────────────────
            # The edge connecting u to the MST is confirmed the moment u is popped.
            e = exp(f"Pop min: node {u},  key = {k_u:.1f} — added to MST!", YELLOW)
            pop_anims = [
                Write(e, run_time=1.875),
                circles[u].animate
                    .set_fill(color=self.C_CURRENT_FILL, opacity=0.9)
                    .set_stroke(color=YELLOW, width=3),
            ]
            if pq_items:
                pop_anims.append(pq_items[0].animate.set_color(YELLOW))
            # confirm the MST edge immediately
            if prev[u] is not None:
                mst_ekey = (min(prev[u], u), max(prev[u], u))
                if mst_ekey in e_lines:
                    pop_anims.append(
                        e_lines[mst_ekey].animate.set_stroke(color=YELLOW, width=4)
                    )
            self.play(*pop_anims)
            self.wait(1.35)
            # now remove it from the PQ display
            self.play(*refresh_pq(heap))
            self.wait(1.65)
            self.play(FadeOut(e))

            # ── relax outgoing edges ───────────────────────────────────
            e_relax = exp(f"Now checking node {u}'s outgoing edges to update neighbor keys.", WHITE)
            self.play(Write(e_relax, run_time=1.875))
            self.wait(1.35)
            self.play(FadeOut(e_relax))

            # Key difference from Dijkstra: we use w directly (not key[u] + w).
            # We're asking: "is this edge cheaper than the best edge to v so far?"
            for v, w in sorted(adj[u].items()):
                if v in in_mst:
                    continue

                old_key     = key_vals[v]
                ekey        = (min(u, v), max(u, v))
                old_key_str = f"{old_key:.1f}" if old_key < INF else "∞"

                # highlight edge + candidate neighbor
                e = exp(
                    f"Edge {u}→{v}   w={w:.1f}     Is {w:.1f} < key[{v}] ({old_key_str})?",
                    WHITE,
                )
                self.play(
                    Write(e, run_time=1.875),
                    e_lines[ekey].animate.set_stroke(color=self.C_RELAXED_EDGE, width=3),
                    circles[v].animate
                        .set_fill(color=self.C_NEIGHBOR_FILL, opacity=0.85)
                        .set_stroke(color=ORANGE, width=2),
                )
                self.wait(1.35)

                if w < old_key:
                    # cheaper connection to MST found — update key and PQ
                    key_vals[v] = w
                    prev[v]     = u
                    heapq.heappush(heap, (w, v))
                    new_lbl = Text(f"{w:.1f}", font_size=23, color=GREEN) \
                                  .move_to(pos[v] + UP * 0.58)
                    e2 = exp(
                        f"Cheaper connection!  key[{v}] = {w:.1f}  (was {old_key_str})",
                        GREEN,
                    )
                    self.play(
                        FadeOut(e), Write(e2, run_time=1.875),
                        Transform(key_lbls[v], new_lbl),
                        e_lines[ekey].animate.set_stroke(color=self.C_EDGE, width=2),
                        *refresh_pq(heap),
                    )
                    self.wait(1.35)
                    self.play(FadeOut(e2))
                else:
                    # no improvement
                    e2 = exp(
                        f"No improvement for node {v}  "
                        f"(key[{v}] = {old_key_str} ≤ {w:.1f})",
                        "#888888",
                    )
                    self.play(
                        FadeOut(e), Write(e2, run_time=1.875),
                        e_lines[ekey].animate.set_stroke(color=self.C_EDGE, width=2),
                    )
                    self.wait(1.25)
                    self.play(FadeOut(e2))

                # restore neighbor's appearance if not yet in MST
                if v not in in_mst:
                    self.play(
                        circles[v].animate
                            .set_fill(color=self.C_NODE_FILL, opacity=0.7)
                            .set_stroke(color=self.C_NODE_STROKE, width=2),
                    )

            # node is already in MST (announced at pop); just settle its colour
            self.play(
                circles[u].animate
                    .set_fill(color=self.C_VISITED_FILL, opacity=0.88)
                    .set_stroke(color=GREEN, width=2),
            )

        # ══════════════════════════════════════════════════════════════════
        #  RESULT — highlight the minimum spanning tree
        # ══════════════════════════════════════════════════════════════════
        self.next_section("Result")

        e = exp("MST complete!  Highlighting the minimum spanning tree.", GREEN_C)
        self.play(Write(e, run_time=1.875))

        tree_anims = []
        for v in range(n):
            if prev[v] is not None:
                ekey = (min(prev[v], v), max(prev[v], v))
                if ekey in e_lines:
                    tree_anims.append(
                        e_lines[ekey].animate.set_stroke(color=YELLOW, width=5)
                    )
        if tree_anims:
            self.play(*tree_anims)

        self.wait(2.25)
        final = exp(
            "Labels show each node's cheapest edge weight connecting it to the MST.", WHITE
        )
        self.play(FadeOut(e), Write(final, run_time=1.875))
        self.wait(3.25)
        self.play(FadeOut(final))
        self.wait(1.25)
