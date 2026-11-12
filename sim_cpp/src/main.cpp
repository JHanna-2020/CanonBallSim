#include "Simulation.h"
#include <vector>

int main() {
    std::vector<double> initial_conditions = {50.0, 0.785398, 0.0};
    run_simulation(initial_conditions);
    return 0;
}
