from app.cell_defs.qca_cell import qca_cell, get_xy
import math
import numpy as np


def test_calc_potential_at_obsv():
    # set up the circuit
    driver = qca_cell([0, 0, 0])
    driver.driver = True
    driver.cellID = 0
    driver.polarization = 1
    driver.angle = 90

    # test points
    obsv_locs = [[1, 0, 0], [2, 0, 0], [2, 2, 2], [-1, 0, 0], [-2, 0, 0],
                 [-2, -2, -2]]

    # manually calculated
    answers = [
        0.2642440206405843, 0.04117734937323406, 0.008398659157986122,
        0.2642440206405843, 0.04117734937323406, 0.008398659157986122
    ]

    for idx, loc in enumerate(obsv_locs):
        return_val = driver.calc_potential_at_obsv(loc)
        assert math.isclose(return_val, answers[idx])


def test_get_true_dot_position():

    obsv_locs = [[1, 0, 0], [2, 2, 2], [-1, 0, 0], [-2, -2, -2]]
    answers = [[
        np.array([1., 0.5, 0.5]),
        np.array([1., 0., 0.]),
        np.array([1., -0.5, 0.5])
    ],
               [
                   np.array([2., 2.5, 2.5]),
                   np.array([2., 2., 2.]),
                   np.array([2., 1.5, 2.5])
               ],
               [
                   np.array([-1., 0.5, 0.5]),
                   np.array([-1., 0., 0.]),
                   np.array([-1., -0.5, 0.5])
               ],
               [
                   np.array([-2., -1.5, -1.5]),
                   np.array([-2., -2., -2.]),
                   np.array([-2., -2.5, -1.5])
               ]]

    testcell = qca_cell([0, 0, 0])
    for idx, loc in enumerate(obsv_locs):
        testcell = qca_cell(loc)
        return_val = testcell.get_true_dot_position()
        print("ret:", return_val)
        print("ans:", answers[idx])
        assert np.array_equal(return_val, answers[idx])


def test_get_xy():
    angles = [45, 90, 135, 180, 225, 270, 315, 360]
    answers = [[0.707106, 0.707106], [0, 1], [-0.707106, 0.707106], [-1, 0],
               [-0.707106, -0.707106], [0, -1], [0.707106, -0.707106], [1, 0]]
    radius = 1
    for idx, angle in enumerate(angles):
        return_val = get_xy(angle, radius)
        assert math.isclose(return_val[0], answers[idx][0], rel_tol=1e3)
        assert math.isclose(return_val[1], answers[idx][1], rel_tol=1e3)
