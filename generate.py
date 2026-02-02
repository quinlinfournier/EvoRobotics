import pyrosim.pyrosim as pyrosim
length = 1
width = 1
height = 1
x = 0
y = 0
z = 0.5
pyrosim.Start_SDF("boxs.sdf")
for k in range(5):
    for j in range(5):
        for i in range(10):
            pyrosim.Send_Cube(name="Box"+str(i), pos=[x+k*1,y+j*1,z+i*1], size=[length*.9**i,width*.9**i,height*.9**i])
pyrosim.End()