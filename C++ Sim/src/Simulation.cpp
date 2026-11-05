//
// Created by John Hanna on 11/5/26.
//
#include "Simulation.h"
#include <fstream>
#include <iostream>

void Simulation::runIntegration(double vi, double theata, double phi, double dt, double total_time) {
    CannonBall ball(vi, theata, phi);
    std::ofstream outFile("trajectory.csv");
    outFile << "time,x,y,z\n";
    double currentTime = 0;
    while (currentTime <= total_time && ball.y >=0) {
        outFile << currentTime << "," << ball.x << "," << ball.y << "," << ball.z << "\n";
        ball.update(dt);
        currentTime += dt;
    }
    outFile.close();
    std::cout << "Success: Data exported to trajectory.csv\n";
}
