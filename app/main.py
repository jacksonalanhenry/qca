from cell_defs.qca_cell import qca_cell
import sys
import matplotlib.pyplot as plt
import numpy as np

# sys.path.insert(0, './cell_def`')
# print(sys.path)


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


driver.polarization = 0.99
driver.activation = 0.66

driver.angle = 120
cell1.angle = 90
cell2.angle = 90

cell1.neighbor_list = np.array([driver, cell2])
cell2.neighbor_list = np.array([cell1])
cell1.calc_hamiltonian()
cell1.calc_polarization_activation()


circuit = [driver, cell1, cell2]

for cell in circuit:
    cell.print_cell()
    cell.draw_cell(axes)

# plt.title("Circuit")
# plt.savefig("./fig.png")
plt.show()
