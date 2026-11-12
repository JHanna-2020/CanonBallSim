#include "CannonBall.h"
#include <stdexcept>

namespace {
    enum StateIndex {
        X = 0,
        Y = 1,
        Z = 2,
        VX = 3,
        VY = 4,
        VZ = 5
    };
}

CannonBall::CannonBall(const std::vector<double>& initial_state)
    : state_vector(initial_state) {
    if (state_vector.size() != 6) {
        throw std::invalid_argument("initial_state must contain 6 elements: [x, y, z, vx, vy, vz]");
    }
}

void CannonBall::update_state(double dt, double gravity) {
    state_vector[X] += state_vector[VX] * dt;
    state_vector[Y] += state_vector[VY] * dt;
    state_vector[Z] += state_vector[VZ] * dt;

    state_vector[VZ] -= gravity * dt;
}

bool CannonBall::has_hit_ground() const {
    return state_vector[Z] <= 0.0;
}
