import numpy as np
import matplotlib.pyplot as plt


fitnessFuntionA = np.loadtxt("fitnessMatrix.txt", delimiter=",")

print(fitnessFuntionA)

plt.plot(fitnessFuntionA, label="Fitness Function A", linewidth=2)

legend = plt.legend()

legend.get_frame().set_facecolor('white')

plt.show()