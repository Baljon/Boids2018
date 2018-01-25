import numpy as np
from math import sqrt
from scipy.spatial.distance import squareform, pdist
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import argparse - ew.potrzebne póżniej, żeby użytkownik mógł zdefiniować liczbę ptaków


##WHAT A MESS

width, height = 800, 600

#minimalny dystans między boidami - ZASADA 1
minDistance = 15.0
#maksymalna wielkość kolejnych "kroków" w dostosowywaniu prędkości wg zasad
maxStepVelocity = 0.4
#maksymalna wielkość finalnej prędkości
maxVelocity = 4.0


def birds(N):

    '''inicjowanie symulacji ptaków'''
    #inicjowanie pozycji ptaków
    pos = [width/2.0, height/2.0] + 25*np.random.rand(2*N).reshape(N, 2)

    #tworzenie tablicy prędkości (znormalizowanej) boidów
    vel = np.random.uniform(-1, 1, (N, 2))

    return (pos, vel)


# funkcja ograniczająca wartości danego wektora (żeby nie były kosmiczne)
def vectorLim(vector, lim):
    magnitude = sqrt(vector[0]**2 + vector[1]**2)
    if magnitude > lim:
        vector[0], vector[1] = vector[0] * lim / magnitude, vector[1] * lim / magnitude

# funkcja ograniczająca wartości wektorów w tablicy X (korzysta z funkcji vectorLim)
def matrixLim(matrix, lim):
    for vector in matrix:
        vectorLim(vector, lim)


def applyBC(matrix):
    """zastosowanie warunków brzegowych"""
    deltaR = 2.0
    for coord in matrix:
        if coord[0] > width + deltaR:
            coord[0] = - deltaR
        if coord[0] < - deltaR:
            coord[0] = width + deltaR
        if coord[1] > height + deltaR:
            coord[1] = - deltaR
        if coord[1] < - deltaR:
            coord[1] = height + deltaR


def distanceUpdate(pos):
    distMatrix = squareform(pdist(pos))
    return distMatrix

def update(pos, vel):
    #N=50
    #pos, vel = birds(N)
    """aktualizacja symulacji o jeden krok czasowy"""
    # matryca z odległościami między parami ptaków
    #distMatrix = distanceUpdate(pos)
    #FALLOW THE RULES
    vel += behaviourRules(pos, vel)
    matrixLim(vel, maxVelocity)
    pos += vel
    applyBC(pos)
    #aktualizowanie pozycji
    #body.set_data(pos.reshape(2*N)[::2],
    #              pos.reshape(2*N)[1::2])
    return (pos, vel)

def behaviourRules(pos, vel):
    #N=50
    #pos, vel = birds(N)
    N = pos.shape[0]

    distMatrix = distanceUpdate(pos)
    # ZASADA 1 - SEPARATION (minimal distance)
    distances = distMatrix < minDistance  # boolean matrix -> True, jeśli sąsiad jest za blisko
    vel = (vel * distances[:, :, None]).sum(axis=1) / distances.sum(axis=1).reshape(N, 1) * (-1)
    matrixLim(vel, maxStepVelocity)

    # ZASADA 2 - ALIGNMENT
    distances = distMatrix < 25.0 # szukamy lokalnej grupy

    vel2 = (vel * distances[:, :, None]).sum(axis=1) / distances.sum(axis=1).reshape(N, 1)
    matrixLim(vel, maxStepVelocity)
    vel += vel2

    # ZASADA 3 - COHESION
    vel3 = (pos * distances[:, :, None]).sum(axis=1) / distances.sum(axis=1).reshape(N, 1) - pos
    matrixLim(vel3, maxStepVelocity)
    vel += vel3

    return vel


def animate(frameNum):
    #aktualizacja funkcji do animacji
    update(frameNum, pos, vel)
    body.set_offsets(pos.transpose())


# funkcja main()
def main():

    print('Birds are being born...WAIT FOR IT')

    parser = argparse.ArgumentParser(description="Symulacja chmury ptaków...")
    #dodanie argumentu - liczby ptaków
    parser.add_argument('--birdsN', dest='N', required=False)
    args = parser.parse_args()

    # definiujemy liczbę ptaków
    N = 100
    if args.N:
      N = int(args.N)

    pos, vel = birds(N)

    # rysowanie ptaków
    #fig = plt.figure()
    #plt.axes(xlim=(0, width), ylim=(0, height))
    for _ in range(1):
        #plt.axes(xlim=(0, width), ylim=(0, height))
        plt.scatter(pos[:, 0], pos[:, 1])
        plt.show()
        pos, vel = update(pos, vel)

    #body, = ax.plot(pos[:,0], pos[:,1], markersize=10, c='skyblue', marker='o', ls='None')
    #beak = ax.plot(pos[:,1], markersize=4, c='black', marker='*', ls='None')

    # plt.show()
    # body.scatter(pos[:, 0], pos[:, 1])
    # anim = animation.FuncAnimation(fig, animate, frames=50, interval=50)




# wywołanie main
if __name__ == '__main__':
    main()


 # #inicjowanie pozycji ptaków
 #    pos1 = [width/2.0, height/2.0] + 25*np.random.rand(2*N).reshape(N, 2)
 #
 #    #tworzenie tablicy prędkości (znormalizowanej) boidów
 #    vel1 = np.random.uniform(-1, 1, (50, 2))

