# 3D Cannonball Flight Simulator

A physics simulation of 3D projectile motion. The numerical integration runs in **C++** for speed and is exposed to **Python** through [nanobind](https://github.com/wjakob/nanobind). An interactive **Dash + Plotly** web app is the front end. Everything builds with **Bazel**.

## 🏗️ Architecture

```
Dash web UI (Python)  ──►  sim_engine (nanobind module)  ──►  C++ physics_engine
  sliders + Plotly 3D        run_simulation()                   CannonBall + Simulation
                             run_multiple_simulations()
```

- **C++ physics engine:** advances the state `[x, y, z, vx, vy, vz]` with explicit Euler integration (`dt = 0.01 s`) under constant gravity until the ball hits the ground (`z <= 0`).
- **Parallel batch mode:** `run_multiple_simulations` splits independent trajectories across all CPU cores using `std::thread`.
- **Python bindings:** nanobind compiles the C++ code into a native Python module, `sim_engine`. No file I/O or subprocesses are involved.
- **Web UI:** Dash sliders set the launch parameters, and Plotly renders the trajectory in an interactive 3D view.

## 📂 Project structure

```text
Simulation/
├── MODULE.bazel             # Bazel dependencies (rules_cc, rules_python, nanobind_bazel, apple_support)
├── .bazelrc                 # C++17 build flags
├── requirements.in / .txt   # Python deps (dash, plotly), pinned lockfile
├── sim_cpp/
│   ├── BUILD.bazel          # physics_engine, sim_engine, main
│   ├── include/
│   │   ├── CannonBall.h     # Projectile state + Euler step
│   │   └── Simulation.h     # Single and batch simulation API
│   └── src/
│       ├── CannonBall.cpp
│       ├── Simulation.cpp
│       ├── sim_bindings.cpp # nanobind module definition
│       └── main.cpp         # Standalone C++ demo: 1000 random balls in parallel
└── sim_py/
    ├── BUILD.bazel          # run_simulation (app), test_simulation (tests)
    ├── run_simulation.py    # Dash UI
    └── tests/
        └── test_simulation.py
```

## ⚙️ Prerequisites

- **Bazel**: installing via [Bazelisk](https://github.com/bazelbuild/bazelisk) is recommended (`brew install bazelisk` on macOS)
- **C++17 compiler**: on macOS, Xcode Command Line Tools (`xcode-select --install`)

You don't need a local Python install or a virtualenv. Bazel downloads a hermetic **Python 3.11** toolchain and installs the pinned packages from `requirements.txt` automatically.

## 🚀 Usage

Run the web app:
```bash
bazel run //sim_py:run_simulation
```
Then open http://127.0.0.1:8050 and adjust:
- **Initial velocity** (5–150 m/s)
- **Launch angle θ**: elevation above the ground (1°–89°)
- **Azimuth angle φ**: compass direction in the ground plane (0°–360°)

The 3D plot and impact summary update live.

Run the tests:
```bash
bazel test //sim_py:test_simulation
```

Run the standalone C++ batch demo:
```bash
bazel run //sim_cpp:main
```

## 🐍 Python API

```python
from sim_cpp import sim_engine
import math

# Single trajectory: returns a list of [x, y, z, vx, vy, vz] states
traj = sim_engine.run_simulation([50.0, math.radians(45), math.radians(30)])

# Many trajectories in parallel: returns one trajectory per input, in order
batch = sim_engine.run_multiple_simulations([
    [50.0, math.radians(45), 0.0],
    [80.0, math.radians(30), math.radians(90)],
])
```
Angles are in **radians**. θ is the elevation and φ is the azimuth.

## 🧪 Tests

The tests compare simulation output against analytic projectile formulas:
- the trajectory stops at ground impact
- vertical shot: peak height ≈ v0² / 2g
- 45° shot: range ≈ v0² / g
- φ = 90° sends the ball along +y
- parallel batch results exactly match individual runs

Tolerances in these tests account for the error of first-order Euler integration.

## 🚧 In progress: multi-ball firing (`MultiSim` branch)

`run_batch()` in `run_simulation.py` generates N launches with Gaussian scatter around the slider values:

| Parameter | σ | ~99.7% of balls within |
|---|---|---|
| v0 | 1.0 m/s | ±3 m/s |
| θ | 0.5° | ±1.5° |
| φ | 1.0° | ±3° |

The values are clamped (v0 > 0, θ in [1°, 89°]) and simulated in a single parallel C++ call. The random generator is seeded (`42`), so results can be reproduced.

**Next:** wire `run_batch` into the UI with a ball-count control and draw one trace per ball.

## 🔭 Possible improvements

- Air drag (quadratic) with mass, radius and drag coefficient
- A higher-order integrator (RK4) or a configurable time step
- Interpolate the exact impact point (the last sample currently lands slightly below z = 0)

## 📝 macOS + USB drive notes

- **AppleDouble files:** hidden `._*` files can break builds. Clean them with:
  ```bash
  dot_clean -m .
  ```
- **`could not get working directory`:** if the drive is ejected or reconnected while a terminal is open, that terminal's folder becomes invalid. `cd` back into the project (or open a new terminal).