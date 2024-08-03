import numpy as np

def euclidean_dist(x,y):
    return np.linalg.norm(x-y)

def euclidean_dists(x, centers):
    return [euclidean_dist(x,center) for center in centers]

# unimplemented
def gaussian_pdf(x,y):
    return 0

# unimplemented
def binomial_pdf(k,n,p):
    return 0

