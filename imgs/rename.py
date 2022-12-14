from os import *

# tiles créées avec :
# convert jeu-carte.png -crop 192x279  +repage -resize 64x64 tile%d.gif

suites = [ (0,'T'), (14, 'K'), (28, 'C'), (42, 'P') ]

for start, suite in suites:
    for i in range(1,14):
        targ = str(i)
        if i == 1:
            targ = 'A'
        elif i == 11:
            targ = 'V'
        elif i == 12:
            targ = 'D'
        elif i == 13:
            targ = 'R'
        try:
            rename ('tile'+str(start + i - 1)+'.gif', 'carte-'+targ+'-' + suite + '.gif')
        except FileNotFoundError:
            pass

for i,c in [(56, 'J-N'), (57, 'J-R'), (58, 'dos')]:
    rename ('tile' + str(i) + '.gif', 'carte-' + c + '.gif')
