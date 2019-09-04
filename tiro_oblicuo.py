import math

import numpy as np
from scipy.spatial.distance import pdist, squareform

import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

class ParticleBox:
	def __init__(self,
				 init_state = [[1, 0, 0, -1],
							   [-0.5, 0.5, 0.5, 0.5],
							   [-0.5, -0.5, -0.5, 0.5]],
				 bounds = [0, 300, -1, 300],
				 size = 0.04):
		self.init_state = np.asarray(init_state, dtype=float)
		self.size = size
		self.state = self.init_state.copy()
		self.time_elapsed = 0
		self.bounds = bounds

	def step(self, dt):
		"""step once by dt seconds"""
		self.time_elapsed += dt

		self.state[0, 1] += dt * self.state[0, 3]
		self.state[0,3] -=9.81*dt
		self.state[0,0] +=dt*self.state[0,2]
		if(self.state[0,1]<1.077):
			self.state[0,2]=0

		crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.size)
		crossed_x2 = (self.state[:, 0] > self.bounds[1] - self.size)
		crossed_y1 = (self.state[:, 1] < self.bounds[2] + self.size)
		crossed_y2 = (self.state[:, 1] > self.bounds[3] - self.size)

		self.state[crossed_x1 | crossed_x2, 2] *= 0
		self.state[crossed_y1 | crossed_y2, 3] *= 0


dt = 1. / 30 # 30fps  
angulo=30 #en grados
velocidadInicial=50 #metros sobre segundos
velocidadInicialX=velocidadInicial*( math.cos(math.radians(30)))
velocidadInicialY=velocidadInicial* (math.sin(math.radians(30)))
init_state = np.zeros((1,4),dtype=float)
init_state[0, 0] = 2           #posicionInicialX
init_state[0, 1] = 2    #posicionInicialY
init_state[0, 2] = velocidadInicialX
init_state[0, 3] = velocidadInicialY   #velocidad en y

box = ParticleBox(init_state, size=2.5)
dt = 1. / 30 # 30fps

fig = plt.figure()
ax = plt.axes(xlim=(0, 300), ylim=(-1, 300))
particles, = ax.plot([], [], 'bo', ms=5)

def init():
	global box
	particles.set_data([], [])
	return particles,

def animate(i):
	global box, dt, ax, fig
	box.step(dt)

	particles.set_data(box.state[:, 0], box.state[:, 1])
	particles.set_markersize(5)
	return particles,

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

plt.show()
