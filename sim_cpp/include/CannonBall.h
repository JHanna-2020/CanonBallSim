#pragma once
#include <vector>

class CannonBall {
public:
    std::vector<double> state_vector;
    CannonBall(const std::vector<double> &initial_state);
    void update_state(double dt, double gravity = 9.81);
    bool has_hit_ground() const;

};
