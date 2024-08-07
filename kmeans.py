# this implementation is broken up and made more complicated because 
# I want to be able to inspect and visualized the state of the algorithm after each step

import random
import numpy as np
import loss_functions

class KmeansState:
    """Kmeans state class to be able to track the state of the kmeans algorithm after each step"""
    def __init__(self, data, assignments, cluster_centers):
        self.data = data
        self.assignments = assignments.copy()
        self.cluster_centers = cluster_centers.copy()

def kmeans_initialize(data, k, seed):
    gen = random.Random()
    gen.seed(seed)
    
    cluster_center_indices = gen.sample(range(len(data)), k)
    cluster_centers = []
    for index in cluster_center_indices:
        cluster_centers.append(data[index])
    
    cluster_centers = np.array(cluster_centers)
    
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
        new_centers[i] = new_centers[i] if any(denoms[i] == 0) else new_centers[i]/denoms[i]
    return np.asarray(new_centers)

def kmeans_iteration(data, centers):
    assignments1 = kmeans_assign_datapoints(data, centers)
    state1 = KmeansState(data, assignments1, centers)
    centers2 = kmeans_update_cluster_centers(data, assignments1, centers)
    state2 = KmeansState(data, assignments1, centers2)
    anychange = False
    for i in range(len(centers)):
        anychange |= any(centers[i] != centers2[i])
    return (anychange, [state1, state2])



