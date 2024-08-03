# this implementation is broken up and made more complicated because 
# I want to be able to inspect and visualized the state of the algorithm after each step

import random
import numpy as np
import loss_functions

class KmeansState:
    """Kmeans state class to be able to track the state of the kmeans algorithm after each step"""
    def __init__(self, data, assignments, cluster_centers):
        self.data = data
        self.assignments = assignments.deepcopy()
        self.cluster_centers = cluster_centers.deepcopy()

def kmeans_initialize(data, k, seed):
    gen = random.Random()
    gen.seed(seed)
    cluster_centers = random.sample(data, k)
    return cluster_centers 

def kmeans_assign_datapoints(data, centers):
    return [np.argmin(loss_functions.euclidean_dists(x,centers)) for x in data] 

def kmeans_update_cluster_centers(data, assignments, centers):
    new_centers = np.zeros(np.shape(centers))
    denoms = np.zeros(np.shape(centers))
    for (x, assignment) in zip(data, assignments):
        new_centers[assignment] += x
        denoms[assignment] += 1
    for i in range(len(centers)):
        new_centers[assignment] = new_centers[assignment] if denoms[assignment] == 0 else new_centers[assignment]/denoms[assignment]
    return new_centers

def kmeans_iteration(data, k, seed):
    centers = kmeans_initialize(data, k, seed)
    assignments = kmeans_assign_datapoints(data, centers)
    state1 = KmeansState(data, assignments, centers)
    centers = kmeans_update_cluster_centers(data, assignments, centers)
    state2 = KmeansState(data, assignments, centers)
    return [state1, state2]



