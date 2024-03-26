from dataclasses import dataclass
from pulp import *
from util import *

MATCHING_COLOR = MAROON_E
EXPOSED_COLOR = GREEN_E
AUGMENTING_COLOR = RED_E
BFS_COLOR = PURPLE_C

HIDDEN_COLOR = GRAY

MATCHED_WIDTH = 15

GRAPH_SCALE = 1.3
NODE_SCALE = 1.25

SHORT_CODE_PAUSE = 1

Vertex = int
Edge = Tuple[Vertex, Vertex]
MyGraph = Tuple[List[Vertex], List[Edge]]

def match_vertex(mob, where=None, width=50):
    mob.set_stroke_width(width)
    mob.move_to(where)
    return mob

def unmatch_vertex(mob, where=None, width=4):
    mob.set_stroke_width(width)
    mob.move_to(where)
    return mob

def match_edge(mob, change_color=True, width=MATCHED_WIDTH):
    mob.set_stroke_width(width)

    if change_color:
        mob.set_color(MATCHING_COLOR)

    return mob

def unmatch_edge(mob, change_color=True):
    mob.set_stroke_width(4)

    if change_color:
        mob.set_color(BLACK)

    return mob


def animate_augment_path(self, g, path, add_animations_first=None, add_animations_between=None, add_animations_second=None, instant=False, switch=False, run_time=None, operation=None):
    """If animations is lambda, do them only here I don't know that I'm doing."""
    A = path
    AV = edgesToVertices(A)

    offset = 0 if not switch else 1

    if instant:
        self.play(
            *([] if add_animations_second is None else add_animations_second() if type(add_animations_second) is type(lambda: None) else add_animations_second),
            *[
                ApplyFunction(lambda x: match_edge(x), g.edges[e])
                for e in A[offset::2]
            ],
            *[
                ApplyFunction(lambda x: unmatch_edge(x), g.edges[e])
                for e in A[(offset+1)%2::2]
            ],
            **(dict() if run_time is None else {"run_time": run_time})
        )
        return
    if operation == "A":
        self.play(
            *([] if add_animations_first is None else add_animations_first() if type(add_animations_first) is type(lambda: None) else add_animations_first),
            *[g.edges[e].animate.set_color(AUGMENTING_COLOR) for e in A],
            *[g.vertices[v].animate.set_color(AUGMENTING_COLOR) for v, _ in A],
            *[g.vertices[v].animate.set_color(AUGMENTING_COLOR) for _, v in A],
            **(dict() if run_time is None else {"run_time": run_time})
        )

    if add_animations_between is not None:
        self.play(
                *add_animations_between,
                **(dict() if run_time is None else {"run_time": run_time})
                )

    self.play(
        *([] if add_animations_second is None else add_animations_second() if type(add_animations_second) is type(lambda: None) else add_animations_second),
        *[
            ApplyFunction(lambda x: match_edge(x, change_color=False), g.edges[e])
            for e in A[offset::2]
        ],
        *[
            ApplyFunction(lambda x: unmatch_edge(x, change_color=False), g.edges[e])
            for e in A[(offset+1)%2::2]
        ],
        **(dict() if run_time is None else {"run_time": run_time})
    )

def animate_correct_graph_color(self, g, M, set_lines=None, code=None, add_animations=None, run_time=None):
    MV = edgesToVertices(M)

    self.play(
        *([] if add_animations is None else add_animations() if type(add_animations) is type(lambda: None) else add_animations),
        *([] if set_lines is None else set_lines(self, code, [24])),
        *[g.edges[e].animate.set_color(BLACK) for e in g.edges if e not in M],
        *[g.edges[e].animate.set_color(MATCHING_COLOR) for e in g.edges if e in M],
        *[
            g.vertices[v].animate.set_color(EXPOSED_COLOR)
            for v in g.vertices
            if v not in MV
        ],
        *[
            g.vertices[v].animate.set_color(MATCHING_COLOR)
            for v in g.vertices
            if v in MV
        ],
        **(dict() if run_time is None else {"run_time": run_time})
    )


