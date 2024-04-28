import numpy as np
import matplotlib.pyplot as plt
import math


class qca_cell:
    cellID = 0
    # Type = 'Node';% Driver/Node
    driver = False
    center_position = [0, 0, 0]
    angle = 90
    # dot_posistion = [] #position of dots relative to cell center
    # dot_position =  0.5*[0,1,1; \
    #                 0,0,0; \
    #                 0,-1,1; ]
    # dot_position = []

    hamiltonian = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    wavefunction = np.array([0, 0, 0])

    polarization = 0
    activation = 1
    characteristic_length = 1  # [nm]
    gamma = 0.05  # [eV] from Henry, Blair 2017: 0 < gamma < 0.3*Ek
    # for now, 0 <--> 0.1265 for characteristic length
    # 1nm
    electric_field = np.array([0, 0, 0])  # Electric Field [V/nm]
    neighbor_list = []  # this Cell's Neighbor id's

    # hardcoded constants for now
    qe = 1  # charge of electron
    epsilon_0 = 8.854e-12  # Vacuum Permitivity [C/(V*m)]
    qeV2J = 1.602e-19  # Conversion factor or Charge of Electron[J]
    qeC2e = -1.60217662e-19  # J

    # Helpful operators we just keep around
    Z = np.array([[-1, 0, 0], [0, 0, 0], [0, 0, 1]])

    Pnn = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])

    def __init__(self, pos=[0, 0, 0]):
        self.center_position = pos

    def print_cell(self):
        cell_info = (
            "Cell: "
            + str(self.cellID)
            + " Polarization: "
            + str(self.polarization)
            + " Activation: "
            + str(self.activation)
            + " Position: "
            + str(self.center_position)
        )
        print(cell_info)

    def internal_potential(self):
        k = 1 / (4 * math.pi * self.epsilon_0) * self.qeC2e
        h = -1 * self.qe
        internal_potential = np.array([0.0, 0.0, 0.0])

        true_dot_pos = np.array(self.get_true_dot_position())
        # print("Cell(", self.cellID, "): True Dot Pos:\n", true_dot_pos)

        # ZERO DOT
        displacement = np.subtract(true_dot_pos[0], true_dot_pos[1])
        distance = np.sum(np.square(displacement))
        u12 = self.qe * h / distance
        internal_potential[0] = k * u12

        # NULL DOT
        internal_potential[1] = 0

        # ONE DOT
        displacement = np.subtract(true_dot_pos[1], true_dot_pos[2])
        distance = np.sum(np.square(displacement))
        u23 = self.qe * h / distance

        internal_potential[2] = k * u23
        print("Cell(", self.cellID, "): Internal Potential:", internal_potential)
        return internal_potential

    # Calculates the potential that this qca cell
    # is causing at some observation location
    def calc_potential_at_obsv(self, obsvLocation):
        # calc the charge at each dot based on Act&Pol
        qe = self.qe
        time = 0

        total_cell_charge = np.array(
            [
                qe * self.activation * (1 / 2) * (1 - self.get_polarization(time)),
                1 - self.activation - 1,
                qe * self.activation * (1 / 2) * (self.get_polarization(time) + 1),
            ]
        )
        # -1 on qN is for the null charge of the null dot
        # charge_str = "q0: " + str(total_cell_charge[0]) + " qN: " + str(
        #     total_cell_charge[1]) + " q1: " + str(total_cell_charge[2])
        # print(charge_str)

        # find distance between obsvLoc and each self.trueDotPosition()
        distance = np.array([1, 1, 1])  # meters
        true_dot_pos = np.array(self.get_true_dot_position())
        displacement = np.subtract(obsvLocation, true_dot_pos)

        distance = np.sqrt(np.sum(np.square(displacement), axis=1))

        # charge_potential calc factored out multiply by the sum of the charge
        # on each dot after it has been divided by its distance from obsvLoc
        distance_nm = np.multiply(distance, 1e-9)
        potential = np.multiply(
            (1 / (4 * math.pi * self.epsilon_0) * self.qeC2e),
            np.sum(np.divide(total_cell_charge, distance_nm)),
        )

        return potential

    def potential_caused_by_cell_list(self, neighbor_list=""):
        if len(neighbor_list) == 0:
            neighbor_list = self.neighbor_list
        self_true_dot_pos = np.array(self.get_true_dot_position())

        self_pot_by_neighbors = np.zeros(np.shape(self_true_dot_pos)[0])

        for cell in neighbor_list:
            for idx, dot in enumerate(self_true_dot_pos):
                self_pot_by_neighbors[idx] += cell.calc_potential_at_obsv(dot)
        return self_pot_by_neighbors

    def calc_polarization_activation(self, normpsi=""):
        if self.driver:
            # don't relax drivers
            return
        # given some normpsi, set wavefunc and calculate pol/act
        if not normpsi:
            [eig_vals, eig_vecs] = np.linalg.eig(self.hamiltonian)

            idx = eig_vals.argsort()
            eig_vals = eig_vals[idx]
            eig_vecs = eig_vecs[:, idx]

            print("eigVals: ", eig_vals)
            print("eigVecs:\n", eig_vecs)
            normpsi = eig_vecs[:, 0]  # ground state

        self.wavefunction = normpsi
        self.polarization = np.matmul(np.matmul(normpsi.transpose(), self.Z), normpsi)
        self.activation = 1 - np.matmul(np.matmul(normpsi.transpose(), self.Pnn), normpsi)
        print(self.wavefunction)
        print(self.polarization)
        print(self.activation)
        print("end")

    def calc_hamiltonian(self):  # hardcoding mobile charge atm
        # potential at self_dots due to all others
        dot_potential = self.potential_caused_by_cell_list(self.neighbor_list)
        print("Cell(", self.cellID, "): Dot Potentials:", dot_potential)

        gamma_matrix = -self.gamma * np.matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        hamiltonian = np.add(-1 * np.diag(dot_potential), gamma_matrix)

        print("Cell(", self.cellID, "): Hamiltonian:\n", hamiltonian)

        [q0_pos, qN_pos, q1_pos] = self.get_true_dot_position()
        #h = abs(obj.DotPosition(2, 3)-obj.DotPosition(1, 3))
        h = abs(q0_pos - qN_pos)
        # %Field over entire height of cell
        # x = abs(obj.DotPosition(3, 1)-obj.DotPosition(1, 1))
        # y = abs(obj.DotPosition(3, 2)-obj.DotPosition(1, 2))
        lengthh = np.array([x, y, 0])

        inputFieldBias = -self.electric_field * lengthh.transpose()
        Eo = (
            np.square(self.qe)
            * (self.qeV2J)
            / (4 * math.pi * self.epsilon_0 * self.characteristic_length * 1e-9)
            * (1 - 1 / math.sqrt(2))
        )
        kink_strength = 0.1
        print("Cell(", self.cellID, "): ", kink_strength, "*Eo:\n", kink_strength * Eo)


        # add kink strength
        hamiltonian[1, 1] = hamiltonian[1, 1] + kink_strength * Eo
        # add clock E
        hamiltonian[1, 1] = hamiltonian[1, 1] + self.electric_field * h
        print("Cell(", self.cellID, "): Hamiltonian:\n", hamiltonian)
        
        # %add input field to 0 dot
        # hamiltonian[0, 0] = hamiltonian[0, 0] + (-inputFieldBias)/2
        # %add input field to 1 dot
        # hamiltonian[2, 2] = hamiltonian[2, 2] + inputFieldBias/2

        # Calculate internal potential and add them to hamiltonian
        hamiltonian = np.add(np.diag(self.internal_potential()), hamiltonian)
        print("Cell(", self.cellID, "): Hamiltonian:\n", hamiltonian)
        self.hamiltonian = hamiltonian
        return hamiltonian

    def get_polarization(self, time=""):
        return self.polarization

    def get_true_dot_position(self):
        q1_xy = get_xy(self.angle, 1)
        q2_xy = get_xy(self.angle, 0)
        q3_xy = get_xy(self.angle, -1)

        q1_xyz = np.append(q1_xy, 1)
        q2_xyz = np.append(q2_xy, 0)
        q3_xyz = np.append(q3_xy, 1)

        q1_pos = q1_xyz * 0.5 + self.center_position
        q2_pos = q2_xyz * 0.5 + self.center_position
        q3_pos = q3_xyz * 0.5 + self.center_position

        return np.array([q1_pos, q2_pos, q3_pos])

    def draw_cell(self, axes):
        # Get dot positions
        [q0_pos, qN_pos, q1_pos] = self.get_true_dot_position()

        # define dot sites
        radius = 0.25
        q0_site = plt.Circle(q0_pos[:2], radius, ec="Black", fc="White")
        qN_site = plt.Circle(qN_pos[:2], radius * 3 / 4, ec="Black", fc="White")
        q1_site = plt.Circle(q1_pos[:2], radius, ec="Black", fc="White")

        # define lines
        pt1_1 = get_xy(self.angle, radius * 3 / 4) + np.array(
            [self.center_position[0], self.center_position[1]]
        )

        pt1_2 = get_xy(self.angle, 0.5 * self.characteristic_length - radius) + np.array(
            [self.center_position[0], self.center_position[1]]
        )

        pt2_1 = get_xy(self.angle, -radius * 3 / 4) + np.array(
            [self.center_position[0], self.center_position[1]]
        )

        pt2_2 = get_xy(self.angle, -0.5 * self.characteristic_length + radius) + np.array(
            [self.center_position[0], self.center_position[1]]
        )

        line1 = plt.Line2D([pt1_1[0], pt1_2[0]], [pt1_1[1], pt1_2[1]], linewidth=1.5, c="Black")
        line2 = plt.Line2D([pt2_1[0], pt2_2[0]], [pt2_1[1], pt2_2[1]], linewidth=1.5, c="Black")

        # draw electron polarization
        q0 = (self.activation / 2) * (1 - self.polarization)
        qN = 1 - self.activation
        q1 = (self.activation / 2) * (1 + self.polarization)

        # print(q0, qN, q1)

        scalefactor = 0.90

        if self.driver:
            color = "green"
        else:
            color = "red"

        e0 = plt.Circle(q0_pos[:2], q0 * scalefactor * radius, ec=color, fc=color)
        eN = plt.Circle(qN_pos[:2], qN * scalefactor * radius * 3 / 4, ec=color, fc=color)
        e1 = plt.Circle(q1_pos[:2], q1 * scalefactor * radius, ec=color, fc=color)

        # add everything to patches list
        patches = [line1, line2, q0_site, qN_site, q1_site, e0, eN, e1]

        # add patches to plot
        for patch in patches:
            axes.add_artist(patch)


def get_xy(angle, radius):
    # find the end point
    y = radius * math.sin(math.radians(angle))
    x = radius * math.cos(math.radians(angle))
    xy = np.array([x, y])
    return xy
