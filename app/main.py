from cell_defs.qca_cell import *
import sys
import matplotlib.pyplot as plt

sys.path.insert(0, './cell_def`')
# print(sys.path)


# set up axes
figure, axes = plt.subplots()
axes.set_aspect(1)
axes.axis([-2, 4, -2, 2])
axes.axis("equal")


# set up the circuit
driver = qca_cell([0, 0, 0])
driver.driver = True
cell1 = qca_cell([2, 0, 0])

# cell1.driver = False

driver.polarization = -.75
cell1.activation = .66

driver.angle = 90
cell1.angle = 90

driver.calc_potential_at_obsv([1, 0, 0])

circuit = [driver, cell1]

for cell in circuit:
    cell.print_cell()
    cell.draw_cell(axes)


plt.title('Circuit')
# plt.show()
plt.savefig('./fig.png')
plt.show()
