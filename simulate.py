import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c
from simulation import SIMULATION

simulation = SIMULATION()
simulation.Run()



# np.save("data/backLegTouch.npy", backLegTouch)
# np.save("data/frontLegTouch.npy", frontLegTouch)
