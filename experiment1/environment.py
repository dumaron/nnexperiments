class Environment:
    def __init__(self, rows, columns):
        self.clean = 2
        self.dirt = 0
        self.robot = 1
        self.map = []
        self.rows = rows
        self.columns = columns
        self.robotX = 0
        self.robotY = 0

        for i in range(0, rows):
            row = []
            for j in range(0, columns):
                row.append(self.dirt)
            self.map.append(row)

        self.map[self.robotX][self.robotY] = self.robot

    def move(self, direction):
        if direction == 'none':
            return False

        movement_x = 0
        movement_y = 0

        if direction == 'top':
            movement_y = -1
        elif direction == 'bottom':
            movement_y = 1
        elif direction == 'left':
            movement_x = -1
        elif direction == 'right':
            movement_x = 1

        if 0 <= self.robotX + movement_x < self.columns and 0 <= self.robotY + movement_y < self.rows:
            self.map[self.robotX][self.robotX] = self.clean
            self.robotX += movement_x
            self.robotY += movement_y
            self.map[self.robotX][self.robotY] = self.robot
            return True
        else:
            return False

    def get_signals(self):
        return [cell for row in self.map for cell in row]
