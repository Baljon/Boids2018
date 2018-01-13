# to be written
# PSEUDOKOD:
#
# initialise_positions()
#
# LOOP
# draw_boids()
# move_all_boids_to_new_positions()
# END
# LOOP
n=50


from scipy.spatial.distance import squareform, pdist

def minimal_distance_rule(pos): #small distance away from other objects (including other boids)
    distances = pdist(pos) #matrix with distances between each pair of boids
    all_distances = squareform(distances) #one tuple contains all distances from one boid to the others
    min_distances = all_distances < 20 #arbitral minimal distance
    vel = pos*min_distances.sum(axis=1).reshape(n,1)-min_distances.dot(pos)
    return vel;

