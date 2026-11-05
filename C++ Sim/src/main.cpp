#include "Simulation.h"
#include <iostream>
#include <fstream>
int main() {
    double v0 = 50.0, theata = 45.0, phi = 90.0, dt = 0.01, total_time = 10;
    std::ifstream configFile("config.txt");
    if (configFile.is_open()) {
        configFile >> v0 >> theata >> phi >> dt >> total_time;
        configFile.close();
        std::cout << "loaded params from config.txt\n";
    }
    else {
        std::cout << "Error loading params from config.txt, using default values\n";
    }
    std::cout << "Firing CannonBall...\n";
    Simulation sim;
    sim.runIntegration(v0, theata, phi, dt, total_time);
    return 0;
}

