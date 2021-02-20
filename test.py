import pyplot_over_ip as pltip
import matplotlib.pyplot as plt


# run this once when starting your script.
pltip.setup("127.0.0.1", "your_secure_password")

plt.plot([0.5, 1.0, 3.0], [12.0, 5.0, 8.0])
pltip.show()

fig, ax = plt.subplots()
ax.plot([0.3, 1.1, 6.0], [3.0, 9.0, 4.0])
pltip.show(fig)
