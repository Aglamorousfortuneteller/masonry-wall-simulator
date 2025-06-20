# wall.py — Wall generation and visualisation with different bond types

from ansi_colors import STRIDE_COLOR_PAIRS, RESET
from brick import (
    BRICK_LENGTH, HALF_BRICK_LENGTH, HEAD_JOINT,
    FULL_BRICK_CHAR, HALF_BRICK_CHAR,
    BUILT_FULL_CHAR, BUILT_HALF_CHAR,
    BUILT_FRONT_CHAR, FRONT_BRICK_CHAR,
)
import random

class Wall:
    def __init__(self, num_rows=None, bond_type="stretcher"):
        # Basic geometry definitions
        self.brick_length = BRICK_LENGTH
        self.head_joint = HEAD_JOINT
        self.course_height = 62.5
        self.wall_width = 2300  # total wall width in mm

        # Determine number of rows by height if not specified
        self.rows = num_rows if num_rows is not None else int(2000 // self.course_height)
        self.wall_height = self.rows * self.course_height
        self.brick_row_length = self.wall_width
        self.bond_type = bond_type

        # Generate wall map based on bond type
        if bond_type == "flemish":
            self.wall_map = self._generate_flemish_bond()
        elif bond_type == "wild":
            self.wall_map = self._generate_wild_bond()
        else:
            self.wall_map = self._generate_stretcher_bond()

    def _generate_stretcher_bond(self):
        """
        Standard brick pattern with alternating half-brick offsets per row.
        """
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

            # Optionally add trailing half-brick if it fits
            if row % 2 == 1 and remaining >= HALF_BRICK_LENGTH:
                course.append({"type": "half", "built": False})

            wall_map.append(course)
        return wall_map

    def _generate_flemish_bond(self):
        """
        Alternates between full bricks and headers ("front" bricks),
        staggered every row like Flemish bond.
        """
        wall_map = []
        for row_index in range(self.rows):
            course = []
            current_pos = 0

            # Alternate offset for even/odd rows
            offset = HALF_BRICK_LENGTH + HEAD_JOINT if row_index % 2 == 1 else 0
            if offset > 0:
                course.append({"type": "half", "built": False})
                current_pos += offset

            # Alternate between stretcher and header
            while current_pos + BRICK_LENGTH + HEAD_JOINT <= self.brick_row_length:
                if (len(course) + row_index) % 2 == 0:
                    course.append({"type": "full", "built": False})
                    current_pos += BRICK_LENGTH + HEAD_JOINT
                else:
                    course.append({"type": "front", "built": False})
                    current_pos += HALF_BRICK_LENGTH + HEAD_JOINT

            # Add any trailing brick if fits
            remaining = self.brick_row_length - current_pos
            if remaining >= BRICK_LENGTH:
                course.append({"type": "full", "built": False})
            elif remaining >= HALF_BRICK_LENGTH:
                course.append({"type": "half", "built": False})

            wall_map.append(course)
        return wall_map

    def _generate_wild_bond(self):
        """
        Randomised pattern per row with varying start gaps, offsets, and brick combinations.
        """
        wall_map = []
        previous_offset = -1

        for row in range(self.rows):
            course = []

            # Select a gap offset different from the last one
            allowed_offsets = [i for i in [0, 1, 3] if i != previous_offset]
            offset = random.choice(allowed_offsets)
            previous_offset = offset

            # Add initial gap to simulate physical offset (rendered as whitespace)
            course.append({"type": "gap", "length": offset, "built": True})

            # Optional brick offset (half brick on odd rows, 50/50 chance)
            use_offset = row % 2 == 1 and random.choice([True, False])
            offset = HALF_BRICK_LENGTH + HEAD_JOINT if use_offset else 0
            current_pos = offset
            last_type = "half" if use_offset else None

            if use_offset:
                course.append({"type": "half", "built": False})
                current_pos += HALF_BRICK_LENGTH + HEAD_JOINT

            # Fill the rest of the row randomly with full or half bricks
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
        """
        Marks the next unbuilt brick as 'built'. Used in simulation mode.
        """
        for row in self.wall_map:
            for brick in row:
                if not brick["built"]:
                    brick["built"] = True
                    return True
        return False

    def display(self, colour_by_stride=False):
        """
        Displays the current wall state in terminal.
        If colour_by_stride is enabled, assigns alternating colours to built bricks by stride.
        """
        output = ""
        stride_color_map = {}

        # Print wall from top to bottom
        for row in reversed(self.wall_map):
            line = ""
            stride_counters = {}

            for brick in row:
                # Get character for brick based on type and built state
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

                # Apply stride-based ANSI colour if enabled and brick is built
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

                line += char + ""
            output += line.rstrip("") + "\n"

        print(output)
