class Zoo:
    def __init__(self):
        self.cages = []

    def add_cage(self, cage):
        self.cages.append(cage)
        print(f"Cage {cage.cage_id} added to the zoo.")

    def count_cages(self):
        return len(self.cages)

    def display_cages(self):
        for cage in self.cages:
            cage.list_animals()


class Cage:
    def __init__(self, cage_id):
        self.cage_id = cage_id
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"{animal.name} the {animal.species} added to cage {self.cage_id}.")

    def list_animals(self):
        if not self.animals:
            print(f"Cage {self.cage_id} is empty.")
        else:
            for animal in self.animals:
                print(f"{animal.name} ({animal.species})")


class Animal:
    def __init__(self, name, species, diet):
        self.name = name
        self.species = species
        self.diet = diet

    def feed(self, food_type):
        if food_type == self.diet:
            print(f"{self.name} the {self.species} has been fed.")
        else:
            print(f"{self.name} the {self.species} cannot eat {food_type}.")


class Lion(Animal):
    def __init__(self, name):
        super().__init__(name, "Lion", "carnivore")


class Gazelle(Animal):
    def __init__(self, name):
        super().__init__(name, "Gazelle", "herbivore")


# Example usage:
zoo = Zoo()
cage1 = Cage(1)
zoo.add_cage(cage1)

lion = Lion("Leo")
gazelle = Gazelle("Gizelle")

cage1.add_animal(lion)
cage1.add_animal(gazelle)
cage1.list_animals()

lion.feed("carnivore")
gazelle.feed("carnivore")
