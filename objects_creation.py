import numpy as np
import pygame as pg
import itertools as it
from parameters import screen, display, g, n, num_p, k_b, m, T, lat_walls, bottom_and_upper_walls, altitude, aperture

#----------------------------------- Clases -------------------------------------------

w = screen[0]
h = screen[1]

lw = lat_walls
b_u_w = bottom_and_upper_walls

#------------------------------------------------------------------------------

class Wall():

    def __init__(self,i,f):

        self.i = i
        self.f = f

        self.i[0] += w/2
        self.f[0] += w/2

        self.i[1] = h/2 + self.i[1]*(-1)
        self.f[1] = h/2 + self.f[1]*(-1)

    def draw(self,screen):

        pg.draw.line(screen,(240,240,240), self.i, self.f, width=3)
 
class Ball():

    def __init__(self, mass, radius, color, pos, vel, acc):
        
        self.mass = mass
        self.radius = radius
        self.color = color
        self.pos = np.array(pos).astype(float)
        self.vel = np.array(vel).astype(float)
        self.acc = np.array(acc).astype(float)
        self.cell = None
        self.verif = False

        self.pos[1] = self.pos[1]*(-1)
        self.vel[1] = self.vel[1]*(-1)
        self.acc[1] = self.acc[1]*(-1)

    def draw(self,screen):

        pg.draw.circle(screen,self.color, (w/2 + self.pos[0], h/2 + self.pos[1]), radius=self.radius, width=0)

#----------------------------------- WALLS CREATOR -------------------------------------------

wall_bottom = Wall([-b_u_w/2 , -lw/2 + altitude] , [b_u_w/2 , -lw/2 + altitude])
wall_left = Wall([-b_u_w/2 , -lw/2 + altitude] , [-b_u_w/2, lw/2 + altitude])
wall_right = Wall([b_u_w/2 , -lw/2 + altitude] , [b_u_w/2 , lw/2 + altitude])

wall_top_left = Wall([-b_u_w/2, lw/2 + altitude] , [-aperture/2, lw/2 + altitude])
wall_top_right = Wall([b_u_w/2, lw/2 + altitude] , [aperture/2, lw/2 + altitude])

walls = [wall_bottom,wall_left,wall_right,wall_top_left,wall_top_right]

# ------------------------------------------ MASS CREATOR ----------------------------------------------------

rng = np.random.default_rng()

mass_n = []

cellx = w/n
celly = h/n

cells = {}

j = 0

while j < n:

    for i in range(n):

        cells[f'cell_{j}_{i}'] = []

    j += 1

for punto in range(num_p):

    v_max_boltz = rng.normal(0,scale = np.sqrt((k_b*T)/m))

    mass = 1

    radius = 1

    mass_i = Ball(
        
        mass, 
        
        radius, 
        
        (rng.uniform(220,220), rng.uniform(220,220), rng.uniform(220,220)), 
        
        (rng.uniform(-b_u_w/2 + 10 , b_u_w/2 - 10), rng.uniform(-lw/2 + 10 + altitude , lw/2 - 10 + altitude)), 
        
        (v_max_boltz, v_max_boltz),
        
        (0,g)
        
        )

    mass_n.append(mass_i)

    m_cellx = int((mass_i.pos[0]+(w/2)) // cellx)
    m_celly = int((mass_i.pos[1]+(h/2)) // celly)

    mass_i.cell = f'cell_{str(m_celly)}_{str(m_cellx)}'

    cells[f'cell_{str(m_celly)}_{str(m_cellx)}'].append(mass_i)
