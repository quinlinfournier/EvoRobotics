import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np


physicsClient = p.connect(p.GUI)
# Load plane.urdf
p.setAdditionalSearchPath(pybullet_data.getDataPath()) 
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
# Adding Forces
p.setGravity(0,0,-9.8)
# Adding Floor
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
# Create a simple box in the simulation
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegTouch = np.zeros(1000)
frontLegTouch = np.zeros(1000)
for i in range(1000):
    # print("Simulation step:", i)
    time.sleep(1/60)
    p.stepSimulation()
    backLegTouch[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegTouch[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
print(backLegTouch[i])
np.save("data/backLegTouch.npy", backLegTouch)
np.save("data/frontLegTouch.npy", frontLegTouch)
p.disconnect()