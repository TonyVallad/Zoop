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

def display_menu(stdscr):
    """Display the application title and a list of possible actions in the main menu."""
    stdscr.clear()

    # Get the terminal dimensions
    height, width = stdscr.getmaxyx()

    # Center the title horizontally
    title = "Zoo Management System"
    start_x_title = (width - len(title)) // 2
    stdscr.addstr(0, start_x_title, " ------------------- ", curses.color_pair(4))
    stdscr.addstr(1, start_x_title, title, curses.color_pair(4))
    stdscr.addstr(2, start_x_title, " ------------------- ", curses.color_pair(4))

    stdscr.addstr(4, 0, "Actions", curses.color_pair(4))  # Actions heading in white

    # Menu items with keys in green and text in white
    menu_items = [
        ("C", "Create Species"),
        ("G", "Add Cage"),
        ("A", "Add Animal"),
        ("M", "Move Animal"),
        ("F", "Feed Animal"),
        ("Q", "Quit")
    ]

    for index, (key, action) in enumerate(menu_items, start=6):
        stdscr.addstr(index, 0, key, curses.color_pair(1))  # Green for the key
        stdscr.addstr(index, 2, f"- {action}", curses.color_pair(3))  # White for the text

    stdscr.refresh()

def display_cages(stdscr, start_line):
    """Display a list of cages and their contents."""
    cages = fetch_cages()
    stdscr.addstr(start_line, 0, "Cages and Contents", curses.color_pair(4))
    if not cages:
        stdscr.addstr(start_line + 2, 0, "No cages available", curses.color_pair(6))
    else:
        line = start_line + 2
        for cage in cages:
            stdscr.addstr(line, 0, f"Cage {cage['id']}:", curses.color_pair(3))
            line += 1
            animals = cage['animals']
            if not animals:
                stdscr.addstr(line, 2, "Empty", curses.color_pair(6))
                line += 1
            else:
                for animal in animals:
                    color = curses.color_pair(1 if animal['is_alive'] else 2)
                    stdscr.addstr(line, 2, f"{animal['species']} ({animal['name']})", color)
                    line += 1
        line += 1

def display_species(stdscr, start_line):
    """Display a list of all available species."""
    species = fetch_species()
    stdscr.addstr(start_line, 0, "Available Species", curses.color_pair(4))
    if not species:
        stdscr.addstr(start_line + 2, 0, "No species available.", curses.color_pair(6))
    else:
        line = start_line + 2
        for sp in species:
            stdscr.addstr(line, 0, f"{sp['name']} (Diet: {sp['diet']})", curses.color_pair(3))
            line += 1

def display_unplaced_animals(stdscr, start_line):
    """Display a list of animals that are not placed in any cage."""
    unplaced_animals = fetch_unplaced_animals()
    stdscr.addstr(start_line, 0, "Unplaced Animals", curses.color_pair(4))
    if not unplaced_animals:
        stdscr.addstr(start_line + 2, 0, "None", curses.color_pair(6))
    else:
        line = start_line + 2
        for animal in unplaced_animals:
            color = curses.color_pair(1 if animal['is_alive'] else 2)
            stdscr.addstr(line, 0, f"{animal['species']} ({animal['name']})", color)
            line += 1

def display_all(stdscr):
    """Display the main menu, cages, species, and unplaced animals in one view."""
    stdscr.clear()
    display_menu(stdscr)

    # Display cages
    display_cages(stdscr, start_line=13)

    # Display available species
    display_species(stdscr, start_line=24)

    # Display unplaced animals
    display_unplaced_animals(stdscr, start_line=30)

    stdscr.refresh()
