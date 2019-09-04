import math
from random import randint

import numpy as np
from scipy.spatial.distance import pdist, squareform

import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

def colisionExistente(indice1, indice2,lista):
	combinacion1=str(indice1)+str(indice2)
	combinacion2=str(indice2)+str(indice1)
	for x in range(len(lista)):
		if(combinacion1==lista[x] or combinacion2==lista[x]):
			return True
	return False


class ParticleBox:
	def __init__(self,
				 init_state = [[1, 0, 0, -1],
							   [-0.5, 0.5, 0.5, 0.5],
							   [-0.5, -0.5, -0.5, 0.5]],
				 bounds = [0, 50, 0, 50],
				 size = 0.04):
		self.init_state = np.asarray(init_state, dtype=float)
		self.size = size
		self.state = self.init_state.copy()
		self.time_elapsed = 0
		self.bounds = bounds

	def step(self, dt):
		"""step once by dt seconds"""
		self.time_elapsed += dt

		self.state[:, :2] += dt * self.state[:, 2:]
		
		
		listaColisiones=[]
		contadorColisiones=0
		
		for indice in range(cantidadDeParticulas):
			for indice2 in range(cantidadDeParticulas):
				if(indice!=indice2):
					if(math.sqrt(math.pow(self.state[indice,0]-self.state[indice2,0],2)+math.pow(self.state[indice,1]-self.state[indice2,1],2))<2):
						if(colisionExistente(indice,indice2,listaColisiones)==False):
							listaColisiones.append(str(indice)+str(indice2))
							contadorColisiones=contadorColisiones+1
							variableAuxiliar=self.state[indice,2]
							variableAuxiliar2=self.state[indice,3]
							self.state[indice,2]=self.state[indice2,2]
							self.state[indice,3]=self.state[indice2,3]
							self.state[indice2,2]=variableAuxiliar
							self.state[indice2,3]=variableAuxiliar2	
		crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.size)
		crossed_x2 = (self.state[:, 0] > self.bounds[1] - self.size)
		crossed_y1 = (self.state[:, 1] < self.bounds[2] + self.size)
		crossed_y2 = (self.state[:, 1] > self.bounds[3] - self.size)

		self.state[crossed_x1 | crossed_x2, 2] *= -1
		self.state[crossed_y1 | crossed_y2, 3] *= -1


cantidadDeParticulas=10
init_state = np.zeros((cantidadDeParticulas,4),dtype=float) #2= 2 particulas
for i in range(cantidadDeParticulas):
	init_state[i, 0] = randint(1,40)
	init_state[i, 1] = randint(1,40)
	init_state[i, 2] =randint(1,10)
	init_state[i, 3] =randint(1,10)

init_state[0,0]=15
init_state[0,1]=15
init_state[1,0]=25
init_state[1,1]=25
init_state[0,2]=10
init_state[0,3]=10
init_state[1,2]=10
init_state[1,3]=10

box = ParticleBox(init_state, size=2.5)
dt = 1. / 60 # 30fps

fig = plt.figure()
ax = plt.axes(xlim=(0, 50), ylim=(0, 50))
particles, = ax.plot([], [], 'bo', ms=5)

def init():
	global box
	particles.set_data([], [])
	return particles,

def animate(i):
	global box, dt, ax, fig
	box.step(dt)

	particles.set_data(box.state[:, 0], box.state[:, 1])
	particles.set_markersize(20)
	return particles,

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

plt.show()
