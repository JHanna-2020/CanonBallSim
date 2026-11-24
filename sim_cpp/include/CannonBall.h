#pragma once
#include <vector>
#define GRAVITY 9.81
class CannonBall {
public:
    std::vector<double> state_vector;
    CannonBall(const std::vector<double> &initial_state);
    void update_state(double dt);
    bool has_hit_ground() const;

};
