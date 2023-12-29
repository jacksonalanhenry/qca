from app.cell_defs.qca_cell import *
import math
import sys

sys.path.insert(0, './app')

def test_get_xy():
    angles = [45, 90, 135, 180, 225, 270, 315, 360]
    answers = [[0.707106,0.707106],
               [0,1],
               [-0.707106,0.707106],
               [-1,0],
               [-0.707106,-0.707106],
               [0,-1],
               [0.707106,-0.707106],
               [1,0]]
    radius = 1
    for idx, angle in enumerate(angles):
        return_val = get_xy(angle, radius)
        assert math.isclose(return_val[0], answers[idx][0], rel_tol=1e3)
        assert math.isclose(return_val[1], answers[idx][1], rel_tol=1e3)
        assert False


def test_calc_potential_at_obsv():
    # set up the circuit
    driver = qca_cell([0, 0, 0])
    driver.driver = True
    driver.cellID = 0
    driver.polarization = 1
    driver.angle = 90

    #test points
    obsv_locs = [[1,0,0],[2,0,0],[2,2,2],[-1,0,0],[-2,0,0],[-2,-2,-2]]

    #manually calculated
    answers = [0.2642440206405843,
                0.04117734937323406,
                0.008398659157986122,
                0.2642440206405843,
                0.04117734937323406,
                0.008398659157986122]

    for idx, loc in enumerate(obsv_locs):
        return_val = driver.calc_potential_at_obsv(loc)
        assert math.isclose(return_val, answers[idx])
