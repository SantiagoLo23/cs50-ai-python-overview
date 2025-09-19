# main.py

from visualizer import Visualizer

def main():
    """
    Wilson's Algorithm Maze Generator and Solver
    
    This program:
    1. Generates a random maze using Wilson's Algorithm (visualized)
    2. Solves the same maze using 4 different algorithms simultaneously:
       - Depth-First Search (DFS)
       - Breadth-First Search (BFS) 
       - Greedy Best-First Search
       - A* Search
    
    Configuration:
    - To change maze size, edit MAZE_WIDTH and MAZE_HEIGHT in visualizer.py
    - To change cell size, edit CELL_SIZE in visualizer.py
    - Odd numbers work best for maze dimensions (ensures proper maze structure)
    
    Controls:
    - Press Q to quit at any time
    - Watch the maze generation first, then the solving phase
    
    Features:
    - Real-time Wilson's algorithm visualization
    - All four algorithms displayed in a 2x2 grid
    - Automatic screen scaling for different maze sizes
    - Statistics display for each algorithm
    """
    
    print("="*60)
    print("WILSON'S ALGORITHM MAZE GENERATOR AND SOLVER")
    print("="*60)
    print("Starting maze generation and solving visualization...")
    print("Press Q at any time to quit")
    print("="*60)
    
    visualizer = Visualizer()
    visualizer.run()
    
    print("Program completed. Thank you for using the maze solver!")

if __name__ == "__main__":
    main()