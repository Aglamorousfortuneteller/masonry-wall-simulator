# robot_config.py — Robot parameters for time and energy estimation

# === Time Constants (in seconds) ===

BRICK_PLACEMENT_TIME = 2            # Time to place one brick
HORIZONTAL_MOVE_TIME = 10           # Time to move horizontally to next stride
VERTICAL_MOVE_TIME = 15             # Time to move vertically to next stride

# === Energy Consumption Constants ===

ENERGY_PER_SECOND = 0.5             # Continuous energy use while working (in kWh/s)
MOVE_ENERGY_KWH = 0.05              # Discrete energy cost per movement (in kWh)

# === Robot Arm Physical Limitations (in mm) ===

MAX_STRIDE_HEIGHT_MM = 1300         # Max vertical reach of the robot arm (≈20 courses)
MAX_STRIDE_WIDTH_MM = 800           # Max horizontal reach per stride
