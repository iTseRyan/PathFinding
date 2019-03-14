import heapq
# import time

# Cell Class (points on grid)
class Cell:
    def __init__(self, x, y, accessible):
        self.x = x
        self.y = y

        self.accessible = accessible
        self.previous = None

        # G and H used for A* calculations, cost to move, G actual cost, H estimates
        self.g = 0
        self.h = 0
        # F = G + H
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


# Main class for solving maze
class PathFinder:
    # Initialize variables and execute functions
    def __init__(self, file):
        # Width and height of maze
        self.width = 0
        self.height = 0

        # Start and end nodes/cell
        self.start = None
        self.goal = None

        # The generated cells of the maze and the maze generated from the txt
        self.maze = []
        self.cells = []

        # File name
        self.file = file

        # Read txt file and generate grid
        self.read_file()
        self.create_grid()

        # Solve(Greedy: Boolean, Diagonal Travel: Boolean)
        # Greedy Non Diagonal
        self.solve(True, False)
        self.reset_cells()
        # A* Non Diagonal
        self.solve(False, False)
        self.reset_cells()
        # Greedy Diagonal
        self.solve(True, True)
        self.reset_cells()
        # A* Diagonal
        self.solve(False, True)

    # Reads file
    def read_file(self):
        with open(self.file, 'r') as f:
            self.maze = [line.strip() for line in f]
        self.width = len(self.maze[0])
        self.height = len(self.maze)

    # Creates grid based on text file
    def create_grid(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.maze[y][x].lower() == 'x':
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
                if self.maze[y][x].lower() == 's':
                    self.start = self.check_cell(x, y)
                if self.maze[y][x].lower() == 'g':
                    self.goal = self.check_cell(x, y)

    # Calculate heuristics
    def calculate_heuristics_manhattan(self, cell):
        return abs(cell.x - self.goal.x) + abs(cell.y - self.goal.y)

    # Calculate heuristics
    def calculate_heuristics_chebyshev(self, cell):
        return max(abs(cell.x - self.goal.x), abs(cell.y - self.goal.y))

    # Generates a cell class object based on x, y
    def check_cell(self, x, y):
        return self.cells[x * self.height + y]

    # Generates adjacent cells
    def get_adjacent_cells(self, cell, diagonal):
        cells = []

        space_available_right = cell.x < self.width-1
        space_available_left = cell.x > 0
        space_available_down = cell.y > 0
        space_available_up = cell.y < self.height-1

        if space_available_right:
            cells.append(self.check_cell(cell.x+1, cell.y))
        if space_available_left:
            cells.append(self.check_cell(cell.x-1, cell.y))
        if space_available_down:
            cells.append(self.check_cell(cell.x, cell.y-1))
        if space_available_up:
            cells.append(self.check_cell(cell.x, cell.y+1))
        if diagonal:
            if space_available_up and space_available_right:
                cells.append(self.check_cell(cell.x+1, cell.y+1))
            if space_available_down and space_available_right:
                cells.append(self.check_cell(cell.x+1, cell.y-1))
            if space_available_up and space_available_left:
                cells.append(self.check_cell(cell.x-1, cell.y+1))
            if space_available_down and space_available_left:
                cells.append(self.check_cell(cell.x-1, cell.y-1))
        return cells

    # Updates the next cells information
    def next_cell(self, current, next_cell, greedy, diagonal):
        if greedy:
            next_cell.g = current.g + (14 if diagonal else 10)
        else:
            next_cell.g = 0

        if diagonal:
            next_cell.h = self.calculate_heuristics_chebyshev(next_cell)
        else:
            next_cell.h = self.calculate_heuristics_manhattan(next_cell)

        next_cell.previous = current
        next_cell.f = next_cell.g + next_cell.h

    # Resets the cell values to run the pathfinding again
    def reset_cells(self):
        for cell in self.cells:
            cell.g = 0
            cell.f = 0
            cell.h = 0
            cell.previous = None

    def solve(self, greedy, diagonal):
        pending = []
        heapq.heapify(pending)
        visited = set()
        heapq.heappush(pending, (self.start.f, self.start))

        # While there are open nodes pending, continue searching
        while len(pending):
            f, cell = heapq.heappop(pending)
            visited.add(cell)

            # If the current cell is the goal, end the while loop
            if cell is self.goal:
                self.generate_path(greedy, diagonal)
                break

            next_cells = self.get_adjacent_cells(cell, diagonal)
            for next_cell in next_cells:
                if next_cell.accessible and next_cell not in visited:
                    if (next_cell.f, next_cell) in pending:
                        if not greedy:
                            if next_cell.g > cell.g + 10:
                                self.next_cell(cell, next_cell, greedy, diagonal)
                    else:
                        self.next_cell(cell, next_cell, greedy, diagonal)
                        heapq.heappush(pending, (next_cell.f, next_cell))

    # Get the calculated path
    def generate_path(self, greedy, diagonal):
        cell = self.goal
        path = [(cell.x, cell.y)]
        while cell.previous is not self.start:
            cell = cell.previous
            path.append((cell.x, cell.y))
        path.append((self.start.x, self.start.y))
        path.reverse()
        self.create_solution(path, greedy, diagonal, len(path))
        return path

    # Create output file
    def create_solution(self, path, greedy, diagonal, moves):
        # Remove the start and end point from the path (preserves S and G when replacing)
        solved_maze = []
        trim_result = path[1:len(path)-1]
        if greedy:
            title = 'Greedy: '+str(moves)+' movements'
        else:
            title = 'A*: '+str(moves)+' movements'
        for y in range(self.height):
            new_line = ''
            for x in range(self.width):
                if (x, y) in trim_result:
                    new_line += 'P'
                else:
                    new_line += self.maze[y][x][0]
            solved_maze.append(new_line)
        if diagonal:
            if greedy:
                output = open('pathfinding_b_out.txt', 'w')
            else:
                output = open('pathfinding_b_out.txt', 'a')
        else:
            if greedy:
                output = open('pathfinding_a_out.txt', 'w')
            else:
                output = open('pathfinding_a_out.txt', 'a')
        output.write(title)
        output.write('\n')
        for line in solved_maze:
            output.write(line)
            output.write('\n')
        output.close()
        return solved_maze


# Runs the class based on txt file
PathFinder('pathfinding_a.txt')
