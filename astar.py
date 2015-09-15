# coding=utf-8
from queue import PriorityQueue
from Catalonia import *
from copy import deepcopy


class Node:
    def __init__(self):
        self.priority = 0
        self.parent = None
        self.state = None
        self.step = None
        self.cost = 0
        self.prevoius_state = None
        pass

    def __lt__(self, other):
        return self.priority < other.priority


def find_nearest(node_pos, goal):
    if len(goal) == 0:
        return 0
    return min([taxi(node_pos, x) for x in goal])


def heuristics(node, instance):
    node_pos = (node[0], node[1])
    target_pos = (
    instance.get_target_state()[0], instance.get_target_state()[1])
    return taxi(node_pos, target_pos)


def taxi(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def astar(instance, h=heuristics):
    closed = []  # zbiór zamknięty
    # inicjujemy zbiór otwarty stanem początkowym. Decyzję ustawiamy na null
    # koszt na 0 - nie ma to znaczenia. Rodzicem jest również null (jest to
    # korzeń drzewa
    # fringe dla UCS jest kolejką priorytetową (niższy priorytet powoduje szybsze zdjęcie
    # elementu
    # enqueue - put
    # dequeue - get
    fringe = PriorityQueue()
    # format wierzchołka to:
    # (priorytet,[(stan, decyzja, koszt), rodzic])
    # jest to wymagane przez kolejkę.
    root_node = Node()
    root_node.parent = None
    root_node.cost = 0
    root_node.step = None
    root_node.state = instance.get_start_state()
    root_node.priority = 0
    root_node.prevoius_state = None
    fringe.put(root_node)
    # znaleziony cel
    target = None

    while True:
        # jeśli zbiór otwarty jest pusty to nie istnieje droga do celu
        if fringe.empty():
            return []
        # pobierz kolejny węzeł z kolejki - ten o najniższym priorytecie
        # ignorujemy koszt pobrany z kolejki, zamiast niego używamy własności cost węzła
        node = fringe.get()
        node_cost = node.cost

        # jeśli jesteśmy w stanie docelowym, ustaw cel i zakończ
        if instance.is_goal_state(node.state):
            target = node
            break

        # jeśli węzeł nie był rozwijany
        if node.state not in closed:
            # dodaj go do zbioru zamkniętego (innymi słowy oznacz jako rozwinięty)
            closed.append(node.state)
            # rozwiń go
            children = instance.get_children(node.state)

            # print node.state, children
            # i dla każdego następnika
            for child in children:
                child_state, child_step, child_cost = child
                # dodaj informację o poprzedniku (node jest rodzicem child)
                # jako koszt ustaw sumę następnika i koszt dojścia do rodzica -
                # został on odczytany przy rozpakowywaniu krotki zwróconej przez
                # fringe.get()
                heuristic_cost = h(child_state,
                                   instance)  # koszt do wyjścia oszacowany przez heurystykę
                vertex = Node()
                vertex.step = child_step
                vertex.cost = child_cost + node_cost
                vertex.parent = node
                vertex.state = child_state
                vertex.priority = vertex.cost + heuristic_cost
                vertex.prevoius_state = node.state
                fringe.put(vertex)

    # lista decyzji prowadzących do rozwiązania
    solution = []
    # zaczynamy od węzła z wynikiem
    i = target
    # dopóki ma rodzica (nie jesteśmy w korzeniu)
    while i.parent is not None:
        # dodaj decyzję która nas tutaj doprowadziła
        solution.append(i)
        # przejdź do rodzica
        i = i.parent
    # podążaliśmy od wyjścia do startu przez co trzeba odwrócić kolejność
    solution.reverse()

    return solution


arrows = {'East': '>',
          'North': '^',
          'South': 'v',
          'West': '<'}

TilePrint = {Tile.Bus: 'B',
             Tile.Ship: 'S',
             Tile.Walk: ' ',
             Tile.Train: 'T'
             }


def print_solution(layout, solution):
    s = "\n".join([''.join(map(lambda x: TilePrint[x], row)) for row in layout])

    rows = s.split('\n')
    m = [  list(x) for x in rows]


    for i, step in enumerate(solution):
        assert isinstance(step, Node)
        x, y = step.prevoius_state
        m[y][x] = arrows[step.step]

    s = '\n'.join([''.join(x) for x in m  ]  )
    print(s)

if __name__ == "__main__":
    c = Catalonia()
    c.cost_function = c.time_cost_func
    c.load_from_file("input.txt")
    result = astar(c)
    print_solution(c.layout, result)
    print([node.cost for node in result] )
