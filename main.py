import sys
import matplotlib.pyplot as plt

sys.path.insert(0, '/home/jahenry/qca/cell_def`')
#print(sys.path)

from cell_defs.qca_cell import *

#import qca_cell


mycell = qca_cell()

mycell.print_cell()
