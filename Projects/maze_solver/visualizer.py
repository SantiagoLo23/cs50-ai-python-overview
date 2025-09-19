import pygame
from maze_generator import MazeGenerator
from maze_solver import Maze, StackFrontier, QueueFrontier, GreedyBestFirstFrontier, AStarFrontier

# Maze configuration
MAZE_WIDTH = 41
MAZE_HEIGHT = 31
MARGIN = 10
FPS = 30

# Colors
WALL_COLOR = (40, 40, 40)
START_COLOR = (255, 0, 0)
GOAL_COLOR = (0, 171, 28)
EXPLORED_COLOR = (212, 97, 85)
SOLUTION_COLOR = (220, 235, 113)
EMPTY_COLOR = (237, 240, 252)
GENERATION_COLOR = (100, 100, 255)
WALK_COLOR = (255, 255, 0)

class Visualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h

        # Dynamic cell size and quadrant dimensions
        self.quadrant_width = self.screen_width // 2 - 2 * MARGIN
        self.quadrant_height = (self.screen_height - 60) // 2 - 2 * MARGIN
        self.cell_size = min(self.quadrant_width // MAZE_WIDTH, self.quadrant_height // MAZE_HEIGHT)

        # Dynamic fonts
        title_font_size = max(16, self.screen_width // 80)
        stats_font_size = max(12, self.screen_width // 100)
        self.title_font = pygame.font.SysFont("Arial", title_font_size, bold=True)
        self.stats_font = pygame.font.SysFont("Arial", stats_font_size, bold=True)

        self.clock = pygame.time.Clock()
        self.mazes = [Maze() for _ in range(4)]
        self.titles = ["DFS", "BFS", "Greedy Best-First", "A* Search"]
        self.generators = None
        self.generation_complete = False

    def draw_generation_cell(self, maze_data, row, col, offset_x, offset_y, status, extra_data):
        x = offset_x + col * self.cell_size
        y = offset_y + row * self.cell_size
        cell = maze_data[row][col]

        if cell == '#':
            color = WALL_COLOR
        elif cell == 'A':
            color = START_COLOR
        elif cell == 'B':
            color = GOAL_COLOR
        elif cell == ' ':
            color = WALK_COLOR if status == "walking" and extra_data and (row, col) in extra_data else EMPTY_COLOR
        else:
            color = WALL_COLOR

        pygame.draw.rect(self.screen, color, (x, y, self.cell_size - 1, self.cell_size - 1))

    def draw_solving_cell(self, maze, row, col, offset_x, offset_y):
        x = offset_x + col * self.cell_size
        y = offset_y + row * self.cell_size

        if maze.walls[row][col]:
            color = WALL_COLOR
        elif (row, col) == maze.start:
            color = START_COLOR
        elif (row, col) == maze.goal:
            color = GOAL_COLOR
        elif maze.solution and (row, col) in maze.solution[1]:
            color = SOLUTION_COLOR
        elif (row, col) in maze.explored:
            color = EXPLORED_COLOR
        else:
            color = EMPTY_COLOR

        pygame.draw.rect(self.screen, color, (x, y, self.cell_size - 1, self.cell_size - 1))

    def draw_maze_generation(self, maze_data, status, extra_data):
        maze_width = len(maze_data[0]) * self.cell_size
        maze_height = len(maze_data) * self.cell_size
        offset_x = (self.screen_width - maze_width) // 2
        offset_y = (self.screen_height - maze_height) // 2

        for i in range(len(maze_data)):
            for j in range(len(maze_data[0])):
                self.draw_generation_cell(maze_data, i, j, offset_x, offset_y, status, extra_data)

        status_text = f"Generating maze using Wilson's Algorithm... Status: {status}"
        text = self.title_font.render(status_text, True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        inst_text = self.stats_font.render("Press Q to quit during generation", True, (200, 200, 200))
        self.screen.blit(inst_text, (10, 30))

    def draw_maze_solving(self, maze, offset_x, offset_y, title):
        for i in range(maze.height):
            for j in range(maze.width):
                self.draw_solving_cell(maze, i, j, offset_x, offset_y)

        title_text = self.title_font.render(title, True, (255, 255, 255))
        stats = f"Explored: {len(maze.explored)}, Solution: {len(maze.solution[1])}" if maze.solution else f"Explored: {len(maze.explored)}"
        stats_text = self.stats_font.render(stats, True, (200, 200, 200))

        self.screen.blit(title_text, (offset_x + 5, offset_y + maze.height * self.cell_size + 5))
        self.screen.blit(stats_text, (offset_x + 5, offset_y + maze.height * self.cell_size + 25))

    def generate_maze(self):
        generator = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
        gen = generator.wilson_algorithm_generator()

        for maze_data, status, extra_data in gen:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            self.draw_maze_generation(maze_data, status, extra_data)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    return None

            pygame.display.flip()

        return generator.maze

    def initialize_mazes(self, maze_data):
        for maze in self.mazes:
            maze._init_from_data(maze_data)

        frontiers = [
            StackFrontier(),
            QueueFrontier(),
            GreedyBestFirstFrontier(self.mazes[2].goal),
            AStarFrontier(self.mazes[3].goal)
        ]

        self.generators = [maze.solve_generator(frontier) for maze, frontier in zip(self.mazes, frontiers)]

    def run(self):
        print("Generating maze using Wilson's Algorithm...")
        maze_data = self.generate_maze()
        if not maze_data:
            return

        print("Maze generation complete! Starting solving phase...")
        self.initialize_mazes(maze_data)
        self.generation_complete = True

        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))

            for i, (maze, gen, title) in enumerate(zip(self.mazes, self.generators, self.titles)):
                col = i % 2
                row = i // 2

                maze_pixel_width = maze.width * self.cell_size
                maze_pixel_height = maze.height * self.cell_size

                offset_x = col * self.screen_width // 2 + (self.quadrant_width - maze_pixel_width) // 2
                offset_y = row * self.screen_height // 2 + (self.quadrant_height - maze_pixel_height) // 2

                try:
                    status, state = next(gen)
                    if status == "exploring":
                        maze.explored.add(state)
                except StopIteration:
                    pass

                self.draw_maze_solving(maze, offset_x, offset_y, title)

            inst_text = self.stats_font.render("Press Q to quit", True, (200, 200, 200))
            self.screen.blit(inst_text, (10, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    running = False

            pygame.display.flip()

        pygame.quit()
