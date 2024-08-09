import numpy as np
import scipy 
import random

def generate_simple(k, n, max, standard_deviation, seed):
    rand = random.Random()
    rand.seed(seed)
    centers = []
    for _ in range(k):
        x = rand.random()*max
        y = rand.random()*max
        centers.append([x,y])
    centers = np.asarray(centers)
    data = []
    gen = np.random.default_rng(seed=int(seed))
    
    for clust in range(k):
        for _ in range(n//k):
            x = gen.normal(centers[clust], scale=standard_deviation)
            data.append(x)
            
    data = np.asarray(data)
    return data
    

def generate_linear(n, max, seed):
    rand = random.Random()
    rand.seed(seed)
    return [int(rand.random()*max) for x in range(n)]
