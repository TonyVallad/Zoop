import sqlite3
from .database import add_species, add_animal, fetch_cages, fetch_species

class Zoo:
    def __init__(self):
        self.cages = fetch_cages()

    def add_cage(self):
        conn = sqlite3.connect("zoo.db")
        c = conn.cursor()
        c.execute("INSERT INTO cages DEFAULT VALUES")
        conn.commit()
        conn.close()

    def add_species(self, name, diet):
        add_species(name, diet)

    def add_animal(self, name, species_id, cage_id=None):
        add_animal(name, species_id, cage_id)


class Animal:
    def __init__(self, name, species, diet, is_alive=True):
        self.name = name
        self.species = species
        self.diet = diet
        self.is_alive = is_alive
