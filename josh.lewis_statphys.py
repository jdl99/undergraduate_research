from vpython import *
#GlowScript 3.1 VPython

#import random as rand
'''defining constants'''
side = 6.0
thk = 0.1
s2 = 2*side - thk
s3 = thk
n = 1000
ball_cap = 400
mass = 1.0
k = 1.4E-23 # Boltzmann constant
T = 300 # around room temperature
dt = 1E-5
rad = 0.1
balls = []
l = []
bpos = []
p = []
#pavg = sqrt(2*mass*k*T) # average kinetic energy p**2/(2mass) = (2/2)kT <-- since we're in 2d
pavg = 5

wallR = box (pos=vector( side, 0, 0), size=vector(thk, s2, s3),  color = color.red)
wallL = box (pos=vector(-side, 0, 0), size=vector(thk, s2, s3),  color = color.red)
wallB = box (pos=vector(0, -side, 0), size=vector(s2, thk, s3),  color = color.blue)
wallT = box (pos=vector(0,  side, 0), size=vector(s2, thk, s3),  color = color.blue)


side = side - thk*0.5 - rad

# initializing balls
xp = []
yp = []
inc = floor(side/(1.5*rad))
for i in range(inc):
    for j in range(inc):
        xp.append(i*3*rad + 1.25*rad)
        yp.append(j*3*rad + 1.25*rad)

for i in range(n):
    theta = 2 * pi * random()
    #theta = 2*pi*cos(i/3)
    px = pavg*cos(theta)
    py = pavg*sin(theta)
    
    xpos = xp[i] - side
    ypos = yp[i] - side
    
    c = vec(random(),random(),random())
    balls.append(sphere (color = c, radius = rad))
    balls[i].mass = mass
    balls[i].pos = vec(xpos, ypos, 0)
    balls[i].p = vec(px, py, 0)
    balls[i].flags = []
    for j in range(n):
        balls[i].flags.append(False)
    bpos.append(balls[i].pos)
    p.append(balls[i].p)
    if i > ball_cap: balls[i].visible = False
    #l.append(label(pos=balls[i].pos, text=i, height=12, box=False))


'''histograms'''
# binning, setting up histogram
dv = 0.45
vmax = 10
def sort(v):
    return int(v/dv)

histo = []
for i in range(int(vmax/dv)): histo.append(0.0)
histo[sort(pavg/mass)] = n

# create histogram
grph = graph(width=400, height=250,
      title='<b>Speed Distribution</b>',
      xtitle='speed', ytitle='# of particles',
      foreground=color.black, background=color.white,
      xmin=0, xmax=vmax, ymin=0, ymax=300, align='left')
dist = gvbars(graph=grph,delta=dv*0.75, color=color.blue)
data = []
for i in range(int(vmax/dv)): data.append([dv*(i+.5),0])
dist.data = data

cum_grph = graph(width=400, height=250,
      title='<b>Cumulative Speed Distribution</b>',
      xtitle='speed', ytitle='# of particles',
      foreground=color.black, background=color.white,
      xmin=0, xmax=vmax, ymin=0, ymax=300, align='left')
cum_dist = gvbars(graph=cum_grph,delta=dv*0.75, color=color.red)
n_shots = 0 # number of histogram snapshots to average over
cum_data = []
totals = []
for i in range(int(vmax/dv)): cum_data.append([dv*(i+.5),0])
for i in range(int(vmax/dv)): totals.append([dv*(i+.5),0])
cum_dist.data = cum_data


'''functions'''
def interchange(v1, v2):  # remove from v1 bar, add to v2 bar
    bar1 = sort(v1)
    bar2 = sort(v2)
    if bar1 == bar2:  return
    if bar1 >= len(histo) or bar2 >= len(histo): return
    histo[bar1] -= 1
    histo[bar2] += 1

def collide(b1, b2):
    v1 = b1.p/b1.mass
    v2 = b2.p/b1.mass    
    bdiff = b1.pos-b2.pos
    b1.p = (v1 - (dot(v1-v2,bdiff)/mag2(bdiff))*bdiff) * b1.mass
    b2.p = (v2 - (dot(v2-v1,-bdiff)/mag2(-bdiff)*-bdiff)) * b2.mass

def walls(i):
#    print("checked")
    b = balls[i]
    if not (side > b.pos.x):
        b.p.x = -abs(b.p.x)
    if not (b.pos.x > -side):
        b.p.x = abs(b.p.x)
    if not (side > b.pos.y):
        b.p.y = -abs(b.p.y) 
    if not (b.pos.y > -side):
        b.p.y = abs(b.p.y)

def checkColl():
    hit = []
    for i in range(len(balls)):
        for j in range(1, n-i):
            if (mag(balls[i].pos - balls[i+j].pos) < 2*rad):
                hit.append([i,i+j])
            else:
                balls[i].flags[i+j] = False
    return hit

#def checkColl():
 #   hitlist = []
  #  r2 = 2*rad
   # r2 *= r2
    #for i in range(n):
     #   ai = bpos[i]
      #  for j in range(i) :
       #     aj = bpos[j]
        #    dr = ai - aj
         #   if mag2(dr) < r2: hitlist.append([i,j])
    #return hitlist


'''animation loop'''
scene.waitfor("click")
k = 0
dt = 0.005
while True:
    rate(1600)
    

    #if k>8300: 
    if False:
        scene.waitfor('click')
        print(f'b1 - p={balls[1].p}')
        print(f'b26 - p={balls[26].p}')
        print(balls[1].flags[26])
        #print(f'balls[10].flags[20]: {balls[10].flags[20]}')
        #print(f'balls[10].flags[22]: {balls[10].flags[22]}')
      #  print("b1 ",balls[0].p)
       # print("b2 ",balls[1].p) 
        #print("rrel ",abs(balls[0].pos.mag - balls[1].pos.mag))
        
    if (k % 1 == 0):
        n_shots += 1
        for i in range(len(histo)):
            data[i][1] = abs(histo[i])
            totals[i][1] = totals[i][1] + data[i][1]
            cum_data[i][1] = totals[i][1] / n_shots # average histogram data over all snapshots
        
        cum_dist.data = cum_data
        dist.data = data
    
    for i in range(n):
        balls[i].pos += (balls[i].p/mass)*dt
        #l[i].pos = balls[i].pos

    hit = checkColl()
    for ij in hit:
        if ij == [1,26]: print('boink')
        bi = balls[ij[0]]
        bj = balls[ij[1]]
        flag = bi.flags[ij[1]]
        bi.flags[ij[1]] = True
        vi = bi.p / mass
        vj = bj.p / mass
        vrel = vi - vj
        a = vrel.mag2
        #if a == 0: continue;  # exactly same velocities
        #rrel = bi.pos-bj.pos
        #if rrel.mag > rad: continue
        
        #print(f'i={ij[0]} j={ij[1]} flag={flag}')
        
        if not flag:
            collide(bi,bj)
            interchange(vi.mag, bi.p.mag/mass)
            interchange(vj.mag, bj.p.mag/mass)
    
    for i in range(n):
        walls(i)
        
    k += 1