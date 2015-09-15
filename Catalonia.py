Directions = {
    'East': (1, 0),
    'North': (0, -1),
    'South': (0, 1),
    'West': (-1, 0)
}


'''
- Na piechotę: 10 jednostek czasu, koszt darmowy
- Autobusy: 3 jednostki czasu, kosztuje 2 euro
- Statek 5 jednostek czasu, kosztuje 5 euro
- Pociąg: 1 jednostka czasu, kosztuje 3 euro
'''

class Tile(object):
    def __int__(self):
        pass

    Walk, Bus, Train, Ship = range(4)


MoneyCost = {
    Tile.Walk : 0,
    Tile.Bus : 2,
    Tile.Ship : 5,
    Tile.Train : 3
}

TimeCost = {
    Tile.Walk : 10,
    Tile.Bus : 3,
    Tile.Ship : 5,
    Tile.Train : 1
}


# State is simply tuple (x, y)

class Catalonia(object):

    def money_cost_func(self, state):
        x , y = state
        tile = self.layout[y][x]
        return MoneyCost[tile]


    def time_cost_func(self, state):
        x , y = state
        tile = self.layout[y][x]
        return TimeCost[tile]

    def __init__(self):
        self.layout = []
        self.expanded = []
        self.shape = (0, 0)

        self.startState = (0,0)
        self.goalState = (9,9)

        self.cost_function = lambda s: 0

    def get_target_state(self):
        assert self.startState is not None
        return self.startState

    def load_from_file(self, filename):
        rows = 0
        with open(filename, 'r') as f:
            for line in f:
                self.layout.append([])
                self.expanded.append([])
                rows += 1
                cols = 0
                for char in line:
                    tile = None
                    if char == '.':
                        tile = Tile.Walk
                    elif char == 'S':
                        tile = Tile.Ship
                    elif char == 'T':
                        tile = Tile.Train
                    elif char == 'B':
                        tile = Tile.Bus
                    elif char == '*':
                        tile = Tile.Walk
                        self.startState = (cols, rows - 1)
                    elif char == 'G':
                        tile = Tile.Walk
                        self.targetState = (cols, rows - 1)
                    elif char == '\r' or char == '\n':
                        break
                    else:
                        raise Exception('Unknown tile type: \'' + char + '\'')
                    self.layout[-1].append(tile)
                    self.expanded[-1].append(False)
                    cols += 1
        self.shape = (cols, rows)

    def get_start_state(self):
        return self.startState

    def get_children(self, state):
        # for each possible move check if it is valid. If so - return it
        for k, v in Directions.items():
            dx, dy = v
            newx = state[0] + dx
            newy = state[1] + dy
            if 0 <= newx < self.shape[0] and 0 <= newy < self.shape[1]:
                yield ((newx, newy),k, self.cost_function((newx, newy)))

    def is_goal_state(self, state):
        return state == self.goalState


if __name__ == "__main__":
    c = Catalonia()
    c.load_from_file("input.txt")

    for l in range(c.shape[1]):
        row = c.layout[l]
        print("".join(map(str, row)))

    print([x for x in c.get_children((1,1))])
