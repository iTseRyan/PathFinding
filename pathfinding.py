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
    def __init__(self, file):
        self.width = 0
        self.height = 0

        self.pending = []
        heapq.heapify(self.pending)
        self.visited = set()

        self.start = None
        self.goal = None

        self.maze = []
        self.cells = []

        self.file = file

        self.read_file()
        self.create_grid()

        # self.start_time = time.time()
        # self.end_time = 0
        self.solve()
        # self.print_runtime()

    # Prints runtime
    # def print_runtime(self):
    #     self.end_time = time.time()
    #     print(self.end_time - self.start_time)
    #     hours, rem = divmod(self.end_time - self.start_time, 3600)
    #     minutes, seconds = divmod(rem, 60)
    #     print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

    # Reads file
    def read_file(self):
        with open(self.file, 'r') as f:
            self.maze = [line.strip() for line in f]
        self.width = len(self.maze[0])
        self.height = len(self.maze)
        print(self.maze)

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

    # Does not account for obstacles
    def calculate_heuristics(self, cell):
        return abs(cell.x - self.goal.x) + abs(cell.y - self.goal.y)

    # Generates a cell class object based on x, y
    def check_cell(self, x, y):
        return self.cells[x * self.height + y]

    # Generates adjacent cells
    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x < self.width-1:
            cells.append(self.check_cell(cell.x+1, cell.y))
        if cell.x > 0:
            cells.append(self.check_cell(cell.x-1, cell.y))
        if cell.y > 0:
            cells.append(self.check_cell(cell.x, cell.y-1))
        if cell.y < self.height-1:
            cells.append(self.check_cell(cell.x, cell.y+1))
        return cells

    # Get the calculated path
    def display_path(self):
        cell = self.goal
        path = [(cell.x, cell.y)]
        while cell.previous is not self.start:
            cell = cell.previous
            path.append((cell.x, cell.y))
        path.append((self.start.x, self.start.y))
        path.reverse()
        print(path)
        return path

    # Updates the next cells information
    def next_cell(self, current, next_cell):
        next_cell.g = current.g + 10
        next_cell.h = self.calculate_heuristics(next_cell)
        next_cell.previous = current
        next_cell.f = next_cell.g + next_cell.h

    def solve(self):
        heapq.heappush(self.pending, (self.start.f, self.start))
        while len(self.pending):
            f, cell = heapq.heappop(self.pending)
            self.visited.add(cell)
            if cell is self.goal:
                self.display_path()
                break
            next_cells = self.get_adjacent_cells(cell)
            for next_cell in next_cells:
                if next_cell.accessible and next_cell not in self.visited:
                    if (next_cell.f, next_cell) in self.pending:
                        if next_cell.g > cell.g + 10:
                            self.next_cell(cell, next_cell)
                    else:
                        self.next_cell(cell, next_cell)
                        heapq.heappush(self.pending, (next_cell.f, next_cell))


# Runs the class based on txt file
PathFinder('maze.txt')
