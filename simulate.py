import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np

amplitudeFrontLeg = np.pi/4
frequencyFrontLeg = 4
phaseOffsetFrontLeg = 0
amplitudeBackLeg = np.pi/4
frequencyBackLeg = 4
phaseOffsetBackLeg = np.pi/2


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

x = np.linspace(0,2*np.pi,1000)

targetAnglesBack = np.zeros(1000)
targetAnglesFront = np.zeros(1000)
backLegTouch = np.zeros(1000)
frontLegTouch = np.zeros(1000)

for i in range(1000):
    # print("Simulation step:", i)
    time.sleep(1/60)
    p.stepSimulation()
    backLegTouch[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegTouch[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    targetAnglesFront[i] = (np.sin(x[i]*frequencyFrontLeg + phaseOffsetFrontLeg))*(amplitudeFrontLeg)
    targetAnglesBack[i] = (np.sin(x[i]*frequencyBackLeg + phaseOffsetBackLeg))*(amplitudeBackLeg)

    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b'Torso_BackLeg', controlMode=p.POSITION_CONTROL, targetPosition=targetAnglesBack[i], maxForce=500)
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b'Torso_FrontLeg', controlMode=p.POSITION_CONTROL, targetPosition=targetAnglesFront[i], maxForce=500)

print(backLegTouch[i])
# np.save("data/targetAnglesFront.npy", targetAnglesFront)
# np.save("data/targetAnglesBack.npy", targetAnglesBack)
np.save("data/backLegTouch.npy", backLegTouch)
np.save("data/frontLegTouch.npy", frontLegTouch)
p.disconnect()