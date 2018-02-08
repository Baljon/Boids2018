#Projekt zaliczeniowy na zajęcia Python dla Kognitywistów, prowadzący: Julian Zubek
#Autorzy: Anna Alińska, Anna Baljon, Martyna Pietrzak

import numpy as np
from scipy.spatial.distance import squareform, pdist
from numpy.linalg import norm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import argparse


width, height = 800, 600


class Birds:
    '''chmura ptaków'''
    def __init__(self, N):

        #inicjowanie pozycji ptaków
        self.pos = [width/2.0, height/2.0, height/2.0] + 25*np.random.rand(3*N).reshape(N, 3)
        #tworzenie tablicy prędkości (znormalizowanej) boidów
        self.vel = np.random.uniform(-1, 1, (N, 3))
        self.N = N
        # minimalny dystans między boidami - ZASADA 1
        self.minDistance = 30.0
        # promień lokalnej grupy - ZASADA 2 i 3
        self.localGroup = 60.0
        # maksymalna wielkość kolejnych "kroków" w dostosowywaniu prędkości wg zasad
        self.maxStepVelocity = 0.03*1.2
        # maksymalna wielkość finalnej prędkości
        self.maxVelocity = 2.5*1.2

    #funkcja ograniczająca wartości danego wektora (żeby nie były kosmiczne)
    def vectorLim(self, vector, lim):
        magnitude = norm(vector)
        if magnitude > lim:
            vector[0], vector[1], vector[2] = vector[0]*lim/magnitude, vector[1]*lim/magnitude, vector[2]*lim/magnitude

    #funkcja ograniczająca wartości wektorów w tablicy matrix (korzysta z funkcji vectorLim)
    def matrixLim(self, matrix, lim):
        for vector in matrix:
            self.vectorLim(vector, lim)

    def update(self, frameNum, body, beak, shadow):
        """aktualizacja co jeden krok czasowy"""

        #tablica z odległościami między parami ptaków
        self.distMatrix = squareform(pdist(self.pos))

        #FALLOW THE RULES
        self.vel += self.behaviourRules()
        self.matrixLim(self.vel, self.maxVelocity)
        self.pos += self.vel

        self.borders()

        #aktualizowanie pozycji
        body.set_data(self.pos.reshape(3*self.N)[::3],
                      self.pos.reshape(3*self.N)[1::3])
        body.set_3d_properties(self.pos.reshape(3 * self.N)[2::3])
        vec = self.pos + 10 * self.vel / self.maxVelocity
        beak.set_data(vec.reshape(3 * self.N)[::3],
                      vec.reshape(3 * self.N)[1::3])
        beak.set_3d_properties(vec.reshape(3 * self.N)[2::3])
        vec2 = self.pos - 5
        shadow.set_data(vec2.reshape(3 * self.N)[::3],
                        vec2.reshape(3 * self.N)[1::3])
        shadow.set_3d_properties(vec2.reshape(3 * self.N)[2::3])


    def borders(self):
        """warunki brzegowe (przelatywanie przez ściany)"""
        # zmiana współrzędnych ptaków, gdy wylatują za ścianę
        margin = 10.0
        for coord in self.pos:
            if coord[0] > width + margin:
                coord[0] = - margin
            if coord[0] < - margin:
                coord[0] = width + margin
            if coord[1] > height + margin:
                coord[1] = - margin
            if coord[1] < - margin:
                coord[1] = height + margin
            if coord[2] > height + margin:
                coord[2] = - margin
            if coord[2] < - margin:
                coord[2] = height + margin



    def behaviourRules(self):

        vel = self.vel

        # ZASADA 1 - SEPARATION (minimal distance)
        distances = self.distMatrix < self.minDistance  # boolean matrix -> True, jeśli sąsiad jest za blisko
        vel1 = ((self.vel * distances[:, :, None]).sum(axis=1) / distances.sum(axis=1).reshape(self.N, 1)) * (-1)
        self.matrixLim(vel1, self.maxStepVelocity)
        vel += vel1

        # ZASADA 2 - ALIGNMENT
        distances = self.distMatrix < self.localGroup  # szukamy lokalnej grupy

        vel2 = (self.vel * distances[:, :, None]).sum(axis=1) / distances.sum(axis=1).reshape(self.N, 1)
        self.matrixLim(vel2, self.maxStepVelocity)
        vel += vel2

        # ZASADA 3 - COHESION
        vel3 = (self.pos * distances[:, :, None]).sum(axis=1) / distances.sum(axis=1).reshape(self.N, 1) - self.pos
        self.matrixLim(vel3, self.maxStepVelocity)
        vel += vel3

        return vel


def animate(frameNum, body, beak, shadow, birds):
    #aktualizacja funkcji do animacji
    birds.update(frameNum, body, beak, shadow)
    return body, beak, shadow


# funkcja main()
def main():

    print('Birds are being born...WAIT FOR IT')

    parser = argparse.ArgumentParser(description="Symulacja chmury ptaków...")
    #możliwość dodania argumentu przez użytkownika - liczby ptaków
    parser.add_argument('--birdsN', dest='N', required=False)
    args = parser.parse_args()

    # domyślna liczba ptaków
    N = 150
    if args.N:
        N = int(args.N)

    # nasze ptaszki
    birds = Birds(N)

    # rysowanie ptaków
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlim3d(0, width)
    ax.set_ylim3d(0, height)
    ax.set_zlim3d(0, height)
    ax.set_facecolor('midnightblue')
    title=ax.set_title('* Ptaki Oktagonalne Wypukłe *')
    plt.setp(title, color='powderblue', fontsize=14)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    # ax.axis('off')


    shadow, = ax.plot([], [], [], markersize=9, c=(0,0,0,0.09), marker='8', ls='None')
    body, = ax.plot([], [], [], markersize=10, c='lightseagreen', marker='8', ls='None')
    beak, = ax.plot([], [], [], markersize=4, c='powderblue', marker='*', ls='None')

    anim = animation.FuncAnimation(fig, animate, fargs=(body, beak, shadow, birds), interval=50)


    plt.show()


# wywołanie main
if __name__ == '__main__':
    main()