class Blossom(Scene):
    @fade
    def construct(self):
        self.camera.background_color = WHITE
        @dataclass
        class Context:
            graph: MyGraph
            self: Blossom
            code: 'typing.Any'
            set_lines: 'typing.Any'

        g = parse_graph(
            """
5 0 <-16.05615947107685, -12.504911246689693> <-14.446419714646854, -6.866013725874188>
0 8 <-14.446419714646854, -6.866013725874188> <-16.42527207725241, -1.8140283988138854>
12 0 <-19.64155534824222, -7.330631498406216> <-14.446419714646854, -6.866013725874188>
1 3 <-4.698194206378598, 0.11011604485983129> <-10.209550409185647, -2.9552644219000106>
1 10 <-4.698194206378598, 0.11011604485983129> <0.9003340177597777, -2.5845025309871477>
3 2 <-10.209550409185647, -2.9552644219000106> <-10.670793355913192, -9.290296998392101>
5 2 <-16.05615947107685, -12.504911246689693> <-10.670793355913192, -9.290296998392101>
3 8 <-10.209550409185647, -2.9552644219000106> <-16.42527207725241, -1.8140283988138854>
4 6 <-1.0383909201343497, -12.64149137008625> <-7.062170194186263, -14.061899786709596>
4 7 <-1.0383909201343497, -12.64149137008625> <3.324971894939845, -8.293802236457113>
4 11 <-1.0383909201343497, -12.64149137008625> <-3.3577054035744847, -6.997621303069259>
12 5 <-19.64155534824222, -7.330631498406216> <-16.05615947107685, -12.504911246689693>
7 9 <3.324971894939845, -8.293802236457113> <7.465014371318295, -3.8180621675279958>
10 7 <0.9003340177597777, -2.5845025309871477> <3.324971894939845, -8.293802236457113>
12 8 <-19.64155534824222, -7.330631498406216> <-16.42527207725241, -1.8140283988138854>
8 13 <-16.42527207725241, -1.8140283988138854> <-12.470684295924984, 2.950307523065462>
10 11 <0.9003340177597777, -2.5845025309871477> <-3.3577054035744847, -6.997621303069259>
10 14 <0.9003340177597777, -2.5845025309871477> <5.227801852655065, 1.8530677198156864>
                """,
            s=0.065,
            t=-0.070,
        ).scale(GRAPH_SCALE * NODE_SCALE).rotate(-PI / 2).shift(3.3 * RIGHT)

        for v in g.vertices:
            g.vertices[v].set_color(GRAY)
        for e in g.edges:
            g.edges[e].set_color(GRAY)

        code_str = """def find_maximum_matching(G, M):
	P ← find_augmenting_path(G, M)
	if P ≠ []:
		Add alternating edges of P to M
		return find_maximum_matching(G, M)
	else
		return M

def find_augmenting_path(G, M):
	F ← empty forest
    unmark all edges in G, mark all edges in M
	nodes_to_check ← exposed vertices in G
	for v in nodes_to_check:
		create a singleton tree {v} and add the tree to F
		root(v) ← v
	for v in nodes_to_check:
		while there exists an unmarked edge e = (v, w):
			if w ∉ F:       #Vertex w is in M
				add_to_forest(M, F, v, w)
			else:
				if dist(w, root(w)) even:
					if root(v) ≠ root(w):
						P ← return augmenting path(F, v, w)
					else:
						(B,G1,M1) ← contract_blossom(G, M, F, v, w)
						P1 ← find_augmenting_path(G1, M1)
						P ← lift_blossom(B,P1)
					return P
				else:
					continue
			mark edge e
	return []
"""
        code = Code(code=code_str, font="Fira Mono", line_spacing=0, style="Abap", language="python")
        code.background_mobject[0].set_opacity(0)
        code.scale(0.55).shift(2.8 * LEFT)
        
        c = 0.075

        for i in range(1, len(code.code)):
            code.code[i].shift(i * DOWN * c)
            code.line_numbers[i].shift(i * DOWN * c)

        code.shift(UP * len(code.code) * c / 2)

        frame = SurroundingRectangle(code, color=BLACK, stroke_width=2)
        frame.round_corners(0.2).shift(DOWN * 0.1)

        self.play(Write(code), Write(g), Write(frame))
        

        M = []

        def set_lines(self, code, lines, previous_lines=[]):
            
            if previous_lines == []:
                for i in range(len(code.code_string.splitlines())):
                    previous_lines.append(i + 1)
                    code.code.chars[i - 1].save_state()

            new_lines = [l for l in lines if l not in previous_lines]

            dis_lines = [l for l in previous_lines if l not in lines]

            for l in dis_lines:
                code.code.chars[l - 1].save_state()

            new_lines_animation = [code.line_numbers[i - 1].animate.set_color(BLACK) for i in new_lines] + \
                                  [code.code.chars[i - 1].animate.restore() for i in new_lines]
            dis_lines_animation = [code.line_numbers[i - 1].animate.set_color(HIDDEN_COLOR) for i in dis_lines] + \
                                  [code.code.chars[i - 1].animate.set_color(HIDDEN_COLOR) for i in dis_lines]

            while len(previous_lines) != 0:
                previous_lines.pop()

            for e in lines:
                previous_lines.append(e)

            return new_lines_animation + dis_lines_animation

        operations = [
            ("R", None),
            ("FM",None),
            ("F",[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]),
            ("I", 8),
            ("N", [(8, 0), (8, 12), (8, 3), (8, 13)]),
            ("A", [(8, 12)]),
            ("FM",None),
            ("F",[0,1,2,3,4,5,6,7,9,10,11,13,14]),
            ("I", 1),
            ("N", [(1, 3), (1, 10)]),
            ("A", [(1, 10)]),
            ("FM",None),
            ("F",[0,2,3,4,5,6,7,9,11,13,14]),
            ("I", 3),
            ("N", [(3, 8), (3, 2), (3, 1)]),
            ("B", [(3, 8)]),
            ("BO", [(8,12)]),
            ("N", [(3, 2), (3, 1)]),
            ("A", [(3,2)]),
            ("FM",None),
            ("F",[0,4,5,6,7,9,11,13,14]),
            ("I", 4),
            ("N", [(4, 11), (4, 6), (4, 7)]),
            ("A", [(4, 11)]),
            ("FM",None),
            ("F",[0,5,6,7,9,13,14]),
            ("I", 5),
            ("N", [(5, 0), (5, 12), (5, 2)]),
            ("A", [(5, 0)]),
            ("FM",None),
            ("F",[6,7,9,13,14]),
            ("I", 9),
            ("N", [(9, 7)]),
            ("A", [(9, 7)]),
            ("FM",None),
            ("F",[6,13,14]),
            ("I", 14),
            ("N", [(14, 10)]),
            ("B", [(14, 10)]),
            ("BO", [(1, 10)]),
            ("I", 1),
            ("DN", [(1, 10),(1,3)]),
            ("N", [(1, 3)]),
            ("B", [(1, 3)]),
            ("BO", [(3, 2)]),
            ("I", 2),
            ("DN", [(2, 3),(2,5)]),
            ("N", [(2, 5)]),
            ("B", [(2, 5)]),
            ("BO", [(5, 0)]),
            ("I", 0),
            ("N", [(0, 8), (0, 12),(0,5)]),
            ("B", [(0,12)]),
            ("BO", [(8, 12)]),
            ("N", [(0, 8),(0,5)]),
            ("BC", [(0, 8)]),
            ("C", [0, 8, 12]),
            ("FA",None),
            ("F",[6,13,14]),
            ("I", 14),
            ("N", [(14, 10)]),
            ("B", [(14, 10)]),
            ("BO", [(1, 10)]),
            ("I", 1),
            ("DN", [(1, 10),(1,3)]),
            ("N", [(1, 3)]),
            ("B", [(1, 3)]),
            ("BO", [(3, 2)]),
            ("I", 2),
            ("DN", [(2, 3),(2,5)]),
            ("N", [(2, 5)]),
            ("B", [(2, 5)]),
            ("BO", [(5, 0), (0, 8), (0, 12), (8, 12)]),
            ("BA", [(8, 13)]),
            ("AB", [(14, 10), (10, 1), (1, 3), (3, 2), (2, 5), (5, 0), (0, 12), (12, 8), (8, 13)]),
            ("U", [0, 8, 12]),
            ("FM",None),
            ("F", [6]),
            ("I", 6),
            ("N", [(6, 4)]),
            ("B", [(6, 4)]),
            ("BO", [(4, 11)]),
            ("I", 11),
            ("DN", [(11, 4),(11,10)]),
            ("N", [(11, 10)]),
            ("B", [(11, 10)]),
            ("BO", [(14, 10)]),
            ("Q", None),
            ("RR", None),
        ]

        fk = (12, 5)
        g.add_to_back(g.edges[fk if fk in g.edges else (fk[1], fk[0])])

        for operation, argument in operations:
            if operation == "R":
                animate_correct_graph_color(self, g, M, run_time=0.8)

            if operation == "RR":
                animate_correct_graph_color(self, g, M, lambda x, y, z: [], None, add_animations=lambda: set_lines(self, code, [i + 1 for i in range(len(code.code))]), run_time=0.8)

            if operation == "FM":
                self.play(*set_lines(self, code, [1]), run_time = 0.7)
                self.play(*set_lines(self, code, [1,2]), run_time = 0.7)
                self.play(*set_lines(self, code, [9]), run_time = 0.7)
                animate_correct_graph_color(self, g, M, add_animations=lambda: set_lines(self, code, [10,11]),run_time=0.7)
                self.play(*set_lines(self, code, [12,13]), run_time = 0.7)
                self.play(*set_lines(self, code, [14,15]), run_time = 0.7)

            if operation == "FA":
                self.play(*set_lines(self, code, [9]), run_time = 0.7)
                animate_correct_graph_color(self, g, M, add_animations=lambda: set_lines(self, code, [10,11]),run_time=0.7)
                self.play(*set_lines(self, code, [12,13]), run_time = 0.7)
                self.play(*set_lines(self, code, [14,15]), run_time = 0.7)

            if operation == "F":
                self.play(
                    *[g.vertices[v].animate.set_color(BLUE_C)
                        for v in argument],
                    *set_lines(self, code, [16]),
                    run_time = 0.7
                )
                animate_correct_graph_color(self, g, M, run_time=0.6)

            if operation == "I":
                g.save_state()
                self.play(
                    Circumscribe(g.vertices[argument], Circle, color=BFS_COLOR),
                    g.vertices[argument].animate.set_color(BFS_COLOR),
                    *set_lines(self, code, [16]),
                    run_time = 0.8
                )

            if operation == "N":
                g.save_state()
                self.play(
                    *[g.vertices[v].animate.set_color(BFS_COLOR) for v in edgesToVertices(argument)],
                    *[g.edges[e if e in g.edges else (e[1], e[0])].animate.set_color(BFS_COLOR) for e in argument],
                    *set_lines(self, code, [17]),
                    run_time = 0.6
                )
                self.play(Restore(g), run_time=0.5)

            if operation == "DN":
                self.play(
                    *[g.vertices[v].animate.set_color(BFS_COLOR) for v in edgesToVertices(argument)],
                    *[g.edges[e if e in g.edges else (e[1], e[0])].animate.set_color(BFS_COLOR) for e in argument],
                    *set_lines(self, code, [17]),
                    run_time = 0.6
                )
                self.play(
                    Restore(g),
                    *set_lines(self, code, [20,29,30]),
                    run_time = 0.7
                )

            if operation[0] == "B":
                if operation == "B" or operation == "BN" :
                    c = [18]
                elif operation == "BO":
                    c = [19]
                elif operation == "BC":
                    c = [20,21,24]
                else:
                    c = [20,21,22]
                self.play(
                    *[g.vertices[v].animate.set_color(AUGMENTING_COLOR) for v in edgesToVertices(argument)],
                    *[g.edges[e if e in g.edges else (e[1], e[0])].animate.set_color(AUGMENTING_COLOR) for e in argument],
                    *set_lines(self, code, c),
                    run_time = 0.8
                )
                if operation == "BO":
                    self.play(*set_lines(self, code, [31]), run_time = 0.7)


            if operation[0] == "A":
                augmenting_path = [(e if e in g.edges else (e[1], e[0])) for e in argument]

                animate_augment_path(self, g,
                        augmenting_path,
                            add_animations_first=lambda: set_lines(self, code, [20,21,22]),
                            add_animations_second=lambda: set_lines(self, code, [23]),
                            operation = operation,
                            run_time = 0.8
                        )

                # improve M
                for i in range(0, len(augmenting_path), 2):
                    M.append(augmenting_path[i])
                for i in range(1, len(augmenting_path), 2):
                    M.remove(augmenting_path[i])

                self.play(*set_lines(self, code, [28]), run_time = 0.7)

                if operation == "A":
                    self.play(*set_lines(self, code, [2,3,4,5]), run_time = 0.7)
                else:
                    self.play(*set_lines(self, code, [26]), run_time = 0.8)

            if operation == "C":
                small_random = [1 + i / 10000 for i in range(len(argument))]

                average = sum(g.vertices[v].get_center() for v in argument) / len(argument)

                original_vertices = argument
                original_positions = [g.vertices[v].get_center() for v in argument]

                self.play(
                    ApplyFunction(lambda x: match_vertex(x, where=average * small_random[0]), g.vertices[0]),
                    ApplyFunction(lambda x: match_vertex(x, where=average * small_random[1]), g.vertices[8]),
                    ApplyFunction(lambda x: match_vertex(x, where=average * small_random[2]), g.vertices[12]),
                    *set_lines(self, code, [25]),
                    run_time = 0.8
                )

                self.play(*set_lines(self, code, [26]), run_time = 0.8)


            if operation == "U":
                self.play(
                    ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[0]), g.vertices[0]),
                    ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[1]), g.vertices[8]),
                    ApplyFunction(lambda x: unmatch_vertex(x, where=original_positions[2]), g.vertices[12]),
                    *set_lines(self, code, [27,28]),
                    run_time = 0.8
                )

                self.play(*set_lines(self, code, [2,3,4,5]), run_time = 0.7)

            if operation == "Q":
                self.play(*set_lines(self, code, [32]), run_time=SHORT_CODE_PAUSE)
                self.play(*set_lines(self, code, [1,2]), run_time=SHORT_CODE_PAUSE)
                self.play(*set_lines(self, code, [6,7]), run_time=SHORT_CODE_PAUSE)
