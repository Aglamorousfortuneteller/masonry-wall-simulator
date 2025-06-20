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

        for start_row in range(0, total_rows, courses_per_stride):
            end_row = min(start_row + courses_per_stride, total_rows)
            for row_idx in range(start_row, end_row):
                row = self.wall_map[row_idx]
                offset = HALF_BRICK_LENGTH + HEAD_JOINT if row_idx % 2 == 1 else 0
                cumulative_length = offset
                current_stride = 1
                for brick in row:
                    brick_len = BRICK_LENGTH if brick["type"] == "full" else HALF_BRICK_LENGTH
                    if cumulative_length + brick_len > self.stride_width:
                        current_stride += 1
                        cumulative_length = 0
                    brick["stride"] = f"S{stride_id}_{current_stride}"
                    cumulative_length += brick_len + HEAD_JOINT
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

    def estimate_time_and_energy(self):
        total_bricks = sum(len(row) for row in self.wall_map)
        total_strides = len(set(b["stride"] for row in self.wall_map for b in row))
        vertical_blocks = int(self.wall_height_mm // self.stride_height)

        time = (total_bricks * BRICK_PLACEMENT_TIME +
                total_strides * HORIZONTAL_MOVE_TIME +
                vertical_blocks * VERTICAL_MOVE_TIME)

        energy = time * ENERGY_PER_SECOND
        return time, energy
