#pragma once
#include <vector>

std::vector<std::vector<double>> run_simulation(const std::vector<double>& initial_conditions);
std::vector<std::vector<std::vector<double>>> run_multiple_simulations(const std::vector<std::vector<double>>& batch_initial_conditions);
