# stride_optimiser.py - Optimised build order by stride

from brick import *
from robot_config import *

class StrideOptimiser:
    def __init__(self, wall_map, wall_width_mm, wall_height_mm):
        self.wall_map = wall_map
        self.wall_width_mm = wall_width_mm
        self.wall_height_mm = wall_height_mm
        self.stride_width = MAX_STRIDE_WIDTH_MM   # Horizontal limit per robot stride
        self.stride_height = MAX_STRIDE_HEIGHT_MM # Vertical limit per robot stride
        self.course_height = COURSE_HEIGHT        # Height per row (brick + joint)
        self.assign_strides()                     # Automatically assign strides at init

    def assign_strides(self):
        """
        Assigns a stride ID to each brick depending on its horizontal and vertical group.
        Tries to pack as many bricks as possible into each stride, without exceeding limits.
        """
        stride_id = 1
        total_rows = len(self.wall_map)
        courses_per_stride = int(self.stride_height // self.course_height)
        min_remaining = HALF_BRICK_LENGTH  # Prevent tiny leftover space that breaks flow

        # Iterate over blocks of rows (vertical stride blocks)
        for start_row in range(0, total_rows, courses_per_stride):
            end_row = min(start_row + courses_per_stride, total_rows)
            for row_idx in range(start_row, end_row):
                row = self.wall_map[row_idx]
                current_stride = 1
                cumulative_length = 0

                i = 0
                if row and row[0]["type"] == "gap":
                    # Assign visual offset 'gap' to dummy stride
                    row[0]["stride"] = "GAP"
                    cumulative_length = row[0]["length"]
                    i = 1

                bricks = row[i:]
                j = 0
                while j < len(bricks):
                    brick = bricks[j]
                    brick_len = BRICK_LENGTH if brick["type"] == "full" else HALF_BRICK_LENGTH

                    # Look ahead to see if the next brick will also fit
                    next_len = 0
                    if j + 1 < len(bricks):
                        next_type = bricks[j + 1]["type"]
                        next_len = BRICK_LENGTH if next_type == "full" else HALF_BRICK_LENGTH

                    remaining_space = self.stride_width - cumulative_length

                    # Decide if current brick needs to go into next stride
                    if (remaining_space < brick_len) or \
                    (remaining_space - brick_len < min_remaining and next_len > 0):
                        current_stride += 1
                        cumulative_length = 0

                    # Assign stride label and update length tracker
                    brick["stride"] = f"S{stride_id}_{current_stride}"
                    cumulative_length += brick_len + HEAD_JOINT
                    j += 1

            stride_id += 1

    def get_stride_order(self):
        """
        Returns all bricks ordered by stride label, for optimal build sequence.
        """
        bricks_in_order = []
        stride_blocks = {}

        # Group bricks by their stride ID
        for row in self.wall_map:
            for brick in row:
                sid = brick.get("stride", "S0_0")
                if sid not in stride_blocks:
                    stride_blocks[sid] = []
                stride_blocks[sid].append(brick)

        # Sort strides and flatten into one list
        for stride_id in sorted(stride_blocks.keys()):
            bricks_in_order.extend(stride_blocks[stride_id])

        return bricks_in_order

    def get_stride_metrics(self):
        """
        Returns the number of bricks, number of strides, and average bricks per stride.
        """
        stride_counts = {}
        for row in self.wall_map:
            for brick in row:
                sid = brick["stride"]
                stride_counts.setdefault(sid, 0)
                stride_counts[sid] += 1

        total_bricks = sum(stride_counts.values())
        total_strides = len(stride_counts)
        avg_per_stride = total_bricks / total_strides if total_strides else 0

        return total_bricks, total_strides, avg_per_stride

    def estimate_time_and_energy(self, mode):
        """
        Estimates total build time and energy use for the wall.

        Args:
            mode (str): Either 'stride' or 'sequential'

        Returns:
            Tuple (time in seconds, energy in kWh)
        """
        total_bricks = sum(len(row) for row in self.wall_map)
        total_strides = len(set(b["stride"] for row in self.wall_map for b in row))
        vertical_blocks = int(self.wall_height_mm // self.stride_height)
        rows = len(self.wall_map)

        # Time spent placing bricks and moving vertically
        time = (
            total_bricks * BRICK_PLACEMENT_TIME +
            vertical_blocks * VERTICAL_MOVE_TIME
        )

        # Additional movement time and energy based on mode
        if mode == "stride":
            movement_time = total_strides * HORIZONTAL_MOVE_TIME
            movement_energy = total_strides * MOVE_ENERGY_KWH
        elif mode == "sequential":
            movement_time = rows * 2 * HORIZONTAL_MOVE_TIME  # L–R–L zigzag
            movement_energy = rows * 2 * MOVE_ENERGY_KWH
        else:
            raise ValueError("Invalid mode: use 'stride' or 'sequential'")

        time += movement_time
        energy = time * ENERGY_PER_SECOND + movement_energy

        return time, energy
