import curses
import sqlite3
from src.database import add_species, add_animal, fetch_species, fetch_cages, move_animal_to_cage, fetch_unplaced_animals
from src.utils import predator_prey_check
from src.display import display_title

def create_species(stdscr):
    """Prompt user to add a new species using curses."""
    start_line = display_title(stdscr)

    stdscr.addstr(start_line, 0, "Add a New Species", curses.A_BOLD)
    stdscr.addstr(start_line + 2, 0, "Enter species name: ")
    curses.echo()
    name = stdscr.getstr(start_line + 2, 20).decode("utf-8")
    curses.noecho()

    # Display diet options and prompt user to select a diet
    stdscr.addstr(start_line + 4, 0, "Select diet by number:", curses.A_BOLD)
    stdscr.addstr(start_line + 5, 0, "1 - Carnivore", curses.color_pair(3))
    stdscr.addstr(start_line + 6, 0, "2 - Herbivore", curses.color_pair(3))
    stdscr.addstr(start_line + 7, 0, "3 - Omnivore", curses.color_pair(3))
    stdscr.addstr(start_line + 9, 0, "Enter your choice: ", curses.color_pair(3))
    curses.echo()
    try:
        diet_choice = int(stdscr.getstr(start_line + 9, 20).decode("utf-8"))
    except ValueError:
        diet_choice = None
    curses.noecho()

    # Map numeric choices to diet types
    diet_map = {1: "carnivore", 2: "herbivore", 3: "omnivore"}
    diet = diet_map.get(diet_choice)

    if not diet:
        stdscr.addstr(start_line + 11, 0, "Invalid choice. Press any key to return.", curses.color_pair(2))  # Red for invalid
        stdscr.refresh()
        stdscr.getch()
        return

    # Add species to the database
    add_species(name, diet)

    # Display success message
    start_line = display_title(stdscr)
    stdscr.addstr(start_line, 0, f"Species '{name}' with diet '{diet}' added successfully!", curses.color_pair(1))  # Green for success
    stdscr.addstr(start_line + 2, 0, "Press any key to return to the main menu.")
    stdscr.refresh()
    stdscr.getch()

def add_cage(stdscr, zoo):
    """Add a new cage using curses."""
    start_line = display_title(stdscr)

    zoo.add_cage()
    stdscr.addstr(start_line, 0, "New cage added to the zoo.", curses.A_BOLD)
    stdscr.addstr(start_line + 2, 0, "Press any key to return to the main menu.")
    stdscr.refresh()
    stdscr.getch()

