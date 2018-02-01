import numpy as np
from scipy.spatial.distance import squareform, pdist
from numpy.linalg import norm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import argparse


width, height = 800, 600

#3D - tam gdzie były matryce 2d -> dodany trzeci wymiar, por. birds_2d

class Birds:
    '''chmara ptaków'''
    def __init__(self, N):

        #inicjowanie pozycji ptaków
        self.pos = [width/2.0, height/2.0, height/2.0] + 25*np.random.rand(3*N).reshape(N, 3)
        #tworzenie tablicy prędkości (znormalizowanej) boidów
        self.vel = np.random.uniform(-1, 1, (N, 3))
        self.N = N
        # minimalny dystans między boidami - ZASADA 1
        self.minDistance = 40.0
        # promień lokalnej grupy - ZASADA 2
        self.localGroup = 50.0
        # maksymalna wielkość kolejnych "kroków" w dostosowywaniu prędkości wg zasad
        self.maxStepVelocity = 0.02
        # maksymalna wielkość finalnej prędkości
        self.maxVelocity = 2.0

    #funkcja ograniczająca wartości danego wektora (żeby nie były kosmiczne)
    def vectorLim(self, vector, lim):
        magnitude = norm(vector)
        if magnitude > lim:
            vector[0], vector[1], vector[2] = vector[0]*lim/magnitude, vector[1]*lim/magnitude, vector[2]*lim/magnitude

    #funkcja ograniczająca wartości wektorów w tablicy X (korzysta z funkcji vectorLim)
    def matrixLim(self, matrix, lim):
        for vector in matrix:
            self.vectorLim(vector, lim)

    def update(self, frameNum, body, beak):

        """aktualizacja co jeden krok czasowy"""

        #matryca z odległościami między parami ptaków
        self.distMatrix = squareform(pdist(self.pos))
        #FALLOW THE RULES
        self.vel += self.behaviourRules()
        self.matrixLim(self.vel, self.maxVelocity)
        self.pos += self.vel
        self.borders()

        #aktualizowanie pozycji
        #3D dodanie koordynaty Z
        body.set_data(self.pos.reshape(3*self.N)[::3],
                      self.pos.reshape(3*self.N)[1::3])
        body.set_3d_properties(self.pos.reshape(3 * self.N)[2::3])
        vec = self.pos + 8 * self.vel / self.maxVelocity
        beak.set_data(vec.reshape(3 * self.N)[::3],
                      vec.reshape(3 * self.N)[1::3])
        beak.set_3d_properties(vec.reshape(3 * self.N)[2::3])


    def borders(self):
        """warunki brzegowe (granice pola)"""
        #zmiana współrzędnych ptaków, gdy nachodzą na ścianę
        delta = 10.0
        for coord in self.pos:
            if coord[0] > width + delta:
                coord[0] = - delta
            if coord[0] < - delta:
                coord[0] = width + delta
            if coord[1] > height + delta:
                coord[1] = - delta
            if coord[1] < - delta:
                coord[1] = height + delta
            if coord[2] > height + delta:
                coord[2] = - delta
            if coord[2] < - delta:
                coord[2] = height + delta



    def behaviourRules(self):

        # ZASADA 1 - SEPARATION (minimal distance)
        distances = self.distMatrix < self.minDistance  # boolean matrix -> True, jeśli sąsiad jest za blisko
        vel = ((self.vel * distances[:, :, None]).sum(axis=1) - distances.sum(axis=1).reshape(self.N, 1)) * (-1)
        self.matrixLim(vel, self.maxStepVelocity)

        # ZASADA 2 - ALIGNMENT
        distances = self.distMatrix < self.localGroup # szukamy lokalnej grupy
        vel2 = (self.vel * distances[:, :, None]).sum(axis=1) - distances.sum(axis=1).reshape(self.N, 1)
        self.matrixLim(vel2, self.maxStepVelocity)
        vel += vel2

        # ZASADA 3 - COHESION
        vel3 = (self.pos * distances[:, :, None]).sum(axis=1) - distances.sum(axis=1).reshape(self.N, 1) - self.pos
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
    #dodanie argumentu - liczby ptaków
    parser.add_argument('--birdsN', dest='N', required=False)
    args = parser.parse_args()

    # definiujemy liczbę ptaków
    N = 50
    if args.N:
        N = int(args.N)

    # nasze ptaszki
    birds = Birds(N)

    # rysowanie ptaków
    #3D plot
    fig = plt.figure()
    #ax = plt.axes(xlim=(0, width), ylim=(0, height))
    ax = fig.add_subplot(111, projection='3d')

    #3D - dodanie koordynaty
    body, = ax.plot([], [], [], markersize=10, c='crimson', marker='o', ls='None')
    beak, = ax.plot([], [], [], markersize=6, c='lightcoral', marker='*', ls='None')

    anim = animation.FuncAnimation(fig, animate, fargs=(body, beak, birds), interval=50)


    plt.show()

# wywołanie main
if __name__ == '__main__':
    main()
