import pybullet as p
import pybullet_data
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time

import constants as c

from world import WORLD
from robot import ROBOT
class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        self.gravity = p.setGravity(0,0,-9.8)

        self.WORLD = WORLD()
        self.ROBOT = ROBOT()



    def __del__(self):
        p.disconnect()

    def Run(self):
        for i in range(c.numberOfSteps):
            print("Simulation step:", i)
            time.sleep(1/60)
            p.stepSimulation()
            self.ROBOT.Sense(i)
            self.ROBOT.Think()
            self.ROBOT.Act(i)
