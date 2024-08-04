import numpy as np
import scipy 
import random

def generate_simple(k, n, max, standard_deviation, seed):
    rand = random.Random()
    rand.seed(seed)
    centers = []
    for _ in range(k):
        centers.append([rand.random()*max, rand.random()*max])
    centers = np.asarray(centers)
    data = []
    for clust in range(k):
        for _ in range(n//k):
            data.append(np.random.normal(centers[clust], scale=standard_deviation))
    data = np.asarray(data)
    return data
    
