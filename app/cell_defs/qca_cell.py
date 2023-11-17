import numpy as np
import matplotlib.pyplot as plt
import math

class qca_cell():
    cellID = 0
    #Type = 'Node';% Driver/Node
    driver = False
    center_position = [0,0,0]
    angle = 90;
    #dot_posistion = [] #position of dots relative to cell center
    # dot_position =  0.5*[0,1,1; \
    #                 0,0,0; \
    #                 0,-1,1; ]
    #dot_position = []

    hamiltonian = np.array([[ 0, 0, 0],
                            [ 0, 0, 0],
                            [ 0, 0, 0]])

    wavefunction = np.array([0, 0, 0])

    polarization = 0
    activation = 1
    characteristic_length = 1; # [nm]
    gamma = 0.05;   # [eV] from Henry, Blair 2017: 0 < gamma < 0.3*Ek 
                    # for now, 0 <--> 0.1265 for characteristic length
                    # 1nm
    electric_field = [0, 0, 0]; #Electric Field [V/nm]
    neighborList = []; #this Cell's Neighbor id's
    


    #Helpful operators we just keep around
    Z = np.array([[-1, 0, 0],
                  [ 0, 0, 0],
                  [ 0, 0, 1]])

    Pnn = np.array([[0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0]])




    def __init__(self, pos = [0,0,0]):
        self.center_position = pos

    def print_cell(self):
        cell_info = "Cell: " + str(self.cellID) + \
        " Polarization: " + str(self.polarization) + \
        " Activation: " + str(self.activation) + \
        " Position: " + str(self.center_position)
        print(cell_info)

    def get_true_dot_position(self):
        q1_xy = get_xy(self.angle,1)
        q2_xy = get_xy(self.angle,0)
        q3_xy = get_xy(self.angle,-1)

        q1_xyz = np.append(q1_xy,1)
        q2_xyz = np.append(q2_xy,0)
        q3_xyz = np.append(q3_xy,-1)

        q1_pos = q1_xyz  * 0.5 + self.center_position
        q2_pos = q2_xyz  * 0.5 + self.center_position
        q3_pos = q3_xyz  * 0.5 + self.center_position

        return [q1_pos,q2_pos,q3_pos]


    def calc_polarization_activation(self, normpsi):
        if self.driver:
            #don't relax drivers
            return
        else:
            #given some normpsi, set wavefunc and calculate pol/act
            self.Wavefunction = normpsi
            self.Polarization = normpsi.transpose() * self.Z * normpsi
            self.Activation = 1 - normpsi.transpose() * self.Pnn * normpsi





    def draw_cell(self, axes):
        # Get dot positions                
        [q0_pos, qN_pos, q1_pos] = self.get_true_dot_position()

        #define dot sites
        radius = 0.25
        q0_site=plt.Circle(q0_pos[:2], radius, ec="Black", fc="White")
        qN_site=plt.Circle(qN_pos[:2], radius*3/4, ec="Black", fc="White")
        q1_site=plt.Circle(q1_pos[:2], radius, ec="Black", fc="White")

        #define lines
        pt1_1 = get_xy(self.angle,radius*3/4) + \
            np.array([self.center_position[0],self.center_position[1]])

        pt1_2 = get_xy(self.angle, 0.5*self.characteristic_length-radius) + \
            np.array([self.center_position[0],self.center_position[1]])

        pt2_1 = get_xy(self.angle,-radius*3/4) + \
            np.array([self.center_position[0],self.center_position[1]])

        pt2_2 = get_xy(self.angle, -0.5*self.characteristic_length+radius) + \
            np.array([self.center_position[0],self.center_position[1]])

        line1 = plt.Line2D( [pt1_1[0], pt1_2[0]],[pt1_1[1], pt1_2[1]], \
                linewidth=1.5, c="Black" )
        line2 = plt.Line2D( [pt2_1[0], pt2_2[0]],[pt2_1[1], pt2_2[1]], \
                linewidth=1.5, c="Black" )

        #draw electron polarization
        q0 = (self.activation/2)*(1-self.polarization)
        qN = 1 - self.activation
        q1 = (self.activation/2)*(1+self.polarization)

        print(q0,qN,q1)

        scalefactor = 0.90

        if self.driver:
            color = "green"
        else:
            color = "red"

        e0=plt.Circle(q0_pos[:2], q0*scalefactor*radius, ec=color, fc=color)
        eN=plt.Circle(qN_pos[:2], qN*scalefactor*radius*3/4, ec=color, fc=color)
        e1=plt.Circle(q1_pos[:2], q1*scalefactor*radius, ec=color, fc=color)


        # add everything to patches list
        patches = [line1,line2,q0_site,qN_site,q1_site,e0,eN,e1]

        #add patches to plot
        for patch in patches:
            axes.add_artist(patch)





def get_xy(angle,radius):
    # find the end point
    y = radius * math.sin(math.radians(angle))
    x = radius * math.cos(math.radians(angle))
    xy = np.array([x,y])
    return xy
