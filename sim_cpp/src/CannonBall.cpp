#include "CannonBall.h"
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
}

void CannonBall::update_state(double dt) {
    state_vector[X] += state_vector[VX] * dt;
    state_vector[Y] += state_vector[VY] * dt;
    state_vector[Z] += state_vector[VZ] * dt;

    state_vector[VZ] -= GRAVITY * dt;
}

bool CannonBall::has_hit_ground() const {
    return state_vector[Z] <= 0.0;
}
