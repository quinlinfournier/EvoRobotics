import pybullet as p
import pybullet_data
import time

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
for i in range(1000):
    print("Simulation step:", i)
    time.sleep(1/60)
    p.stepSimulation()
p.disconnect()