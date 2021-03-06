# pyplot-over-ip
X11 Forwarding can be tricky to setup if your want to display matplotlib figures rendered on a remote machine on your local display. Instead this package simply sends [matplotlib.figure.Figure](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.html) as pickled python objects over http. If the remote machine is one the same network no additional setup is required. For remote machines on other networks bidirectional ssh port forwarding is recommended. The connection is secured using http basic auth.

## Installation
The package must be installed on both your local and remote machine.
```shell
pip install git+https://github.com/lorenz-h/pyplot-over-ip.git
```

## Usage
On the remote machine you use for rendering replace plt.show() or plt.figsave() with pltip.show():
```python
import matplotlib.pyplot as plt
import pyplot_over_ip as pltip

# run this once when starting your script.
pltip.setup("ip_of_your_display_machine", "your_secure_password")

plt.plot([0.5, 1.0, 3.0], [12.0, 5.0, 8.0])
pltip.show()

fig, ax = plt.subplots()
ax.plot([0.3, 1.1, 6.0], [3.0, 9.0, 4.0])
pltip.show(fig)

```
To display figures on your local machine run the receiver:

```shell
pyplot-over-ip --password your_secure_password
```
