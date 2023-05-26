import numpy as np
import matplotlib.pyplot as plt

class qca_cell():
    position = [0,0,0]
    polarization = 0

    def __init__(self, pos = [0,0,0]):
        self.position = pos
    
    def plot_cell(self, axes):
        # plot qca cell using Parametric equation of a Circle and polarization
        
        theta = np.linspace( 0 , 2 * np.pi , 150 )
        
        radius = 1
        
        a = radius * np.cos( theta )
        b = radius * np.sin( theta )
        
        axes.plot( a, b )
        axes.set_aspect( 1 )
        