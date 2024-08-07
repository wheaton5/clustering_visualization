import numpy as np

def euclidean_dist(x,y):
    #return np.linalg.norm(x-y)
    sum = 0
    for i in range(2):
        sum += (x[i]-y[i])**2
    #print(x, y, sum, np.sqrt(sum))
    return np.sqrt(sum)

def euclidean_dists(x, centers):
    if x[1] < 0 and x[0] > 25 and x[0] < 30:
        print("dists")
        print(x, centers)
        print([euclidean_dist(x,center) for center in centers])
        print("assignment", np.argmin([euclidean_dist(x,center) for center in centers]))
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

