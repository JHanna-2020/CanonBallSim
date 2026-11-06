//
// Created by John Hanna on 11/5/26.
//
#include "CannonBall.h"
#include <cmath>
const double pi = 3.14159265358979323846;
double toRadians(double degrees) {
    return degrees * pi / 180;
}
CannonBall::CannonBall(double vi, double theata, double phi) {
    x = 0;
    y =0;
    z = 0;
    vx = vi *std::sin(toRadians(theata)) * std::cos(toRadians(phi));
    vy = vi *std::sin(toRadians(theata)) * std::sin(toRadians(phi));
    vz = vi *std::cos(toRadians(theata));

}
void CannonBall::update(double dt) {
    x = x+vx*dt;
    y = y+vy*dt;
    z = z+vz*dt;
    double gravity = -9.81;
    vy = vy +0.5 *gravity*dt;

}