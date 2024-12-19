class Solution:
    def __init__(self):
        self.map = []
        self.width = 0
        self.height = 0
        self.bot_row = 0
        self.bot_col = 0
        self.guide = ""

    def process_input(self, input_text):
        sections = input_text.strip().split("\n\n")
        raw_map = sections[0].strip()
        raw_lines = raw_map.split("\n")

        for raw_line in raw_lines:
            line = ""
            for c in raw_line.strip():
                if c == "#":
                    line += "##"
                elif c == ".":
                    line += ".."
                elif c == "O":
                    line += "[]"
                elif c == "@":
                    line += "@."
            self.map.append(list(line))

        self.height = len(self.map)
        self.width = len(self.map[0])
        raw_guide = sections[1].strip()
        self.guide = "".join(segment.strip() for segment in raw_guide.split("\n"))

        for row in range(self.height):
            for col in range(self.width):
                if self.map[row][col] == "@":
                    self.bot_row = row
                    self.bot_col = col
                    return

    def walk(self):
        for direction in self.guide:
            if direction == "^":
                self.walk_vertical(-1)
            elif direction == "v":
                self.walk_vertical(1)
            elif direction == ">":
                self.walk_horizontal(1)
            elif direction == "<":
                self.walk_horizontal(-1)

    def walk_vertical(self, delta_row):
        future_row = self.bot_row + delta_row
        future_spot = self.map[future_row][self.bot_col]

        if future_spot == "#":
            return
        if future_spot == ".":
            self.map[self.bot_row][self.bot_col] = "."
            self.bot_row = future_row
            self.map[self.bot_row][self.bot_col] = "@"
            return

        if not self.may_move_box_vertical(future_row, self.bot_col, delta_row):
            return
        self.move_box_vertical(future_row, self.bot_col, delta_row)
        self.map[self.bot_row][self.bot_col] = "."
        self.bot_row = future_row
        self.map[self.bot_row][self.bot_col] = "@"

    def walk_horizontal(self, delta_col):
        future_col = self.bot_col
        while True:
            future_col += delta_col
            future_spot = self.map[self.bot_row][future_col]
            if future_spot == "#":
                return
            if future_spot == ".":
                break

        while True:
            previous_col = future_col - delta_col
            self.map[self.bot_row][future_col] = self.map[self.bot_row][previous_col]
            future_col = previous_col
            if future_col == self.bot_col:
                break

        self.map[self.bot_row][self.bot_col] = "."
        self.bot_col += delta_col

    def may_move_box_vertical(self, box_row, box_col, delta_row):
        if self.map[box_row][box_col] == "]":
            box_col -= 1
        future_row = box_row + delta_row
        future_spot_left = self.map[future_row][box_col]
        future_spot_right = self.map[future_row][box_col + 1]

        if future_spot_left == "#" or future_spot_right == "#":
            return False
        if future_spot_left in ["[", "]"]:
            if not self.may_move_box_vertical(future_row, box_col, delta_row):
                return False
        if future_spot_right == "[":
            if not self.may_move_box_vertical(future_row, box_col + 1, delta_row):
                return False
        return True

    def move_box_vertical(self, box_row, box_col, delta_row):
        if self.map[box_row][box_col] == "]":
            box_col -= 1
        future_row = box_row + delta_row
        future_spot_left = self.map[future_row][box_col]
        future_spot_right = self.map[future_row][box_col + 1]

        if future_spot_left in ["[", "]"]:
            self.move_box_vertical(future_row, box_col, delta_row)
        if future_spot_right == "[":
            self.move_box_vertical(future_row, box_col + 1, delta_row)

        self.map[box_row][box_col] = "."
        self.map[box_row][box_col + 1] = "."
        self.map[future_row][box_col] = "["
        self.map[future_row][box_col + 1] = "]"

    def count_boxes_gps(self):
        gps = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.map[row][col] == "[":
                    gps += 100 * row + col
        return gps


def main():
    with open("15.txt", "r") as f:
        input_text = f.read()

    solution = Solution()
    solution.process_input(input_text)
    solution.walk()
    result = solution.count_boxes_gps()
    print("Result:", result)


if __name__ == "__main__":
    main()
