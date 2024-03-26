from manim import *

def fade(f):
    """A decorator for construct method of scenes where all objects should fade at the end."""
    def inner(self):
        f(self)
        self.play(*map(FadeOut, self.mobjects))

    return inner

def parse_graph(graph, s=0.13, t=0.13, scale=2):
    """Parse a graph in a format like this:
    ---
    1 2 <9.118072543948081, 4.650124351556167> <15.236742443226104, 4.832736111387815>
    3 2 <20.843227140026464, 7.251324476362457> <15.236742443226104, 4.832736111387815>
    3 4 <20.843227140026464, 7.251324476362457> <20.151957872799326, 1.2158150606935652>
    4 2 <20.151957872799326, 1.2158150606935652> <15.236742443226104, 4.832736111387815>
    """

    lt = {}
    edges = []
    vertices = set()

    for line in graph.strip().splitlines():
        line = line.strip()
        edge, p1, p2 = line.split("<")
        u, v = list(map(int, edge.strip().split()))
        u_x, u_y = list(map(float, p1[:-2].strip().split(", ")))
        v_x, v_y = list(map(float, p2[:-2].strip().split(", ")))

        lt[u] = [u_x, u_y, 0]
        lt[v] = [v_x, v_y, 0]

        edges.append((u, v))
        vertices.add(u)
        vertices.add(v)

    lt_avg_x = 0
    lt_avg_y = 0

    for i in lt:
        lt_avg_x += lt[i][0]
        lt_avg_y += lt[i][1]

    lt_avg_x /= len(lt)
    lt_avg_y /= len(lt)

    for i in lt:
        lt[i] = ((lt[i][0] - lt_avg_x) * s, (lt[i][1] - lt_avg_y) * t, 0)

    return Graph(sorted(list(vertices)), edges, layout=lt).scale(scale)

def edgesToVertices(edges):
    return list(set([u for u, v in edges] + [v for u, v in edges]))