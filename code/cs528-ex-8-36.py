# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 12:22:04 2019

@author: dunna
"""

# Execution times:
# 100 Molecules / 10,000 iterations:    7.5 seconds
# 1,000 Molecules / 10,000 iterations:  74.51 seconds
# 10,000 Molecules / 10,000 iterations: 725.54 seconds

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('seaborn-pastel')

NUM_MOLECULES = 10000
TIME_STEPS = 10000
RANDOM_WALK_DIST = 0.01
ANIM_FRAMES = 400
ANIM_FRAMES_TIMESTEP = TIME_STEPS // ANIM_FRAMES
PLOT_WIDTH = 12
PLOT_HEIGHT = 8

molX = np.random.random_sample(NUM_MOLECULES)
molY = np.random.random_sample(NUM_MOLECULES)
molX *= 0.25

molXHist = [molX.copy()]
molYHist = [molY.copy()]

tPer = 0
lastTPer = -1

start_time = time.time()

for t in range(TIME_STEPS):
    tPer = np.floor((t / TIME_STEPS) * 100)
    if tPer > lastTPer:
        print("% Completed:", tPer)
        lastTPer = tPer
    for i in range(NUM_MOLECULES):
        randAngle = np.random.uniform(np.pi * -1, np.pi)
        randVector = np.array([np.cos(randAngle), np.sin(randAngle)])
        randVector = randVector * RANDOM_WALK_DIST
        molX[i] = max(min(molX[i] + randVector[0], 1), 0)
        molY[i] = max(min(molY[i] + randVector[1], 1), 0)
        
    if t % ANIM_FRAMES_TIMESTEP == 0:
        molXHist.append(molX.copy())
        molYHist.append(molY.copy())

end_time = time.time()
print("Total execution time:", round(end_time - start_time, 2))

class animatedScatter:
    def __init__(self, molXHist, molYHist):
        self.molXHist = molXHist
        self.molYHist = molYHist
        self.fig = plt.figure()
        self.fig.set_size_inches(PLOT_WIDTH, PLOT_HEIGHT)
        self.ax = plt.axes(xlim=(0, 1), ylim=(0, 1))
        self.itertext = self.ax.text(0.70, 0.9,  '', bbox=dict(facecolor='white', alpha=0.2), transform=self.ax.transAxes)
        print("Creating animation ... Please wait ...")
        self.ani = FuncAnimation(self.fig, self.update, frames=len(molXHist), interval=30, 
                                 init_func=self.setup, blit=True)
        print("Saving gif ... Please wait ...")
        self.ani.save('final_animated.gif', writer='imagemagick')
    def setup(self):
        self.scatter = self.ax.scatter([], [], color = "green")
        return self.scatter,
    def update(self, i):
        self.itertext.set_text('iteration = %d' % (i * ANIM_FRAMES_TIMESTEP))
        self.scatter.remove()
        self.scatter = self.ax.scatter(self.molXHist[i], self.molYHist[i], color = "green", alpha=0.2)
        return self.scatter,


plt.scatter(molXHist[0], molYHist[0], color = "green", alpha=0.2)
plt.title('Gas molecules - Start of random walk')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.gcf().set_size_inches(PLOT_WIDTH, PLOT_HEIGHT)
plt.gcf().savefig("final_start.png")
plt.show()
plt.close();

plt.scatter(molXHist[-1], molYHist[-1], color = "green", alpha=0.2)
plt.title('Gas molecules - End of random walk')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.gcf().set_size_inches(PLOT_WIDTH, PLOT_HEIGHT)
plt.gcf().savefig("final_end.png")
plt.show()
plt.close();

a = animatedScatter(molXHist, molYHist)
print("Done!")

