import curses
from src.database import initialize_db
from src.display import initialize_colors, display_all
from src.actions import create_species, add_cage, add_animal, move_animal, feed_animal, remove_dead_animals_from_cages
from src.zoo import Zoo

def main(stdscr):
    # Initialize the database and setup curses
    initialize_db()
    initialize_colors()

    # Create a Zoo instance
    zoo = Zoo()

    # Main application loop
    while True:
        # Display the main menu and all zoo data
        display_all(stdscr)

        # Wait for user input
        key = stdscr.getch()

        # Handle user input for actions
        if key == ord("c"):
            create_species(stdscr)
        elif key == ord("g"):
            add_cage(stdscr, zoo)
        elif key == ord("a"):
            add_animal(stdscr, zoo)
        elif key == ord("m"):
            move_animal(stdscr, zoo)
        elif key == ord("f"):
            feed_animal(stdscr)
        elif key == ord("r"):
            remove_dead_animals_from_cages(stdscr)
        elif key == ord("q"):
            break

# Run the curses wrapper
if __name__ == "__main__":
    curses.wrapper(main)
