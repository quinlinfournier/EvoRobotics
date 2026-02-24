import numpy as np
import constants as c
from pyrosim import pyrosim

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = np.zeros(c.numberOfSteps)

    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Save_Values(self):
        np.save("data/" + self.linkName + ".npy", self.values)
