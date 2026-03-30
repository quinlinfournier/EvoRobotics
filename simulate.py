import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c
import sys

from simulation import SIMULATION

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]

simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()
fitness = simulation.Get_Fitness()



# np.save("data/backLegTouch.npy", backLegTouch)
# np.save("data/frontLegTouch.npy", frontLegTouch)
