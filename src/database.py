import sqlite3

# Database Initialization
def initialize_db():
    """Create the database and required tables if they do not exist."""
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()
    # Create table for species
    c.execute("""
        CREATE TABLE IF NOT EXISTS species (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            diet TEXT
        )
    """)
    # Create table for animals
    c.execute("""
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY,
            name TEXT,
            species_id INTEGER,
            is_alive INTEGER DEFAULT 1,
            cage_id INTEGER,
            FOREIGN KEY(species_id) REFERENCES species(id),
            FOREIGN KEY(cage_id) REFERENCES cages(id)
        )
    """)
    # Create table for cages
    c.execute("""
        CREATE TABLE IF NOT EXISTS cages (
            id INTEGER PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()

# Species Management
def add_species(name, diet):
    """Add a new species to the species table."""
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO species (name, diet) VALUES (?, ?)", (name, diet))
    conn.commit()
    conn.close()

def fetch_species():
    """Fetch all species from the database."""
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()
    c.execute("SELECT id, name, diet FROM species")
    species = [{"id": row[0], "name": row[1], "diet": row[2]} for row in c.fetchall()]
    conn.close()
    return species

# Cage Management
def add_cage():
    """Add a new cage to the cages table."""
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()
    c.execute("INSERT INTO cages DEFAULT VALUES")
    conn.commit()
    conn.close()

def fetch_cages():
    """Fetch all cages and their contents."""
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()
    c.execute("SELECT id FROM cages")
    cages = [{"id": row[0], "animals": fetch_animals_in_cage(row[0])} for row in c.fetchall()]
    conn.close()
    return cages

# Animal Management
def add_animal(name, species_id, cage_id=None):
    """Add a new animal to the animals table."""
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO animals (name, species_id, cage_id) VALUES (?, ?, ?)",
        (name, species_id, cage_id)
    )
    conn.commit()
    conn.close()

def fetch_animals_in_cage(cage_id):
    """Fetch all animals in a specific cage."""
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()
    c.execute("""
        SELECT animals.id, animals.name, species.name AS species, species.diet, animals.is_alive
        FROM animals
        JOIN species ON animals.species_id = species.id
        WHERE animals.cage_id = ?
    """, (cage_id,))
    animals = [
        {
            "id": row[0],
            "name": row[1],
            "species": row[2],
            "diet": row[3],
            "is_alive": bool(row[4])
        }
        for row in c.fetchall()
    ]
    conn.close()
    return animals

def fetch_unplaced_animals():
    """Fetch all animals not yet placed in a cage."""
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()
    c.execute("""
        SELECT animals.id, animals.name, species.name, animals.is_alive
        FROM animals
        JOIN species ON animals.species_id = species.id
        WHERE animals.cage_id IS NULL
    """)
    animals = [
        {"id": row[0], "name": row[1], "species": row[2], "is_alive": bool(row[3])}
        for row in c.fetchall()
    ]
    conn.close()
    return animals

def update_animal_status(animal_id, is_alive):
    """Update the status of an animal (alive or dead)."""
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()
    c.execute("UPDATE animals SET is_alive = ? WHERE id = ?", (int(is_alive), animal_id))
    conn.commit()
    conn.close()

def move_animal_to_cage(animal_id, cage_id):
    """Move an animal to a new cage."""
    conn = sqlite3.connect("zoo.db")
    c = conn.cursor()
    c.execute("UPDATE animals SET cage_id = ? WHERE id = ?", (cage_id, animal_id))
    conn.commit()
    conn.close()
