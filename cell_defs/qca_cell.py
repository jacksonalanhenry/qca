import numpy as np
import matplotlib.pyplot as plt

class qca_cell():
    cellID = 0
    #Type = 'Node';% Driver/Node
    center_position = [0,0,0]
    #dot_posistion = [] #position of dots relative to cell center
    # dot_position =  0.5*[0,1,1; \
    #                 0,0,0; \
    #                 0,-1,1; ]
    #dot_position = []
    
    polarization = 0
    characteristic_length = 1; # [nm]
    gamma = 0.05;   # [eV] from Henry, Blair 2017: 0 < gamma < 0.3*Ek 
                    # for now, 0 <--> 0.1265 for characteristic length
                    # 1nm
    electric_field = [0, 0, 0]; #Electric Field [V/nm]
    neighborList = []; #this Cell's Neighbor id's

    def __init__(self, pos = [0,0,0]):
        self.center_position = pos
    
    def print_cell(self):
        cell_info = "Cell: " + str(self.cellID) + \
        " Polarization: " + str(self.polarization) + \
        " Position: " + str(self.center_position) + \
        " True Pos: " + str(self.get_true_dot_position())
        print(cell_info)

    def get_true_dot_position(self):
        q1_pos = np.array([0,1,1]) * 0.5 + self.center_position
        q2_pos = np.array([0,0,0]) * 0.5 + self.center_position
        q3_pos = np.array([0,-1,1]) * 0.5 + self.center_position

        return [q1_pos,q2_pos,q3_pos]

    def draw_cell(self, axes):
        # plot qca cell using                
        [q1_pos, q2_pos, q3_pos] = self.get_true_dot_position()

        #define dot sites
        radius = 0.25
        q1=plt.Circle(q1_pos[:2], radius)
        q2=plt.Circle(q2_pos[:2], radius*3/4)
        q3=plt.Circle(q3_pos[:2], radius)

        #define lines
        x1, y1 = [-1, 12], [1, 4]
        x2, y2 = [1, 10], [3, 2]
        line1 = plt.Line2D( [q1_pos[0], q3_pos[0]], [q1_pos[1], q3_pos[1]], linewidth=2.5 )
        #, linewidth=None, linestyle=None, color=None, marker=None


        patches = {q1,q2,q3,line1}

        #add circles to plot
        for patch in patches:
            axes.add_artist(patch)

        # axes.plot( a,b )
        