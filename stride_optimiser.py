# stride_optimiser.py - Optimised build order by stride

from brick import *
from robot_config import *

class StrideOptimiser:
    def __init__(self, wall_map, wall_width_mm, wall_height_mm):
        self.wall_map = wall_map
        self.wall_width_mm = wall_width_mm
        self.wall_height_mm = wall_height_mm
        self.stride_width = MAX_STRIDE_WIDTH_MM  # was hardcoded 800
        self.stride_height = MAX_STRIDE_HEIGHT_MM  # was hardcoded 1300
        self.course_height = COURSE_HEIGHT
        self.assign_strides()

    def assign_strides(self):
        stride_id = 1
        total_rows = len(self.wall_map)
        courses_per_stride = int(self.stride_height // self.course_height)
        min_remaining = HALF_BRICK_LENGTH  # minimum space we want to avoid leaving unused

        for start_row in range(0, total_rows, courses_per_stride):
            end_row = min(start_row + courses_per_stride, total_rows)
            for row_idx in range(start_row, end_row):
                row = self.wall_map[row_idx]
                current_stride = 1
                cumulative_length = 0

                i = 0
                if row and row[0]["type"] == "gap":
                    row[0]["stride"] = "GAP"
                    cumulative_length = row[0]["length"]
                    i = 1

                bricks = row[i:]
                j = 0
                while j < len(bricks):
                    brick = bricks[j]
                    brick_len = BRICK_LENGTH if brick["type"] == "full" else HALF_BRICK_LENGTH

                    # --- Lookahead: check next brick if exists ---
                    next_len = 0
                    if j + 1 < len(bricks):
                        next_type = bricks[j + 1]["type"]
                        next_len = BRICK_LENGTH if next_type == "full" else HALF_BRICK_LENGTH

                    remaining_space = self.stride_width - cumulative_length
                    if (remaining_space < brick_len) or \
                    (remaining_space - brick_len < min_remaining and next_len > 0):
                        current_stride += 1
                        cumulative_length = 0

                    brick["stride"] = f"S{stride_id}_{current_stride}"
                    cumulative_length += brick_len + HEAD_JOINT
                    j += 1

            stride_id += 1


    def get_stride_order(self):
        bricks_in_order = []
        stride_blocks = {}

        for row in self.wall_map:
            for brick in row:
                sid = brick.get("stride", "S0_0")
                if sid not in stride_blocks:
                    stride_blocks[sid] = []
                stride_blocks[sid].append(brick)

        for stride_id in sorted(stride_blocks.keys()):
            bricks_in_order.extend(stride_blocks[stride_id])

        return bricks_in_order

    def get_stride_metrics(self):
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
        total_bricks = sum(len(row) for row in self.wall_map)
        total_strides = len(set(b["stride"] for row in self.wall_map for b in row))
        vertical_blocks = int(self.wall_height_mm // self.stride_height)
        rows = len(self.wall_map)

        # Placement and vertical movement time
        time = (
            total_bricks * BRICK_PLACEMENT_TIME +
            vertical_blocks * VERTICAL_MOVE_TIME
        )

        # Movement time and energy
        if mode == "stride":
            movement_time = total_strides * HORIZONTAL_MOVE_TIME
            movement_energy = total_strides * MOVE_ENERGY_KWH
        elif mode == "sequential":
            movement_time = rows * 2 * HORIZONTAL_MOVE_TIME  # one L–R–L per row
            movement_energy = rows * 2 * MOVE_ENERGY_KWH
        else:
            raise ValueError("Invalid mode: use 'stride' or 'sequential'")

        time += movement_time
        energy = time * ENERGY_PER_SECOND + movement_energy

        return time, energy
