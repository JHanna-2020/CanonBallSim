#include "CannonBall.h"

CannonBall::CannonBall(const std::vector<double>& initial_state)
    : state_vector(initial_state) {}

void CannonBall::update_state(double dt, double gravity) {
    // state_vector = [x, y, z, vx, vy, vz]
    // Position updates: p = p + v * dt
    state_vector[0] += state_vector[3] * dt; // x += vx * dt
    state_vector[1] += state_vector[4] * dt; // y += vy * dt
    state_vector[2] += state_vector[5] * dt; // z += vz * dt

    // Velocity update: gravity acts downwards on vz
    state_vector[5] -= gravity * dt;         // vz -= g * dt
}

bool CannonBall::has_hit_ground() const {
    return state_vector[2] <= 0.0; // z <= 0
}
