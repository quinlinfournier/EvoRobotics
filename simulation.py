import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time

import constants as c

from world import WORLD
from robot import ROBOT
class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)

        self.directOrGUI = directOrGUI

        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        self.gravity = p.setGravity(0,0,-9.8)

        self.WORLD = WORLD()
        self.ROBOT = ROBOT(solutionID)

    def __del__(self):
        p.disconnect()

    def Run(self):
        for i in range(c.numberOfSteps):
            if self.directOrGUI == "GUI":
                time.sleep(1/60)
            p.stepSimulation()
            self.ROBOT.Sense(i)
            self.ROBOT.Think()
            self.ROBOT.Act(i)

    def Get_Fitness(self):
        self.ROBOT.Get_Fitness()