import time

import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random

length = 1
width = 1
height = 1
x = 0
y = 0
z = 0.5

class SOLUTION:

    def __init__(self, nextAvailableID):
        self.solution = 6
        self.weight = np.random.rand(3,2) * 2 - 1
        self.myID = nextAvailableID

    def Start_Simulation(self, directOrGUI):
        if not os.path.exists("world.sdf"):
            self.Create_World()
        if not os.path.exists("body.urdf"):
            self.Generate_Body()

        self.Generate_Brain()

        os.system("start /B python simulate.py " + directOrGUI + " " + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        
        # 1. Wait for the file to exist
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
            
        # 2. Keep trying to open it until Windows drops the lock
        while True:
            try:
                with open(fitnessFileName, "r") as f:
                    self.fitness = float(f.read())
                break # If it successfully opens and reads, break out of the loop!
            except PermissionError:
                time.sleep(0.01) # If Windows says no, wait a tiny fraction of a second and try again
                
        # 3. Clean up
        os.system("del " + fitnessFileName)

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-3,3,z], size=[length,width,height])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="BackLeg", pos=[0,0,0.5], size=[length,width,height])
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "BackLeg" , child = "Torso" , type = "revolute", position = [.5,0,1])
        pyrosim.Send_Cube(name="Torso", pos=[0.5,0,0.5], size=[length,width,height])
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [1,0,0])
        pyrosim.Send_Cube(name="FrontLeg", pos=[.5,0,-.5], size=[length,width,height])

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")

        pyrosim.Send_Motor_Neuron(name = 3, jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 4, jointName = "Torso_FrontLeg")

        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + 3, weight = self.weight[currentRow][currentColumn])
        
        pyrosim.End()


    def mutate(self):
        randomRow = random.randint(0, 2)
        randomColumn = random.randint(0, 1)
        self.weight[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID
