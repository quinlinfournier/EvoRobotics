import numpy as np
import pybullet as p
import constants as c
import pyrosim.pyrosim as pyrosim

from sensor import SENSOR
from motor import MOTOR

import simulation
class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        # self.x = np.linspace(0,2*np.pi,c.numberOfSteps)

        # self.targetAnglesBack = np.zeros(c.numberOfSteps)
        # self.targetAnglesFront = np.zeros(c.numberOfSteps)


    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for sensor in self.sensors:
            self.value = self.sensors[sensor].Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, t):
        for motor in self.motors:
            self.motors[motor].Set_Value(self, t)

