import numpy as np
FPS=30; W,H=1920,1080
VO=1.5          # voice offset
DUR=47.0
SCENES=[0.0,6.6,14.8,25.4,33.0,DUR]
LETTER_T=[6.8+0.28*i for i in range(5)]   # logo letter drop base times
CARD_T=[14.8,17.4,20.0,22.6]
COUNT_T=[26.2,27.6,29.0]
BOOM_T=30.4
rng=np.random.default_rng(7)
FIREWORKS=[]
for t0 in list(np.arange(31.0,45.5,0.55)):
    FIREWORKS.append((float(t0+rng.uniform(-.15,.15)), float(rng.uniform(250,1670)), float(rng.uniform(180,520)),
                      int(rng.integers(0,6)), int(rng.integers(40,70))))
FIREWORKS += [(12.0,380.,260.,1,50),(12.4,1540.,230.,3,50)]
FIREWORKS.sort()
