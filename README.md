# Multi-Agent Patrolling System in Python

## Description

This project simulates a multi-agent patrolling system for museums. The agents move optimally to monitor all rooms. The application leverages artificial intelligence techniques, particularly inspired by ant colony optimization and other pathfinding algorithms, such as evolutionary algorithms and k-means clustering, to compute the most efficient patrol routes for the agents.

The system also features a graphical interface to visualize the museum map, create nodes and edges representing rooms and paths, and dynamically configure parameters.

Link to the YouTube video showcasing the project:  
https://youtu.be/NvPAJv8h5M0

## Features
* **Graph Creation**: Generate a graph from an image of the museum layout, where nodes represent an area and edges represent paths between them.
* **Interactive Interface**: Modify simulation parameters dynamically through the user interface.
* **AI-based Optimization**: Implement Ant Colony Optimization, Evolutional Algorithms, and K-Means clustering to determine the best patrol routes for agents.
* **Data Management**: Save and load adjacency matrices as CSV files for easy reuse. Results can be exported to the results/ folder for comparison of algorithm performance.

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/Gilles-Maurer-Organization/AI50_patrolling.git  
cd AI50_patrolling
```

### 2. Set up the Virtual Environment
Please use **Python 3.11** for compatibility with the libraries and features.
```bash
python -m venv .venv
```
On MacOS and Linux:
```bash
source .venv/bin/activate
```
On Windows:
```bash 
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage
### 1. Run the Application
```bash
python main.py
```

### 2. Features in the UI
* **Graph View**: Visualize the generated graph of nodes and edges.
* **Parameters View**: Adjust simulation parameters, add nodes and edges, and configure algorithm settings dynamically. You can also toggle the alignment assistant to enable or disable the automatic alignment of nodes.
* **Data View**: Visualize real-time metrics such as mean, maximum, and all-time maximum idleness data as the simulation progresses.

### 3. Save and Load Data

* You can save the current graph configuration by using the save button in the Parameters View. This will save the adjacency matrices in the csv_files/ directory, and the associated image in the backgrounds/ folder.
* You can load previously saved configurations by re-importing the associated image or CSV file containing the graph data.

## Project Structure
```bash
AI50_patrolling/
│
├── assets/              # Storing all the static images
├── backgrounds/         # Storing all the imported images linked to a specific graph
├── constants/           # Definition of all the program's constants
├── controllers/         # Managing all the interactions between the views and models
│   ├── buttons/         # Handles the logic and events for button interactions
│   ├── text_boxes/      # Manages text input handling and event triggers
│   └── check_boxes/     # Manages the logic for checkbox interactions and states
├── models/              # Contains all the program's models
│   └──  algorithms/      # Implements the algorithms used in the program
├── views/               # Contains all the program's views
│   ├── popup/           # Manages the pop-up views
│   └──  text_boxes/      # Handles the display and interaction with text boxes
├── services/            # Manages external operations not directly tied to the core MVC structure
├── references/          # Link between a graph and an image
├── csv_files/           # Directory for saving and loading CSV files
├── results/             # CSV files containing the performance results for each algorithm
├── tests/               # Contains unit tests to ensure the correctness of the project
├── main.py              # Entry point of the application
├── requirements.txt     # Project dependencies
├── sonar-project.properties  # Configuration for SonarQube, for code quality analysis
└── tox.ini              # Configuration file for Tox
```

## Creating an Executable with PyInstaller
If you want to package this project into a standalone executable, you can use **PyInstaller**. Follow these steps to generate an executable for your platform:

### 1. Install PyInstaller
First, make sure PyInstaller is installed in your virtual environment:
```bash
pip install pyinstaller
```
### 2. Create the Main Executable
Once PyInstaller is installed, navigate to the root of the project directory and run the following command:  
  
On MacOS and Linux:
```bash
pyinstaller --onefile --add-data "assets:assets" --noconsole main.py
```
On Windows:
```bash
pyinstaller --onefile --add-data "assets;assets" --noconsole main.py
```
This will generate a single executable file. By default, the executable will be located in the dist/ folder.

### 3. Create the Analysis Executable
An executable version of the python script designed for analyzing results (analyse.py) can also be built:  
  
On MacOS, Linux and Windows:
```bash
pyinstaller --onefile --noconsole analyse.py
```
This will also generate a single executable file. By default, the executable will be located in the dist/ folder.  
  
**Note:** This executable is intended to be used only after results have been saved in the data/results folder.

### 3. Run the Executables
To run the executables, simply go to the dist/ folder and execute the main or analyse files. The application should work just like when running from the Python script.

## Acknowledgements
This project makes use of the following libraries and tools:

* **NumPy** – A powerful numerical computing library for Python.
* **Pygame-CE** – A library for creating video games and graphical applications.
* **Pygame GUI** – A GUI library for creating user interfaces with Pygame.
* **SciPy** – A library used for scientific and technical computing.
* **Matplotlib** – A plotting library for creating visualizations in Python.
* **pytest** – A testing framework for Python.
* **tox** – A tool for automating testing across multiple environments.
* **pytest-cov** – A plugin for pytest to measure code coverage.

## Authors
- [Augustin Athane](https://github.com/aathane)
- [Eileen Jovenin](https://github.com/Eileenj57)
- [Gilles Maurer](https://github.com/gilles-maurer)
- [Raphaël Perrin](https://github.com/DynaTiuM)
- [Arnaud Planchin](https://github.com/Lolitono)
- [Guillaume Scherrer](https://github.com/guiguiSCH68)
