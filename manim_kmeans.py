from manim import *
import kmeans
import data_generation
import random


def manim_kmeans_iteration(k, n, standard_deviation, seed):
    rand = random.Random()
    rand.seed(seed)
    data = data_generation.generate_simple(k, n, 100, standard_deviation, rand.random()*1000000)
    print(data)
    centers = kmeans.kmeans_initialize(data, k, rand.random()*1000000)
    print(centers)
    kmeans_states = []
    anychange = True
    while anychange:
        (anychange, states) = kmeans.kmeans_iteration(data, centers)
        print(anychange)
        kmeans_states.append(states)
        centers = states[1].cluster_centers.copy()
    return kmeans_states
    

class PlayKmeans(Scene):
    def construct(self):
        kmeans_states = manim_kmeans_iteration(30, 3000, 0.5, 4)
        ax = Axes(
            x_range=[0, 100, 10],
            y_range=[0, 100, 10],
            tips=False,
            axis_config={"include_numbers": True},
        )
        self.add(ax)
        for x in kmeans_states[0][0].data:
            z = x 
            datapoint = Circle(radius=0.01)
            translated_point = ax.coords_to_point([z])
            datapoint.move_to(translated_point)
            self.add(datapoint)
        



