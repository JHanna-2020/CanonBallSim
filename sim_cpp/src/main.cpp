#include "Simulation.h"
#include <iostream>
#include <vector>

int main() {

    std::vector<double> initial_conditions = {50.0, 0.785398, 0.0};

    std::vector<std::vector<double>> trajectory = run_simulation(initial_conditions);



    return 0;
}
