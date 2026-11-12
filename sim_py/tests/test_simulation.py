import math
import unittest
from sim_cpp import sim_engine


class TestSimulation(unittest.TestCase):
    def test_ground_impact_termination(self):
        trajectory = sim_engine.run_simulation([50.0, math.radians(45.0), 0.0])
        self.assertGreater(len(trajectory), 1)
        self.assertEqual(trajectory[0][2], 0.0)
        self.assertLessEqual(trajectory[-1][2], 0.0)

    def test_vertical_shot(self):
        v0 = 30.0
        trajectory = sim_engine.run_simulation([v0, math.radians(90.0), 0.0])
        final_x, final_y = trajectory[-1][0], trajectory[-1][1]
        max_z = max(state[2] for state in trajectory)

        self.assertAlmostEqual(final_x, 0.0, places=4)
        self.assertAlmostEqual(final_y, 0.0, places=4)
        # Analytic peak height: v0^2 / (2 * g) ≈ 45.87 m
        self.assertAlmostEqual(max_z, (v0 ** 2) / (2 * 9.81), delta=0.5)

    def test_horizontal_range_45_deg(self):
        v0 = 50.0
        trajectory = sim_engine.run_simulation([v0, math.radians(45.0), 0.0])
        final_x = trajectory[-1][0]
        # Analytic range: v0^2 * sin(2*theta) / g ≈ 254.84 m
        self.assertAlmostEqual(final_x, (v0 ** 2) / 9.81, delta=2.0)

    def test_azimuth_90_deg_moves_along_y(self):
        trajectory = sim_engine.run_simulation([50.0, math.radians(45.0), math.radians(90.0)])
        final_x, final_y = trajectory[-1][0], trajectory[-1][1]
        self.assertAlmostEqual(final_x, 0.0, places=4)
        self.assertGreater(final_y, 200.0)


if __name__ == "__main__":
    unittest.main()
