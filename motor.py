import pyrosim.pyrosim as pyrosim
import numpy as np
import pybullet as p
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.amplitudeBackLeg
        self.frequency = c.frequencyBackLeg
        self.offset = c.phaseOffsetBackLeg

        if self.jointName == b'Torso_BackLeg':
             self.frequency = self.frequency / 2

        x = np.linspace(0,2*np.pi,c.numberOfSteps)
        self.motorValues = self.amplitude * np.sin(self.frequency * x + self.offset)
    
    def Set_Value(self, robot, desiredAngle):
            pyrosim.Set_Motor_For_Joint(
                bodyIndex = robot.robotId, 
                jointName = self.jointName, 
                controlMode = p.POSITION_CONTROL, 
                targetPosition = desiredAngle, 
                maxForce = 500
            )

    def Save_Values(self):
        np.save("data/" + self.jointName + ".npy", self.motorValues)    