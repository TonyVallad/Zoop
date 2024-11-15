import sqlite3
from src.database import fetch_animals_in_cage, update_animal_status

# Predator-prey relationship by diet
diet_hierarchy = {
    "carnivore": ["herbivore"],  # Carnivores can eat herbivores
    "omnivore": [],              # Omnivores don’t prey on any specific group
    "herbivore": []              # Herbivores don’t prey on any group
}

def predator_prey_check(cage_id):
    """
    Check for predator-prey interactions within a cage based on diet.
    Carnivores prey on herbivores.
    """
    animals = fetch_animals_in_cage(cage_id)
    diet_groups = {"carnivore": [], "herbivore": [], "omnivore": []}

    # Organize animals by diet
    for animal in animals:
        if animal["is_alive"]:
            diet = animal["diet"]
            diet_groups[diet].append(animal)

    # Process predator-prey interactions
    for carnivore in diet_groups["carnivore"]:
        for herbivore in diet_groups["herbivore"]:
            # Carnivore eats the herbivore
            herbivore["is_alive"] = False
            update_animal_status(herbivore["id"], is_alive=False)
            print(f"{carnivore['name']} the {carnivore['species']} has eaten {herbivore['name']} the {herbivore['species']}.")

def update_animal_status(animal_id, is_alive):
    """
    Update the status of an animal in the database (alive or dead).
    """
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()
    c.execute("UPDATE animals SET is_alive = ? WHERE id = ?", (int(is_alive), animal_id))
    conn.commit()
    conn.close()

def get_prey_status(animals):
    """
    Provides a list of animals in the cage, marking alive or dead status for each.
    """
    prey_status = []
    for animal in animals:
        status = "alive" if animal["is_alive"] else "dead"
        prey_status.append(f"{animal['name']} ({animal['species']}) - {status}")
    return prey_status
