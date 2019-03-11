import heapq


# Cell Class (points on grid)
class Cell:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y

        self.value = value
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
        self.x_len = 0
        self.y_len = 0

        self.pending = []
        heapq.heapify(self.pending)
        self.visited = set()

        self.start = None
        self.goal = None
        self.maze = []
        self.cells = []
        self.file = file

        self.read_file()
        if self.find_endpoints():
            self.solve()

    # Reads file
    def read_file(self):
        with open(self.file, 'r') as f:
            self.maze = [line.strip() for line in f]
        self.x_len = len(self.maze[0])
        self.y_len = len(self.maze)
        print(self.maze)

    # Gets start and goal points, saves to class data
    def find_endpoints(self):
        for row in range(0, self.y_len):
            for col in range(0, self.x_len):
                if self.maze[row][col].lower() == 's':
                    self.start = self.check_cell(col, row)
                elif self.maze[row][col].lower() == 'g':
                    self.goal = self.check_cell(col, row)

        # Check for success
        try:
            if self.start.value.lower() == 's':
                if self.goal.value.lower() == 'g':
                    return True
        except KeyError:
            print('Start location not found')
            return False

    # Does not account for obstacles
    def calculate_heuristics(self, cell):
        return abs(cell.x - self.goal.x) + abs(cell.y - self.goal.y)

    # Generates a cell class object based on x, y
    def check_cell(self, x, y):
        return Cell(x, y, self.maze[y][x])

    # Generates adjacent cells
    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x < self.x_len-1:
            cells.append(self.check_cell(cell.x+1, cell.y))
        if cell.x < 0:
            cells.append(self.check_cell(cell.x-1, cell.y))
        if cell.y > 0:
            cells.append(self.check_cell(cell.x, cell.y-1))
        if cell.y < self.y_len-1:
            cells.append(self.check_cell(cell.x, cell.y+1))
        return cells

    # Get the calculated path
    def display_path(self):
        cell = self.goal
        while cell.parent is not self.start:
            cell = cell.previous
            print('Cell Path: x:{0}, y:{1}'.format(cell.x, cell.y))

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
                if next_cell.value == '_' and next_cell not in self.visited:
                    if (next_cell.f, next_cell) in self.pending:
                        if next_cell.g > cell.g + 10:
                            self.next_cell(cell, next_cell)
                    else:
                        self.next_cell(cell, next_cell)
                        heapq.heappush(self.pending, (next_cell.f, next_cell))

# Runs the class based on txt file
PathFinder('maze.txt')
