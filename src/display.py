import curses
from src.database import fetch_cages, fetch_species, fetch_unplaced_animals

def initialize_colors():
    """Initialize color pairs for animals and text."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Green for alive animals
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Red for dead animals
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)   # White for other text
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)    # Blue
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Cyan
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Yellow

def display_title(stdscr):
    """
    Display the centered title of the Zoo Management System and return the start_line
    for the content beneath it.
    """
    stdscr.clear()

    # Get the terminal dimensions
    _, width = stdscr.getmaxyx()

    # Center the title horizontally
    title = "Zoo Management System"
    start_x_title = (width - len(title)) // 2
    stdscr.addstr(0, start_x_title, " ------------------- ", curses.color_pair(4))
    stdscr.addstr(1, start_x_title, title, curses.color_pair(4))
    stdscr.addstr(2, start_x_title, " ------------------- ", curses.color_pair(4))

    # Return the start line for content beneath the title
    return 4

def display_menu(stdscr):
    """Display the application title and a list of possible actions in the main menu."""
    start_line = display_title(stdscr)

    stdscr.addstr(start_line, 0, "Actions", curses.color_pair(4))  # Actions heading in white

    # Menu items with keys in green and text in white
    menu_items = [
        ("C", "Create Species"),
        ("G", "Add Cage"),
        ("A", "Add Animal"),
        ("M", "Move Animal"),
        ("F", "Feed Animal"),
        ("R", "Remove dead animals"),
        ("Q", "Quit")
    ]

    for index, (key, action) in enumerate(menu_items, start=start_line + 2):
        stdscr.addstr(index, 0, key, curses.color_pair(1))  # Green for the key
        stdscr.addstr(index, 2, f"- {action}", curses.color_pair(3))  # White for the text

    stdscr.refresh()

def display_cages(stdscr, start_line):
    """Display a list of cages and their contents."""
    cages = fetch_cages()
    stdscr.addstr(start_line, 0, "Cages and Contents:", curses.color_pair(4))
    if not cages:
        stdscr.addstr(start_line + 2, 0, "No cages available.", curses.color_pair(6))
        start_line += 1
    else:
        line = start_line + 2
        for cage in cages:
            stdscr.addstr(line, 0, f"Cage {cage['id']}:", curses.color_pair(3))
            line += 1
            animals = cage['animals']
            if not animals:
                stdscr.addstr(line, 2, "Empty", curses.color_pair(6))
                start_line += 1
                line += 1
            else:
                for animal in animals:
                    color = curses.color_pair(1 if animal['is_alive'] else 2)
                    stdscr.addstr(line, 2, f"{animal['species']} ({animal['name']})", color)
                    line += 1
        line += 1
    # Calculate the number of lines occupied
    nb_cages = len(cages)
    nb_animals_in_cages = sum(len(cage['animals']) for cage in cages)
    return start_line + nb_cages + nb_animals_in_cages + 3

def display_species(stdscr, start_line):
    """Display a list of all available species."""
    species = fetch_species()
    stdscr.addstr(start_line, 0, "Available Species", curses.color_pair(4))
    if not species:
        stdscr.addstr(start_line + 2, 0, "None", curses.color_pair(6))
        start_line += 1
    else:
        line = start_line + 2
        for sp in species:
            stdscr.addstr(line, 0, f"{sp['name']} (Diet: {sp['diet']})", curses.color_pair(3))
            line += 1
    # Calculate the number of lines occupied
    nb_species = len(species)
    return start_line + nb_species + 3

def display_unplaced_animals(stdscr, start_line):
    """Display a list of animals that are not placed in any cage and are alive."""
    unplaced_animals = fetch_unplaced_animals()
    
    # Filter the list to include only alive animals
    alive_animals = [animal for animal in unplaced_animals if animal['is_alive']]

    stdscr.addstr(start_line, 0, "Unplaced Animals", curses.color_pair(4))
    if not alive_animals:
        stdscr.addstr(start_line + 2, 0, "None", curses.color_pair(6))
    else:
        line = start_line + 2
        for animal in alive_animals:
            stdscr.addstr(line, 0, f"{animal['species']} ({animal['name']})", curses.color_pair(1))  # Green for alive
            line += 1

    return start_line + len(alive_animals) + 3


def display_all(stdscr):
    """Display the main menu, cages, species, and unplaced animals in one view."""
    stdscr.clear()
    display_menu(stdscr)

    # Display cages and calculate next starting line
    next_start_line = display_cages(stdscr, start_line=14)

    # Display species and calculate next starting line
    next_start_line = display_species(stdscr, start_line=next_start_line)

    # Display unplaced animals
    next_start_line = display_unplaced_animals(stdscr, start_line=next_start_line)

    # Display footer
    stdscr.addstr(next_start_line + 2, 0, "Press a key to take an action... ", curses.color_pair(3))

    stdscr.refresh()
