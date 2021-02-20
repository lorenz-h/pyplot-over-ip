from typing import Mapping
import pyplot_over_ip as pltip
import matplotlib.pyplot as plt
import numpy as np

plt.plot(np.random.random((7)), np.random.random((7)))
pltip.setup("127.0.0.1", "test")
pltip.show()
