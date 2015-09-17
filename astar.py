#!/usr/bin/python
# coding=utf-8
"""
The Art of an Artificial Intelligence
http://art-of-ai.com
https://github.com/artofai
"""

__author__ = 'xevaquor'
__license__ = 'MIT'

from queue import PriorityQueue


class Node(object):
    def __init__(self):
        self.priority = 0  # priority for queue
        self.parent = None  # parent node
        self.state = None  # state at currnet node
        self.step = None  # step taken to be here
        self.cost = 0  # overall cost to be here
        self.previous_state = None  # state in parent node
        pass

    # required for use in PriorityQueue
    def __lt__(self, other):
        return self.priority < other.priority


class AStarSolver(object):
    @staticmethod
    def taxi(p1, p2):
        """
        Computes distance in taxicab (or Manhatan) norm
        :param p1: First point
        :param p2: Second point
        :return: Distance
        """
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    @staticmethod
    def norm_heuristics(node, instance):
        node_pos = (node[0], node[1])
        target_pos = (
            instance.get_target_state()[0], instance.get_target_state()[1])
        return AStarSolver.taxi(node_pos, target_pos)

    def __init__(self, heuristics_func=None, constraint_func=None):
        self.heuristics = heuristics_func if heuristics_func is not None else AStarSolver.norm_heuristics
        self.constraint = constraint_func if constraint_func is not None else lambda state: True

    def solve(self, instance):
        closed = []  # closed set, will contain expanded nodes in orter to avoid cycles
        # inicjujemy zbiór otwarty stanem początkowym. Decyzję ustawiamy na null
        # koszt na 0 - nie ma to znaczenia. Rodzicem jest również null (jest to
        # korzeń drzewa
        # fringe dla UCS jest kolejką priorytetową (niższy priorytet powoduje szybsze zdjęcie
        # elementu
        # enqueue - put
        # dequeue - get
        # fringe (open set) contains nodes that we are currently considering - tehy can be potentially expanded
        # it is a PriorityQueue to acchieve proper order visitng nodes (lower priority will be taken faster)
        # we will be adding nodes here to (maybe) use them later
        fringe = PriorityQueue()

        # initial element in tree is an "empty" node with meaning "we have not taken any decision yet and still stay
        # in initial state"

        root_node = Node()
        root_node.parent = None
        root_node.cost = 0
        root_node.step = None
        root_node.state = instance.get_start_state()
        root_node.priority = 0
        root_node.previous_state = None
        fringe.put(root_node)

        # found goal state (because there can be may of them we need to remember we have actually found
        target = None

        while True:
            # if fringe is empty, that meas we already traversed whole tree and have not found soulution
            # in other words - it is impossible to reach the goal from the initial state. Sorry!
            if fringe.empty():
                return []

            # get next node from the queue (this one with lowest priority)
            # remember that in context of A* cost is roughly the same as priority
            # ignorujemy koszt pobrany z kolejki, zamiast niego używamy własności cost węzła
            node = fringe.get()
            node_cost = node.cost

            # have we found a goal state? if so remember it and get out of loop
            if instance.is_goal_state(node.state):
                target = node
                break

            # if current node had not been expanded before, we are allowed to do it now
            if node.state not in closed:
                # add it to closed set in order to avoid expanding it once again
                closed.append(node.state)
                # expand it
                children = instance.get_children(node.state)

                # and for each descendant
                for child in children:
                    # expand tuple
                    child_state, child_step, child_cost = child

                    # cost of current node is:
                    # parent cost + current state cost + heuristics cost
                    # or
                    # backward cost + forward cost

                    # compute forward cost by given heuristics
                    heuristic_cost = self.heuristics(child_state, instance)

                    # and create a new node

                    vertex = Node()
                    vertex.step = child_step  # step we took to go from parent to this child
                    vertex.cost = child_cost + node_cost  # *BACKWARD* cost of current node
                    vertex.parent = node  # parent node
                    vertex.state = child_state  # state in this node
                    vertex.priority = vertex.cost + heuristic_cost  # priority is back + forward cost
                    # it does allow to choose more promising nodes faster
                    vertex.previous_state = node.state  # state of parent

                    # if node violates constraints we are not considering it, and his children
                    if not self.constraint(vertex):
                        continue

                    fringe.put(vertex)

        # we got out of loop, that is mean we have sequence of decision used to came to the goal.
        # now just need to recreate it

        # sequecne of decisions taken
        solution = []
        # starting from goal node
        i = target
        # while it does not have a parent (in other words: we are not at the root of decision tree)
        while i.parent is not None:
            # add decision taht took us to here
            solution.append(i)
            # and process parent node next
            i = i.parent
        # we was travelling from goal to start, so just need to reverse.
        solution.reverse()

        return solution
