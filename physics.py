import numpy as np
import pygame as pg
#import pandas as pd

from pathlib import Path
from objects_creation import mass_n, cells, walls
from parameters import screen, display
from functions import dynamics, contact, wall_colition, dt

# ------------------------------------------ SIMULATION ----------------------------------------------------

time = 0
velocity = 0
n = 0

pg.init()

#Type of font for text
font = pg.font.Font(Path('~/Projects/Personal/simulations/Fonts/old_terminal/VCR_OSD_MONO_1.001.ttf').expanduser(),36)

j = 0

running = True

# Loop
while running:

    txt1 = font.render(f'Particles that escaped: {j}', False, (240,240,240))
    txt2 = font.render(f'Time: {time:.3f}s', False, (240,240,240))

    # SYSTEM ------------------------------------------------

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    display.fill((1, 1, 1))

    # OBJECTS ------------------------------------

    for i in range(len(walls)):
        
        walls[i].draw(display)

    for mass in mass_n:

        dynamics(mass)
        mass.draw(display)
        wall_colition(mass)

        if mass.verif == True:
            
            j += 1

            mass.verif = False

        if mass.verif == False:

            velocity += np.linalg.norm(mass.vel)

            n += 1

    contact(cells)

    time += dt

    display.blit(txt1, (100,100))
    display.blit(txt2, (100,150))

    # REFRESH IMAGE ---------------------------------------------------------

    pg.display.update()

pg.quit()

#----------------------------------- DATA -------------------------------------------

mean_velocity = velocity/n

print(mean_velocity)

