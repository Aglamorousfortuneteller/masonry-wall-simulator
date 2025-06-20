# ansi_colors.py

RESET = "\033[0m"

# Define colour pairs with increased contrast: (main_color, alternate_shade)
STRIDE_COLOR_PAIRS = [
    ("\033[38;5;196m", "\033[38;5;88m"),   # Bright Red / Dark Red
    ("\033[38;5;208m", "\033[38;5;130m"),  # Bright Orange / Rust
    ("\033[38;5;226m", "\033[38;5;142m"),  # Yellow / Mustard
    ("\033[38;5;46m",  "\033[38;5;28m"),   # Bright Green / Dark Green
    ("\033[38;5;51m",  "\033[38;5;25m"),   # Bright Cyan / Deep Teal
    ("\033[38;5;99m",  "\033[38;5;54m"),   # Bright Purple / Deep Violet
    ("\033[38;5;213m", "\033[38;5;162m"),  # Light Pink / Magenta
    ("\033[38;5;250m", "\033[38;5;240m"),  # Light Grey / Dark Grey
]
