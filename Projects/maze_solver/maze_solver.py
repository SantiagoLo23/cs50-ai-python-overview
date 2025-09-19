# maze_solver.py

class Node():
    def __init__(self, state, parent, action):
        self.state = state  # Current state in the maze
        self.parent = parent  # State before reaching this state
        self.action = action  # Action taken to reach this state from parent


class StackFrontier():
    """Depth-First Search implementation"""
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node  # Remove and return the last node added (LIFO)


class QueueFrontier(StackFrontier):
    """Breadth-First Search implementation"""
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        node = self.frontier.pop(0)
        return node  # Remove and return the first node added (FIFO)


class GreedyBestFirstFrontier(QueueFrontier):
    """Greedy Best-First Search implementation"""
    def __init__(self, goal):
        super().__init__()
        self.goal = goal

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        node = min(self.frontier, key=lambda n: self.heuristic(n.state))
        self.frontier.remove(node)
        return node

    def heuristic(self, state):
        """Manhattan distance heuristic"""
        x1, y1 = state
        x2, y2 = self.goal
        return abs(x1 - x2) + abs(y1 - y2)


class AStarFrontier(QueueFrontier):
    """A* Search implementation"""
    def __init__(self, goal):
        super().__init__()
        self.goal = goal

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        # Find node with lowest f(n) = g(n) + h(n)
        node = min(self.frontier, key=lambda n: self.cost(n) + self.heuristic(n.state))
        self.frontier.remove(node)
        return node

    def cost(self, node):
        """g(n): Cost from start to current node"""
        cost = 0
        while node.parent is not None:
            cost += 1
            node = node.parent
        return cost

    def heuristic(self, state):
        """h(n): Manhattan distance heuristic"""
        x1, y1 = state
        x2, y2 = self.goal
        return abs(x1 - x2) + abs(y1 - y2)


class Maze():
    def __init__(self, maze_data=None):
        if maze_data:
            self._init_from_data(maze_data)
        else:
            self._init_empty()

    def _init_from_data(self, maze_data):
        """Initialize maze from 2D array data"""
        self.height = len(maze_data)
        self.width = len(maze_data[0])
        
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if maze_data[i][j] == "A":
                    self.start = (i, j)
                    row.append(False)
                elif maze_data[i][j] == "B":
                    self.goal = (i, j)
                    row.append(False)
                elif maze_data[i][j] == " ":
                    row.append(False)
                else:
                    row.append(True)
            self.walls.append(row)
        
        self.solution = None
        self.explored = set()
        self.num_explored = 0

    def _init_empty(self):
        """Initialize empty maze"""
        self.height = 0
        self.width = 0
        self.walls = []
        self.start = None
        self.goal = None
        self.solution = None
        self.explored = set()
        self.num_explored = 0

    def neighbors(self, state):
        """Get valid neighboring states"""
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
    
    def solve_generator(self, frontier):
        """Generator that yields search progress for visualization"""
        if not self.start or not self.goal:
            return
            
        start = Node(state=self.start, parent=None, action=None)
        frontier.add(start)

        while True:
            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                yield "done", None
                return

            self.explored.add(node.state)

            neighbors = self.neighbors(node.state)
            for action, state in neighbors:
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

            yield "step_complete", node.state