# Optimised build order by stride

from brick import *
import math

class StrideOptimiser:
    def __init__(self, wall_map, wall_width_mm, wall_height_mm):
        self.wall_map = wall_map
        self.wall_width_mm = wall_width_mm
        self.wall_height_mm = wall_height_mm
        self.stride_width = 800
        self.stride_height = 1300
        self.course_height = COURSE_HEIGHT
        self.assign_strides()

    def assign_strides(self):
        stride_id = 1
        total_rows = len(self.wall_map)
        courses_per_stride = int(self.stride_height // self.course_height)
        bricks_per_stride = int(self.stride_width // (BRICK_LENGTH + HEAD_JOINT))

        for start_row in range(0, total_rows, courses_per_stride):
            end_row = min(start_row + courses_per_stride, total_rows)
            for row_idx in range(start_row, end_row):
                row = self.wall_map[row_idx]
                cumulative_length = 0
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
        """Returns a list of brick references in optimised build order"""
        bricks_in_order = []
        stride_blocks = {}

        for row in self.wall_map:
            for brick in row:
                sid = brick.get("stride", "S0_0")
                if sid not in stride_blocks:
                    stride_blocks[sid] = []
                stride_blocks[sid].append(brick)

        # Build each stride one after another
        for stride_id in sorted(stride_blocks.keys()):
            bricks_in_order.extend(stride_blocks[stride_id])

        return bricks_in_order
