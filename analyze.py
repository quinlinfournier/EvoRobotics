import numpy as np
import matplotlib.pyplot as plt
backLegTouch = np.load("data/backLegTouch.npy")
frontLegTouch = np.load("data/frontLegTouch.npy")
print(backLegTouch)
plt.plot(backLegTouch, label="Back Leg", linewidth=4)
plt.plot(frontLegTouch, label="Front Leg", linewidth=1)

legend = plt.legend()

legend.get_frame().set_facecolor('C0')

plt.show()