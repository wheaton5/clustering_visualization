# this implementation is broken up and made more complicated because 
# I want to be able to inspect and visualized the state of the algorithm after each step

import random
import numpy as np


class KHarmonicMeansState:
    """Kmeans state class to be able to track the state of the kmeans algorithm after each step"""
    def __init__(self, data, assignments, cluster_centers):
        self.data = data
        self.assignments = assignments
        self.cluster_centers = cluster_centers

def k_harmonic_means_initialize(data, k, seed):
    random.seed(seed)
    cluster_centers = random.sample(data, k)
    return cluster_centers 

def k_harmonic_means_assign_datapoints(data, centers):
    return [np.argmin(euclidean_dists(x,centers)) for x in data] 

def euclidean_dists(x, centers):
    return [euclidean_dist(x,center) for center in centers]

def euclidean_dist(x, center):
    return np.sqrt(np.sum([np.pow(x[i]-center[i],2) for i in range(len(x))]))

def kmeans_update_cluster_centers(data, centers):
    
