import sys
import matplotlib.pyplot as plt

sys.path.insert(0, './cell_def`')
#print(sys.path)

from cell_defs.qca_cell import *


#set up axes
figure, axes = plt.subplots()
axes.set_aspect( 1 )
axes.axis([-2, 4, -2, 2])
axes.axis("equal")


#set up the circuit
driver = qca_cell([0,0,0])
driver.driver = True
cell1 = qca_cell([2,0,0])


driver.polarization = -.75
cell1.activation = .66

driver.angle = 45
cell1.angle = 95

circuit = [driver,cell1]

for cell in circuit:
    cell.print_cell()
    cell.draw_cell(axes)


plt.title( 'Circuit' )
plt.show()
