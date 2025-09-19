import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state # Current state in the maze
        self.parent = parent # State before reaching this state
        self.action = action # Action taken to reach this state from parent


class StackFrontier(): # Depth-First Search implementation
    def __init__(self):
        self.frontier = [] # List to store the nodes in the frontier

    def add(self, node):
        self.frontier.append(node) # Add a node to the frontier

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier) # Check if a state is in the frontier

    def empty(self):
        return len(self.frontier) == 0 # Check if the frontier is empty

    def remove(self): 
        if self.empty():
            raise Exception("empty frontier") # Raise an exception if the frontier is empty
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node # Remove and return the last node added to the frontier (LIFO)


class QueueFrontier(StackFrontier): # Inherits from StackFrontier but overrides the remove method to implement FIFO Breadth-First Search

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class GreedyBestFirstFrontier(QueueFrontier): # Inherits from QueueFrontier but overrides the remove method to implement Greedy Best-First Search

    def __init__(self, goal):
        super().__init__()
        self.goal = goal

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            # Find the node with the lowest heuristic value (estimated cost to goal)
            node = min(self.frontier, key=lambda n: self.heuristic(n.state))
            self.frontier.remove(node)
            return node

    def heuristic(self, state):
        # Using Manhattan distance as heuristic
        x1, y1 = state
        x2, y2 = self.goal
        return abs(x1 - x2) + abs(y1 - y2)
    
class AStarFrontier(QueueFrontier): # Inherits from QueueFrontier but overrides the remove method to implement A* Search

# Tends to use more memory
# h(n) is admissible (never overestimates the true cost to reach the goal)
# h(n) is consistent (for every node n and every successor n' of n, the estimated cost of reaching the goal from n is no greater than the cost of getting to n' plus the estimated cost from n' to the goal)
    def __init__(self, goal):
        super().__init__()
        self.goal = goal

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            # Find the node with the lowest f(n) = g(n) + h(n)
            node = min(self.frontier, key=lambda n: self.cost(n) + self.heuristic(n.state))
            self.frontier.remove(node)
            return node

    def cost(self, node):
        # g(n): Cost from start to current node
        cost = 0
        while node.parent is not None:
            cost += 1
            node = node.parent
        return cost

    def heuristic(self, state):
        # h(n): Using Manhattan distance as heuristic
        x1, y1 = state
        x2, y2 = self.goal
        return abs(x1 - x2) + abs(y1 - y2)
    
class Maze():

    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
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


    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)

        """Change to StackFrontier() for DFS"""
        frontier = StackFrontier()

        """Change to QueueFrontier() for BFS"""
        #frontier = QueueFrontier()
        
        """"Change to GreedyBestFirstFrontier(self.goal) for Greedy Best-First Search"""
        #frontier = GreedyBestFirstFrontier(self.goal)

        """Change to AStarFrontier(self.goal) for A* Search"""
        #frontier = AStarFrontier(self.goal)

        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = [] # List to store the actions taken to reach the goal
                cells = [] # List to store the cells visited to reach the goal
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True) # Change to False to hide explored cells
