#pragma once
class CannonBall {
public:
    double x,y,z;
    double vx,vy,vz;
    CannonBall(double vi, double theata, double phi);
    void update(double dt);
};