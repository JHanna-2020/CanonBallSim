#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>
#include "Simulation.h"

namespace nb = nanobind;

NB_MODULE(sim_engine, m) {
    m.doc() = "Simulation Engine";

    m.def(
        "run_simulation",
        &run_simulation,
        nb::arg("initial_conditions"),
        "Integrates projectile trajectory until ground impact"
    );
    m.def(
        "run_multiple_simulations",
        &run_multiple_simulations,
        nb::arg("batch_initial_conditions"),
        "Integrates multiple projectile trajectories in parallel until ground impact"
    );
    
}
