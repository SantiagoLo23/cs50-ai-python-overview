import random
import time

class MazeGenerator:
    def __init__(self, width, height):
        # Ensure odd dimensions for proper maze structure
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.maze = None

    def wilson_algorithm_generator(self):
        """Generator that yields maze states during Wilson's algorithm execution"""
        maze = [['#' for _ in range(self.width)] for _ in range(self.height)]
        in_maze = set()
        start_cell = (1, 1)
        maze[start_cell[0]][start_cell[1]] = ' '
        in_maze.add(start_cell)
        yield maze, "initial", start_cell

        all_cells = [(r, c) for r in range(1, self.height, 2)
                     for c in range(1, self.width, 2)]
        remaining_cells = [cell for cell in all_cells if cell not in in_maze]

        while remaining_cells:
            current = random.choice(remaining_cells)
            path = [current]
            yield maze, "walk_start", current
            time.sleep(0.05)

            steps = 0
            max_steps = 1000

            while current not in in_maze and steps < max_steps:
                steps += 1
                neighbors = []
                for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                    nr, nc = current[0] + dr, current[1] + dc
                    if 1 <= nr < self.height - 1 and 1 <= nc < self.width - 1:
                        neighbors.append((nr, nc))

                if not neighbors:
                    break

                next_cell = random.choice(neighbors)
                if next_cell in path:
                    loop_start = path.index(next_cell)
                    path = path[:loop_start + 1]
                else:
                    path.append(next_cell)

                current = next_cell
                yield maze, "walking", path.copy()
                time.sleep(0.03)

            for i in range(len(path) - 1):
                r1, c1 = path[i]
                r2, c2 = path[i + 1]
                maze[r1][c1] = ' '
                in_maze.add((r1, c1))
                wall_r = (r1 + r2) // 2
                wall_c = (c1 + c2) // 2
                maze[wall_r][wall_c] = ' '
                yield maze, "adding_path", (r1, c1)
                time.sleep(0.02)

            if path:
                final_r, final_c = path[-1]
                maze[final_r][final_c] = ' '
                in_maze.add((final_r, final_c))

            remaining_cells = [cell for cell in all_cells if cell not in in_maze]
            yield maze, "path_complete", None

        # Add start
        maze[1][1] = 'A'

        # Safe goal placement
        def place_goal(maze, width, height):
            start_pos = (1, 1)
            for r in range(height - 2, 0, -2):
                for c in range(width - 2, 0, -2):
                    if maze[r][c] == ' ' and (r, c) != start_pos:
                        maze[r][c] = 'B'
                        return True
            for r in range(height - 2, 0, -1):
                for c in range(width - 2, 0, -1):
                    if maze[r][c] == ' ' and (r, c) != start_pos:
                        maze[r][c] = 'B'
                        return True
            return False

        place_goal(maze, self.width, self.height)

        self.maze = maze
        yield maze, "complete", None
