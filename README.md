### **<h1 align="center">Zoo Management Simulator</h1>**

<p align="center">
  <img src="src/static/logo.png" alt="Zoo Logo" width="250">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README_fr.md">Français</a>
</p>

This project is a command-line zoo management simulation designed to showcase Object-Oriented Programming (OOP) concepts in Python. It allows users to manage a virtual zoo by creating and interacting with animals, cages, and other components, leveraging a SQLite database for data storage and the curses library for terminal-based visualization.

---

### **Table of Contents**

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [How the Project Works](#how-the-project-works)
5. [Technologies Used](#technologies-used)
6. [Project Structure](#project-structure)
7. [Future Improvements](#future-improvements)

---

### **Features**

- **Zoo Management**: Create and manage animals, cages, and species dynamically within a SQLite database.
- **Curses-Based Interface**: Display zoo information such as cages, animals, and species in an interactive terminal interface.
- **Predator-Prey Simulation**: Handle interactions between predators and prey within the zoo.
- **Dynamic Species Creation**: Add new species and animals to expand your zoo.
- **Modular Design**: Separation of concerns between data, business logic, and display functions for scalability.

---

### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/TonyVallad/Zoop.git
   cd Zoop
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

---

### **Usage**

- Start the application and follow the terminal prompts to manage your zoo.
- Perform actions like adding new animals, creating cages, and simulating interactions.

#### Key Functionalities

- **View Zoo Status**: Check the list of cages, animals, and unplaced creatures.
- **Add Animals**: Populate your zoo with species tailored to their environment.
- **Simulate Interactions**: Handle feeding schedules and predator-prey dynamics.

---

### **How the Project Works**

1. **Zoo Initialization**: A SQLite database stores information about animals, species, and cages. The database initializes automatically when the program starts.
2. **Object-Oriented Design**: Classes like `Zoo`, `Cage`, and `Animal` encapsulate functionality.
3. **Dynamic UI**: Uses `curses` to display information interactively in the terminal.
4. **Action Execution**: User actions are handled through a main loop, executing commands based on input.

---

### **Technologies Used**

- **Python**: Core language for simulation logic and database interaction.
- **SQLite**: Lightweight database for storing zoo data persistently.
- **Curses**: Library for terminal-based user interface.

---

### **Project Structure**

```plaintext
Zoop/
│
├── app.py                  # Main entry point
├── src/
│   ├── actions.py          # Actions functions
│   ├── database.py         # Database initialization and management
│   ├── display.py          # Display functions
│   ├── utils.py            # Utility functions
│   ├── zoo.py              # Core Zoo class
│
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

---

### **Future Improvements**

- **Enhanced Interactions**: Add breeding and more complex predator-prey mechanics.
- **Expanded UI**: Improve the curses interface for better navigation and usability.

---

### **License**

This project is licensed under the MIT License. You are free to use, modify, and distribute this software in any project, personal or commercial, provided that you include a copy of the original license and copyright notice.

For more information, see the [LICENSE](LICENSE) file.