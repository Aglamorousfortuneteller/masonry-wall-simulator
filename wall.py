# wall.py

from ansi_colors import STRIDE_COLOR_PAIRS, RESET
from brick import BRICK_LENGTH, HALF_BRICK_LENGTH, HEAD_JOINT, FULL_BRICK_CHAR, HALF_BRICK_CHAR, BUILT_FULL_CHAR, BUILT_HALF_CHAR, BUILT_FRONT_CHAR, FRONT_BRICK_CHAR, FRONT_BRICK_LENGTH
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
        for row_index in range(self.rows):
            course = []
            current_pos = 0

            # Odd rows start with full brick, even rows start with half brick
            offset = HALF_BRICK_LENGTH + HEAD_JOINT if row_index % 2 == 1 else 0
            if offset > 0:
                course.append({"type": "half", "built": False})
                current_pos += offset

            while current_pos + BRICK_LENGTH + HEAD_JOINT <= self.brick_row_length:
                # Alternate: stretcher (full) and header (front-facing)
                if (len(course) + row_index) % 2 == 0:
                    course.append({"type": "full", "built": False})  # stretcher
                    current_pos += BRICK_LENGTH + HEAD_JOINT
                else:
                    course.append({"type": "front", "built": False})  # header
                    current_pos += HALF_BRICK_LENGTH + HEAD_JOINT

            # Optionally add trailing brick
            remaining = self.brick_row_length - current_pos
            if remaining >= BRICK_LENGTH:
                course.append({"type": "full", "built": False})
            elif remaining >= HALF_BRICK_LENGTH:
                course.append({"type": "half", "built": False})

            wall_map.append(course)

        return wall_map



    def _generate_wild_bond(self):
        wall_map = []
        previous_offset = -1

        for row in range(self.rows):
            course = []
            allowed_offsets = [i for i in [0,1,3] if i != previous_offset]

            offset = random.choice(allowed_offsets)
            previous_offset = offset
            course.append({"type": "gap", "length": offset, "built": True})
            # --- PHYSICAL OFFSET LOGIC ---
            use_offset = row % 2 == 1 and random.choice([True, False])
            offset = HALF_BRICK_LENGTH + HEAD_JOINT if use_offset else 0
            current_pos = offset
            last_type = "half" if use_offset else None

            if use_offset:
                course.append({"type": "half", "built": False})
                current_pos += HALF_BRICK_LENGTH + HEAD_JOINT
            # --- BRICK PLACEMENT ---
            while current_pos + HALF_BRICK_LENGTH <= self.brick_row_length:
                options = []
                if current_pos + BRICK_LENGTH <= self.brick_row_length:
                    options.append(("full", BRICK_LENGTH))
                if current_pos + HALF_BRICK_LENGTH <= self.brick_row_length and last_type != "half":
                    options.append(("half", HALF_BRICK_LENGTH))
                if not options:
                    break
                typ, ln = random.choice(options)
                course.append({"type": typ, "built": False})
                current_pos += ln + HEAD_JOINT
                last_type = typ
            wall_map.append(course)
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
        stride_color_map = {}  # stride_id → (color1, color2)

        for row in reversed(self.wall_map):
            line = ""
            stride_counters = {}  # stride_id → brick count within that stride

            for brick in row:
                # Determine character by brick type
                if brick["type"] == "full":
                    char = BUILT_FULL_CHAR if brick.get("built", False) else FULL_BRICK_CHAR
                elif brick["type"] == "half":
                    char = BUILT_HALF_CHAR if brick.get("built", False) else HALF_BRICK_CHAR
                elif brick["type"] == "front":
                    char = BUILT_FRONT_CHAR if brick.get("built", False) else FRONT_BRICK_CHAR
                elif brick["type"] == "gap":
                    gap_len = brick.get("length", 1)
                    char = " " * gap_len

                else:
                    char = "????"

                # Apply stride-based colouring if enabled and brick is built
                if colour_by_stride and brick.get("built", False) and brick["type"] != "gap":
                    stride = brick.get("stride", "S0_0")
                    stride_id = brick.get("stride_id", hash(stride))

                    if stride_id not in stride_color_map:
                        pair_index = len(stride_color_map) % len(STRIDE_COLOR_PAIRS)
                        stride_color_map[stride_id] = STRIDE_COLOR_PAIRS[pair_index]

                    color1, color2 = stride_color_map[stride_id]
                    count = stride_counters.get(stride_id, 0)
                    color = color1 if count % 2 == 0 else color2
                    stride_counters[stride_id] = count + 1

                    char = f"{color}{char}{RESET}"

                line += char+""
            output += line.rstrip("") + "\n"

        print(output)
