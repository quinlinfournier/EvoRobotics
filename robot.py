import numpy as np
import pybullet as p
import constants as c
import pyrosim.pyrosim as pyrosim

from pyrosim.neuralNetwork import NEURAL_NETWORK

from sensor import SENSOR
from motor import MOTOR

import simulation
class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")

        self.nn = NEURAL_NETWORK("brain.nndf")

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
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Neurons_Joint(neuronName).encode('ASCII')
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self, desiredAngle)

                print(neuronName, jointName, desiredAngle)

    
    def Think(self):
        self.nn.Update()
        self.nn.Print()

