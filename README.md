# Masonry Wall Quest Simulator

A retro-styled terminal quest simulator for robotic masonry wall construction. This program simulates the placement of bricks using various bond patterns and two construction methods: sequential and stride-optimised.

## Features

- **Bond Types**:
  - **Stretcher Bond**: Simple alternating rows of full bricks with half-brick offset every second row.
  - **Flemish Bond** (Bonus A): Alternating headers and stretchers, introducing a special "front" brick orientation for visual differentiation.
  - **Wild Bond** (Bonus B): Randomised placement using full and half bricks. Uses an `"offset"` property per row to avoid vertical joint alignment.

- **Construction Methods**:
  - **Sequential Mode**: Bricks placed row-by-row, simulating human-like progress. Can run interactively or with auto-advance.
  - **Stride-Optimised Mode**: Groups bricks into efficient build chunks (“strides”) for robot execution, accounting for vertical reach and workspace.

- **Visualisation**:
  - Retro terminal-style display using ASCII and ANSI colour codes.
  - Full stride annotation for build order.
  - Optional automatic build simulation with animations.

- **Performance Estimation**:
  - Calculates estimated time and energy (kWh) based on brick placement and robot movement:
    - Stride mode: based on stride count and vertical movement.
    - Sequential mode: assumes back-and-forth motion per row.
  - Parameters customisable in robot_config.py.

## Technical Notes (Relaxations & Assumptions)

- Max recommended wall height is **20 rows**, due to robot arm limitations.
    - Reason: Limited by the vertical reach of the robot arm. If height exceeds the configured stride height (e.g. 600 mm), the wall must be split into multiple vertical blocks (strides). Exceeding this makes continuous vertical building impractical for a fixed-position robotic system.
- Flemish Bond: front Brick Orientation
    - The front brick visually marks stretchers to differentiate from headers. This distinction replaces what was otherwise a visual styling in the assignment example images (which couldn't be accessed). Functional logic is preserved: alternating half and full bricks simulate the Flemish pattern. Front bricks don't change stride logic but help with terminal display fidelity.
- Wild bond introduces row-level "offset" property. Offset is chosen randomly (but constrained) to avoid vertical joint alignment, ensuring structural realism.
  - Reason for floating bricks or cut-offs: Because offsets and random combinations of full/half bricks can’t always cleanly fit the stride width, some bricks may visually “float” at the edge of a stride. These represent realistic edge conditions in irregular wall layouts and are expected in wild bond builds.

- Energy is calculated as:
  - **Stride Mode**: `time * energy/sec + strides * move_energy`
  - **Sequential Mode**: `time * energy/sec + 2 * rows * move_energy`
- Brick placement times and energy costs are configurable via `robot_config.py`.
- Brick stride assignment is handled in `stride_optimiser.py`, adjusted per bond type.

## Bond-Specific Logic

### Flemish Bond
- Introduces a new `"front"` brick type, which affects visual appearance.
- If examples were not opening from the assignment, default logic applies alternating full/half brick structure.

### Wild Bond
- Supports `"offset"` parameter to simulate randomness.
- Special logic avoids vertical joint alignment between rows.
- May leave trailing or floating bricks at stride edges—these are intentional for the 'wild' effect.

## How to Run

```bash
python main.py
```
Then follow the terminal prompts:

Choose bond type:
[1] Stretcher
[2] Flemis
[3] Wild 

Choose build method:
[1] Manual (Sequential)
[2] Robot (Stride-Optimised)

Enable or disable auto-build mode.

Set wall height in rows.


## File Overview

- `main.py`: Runs the simulation and UI flow.
- `wall.py`: Manages the wall structure.
- `brick.py`: Defines brick properties and dimensions.
- `stride_optimiser.py`: Assigns and evaluates stride-based build optimisation.
- `robot_config.py`: Constants related to robot arm limits and energy use.
- `ansi_colors.py`: Terminal colour constants for pretty retro visuals.