from timeit import repeat
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random as rand
#BOILERPLATE
plt.style.use('dark_background')
fig = plt.figure()
plt.get_current_fig_manager().window.state('zoomed')
ax = fig.add_subplot(111)
ax.set_aspect( 'auto' )
ax.axis('square')
ax.set_xlim( [ -4e8, 4e8 ] )
ax.set_ylim( [ -4e8, 4e8 ] )
#CONSTANTS
G = 6.67e-11
T_SPAN = 60 * 60 * 24 * 10 # seconds
SPEED = 10 # times faster
n = 0
offset = 10
delta_t = 150 # seconds
STEPS = int(T_SPAN / delta_t)

class Body:
    def __init__(self, rx, ry, vx, vy, mass, color):
        self.rx = rx
        self.ry = ry
        self.vx = vx
        self.vy = vy
        self.mu = G*mass
        self.color = color
        global n
        n+=1
    def state_vectors(self):
        return [self.rx, self.ry, self.vx, self.vy]
# bodies = [
#     #JOOL
#     Body(0,0,0,0,4.2332e24,'green'),
#     #LAYTHE
#     Body(0, -27184000, 3224 , 0, 2.9397e22, 'blue'),
#     #VALL
#     Body(0,-43152000, 2559, 0, 3.1087655e21,'cyan'),
#     #TYLO
#     Body(0,-68500000, 2031, 0, 4.2332127e22,'grey'),
#     #BOP
#     Body(0,-98302500, 1884, 0, 3.726109e19,'brown'),
#     #POL
#     Body(0,-149155794, 1489, 0, 1.0813507e19,'yellow')
# ]
bodies=[]
colours=["blue", "red", "green", "yellow", "white", "purple", "brown", "grey", "orange", "violet"]
for i in range(rand.randint(5,12)):
    bodies.append(Body(rand.randint(-4e8,4e8), rand.randint(-4e8,4e8), rand.randint(-5000,5000), rand.randint(-5000,5000), rand.randint(5e17, 5e24), colours[rand.randint(0, len(colours)-1)]))
states = np.zeros((STEPS, n, 4))
coords = np.zeros((STEPS, n, 2))
# initialize initial state vectors
for i in range(n):
    states[0][i]=bodies[i].state_vectors()
def acceleration(state):
    a = np.zeros((n, 2))
    for x in range(n):
        for i in range(n):
            if (x == i):
                continue
            ri = np.array([state[i][0], state[i][1]])
            rx = np.array([state[x][0], state[x][1]])
            a[x]+=bodies[i].mu*(ri - rx)/(np.linalg.norm(ri-rx))**3
    # Derivative States
    d_states = np.zeros((n, 4))
    for i in range(n):
        d_states[i][0] = state[i][2]
        d_states[i][1] = state[i][3]
        d_states[i][2] = a[i][0]
        d_states[i][3] = a[i][1]
    return d_states

def integrate( f, y, dt ):
    global delta_t
    # Current Step Size
    k1 = f(y )
    k2 = f(y + 0.5 * k1 * dt )
    k3 = f(y + 0.5 * k2 * dt )
    k4 = f(y +       k3 * dt )
    next_step = y + dt / 6.0 * ( k1 + 2 * k2 + 2 * k3 + k4 )
    return next_step



for step in range(STEPS - 1):
    states[step+1]=integrate(acceleration, states[step], delta_t)

  
coordsX = [[] for _ in range(n)] 
coordsY = [[] for _ in range(n)] 
cnt = 0
for state in states:
    for j in range(n):
        if cnt % SPEED == 0:
            coordsX[j].append(state[j][0])
            coordsY[j].append(state[j][1])
    cnt+=1
lines = [plt.plot([], [])[0] for _ in range(2*n)]
def init():
    for i in range(n):
        lines[i].set_data([], [])
        lines[i+n].set_data([],[])
        lines[i].set_color(bodies[i].color)
        lines[i+n].set_color(bodies[i].color)
        lines[i].set_linewidth(1)
        lines[i+n].set_marker('.')
    return lines
def animate(i):
    try:
        for j in range(n):
            if i >= offset:
                lines[j].set_data(coordsX[j][i-offset:i], coordsY[j][i-offset:i])
            else:
                lines[j].set_data(coordsX[j][:i], coordsY[j][:i])
            lines[j+n].set_data(coordsX[j][i], coordsY[j][i])
        return lines
    except IndexError:
        i = 0
        return lines
ani = FuncAnimation(fig, animate, init_func=init, interval=30, blit=True, repeat=True, frames=len(coordsX[0]))    
print(len(coordsX[0]), len(coordsX[1]), len(coordsX[2]), len(coordsX[3]))
plt.show()