def add_animal(stdscr, zoo):
    """Prompt user to add a new animal to a cage using curses."""
    start_line = display_title(stdscr)

    stdscr.addstr(start_line, 0, "Add a New Animal", curses.A_BOLD)

    species_id = select_species(stdscr)
    if not species_id:
        stdscr.addstr(start_line + 4, 0, "Invalid species selection. Press any key to return.", curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()
        return

    start_line = display_title(stdscr)

    stdscr.addstr(start_line + 2, 0, "Enter animal name: ")
    curses.echo()
    name = stdscr.getstr(start_line + 2, 20).decode("utf-8")
    curses.noecho()

    cage_id = select_cage(stdscr)

    start_line = display_title(stdscr)

    if cage_id:
        zoo.add_animal(name, species_id, cage_id)
        stdscr.addstr(start_line, 0, f"Animal '{name}' has been added to cage {cage_id}.", curses.A_BOLD)
        predator_prey_check(cage_id)
    else:
        zoo.add_animal(name, species_id)
        stdscr.addstr(start_line, 0, f"Animal '{name}' has been added but is not in a cage.", curses.A_BOLD)

    stdscr.addstr(start_line + 2, 0, "Press any key to return to the main menu.")
    stdscr.refresh()
    stdscr.getch()

def move_animal(stdscr, zoo):
    """Move an animal to a different cage using curses."""
    start_line = display_title(stdscr)

    stdscr.addstr(start_line, 0, "Move an Animal", curses.A_BOLD)

    animal_id = select_animal(stdscr, "Select an animal to move: ")

    start_line = display_title(stdscr)

    if not animal_id:
        stdscr.addstr(start_line, 0, "Invalid animal selection. Press any key to return.", curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()
        return

    cage_id = select_cage(stdscr)

    start_line = display_title(stdscr)

    if cage_id:
        move_animal_to_cage(animal_id, cage_id)
        stdscr.addstr(start_line, 0, f"Animal has been moved to cage {cage_id}.", curses.A_BOLD)
        predator_prey_check(cage_id)
    else:
        stdscr.addstr(start_line, 0, "No cage selected. Animal not moved.", curses.A_BOLD)

    stdscr.addstr(start_line + 2, 0, "Press any key to return to the main menu.")
    stdscr.refresh()
    stdscr.getch()

def feed_animal(stdscr):
    """Feed an animal using curses."""
    start_line = display_title(stdscr)

    stdscr.addstr(start_line, 0, "Feed an Animal", curses.A_BOLD)

    # Select an animal
    animal_id = select_animal(stdscr, "Select an animal to feed: ")
    if not animal_id:
        stdscr.addstr(start_line + 2, 0, "Invalid animal selection. Press any key to return.", curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()
        return

    start_line = display_title(stdscr)

    # Display food type options
    stdscr.addstr(start_line + 2, 0, "Select food type by number:", curses.color_pair(3))
    stdscr.addstr(start_line + 3, 0, "1 - Carnivore", curses.color_pair(3))
    stdscr.addstr(start_line + 4, 0, "2 - Herbivore", curses.color_pair(3))
    stdscr.addstr(start_line + 5, 0, "3 - Omnivore", curses.color_pair(3))
    stdscr.addstr(start_line + 7, 0, "Enter your choice: ", curses.color_pair(3))
    curses.echo()
    try:
        food_choice = int(stdscr.getstr(start_line + 7, 20).decode("utf-8"))
    except ValueError:
        food_choice = None
    curses.noecho()

    # Map numeric choices to food types
    food_types = {1: "carnivore", 2: "herbivore", 3: "omnivore"}
    food_type = food_types.get(food_choice)

    if not food_type:
        stdscr.addstr(start_line + 9, 0, "Invalid food selection. Press any key to return.", curses.color_pair(2))  # Red
        stdscr.refresh()
        stdscr.getch()
        return

    # Fetch the animal and its diet from the database
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()
    c.execute("""
        SELECT animals.name, species.diet
        FROM animals
        JOIN species ON animals.species_id = species.id
        WHERE animals.id = ?
    """, (animal_id,))
    animal = c.fetchone()
    conn.close()

    if animal:
        name, diet = animal
        if diet == "omnivore" or food_type == diet:
            # Success message in green
            stdscr.addstr(start_line + 9, 0, f"{name} has been fed correctly with {food_type} food.", curses.color_pair(1))
        else:
            # Warning message in red
            stdscr.addstr(start_line + 9, 0, f"Warning: {name} has been fed with inappropriate food ({food_type}). Its diet is {diet}.", curses.color_pair(2))
    else:
        # Error message in red
        stdscr.addstr(start_line + 9, 0, "Animal not found.", curses.color_pair(2))

    stdscr.addstr(start_line + 11, 0, "Press any key to return to the main menu.")
    stdscr.refresh()
    stdscr.getch()

def remove_dead_animals_from_cages(stdscr):
    """
    Remove dead animals from cages by setting their cage_id to NULL.
    Dead animals remain in the database but are no longer assigned to a cage.
    """
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()

    # Update the database: set cage_id to NULL for dead animals
    c.execute("""
        UPDATE animals
        SET cage_id = NULL
        WHERE is_alive = 0
    """)
    conn.commit()
    conn.close()

    start_line = display_title(stdscr)

    stdscr.addstr(start_line, 0, "Removed dead animals from cages.", curses.color_pair(1))

# Helper Functions
def select_species(stdscr):
    """Display available species and allow user to select one by ID using curses."""
    start_line = display_title(stdscr)

    stdscr.addstr(start_line, 0, "Select a Species", curses.A_BOLD)
    species = fetch_species()
    for i, sp in enumerate(species, start=start_line + 2):
        stdscr.addstr(i, 0, f"{sp['id']}: {sp['name']} (Diet: {sp['diet']})")

    stdscr.addstr(start_line + len(species) + 4, 0, "Enter species ID: ")
    curses.echo()
    try:
        species_id = int(stdscr.getstr(start_line + len(species) + 4, 20).decode("utf-8"))
        curses.noecho()
        if any(sp['id'] == species_id for sp in species):
            return species_id
    except ValueError:
        curses.noecho()
    return None

def select_cage(stdscr):
    """Display available cages and allow user to select one by ID using curses."""
    start_line = display_title(stdscr)

    stdscr.addstr(start_line, 0, "Select a Cage", curses.A_BOLD)
    cages = fetch_cages()
    for i, cage in enumerate(cages, start=start_line + 2):
        stdscr.addstr(i, 0, f"Cage {cage['id']}")

    stdscr.addstr(start_line + len(cages) + 4, 0, "Enter cage ID (or leave blank to skip): ")
    curses.echo()
    try:
        cage_id = int(stdscr.getstr(start_line + len(cages) + 4, 40).decode("utf-8"))
        curses.noecho()
        if any(cage['id'] == cage_id for cage in cages):
            return cage_id
    except ValueError:
        curses.noecho()
    return None

def select_animal(stdscr, prompt="Select an animal: "):
    """Display all animals grouped by cage and allow user to select one by ID using curses."""
    start_line = display_title(stdscr)

    stdscr.addstr(start_line, 0, prompt, curses.A_BOLD)
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()

    # Fetch animals grouped by cage_id and ordered by species
    c.execute("""
        SELECT animals.id, animals.name, species.name, animals.is_alive, cages.id
        FROM animals
        JOIN species ON animals.species_id = species.id
        LEFT JOIN cages ON animals.cage_id = cages.id
        ORDER BY cages.id, species.name
    """)
    animals = c.fetchall()
    conn.close()

    if not animals:
        stdscr.addstr(start_line + 2, 0, "No animals available.", curses.color_pair(3))
        stdscr.refresh()
        stdscr.getch()
        return None

    # Group animals by cage_id
    grouped_animals = {}
    for animal in animals:
        cage_id = animal[4]  # Cage ID
        grouped_animals.setdefault(cage_id, []).append(animal)

    line = start_line + 2
    for cage_id, cage_animals in grouped_animals.items():
        if cage_id is None:
            stdscr.addstr(line, 0, "Not in a cage:", curses.color_pair(3))
        else:
            stdscr.addstr(line, 0, f"Cage {cage_id}:", curses.color_pair(3))
        line += 1

        for animal_id, name, species_name, is_alive, _ in cage_animals:
            # Color settings
            id_name_color = curses.color_pair(1 if is_alive else 2)  # Green for alive, red for dead
            species_color = curses.color_pair(4)  # Blue for species

            # Display ID and name with status color
            stdscr.addstr(line, 2, f"{animal_id}: {name}", id_name_color)

            # Display species in blue
            stdscr.addstr(line, len(f"{animal_id}: {name}") + 3, f"the {species_name}", species_color)

            line += 1

    stdscr.addstr(line + 2, 0, "Enter animal ID: ")
    curses.echo()
    try:
        animal_id = int(stdscr.getstr(line + 2, 20).decode("utf-8"))
        curses.noecho()
        # Validate if the entered ID exists
        if any(animal[0] == animal_id for animal in animals):
            return animal_id
    except ValueError:
        curses.noecho()
    return None
