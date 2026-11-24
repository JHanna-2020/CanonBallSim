#include "Simulation.h"
#include "CannonBall.h"
#include <algorithm>
#include <cmath>
#include <thread>

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
std::vector<std::vector<std::vector<double>>> run_multiple_simulations(
    const std::vector<std::vector<double>> & batch_initial_conditions){
        std::size_t n_balls = batch_initial_conditions.size();
        std::vector<std::vector<std::vector<double>>> results(n_balls);
        if(n_balls == 0){
            return results;
        }
        unsigned int hw_threads = std::thread::hardware_concurrency();
        std::size_t num_threads = std::min<std::size_t>(
            n_balls, hw_threads > 0 ? hw_threads : 4 
        );
        std::vector<std::thread> threads;
        threads.reserve(num_threads);

        for(std::size_t t = 0; t < num_threads; ++t){
            threads.emplace_back([&, t](){
                for(std::size_t i = t; i < n_balls; i+= num_threads){
                    results[i] = run_simulation(batch_initial_conditions[i]);
                }
            });
        }
        for(auto& thread : threads){
            thread.join();
        }
        return results;

    }

