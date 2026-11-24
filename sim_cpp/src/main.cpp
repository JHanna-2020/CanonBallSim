#include "Simulation.h"
#include <cmath>
#include <random>
#include <vector>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());

    std::uniform_real_distribution<double> v0_dist(5.0, 150.0);
    std::uniform_real_distribution<double> theta_dist(0.05, M_PI / 2.0 - 0.05);
    std::uniform_real_distribution<double> phi_dist(0.0, 2.0 * M_PI);

    const std::size_t num_balls = 1000;
    std::vector<std::vector<double>> batch_initial_conditions;
    batch_initial_conditions.reserve(num_balls);
    for(std::size_t i = 0; i < num_balls; ++i){
        batch_initial_conditions.push_back({
            v0_dist(gen),
            theta_dist(gen),
            phi_dist(gen)
        });
    }
    run_multiple_simulations(batch_initial_conditions);
    return 0;
}