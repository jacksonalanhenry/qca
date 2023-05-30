import sys
import matplotlib.pyplot as plt

sys.path.insert(0, '/home/jahenry/qca/cell_def`')
#print(sys.path)

from cell_defs.qca_cell import *

#import qca_cell


mycell = qca_cell()

mycell.print_cell()


#set up axes
figure, axes = plt.subplots()

axes.axis([-2, 4,-2, 4])
axes.axis("equal")

mycell = qca_cell([0,1,0])

mycell.draw_cell(axes)

axes.set_aspect( 1 )
plt.title( 'Circuit' )
plt.show()
