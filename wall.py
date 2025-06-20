# wall.py

from ansi_colors import STRIDE_COLORS, RESET
from brick import BRICK_LENGTH, HALF_BRICK_LENGTH, HEAD_JOINT, FULL_BRICK_CHAR, HALF_BRICK_CHAR, BUILT_FULL_CHAR, BUILT_HALF_CHAR
import random

class Wall:
    def __init__(self, num_rows=None, bond_type="stretcher"):
        self.brick_length = BRICK_LENGTH
        self.head_joint = HEAD_JOINT
        self.course_height = 62.5
        self.wall_width = 2300

        self.rows = num_rows if num_rows is not None else int(2000 // self.course_height)
        self.wall_height = self.rows * self.course_height
        self.brick_row_length = self.wall_width
        self.bond_type = bond_type

        if bond_type == "flemish":
            self.wall_map = self._generate_flemish_bond()
        elif bond_type == "wild":
            self.wall_map = self._generate_wild_bond()
        else:
            self.wall_map = self._generate_stretcher_bond()

    def _generate_stretcher_bond(self):
        wall_map = []
        for row in range(self.rows):
            course = []
            offset = HALF_BRICK_LENGTH + HEAD_JOINT if row % 2 == 1 else 0
            remaining = self.brick_row_length - offset

            if offset > 0:
                course.append({"type": "half", "built": False})

            while remaining >= BRICK_LENGTH + HEAD_JOINT:
                course.append({"type": "full", "built": False})
                remaining -= (BRICK_LENGTH + HEAD_JOINT)

            # Optional trailing half-brick if space left
            if row % 2 == 1 and remaining >= HALF_BRICK_LENGTH:
                course.append({"type": "half", "built": False})

            wall_map.append(course)
        return wall_map

    def _generate_flemish_bond(self):
        wall_map = []
        for row in range(self.rows):
            course = []
            flip = row % 2  # alternate pattern
            remaining = self.brick_row_length

            while remaining >= HALF_BRICK_LENGTH + HEAD_JOINT:
                if flip == 0:
                    # Full → Half
                    if remaining >= BRICK_LENGTH + HEAD_JOINT:
                        course.append({"type": "full", "built": False})
                        remaining -= BRICK_LENGTH + HEAD_JOINT
                    if remaining >= HALF_BRICK_LENGTH + HEAD_JOINT:
                        course.append({"type": "half", "built": False})
                        remaining -= HALF_BRICK_LENGTH + HEAD_JOINT
                else:
                    # Half → Full
                    if remaining >= HALF_BRICK_LENGTH + HEAD_JOINT:
                        course.append({"type": "half", "built": False})
                        remaining -= HALF_BRICK_LENGTH + HEAD_JOINT
                    if remaining >= BRICK_LENGTH + HEAD_JOINT:
                        course.append({"type": "full", "built": False})
                        remaining -= BRICK_LENGTH + HEAD_JOINT

            wall_map.append(course)
        return wall_map

    def _generate_wild_bond(self):
        wall_map = []
        joint_positions_prev = set()

        for row_index in range(self.rows):
            course = []
            remaining = self.brick_row_length
            current_pos = 0
            joint_positions = set()

            while remaining >= HALF_BRICK_LENGTH:
                brick_type = random.choice(["full", "half"])

                if brick_type == "full" and remaining >= BRICK_LENGTH + HEAD_JOINT:
                    brick_len = BRICK_LENGTH
                elif brick_type == "half" and remaining >= HALF_BRICK_LENGTH + HEAD_JOINT:
                    brick_len = HALF_BRICK_LENGTH
                else:
                    break

                if current_pos in joint_positions_prev:
                    if remaining >= HALF_BRICK_LENGTH + HEAD_JOINT:
                        brick_len = HALF_BRICK_LENGTH
                        brick_type = "half"
                    else:
                        break

                course.append({"type": brick_type, "built": False})
                current_pos += brick_len + HEAD_JOINT
                joint_positions.add(current_pos)
                remaining = self.brick_row_length - current_pos

            wall_map.append(course)
            joint_positions_prev = joint_positions

        return wall_map

    def mark_next_brick_built(self):
        for row in self.wall_map:
            for brick in row:
                if not brick["built"]:
                    brick["built"] = True
                    return True
        return False

    def display(self, colour_by_stride=False):
        output = ""
        for row in reversed(self.wall_map):
            line = ""
            for brick in row:
                if brick["type"] == "full":
                    char = BUILT_FULL_CHAR if brick["built"] else FULL_BRICK_CHAR
                else:
                    char = BUILT_HALF_CHAR if brick["built"] else HALF_BRICK_CHAR

                if colour_by_stride and brick["built"]:
                    stride = brick.get("stride", "S0_0")
                    stride_id = hash(stride) % len(STRIDE_COLORS)
                    char = f"{STRIDE_COLORS[stride_id]}{char}{RESET}"

                line += char + "\u200A"  # hair space between bricks
            output += line.strip() + "\n"
        print(output)
