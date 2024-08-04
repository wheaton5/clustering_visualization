import numpy as np

def euclidean_dist(x,y):
    return np.linalg.norm(x-y)

def euclidean_dists(x, centers):
    return [euclidean_dist(x,center) for center in centers]

def kmeans_loss(x, centers, assignments):
    loss = 0
    for (i, data_point) in enumeration(x):
        loss += euclidean_dist(data_point, centers[assignments[i]])**2
    return kmeans_loss

# unimplemented
def gaussian_pdf(x,y):
    return 0

# unimplemented
def binomial_pdf(k,n,p):
    return 0

