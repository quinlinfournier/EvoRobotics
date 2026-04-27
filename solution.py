import constants as c
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
        self.weight = np.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
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
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1], size=[length,width,height])

        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0,-0.5,1], jointAxis = "1 0 1") 
        pyrosim.Send_Cube(name="BackLeg", pos=[0,-0.5,0], size=[.2,1,.2])
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0,0.5,1], jointAxis = "1 0 1")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0], size=[.2,1,.2])

        pyrosim.Send_Joint(name="Torso_FrontLeftLeg", parent="Torso", child="FrontLeftLeg", type="revolute", position=[-0.4,0.5,1], jointAxis="0 1 1")
        pyrosim.Send_Cube(name="FrontLeftLeg", pos=[0,0.5,0], size=[.2,1,.2])
        pyrosim.Send_Joint(name="Torso_FrontRightLeg", parent="Torso", child="FrontRightLeg", type="revolute", position=[0.4,0.5,1], jointAxis="0 1 1")
        pyrosim.Send_Cube(name="FrontRightLeg", pos=[0,0.5,0], size=[.2,1,.2])

        pyrosim.Send_Joint(name = "Torso_BackLeftLeg" , parent= "Torso" , child = "BackLeftLeg" , type = "revolute", position = [-0.4,-0.5,1], jointAxis = "0 1 1")
        pyrosim.Send_Cube(name="BackLeftLeg", pos=[0,-0.5,0], size=[.2,1,.2])
        pyrosim.Send_Joint(name = "Torso_BackRightLeg" , parent= "Torso" , child = "BackRightLeg" , type = "revolute", position = [0.4,-0.5,1], jointAxis = "0 1 1")
        pyrosim.Send_Cube(name="BackRightLeg", pos=[0,-0.5,0], size=[.2,1,.2])

        # Lower Legs
        pyrosim.Send_Joint(name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg" , child = "FrontLowerLeg" , type = "revolute", position = [0,1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5], size=[.2,.2,.9])
        pyrosim.Send_Joint(name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [0,-1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0,-0.5], size=[.2,.2,.9])

        pyrosim.Send_Joint(name = "FrontLeftLeg_FrontLeftLowerLeg" , parent= "FrontLeftLeg" , child = "FrontLeftLowerLeg" , type = "revolute", position = [0,1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeftLowerLeg", pos=[0,0,-0.5], size=[.2,.2,1])
        pyrosim.Send_Joint(name = "FrontRightLeg_FrontRightLowerLeg" , parent= "FrontRightLeg" , child = "FrontRightLowerLeg" , type = "revolute", position = [0,1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontRightLowerLeg", pos=[0,0,-0.5], size=[.2,.2,1])

        pyrosim.Send_Joint(name = "BackLeftLeg_BackLeftLowerLeg" , parent= "BackLeftLeg" , child = "BackLeftLowerLeg" , type = "revolute", position = [0,-1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeftLowerLeg", pos=[0,0,-0.5], size=[.2,.2,1])
        pyrosim.Send_Joint(name = "BackRightLeg_BackRightLowerLeg" , parent= "BackRightLeg" , child = "BackRightLowerLeg" , type = "revolute", position = [0,-1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackRightLowerLeg", pos=[0,0,-0.5], size=[.2,.2,1])

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")

        # pyrosim.Send_Sensor_Neuron(name = 9, linkName = "FrontLeftLeg")
        # pyrosim.Send_Sensor_Neuron(name = 10, linkName = "FrontRightLeg")
        # pyrosim.Send_Sensor_Neuron(name = 11, linkName = "BackLeftLeg")
        # pyrosim.Send_Sensor_Neuron(name = 12, linkName = "BackRightLeg")

        pyrosim.Send_Sensor_Neuron(name = 3, linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 4, linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 5, linkName = "FrontLeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 6, linkName = "FrontRightLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 7, linkName = "BackLeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 8, linkName = "BackRightLowerLeg")

        pyrosim.Send_Motor_Neuron(name = 9, jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 10, jointName = "Torso_FrontLeg")

        pyrosim.Send_Motor_Neuron(name = 11, jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 12, jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 13, jointName = "Torso_FrontLeftLeg")
        pyrosim.Send_Motor_Neuron(name = 14, jointName = "FrontLeftLeg_FrontLeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 15, jointName = "Torso_FrontRightLeg")
        pyrosim.Send_Motor_Neuron(name = 16, jointName = "FrontRightLeg_FrontRightLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 17, jointName = "Torso_BackLeftLeg")
        pyrosim.Send_Motor_Neuron(name = 18, jointName = "BackLeftLeg_BackLeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 19, jointName = "Torso_BackRightLeg")
        pyrosim.Send_Motor_Neuron(name = 20, jointName = "BackRightLeg_BackRightLowerLeg")  



        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weight[currentRow][currentColumn])
        pyrosim.End()


    def mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weight[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID
