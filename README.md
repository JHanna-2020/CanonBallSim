# 3D Cannonball Flight Simulator

A cross-language physics simulation that models the 3D trajectory of a projectile. This project utilizes a **C++ backend** for high-performance numerical integration and a **Python frontend** for an interactive web-based graphical user interface (GUI) and 3D data visualization.

## 🏗️ System Architecture

The project is split into two distinct environments that communicate via file I/O:

1. **C++ Physics Engine:** Uses Euler's method (1st-order numerical integration) to calculate position and velocity over time, factoring in gravity and 3D spherical launch coordinates. 
2. **Python UI (Streamlit):** Serves as the control panel. It collects user parameters, triggers the C++ executable in the background, and renders the output data using Matplotlib.

### Data Flow
`Streamlit UI` ➔ writes `config.txt` ➔ `C++ Executable` runs math ➔ writes `trajectory.csv` ➔ `Streamlit UI` renders 3D Graph & Table.

## 📂 Folder Structure

```text
Simulation/
├── C++ Sim/
│   ├── include/          # C++ Header files (.h)
│   └── src/              # C++ Source files (.cpp)
├── Python Code/
│   └── src/
│       └── run_simulation.py  # Streamlit UI & Visualization
├── cmake-build-debug/    # Compiled C++ executable location
├── venv/                 # Python virtual environment (ignored by Git)
├── CMakeLists.txt        # CMake build configuration
└── .gitignore
```

## ⚙️ Prerequisites

*   **C++:** CMake (v3.10+) and a C++17 compatible compiler (GCC, Clang, or MSVC).
*   **Python:** Python 3.8+

## 🚀 Setup & Installation

### 1. Build the C++ Engine
This project uses CMake. If you are using an IDE like CLion, simply load the `CMakeLists.txt` file and build the `sim_executable` target. 
Alternatively, using the terminal:
```bash
mkdir cmake-build-debug
cd cmake-build-debug
cmake ..
make
```

### 2. Configure the Python Environment
Open your terminal in the root `Simulation` folder and set up a virtual environment to prevent package conflicts:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install streamlit pandas matplotlib
```

## 🎮 Running the Simulation

1. Ensure your Python virtual environment is activated.
2. Run the Streamlit web application from the root directory:
```bash
streamlit run "Python Code/src/run_simulation.py"
```
3. A web browser will open at `http://localhost:8501`. Use the sidebar to adjust the Initial Velocity, Launch Angle, Azimuth Angle, and Time Step.
4. Click **Fire Cannon!** to generate the trajectory and view the 3D plot and raw data table.

## 📝 Troubleshooting Note for macOS USB Drives

If you are developing this project on an external flash drive on macOS, you may occasionally encounter build errors related to hidden AppleDouble files (e.g., `._main.cpp`). 
To clear these files and fix the build errors, run the following command in your terminal from the root project directory:
```bash
dot_clean -m .
```