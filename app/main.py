#!/usr/bin/env python
from cell_defs.qca_cell import qca_cell
import matplotlib.pyplot as plt
import numpy as np

# set up axes
figure, axes = plt.subplots()
axes.set_aspect(1)
axes.axis([-4, 6, -2, 2])
axes.axis("equal")


# set up the circuit
driver = qca_cell([0, 0, 0])
driver.driver = True
driver.cellID = 0

cell1 = qca_cell([1, 0, 0])
cell1.cellID = 1

cell2 = qca_cell([2, 0, 0])
cell2.cellID = 2

cell3 = qca_cell([3, 0, 0])
cell3.cellID = 3

driver.polarization = -0.99
driver.activation = 0.66

driver.angle = 60
cell1.angle = 120
cell2.angle = 60
cell3.angle = 90

circuit = [driver, cell1, cell2, cell3]
for cell in circuit:
    cell.electric_field = [0,0,0.125]

cell1.neighbor_list = np.array([driver])
cell2.neighbor_list = np.array([cell1])
cell3.neighbor_list = np.array([cell2])

cell1.calc_hamiltonian()
cell1.calc_polarization_activation()

cell2.calc_hamiltonian()
cell2.calc_polarization_activation()

cell3.calc_hamiltonian()
cell3.calc_polarization_activation()

for cell in circuit:
    cell.print_cell()
    cell.draw_cell(axes)

# plt.title("Circuit")
# plt.savefig("./fig.png")
plt.show()
