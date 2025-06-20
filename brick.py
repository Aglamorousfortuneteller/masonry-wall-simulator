# brick.py

# === Brick and Joint Dimension Definitions ===

# Standard brick dimensions (in millimetres)
BRICK_LENGTH = 210         # Full brick length
BRICK_HEIGHT = 50          # Brick height
BRICK_WIDTH = 100          # Brick depth (not used in 2D view)

# Special brick lengths
HALF_BRICK_LENGTH = 100    # Used in staggered or Flemish patterns
FRONT_BRICK_LENGTH = 105   # Used in Flemish bond for the 'front' brick (visual distinction)

# Mortar joint sizes
HEAD_JOINT = 10            # Horizontal mortar gap between bricks
BED_JOINT = 12.5           # Vertical mortar gap between courses

# Full vertical course height (brick + mortar)
COURSE_HEIGHT = BRICK_HEIGHT + BED_JOINT  # 62.5 mm

# === ASCII Characters Used for Visualisation ===

# Symbols for unbuilt bricks

FULL_BRICK_CHAR = "░░░░"   # Represents a standard full brick

HALF_BRICK_CHAR = "░░"     # Represents a half brick

# Symbols for built (placed) bricks

BUILT_FULL_CHAR = "▓▓▓▓"   # Full brick after placement

BUILT_HALF_CHAR = "▓▓"     # Half brick after placement



# === Flemish Bond Brick Characters ===
# Special brick type for Flemish bond — 'front' bricks for visual variation

FRONT_BRICK_CHAR = "░░░"       # Represents a front-facing brick (not full length)

BUILT_FRONT_CHAR = "▓▓▓"       # Same brick after being built
