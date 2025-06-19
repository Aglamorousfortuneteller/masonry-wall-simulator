# main.py - Runs the wall simulation and handles interaction

import os
from wall import Wall
from stride_optimiser import StrideOptimiser

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def run_wall_simulation(auto=False, delay=0.3):
    wall = Wall(num_rows=int(input("Enter number of wall rows: ").strip()))
    clear_screen()
    wall.display()
    print("\nPress ENTER to place a brick. Ctrl+C to exit.\n")

    while wall.mark_next_brick_built():
        if auto:
            import time
            time.sleep(delay)
        else:
            input()
        clear_screen()
        wall.display()
        print("\nPress ENTER to place a brick. Ctrl+C to exit.\n")

    print("\n✅ All bricks built!")

def run_optimised_simulation(auto=False, delay=0.3):
    wall = Wall(num_rows=int(input("Enter number of wall rows: ").strip()))
    optimiser = StrideOptimiser(wall.wall_map, wall.wall_width, wall.wall_height)
    stride_order = optimiser.get_stride_order()

    clear_screen()
    wall.display()
    print("\nPress ENTER to build by stride. Ctrl+C to exit.\n")

    for brick in stride_order:
        brick["built"] = True
        if auto:
            import time
            time.sleep(delay)
        else:
            input()
        clear_screen()
        wall.display()
        print(f"\nNow building stride: {brick['stride']}\n")

    print("\n✅ All bricks built in optimised stride order!")

    total, strides, avg = optimiser.get_stride_metrics()
    print("\n--- Efficiency Report ---")
    print(f"Total Bricks: {total}")
    print(f"Strides Used: {strides}")
    print(f"Avg Bricks per Stride: {avg:.2f}")
    total_time, energy_used = optimiser.estimate_time_and_energy()
    print(f"\n⏱️ Estimated Build Time: {total_time:.1f} seconds")
    print(f"⚡ Estimated Energy Usage: {energy_used:.2f} kWh")




def ask_for_automation():
    auto = input("\nDo you want to build automatically with visualisation? (y/n): ").strip().lower() == 'y'
    if auto:
        folder = input("Enter folder path to save GIF (or leave blank to skip saving): ").strip()
        return True, folder
    return False, ""

if __name__ == "__main__":
    clear_screen()
    print("🧱 Masonry Wall Simulator\n")
    print("Choose build mode:")
    print("1. Normal build (row by row)")
    print("2. Optimised build (by stride)")

    choice = input("\nEnter choice (1 or 2): ").strip()
    auto, gif_folder = ask_for_automation()

    if choice == "2":
        run_optimised_simulation(auto=auto)
    else:
        run_wall_simulation(auto=auto)
