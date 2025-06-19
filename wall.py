# Wall generation and visualisation (stretcher bond)

from brick import *

class Wall:
    def __init__(self, num_rows=None):
        self.brick_length = 210
        self.head_joint = 10
        self.course_height = 62.5
        self.wall_width = 2300

        self.rows = num_rows if num_rows is not None else int(2000 // self.course_height)
        self.wall_height = self.rows * self.course_height
        self.brick_row_length = self.wall_width
        self.wall_map = self._generate_stretcher_bond()



    def _generate_stretcher_bond(self):
        wall_map = []
        for row in range(self.rows):
            course = []
            offset = HALF_BRICK_LENGTH + HEAD_JOINT if row % 2 == 1 else 0
            remaining = self.brick_row_length - offset
            if row % 2 == 1:
                course.append({"type": "half", "built": False})

            while remaining >= BRICK_LENGTH + HEAD_JOINT:
                course.append({"type": "full", "built": False})
                remaining -= (BRICK_LENGTH + HEAD_JOINT)

            if offset > 0:
                course.append({"type": "half", "built": False})
            wall_map.append(course)
        return wall_map

    def mark_next_brick_built(self):
        for row in self.wall_map:
            for brick in row:
                if not brick["built"]:
                    brick["built"] = True
                    return True
        return False  # all built

    def display(self):
        output = ""
        for row in reversed(self.wall_map):
            line = ""
            for brick in row:
                if brick["type"] == "full":
                    char = BUILT_FULL_CHAR if brick["built"] else FULL_BRICK_CHAR
                else:
                    char = BUILT_HALF_CHAR if brick["built"] else HALF_BRICK_CHAR
                line += char + "\u200A"
            output += line.strip() + "\n"
        print(output)
