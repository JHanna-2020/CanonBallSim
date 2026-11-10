#include "Simulation.h"
#include "CannonBall.h"
#include <cmath>

std::vector<std::vector<double>> run_simulation(const std::vector<double>& initial_conditions) {
    double v0 = initial_conditions[0];
    double theta = initial_conditions[1]; // radians
    double phi = initial_conditions[2];   // radians

    double vx = v0 * std::cos(theta) * std::cos(phi);
    double vy = v0 * std::cos(theta) * std::sin(phi);
    double vz = v0 * std::sin(theta);

    CannonBall ball({0.0, 0.0, 0.0, vx, vy, vz});
    std::vector<std::vector<double>> trajectory;
    double dt = 0.01;

    // Use do...while so the ball launches before checking for ground collision
    do {
        trajectory.push_back(ball.state_vector);
        ball.update_state(dt);
    } while (!ball.has_hit_ground());

    trajectory.push_back(ball.state_vector); // final impact point
    return trajectory;
}
