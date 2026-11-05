#include "Simulation.h"
#include <iostream>
int main() {
    std::cout << "Simulation started" << std::endl;
    Simulation sim;
    sim.runIntegration(50.0, 45.0, 0.0, 0.01, 10.0);

}