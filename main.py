# main.py

import time
import os
import sys

# Import core modules of the simulator
from wall import Wall
from stride_optimiser import StrideOptimiser
from robot_config import MAX_STRIDE_HEIGHT_MM, MAX_STRIDE_WIDTH_MM
from brick import COURSE_HEIGHT, BRICK_LENGTH, HEAD_JOINT


# Clears the terminal screen using ANSI escape codes
def clear_screen():
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()


# Simulates retro terminal output with character-by-character delay
def retro_print(text, delay=0.03):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()


# Displays the main title plate of the simulator
def show_banner(animated=False):
    plate = [
        "╔═══════════════════════════════════════════════╗",
        "║          MASONRY WALL QUEST SIMULATOR         ║",
        "╚═══════════════════════════════════════════════╝"
    ]
    clear_screen()
    if animated:
        for line in plate:
            retro_print(line)
        print()
    else:
        print("\n".join(plate) + "\n")


# Displays animated intro text for the player
def show_intro():
    show_banner(animated=True)
    retro_print("┌───────────────────────────────────────────────┐")
    retro_print("│ Welcome, brave builder! Your quest begins...  │")
    retro_print("└───────────────────────────────────────────────┘\n")


# Prompts the user for bond type, build mode, auto-mode, and number of rows
def prompt_settings():
    max_rows = int(MAX_STRIDE_HEIGHT_MM // COURSE_HEIGHT)
    max_bricks = int(MAX_STRIDE_WIDTH_MM // (BRICK_LENGTH + HEAD_JOINT))

    print("Choose bond type:")
    print("  [1] Stretcher bond")
    print("  [2] Flemish bond")
    print("  [3] Wild bond")
    bond_choice = input("Enter choice (1–3): ").strip()

    if bond_choice == "2":
        bond_type = "flemish"
    elif bond_choice == "3":
        bond_type = "wild"
    else:
        bond_type = "stretcher"

    print("\nChoose build method:")
    print("  [1] Sequential (brick-by-brick)")
    print("  [2] Stride-optimised (robot build)")
    method_choice = input("Enter choice (1–2): ").strip()
    use_stride = method_choice == "2"

    print("\nAuto-build mode (for magical speed)? (y/n):")
    auto = input("> ").strip().lower() == "y"

    rows = int(input(f"\nEnter number of wall rows (recommended ≤ {max_rows}): ").strip())
    if rows > max_rows:
        print(f"\n⚠ Robot arm cannot reach above row {max_rows}.")
        print("   The wall will be split into vertical strides automatically.\n")

    return bond_type, use_stride, auto, rows


# Displays the current wall layout with brick placement prompt
def display_wall_with_prompt(wall, auto=False):
    clear_screen()
    print("The top of the wall.")
    wall.display(colour_by_stride=True)
    if not auto:
        print("\n✦ Press ENTER to place a brick. Ctrl+C to flee the quest. ✦\n")


# Displays wall layout during stride-based building, highlighting current stride
def display_wall_stride_prompt(wall, stride_name, auto=False):
    clear_screen()
    print("The top of the wall.")
    wall.display(colour_by_stride=True)
    if not auto:
        print(f"\n✦ Press ENTER to build by stride. Ctrl+C to abandon the quest. (Now building: {stride_name}) ✦\n")


# Shows a summary report with time, energy, and performance grade
def show_efficiency_report(optimiser, mode="stride", delay=0.03):
    total, strides, avg = optimiser.get_stride_metrics()
    total_time, energy = optimiser.estimate_time_and_energy(mode)

    print("\n" + "═" * 51)
    retro_print("           ✦ QUEST COMPLETION SCROLL ✦  ")
    print("═" * 51 + "\n")

    if mode == "sequential":
        # Manual mode – less efficient
        retro_print("You have finished the wall by hand...")
        retro_print("With sweat and tears, each brick was placed.")
        retro_print("But alas... the scroll reveals some truths:\n")
        retro_print(f" ▒ Total Bricks Placed     : {total}")
        retro_print(f" ▒ Number of Strides Taken : — (inefficient)")
        retro_print(f" ▒ Avg Bricks per Stride   : — ")
        retro_print(f" ▒ Estimated Build Time    : {total_time:.1f} sec")
        retro_print(f" ▒ Estimated Energy Used   : {energy:.2f} kWh\n")
        retro_print(" Grade: C+")
        retro_print(" Comment: Honourable effort, but the robot weeps...")
        retro_print(" Hint: Try using Stride Mode for glory.\n")
    else:
        # Optimised robot build – efficient
        retro_print("Stride protocol: ENGAGED.")
        retro_print("The robot moves with mechanical precision.")
        retro_print("Let the scroll of excellence be unfurled:\n")
        retro_print(f" ▒ Total Bricks Placed     : {total}")
        retro_print(f" ▒ Number of Strides Used  : {strides} (efficient)")
        retro_print(f" ▒ Avg Bricks per Stride   : {avg:.2f}")
        retro_print(f" ▒ Estimated Build Time     : {total_time:.1f} sec")
        retro_print(f" ▒ Estimated Energy Used    : {energy:.2f} kWh\n")
        retro_print(" Grade: S")
        retro_print(" Comment: You are a master of efficiency and bricks.")
        retro_print(" The wall stands tall. Glory is yours.\n")

    input("Press ENTER to return from your quest...")


# Handles manual sequential brick-by-brick building
def run_manual(wall, auto=False):
    show_banner()
    while wall.mark_next_brick_built():
        display_wall_with_prompt(wall, auto)
        if auto:
            time.sleep(0.3)
        else:
            input()
    retro_print("\n★ All bricks built! Quest complete. ★\n", delay=0.01)
    optimiser = StrideOptimiser(wall.wall_map, wall.wall_width, wall.wall_height)
    show_efficiency_report(optimiser, mode="sequential")


# Handles optimised robot building by strides
def run_stride(wall, auto=False):
    optimiser = StrideOptimiser(wall.wall_map, wall.wall_width, wall.wall_height)
    build_order = optimiser.get_stride_order()
    show_banner()
    for brick in build_order:
        brick["built"] = True
        display_wall_stride_prompt(wall, brick["stride"], auto)
        if auto:
            time.sleep(0.3)
        else:
            input()
    retro_print("\n★ All bricks built! Quest complete. ★\n", delay=0.01)
    show_efficiency_report(optimiser, mode="stride")


# Main entry point for starting the wall building quest
def start_wall_quest(skip_intro=False):
    if not skip_intro:
        show_intro()
    else:
        show_banner(animated=False)

    # Get simulation parameters from player
    bond_type, use_stride, auto, rows = prompt_settings()
    wall = Wall(num_rows=rows, bond_type=bond_type)

    # Run appropriate build method
    if use_stride:
        run_stride(wall, auto)
    else:
        run_manual(wall, auto)


# Starts the game loop
if __name__ == "__main__":
    try:
        first_run = True
        while True:
            start_wall_quest(skip_intro=not first_run)
            first_run = False

            again = input("\nWould you like to build another wall? (y/n): ").strip().lower()
            if again != "y":
                print("\n🏰 The builder retires, proud of their masonry legacy. Farewell!\n")
                break

    except KeyboardInterrupt:
        # Graceful exit if user hits Ctrl+C
        print("\n\n☠ The builder has fled the quest...\n")
