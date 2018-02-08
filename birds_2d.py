#Projekt zaliczeniowy na zajęcia Python dla Kognitywistów, prowadzący: Julian Zubek
#Autorzy: Anna Alińska, Anna Baljon, Martyna Pietrzak

import numpy as np
from numpy.linalg import norm
from scipy.spatial.distance import squareform, pdist
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import argparse


width, height= 800, 600


class Birds:
    '''chmura ptaków'''
    def __init__(self, N):

        #inicjowanie pozycji ptaków
        self.pos = [width/2.0, height/2.0] + 25*np.random.rand(2*N).reshape(N, 2)
        #tworzenie tablicy prędkości (znormalizowanej) boidów
        self.vel = np.random.uniform(-1, 1, (N, 2))
        self.N = N
        # minimalny dystans między boidami - ZASADA 1
        self.minDistance = 25.0
        # promień lokalnej grupy - ZASADA 2 i 3
        self.localGroup = 50.0
        # maksymalna wielkość kolejnych "kroków" w dostosowywaniu prędkości wg zasad
        self.maxStepVelocity = 0.03
        # maksymalna wielkość finalnej prędkości
        self.maxVelocity = 2.0

    def update(self, frameNum, body, beak):

        """aktualizacja o jeden krok czasowy"""
        # tablica z odległościami między parami ptaków
        self.distMatrix = squareform(pdist(self.pos))

        #FALLOW THE RULES
        self.vel += self.behaviourRules()
        self.matrixLim(self.vel, self.maxVelocity)
        self.pos += self.vel

        self.borders()

        #aktualizowanie pozycji
        body.set_data(self.pos.reshape(2*self.N)[::2],
                      self.pos.reshape(2*self.N)[1::2])
        vec = self.pos + 8 * self.vel / self.maxVelocity
        beak.set_data(vec.reshape(2 * self.N)[::2],
                      vec.reshape(2 * self.N)[1::2])

    # funkcja ograniczająca wartości danego wektora (żeby nie były kosmiczne)
    def vectorLim(self, vector, lim):
        magnitude = norm(vector)
        if magnitude > lim:
            vector[0], vector[1] = vector[0] * lim / magnitude, vector[1] * lim / magnitude

    # funkcja ograniczająca wartości wektorów w matrix (korzysta z funkcji vectorLim)
    def matrixLim(self, matrix, lim):
        for vector in matrix:
            self.vectorLim(vector, lim)

    def borders(self):
        """warunki brzegowe (przelatywanie przez ściany)"""
        # zmiana współrzędnych ptaków, gdy wylatują za ścianę
        delta = 5.0
        for coord in self.pos:
            if coord[0] > width + delta:
                coord[0] = - delta
            if coord[0] < - delta:
                coord[0] = width + delta
            if coord[1] > height + delta:
                coord[1] = - delta
            if coord[1] < - delta:
                coord[1] = height + delta


    def behaviourRules(self):

        vel=self.vel

        # ZASADA 1 - SEPARATION (minimal distance)
        distances = self.distMatrix < self.minDistance  # boolean matrix -> True, jeśli sąsiad jest za blisko
        vel1 = ((self.vel * distances[:, :, None]).sum(axis=1)/distances.sum(axis=1).reshape(self.N, 1)) * (-1)
        self.matrixLim(vel1, self.maxStepVelocity)
        vel += vel1

        # ZASADA 2 - ALIGNMENT
        distances = self.distMatrix < self.localGroup # szukamy lokalnej grupy
        vel2 = (self.vel * distances[:, :, None]).sum(axis=1)/distances.sum(axis=1).reshape(self.N, 1)
        self.matrixLim(vel2, self.maxStepVelocity)
        vel += vel2

        # ZASADA 3 - COHESION
        vel3 = (self.pos * distances[:, :, None]).sum(axis=1)/distances.sum(axis=1).reshape(self.N, 1) - self.pos
        self.matrixLim(vel3, self.maxStepVelocity)
        vel += vel3

        return vel


def animate(frameNum, body, beak, birds):
    #aktualizacja funkcji do animacji
    birds.update(frameNum, body, beak)
    return body, beak


# funkcja main()
def main():

    print('Birds are being born...WAIT FOR IT')

    parser = argparse.ArgumentParser(description="Symulacja chmury ptaków...")
    # możliwość dodania argumentu przez użytkownika - liczby ptaków
    parser.add_argument('--birdsN', dest='N', required=False)
    args = parser.parse_args()

    # definiujemy liczbę ptaków
    N = 150
    if args.N:
        N = int(args.N)

    # nasze ptaszki
    birds = Birds(N)

    # rysowanie ptaków
    fig = plt.figure()
    fig.patch.set_facecolor('pink')
    ax = plt.axes(xlim=(0, width), ylim=(0, height))
    ax.axis('off')
    title = ax.set_title('* Ptaki Płaskie *')
    plt.setp(title, color='lightcoral', fontsize=14)

    body, = ax.plot([], [], markersize=10, c='crimson', marker='o', ls='None')
    beak, = ax.plot([], [], markersize=6, c='lightcoral', marker='*', ls='None')


    anim = animation.FuncAnimation(fig, animate, fargs=(body, beak, birds), interval=50)

    plt.show()


# wywołanie main
if __name__ == '__main__':
    main()
