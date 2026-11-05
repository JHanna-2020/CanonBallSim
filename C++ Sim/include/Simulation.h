#pragma once
#include "CannonBall.h"
class Simulation {
public:
    void runIntegration(double vi, double theata, double phi, double dt, double total_time);
};