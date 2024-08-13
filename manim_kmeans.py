from manim import *
import kmeans
import data_generation
import random
from colour import Color


def manim_data(k, n, standard_deviation, seed):
    rand = random.Random()
    rand.seed(seed)
    data = data_generation.generate_simple(k, n, 100, standard_deviation, rand.random()*1000000)
    return data

def manim_kmeans_iteration(data, k, standard_deviation, seed, max_iter = 1000):
    rand = random.Random()
    rand.seed(seed)
    centers = kmeans.kmeans_initialize(data, k, rand.random()*1000000)
    kmeans_states = []
    anychange = True
    iteration = 1
    while anychange:
        (anychange, states) = kmeans.kmeans_iteration(data, centers)
        iteration += 1
        print(anychange)
        kmeans_states.append(states)
        centers = states[1].cluster_centers.copy()
        if iteration >= max_iter:
            break
    return kmeans_states
    


class PlayKmeans(Scene):
    def construct(self):
        num_clusters = 5
        data = manim_data(num_clusters, 1000, 7, 4)
        kmeans_states = manim_kmeans_iteration(data, num_clusters, 7, 7)
        ax = Axes(
            x_range=[0, 100, 10],
            y_range=[0, 100, 10],
            tips=False,
            axis_config={"include_numbers": True},
            y_length=5.5,
            x_length=5.5
        )
        ax.to_edge(LEFT)
        ax.shift(DOWN*0.25)
        
        self.add(ax)
        colors = [Color(hue=i/num_clusters, saturation=1, luminance=0.5).get_hex_l() for i in range(num_clusters)]
        data_objects = []
        for x in kmeans_states[0][0].data:
            z = x 
            datapoint = Dot(color="white")
            datapoint.scale(0.25)
            data_objects.append(datapoint)
            translated_point = ax.coords_to_point([z])
            datapoint.move_to(translated_point)
            self.add(datapoint)
        text = Text("Kmeans Clustering -- Lloyd's algorithm").to_edge(UP) 
        self.add(text)
        
        text1 = Text("1. Randomly choose k data points\n as cluster centers")
        text1.scale(0.5)
        text2 = Text("2. Assign data points to their\n closest cluster center ")
        text2.scale(0.5)
        text3 = Text("3. Update cluster centers to the\n average position of the data points\n which are assigned to them")
        text3.scale(0.5)
        text4 = Text("4. Repeat 2-3 until no change")
        text4.scale(0.5)
        text5 = Text("5. Repeat 1-4 many times and\n choose the solution with\n the lowest sum of squared distances\n from a data point to its cluster center")
        text5.scale(0.5)
        text_group = VGroup(text1, text2, text3, text4, text5).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        text_group.move_to([3,-0.5,0])
        self.play(Create(text1, run_time=4))
        self.play(Wait(1))
        animations1 = []
        animations2 = []
        cluster_center_objects = []
        points_to_remove = []
        for clust in range(len(kmeans_states[0][0].cluster_centers)):
            center = Star(fill_color = colors[clust],fill_opacity=1.0, stroke_color="light_grey", stroke_width=4)

            center.scale(0.3)
            translated_point = ax.coords_to_point([kmeans_states[0][0].cluster_centers[clust]])
            center.move_to(translated_point)
            cluster_center_objects.append(center)
            point = Dot(color="white")
            points_to_remove.append(point)
            point.move_to(translated_point)
            point.scale(0.25)
            self.add(point)
            animations1.append(Indicate(point, scale_factor=8, color = "yellow", run_time=2))
            animations2.append(Create(center,run_time=2))
        self.play(animations1)
        self.play(animations2)
        self.play(Create(text2, run_time=4))
        for point in points_to_remove:
            self.remove(point)
        self.play(Wait(1))
        animations3 = []
        for index in range(len(data_objects)):
            animations3.append(FadeToColor(data_objects[index], color=colors[kmeans_states[0][0].assignments[index]]))
        self.play(animations3, run_time = 2)
        self.play(Wait(1.5))
        self.play(Create(text3, run_time=5))
        self.play(Wait(1))
        animations4 = []
        for clust in range(len(kmeans_states[0][0].cluster_centers)):
            cluster_obj = cluster_center_objects[clust]
            translated_point = ax.coords_to_point([kmeans_states[0][1].cluster_centers[clust]])
            line = Line(cluster_obj.get_center(), translated_point)
            animations4.append(MoveAlongPath(cluster_obj, line))
        self.play(animations4, run_time=2.5)
        self.play(Create(text4, run_time=2))
        self.play(Wait(1))
        for kmeans_state_i in range(1,min(4,len(kmeans_states))):
            #self.play(Wiggle(text2))
            animations3 = []
            for index in range(len(data_objects)):
                animations3.append(FadeToColor(data_objects[index], color=colors[kmeans_states[kmeans_state_i][0].assignments[index]]))
            self.play(Indicate(text2), animations3, run_time = 2.5)
            #self.play(Wiggle(text3))
            animations4 = []
            for clust in range(len(kmeans_states[0][0].cluster_centers)):
                cluster_obj = cluster_center_objects[clust]
                translated_point = ax.coords_to_point([kmeans_states[kmeans_state_i][1].cluster_centers[clust]])
                line = Line(cluster_obj.get_center(), translated_point)
                animations4.append(MoveAlongPath(cluster_obj, line))
            self.play(Indicate(text3),animations4, run_time = 2.5)
        self.play(Create(text5, run_time=7))
        self.play(Wait(1))
        kmeans_states = manim_kmeans_iteration(data, num_clusters, 7, 4, max_iter = 5)
        animations1 = []
        animations2 = []
        for data_obj in data_objects:
            animations1.append(FadeToColor(data_obj, color = "white"))
        for cluster in range(num_clusters):
            animations1.append(FadeOut(cluster_center_objects[cluster]))
            animations2.append(Create(cluster_center_objects[cluster]))
        self.play(animations1)
        for cluster in range(num_clusters):
            print("cluster center ", cluster, " point ", kmeans_states[0][0].cluster_centers[cluster])
            translated_point = ax.coords_to_point([kmeans_states[0][0].cluster_centers[cluster]])
            print("translated point ",translated_point)
            cluster_center_objects[cluster].move_to(translated_point)
        self.wait(1)
        self.play(animations2)
        for kmeans_state_i in range(0,min(4,len(kmeans_states))):
            #self.play(Wiggle(text2))
            animations3 = []
            for index in range(len(data_objects)):
                animations3.append(FadeToColor(data_objects[index], color=colors[kmeans_states[kmeans_state_i][1].assignments[index]]))
            self.play(Indicate(text2), animations3, run_time = 2.5)
            #self.play(Wiggle(text3))
            animations4 = []
            for clust in range(len(kmeans_states[0][0].cluster_centers)):
                cluster_obj = cluster_center_objects[clust]
                translated_point = ax.coords_to_point([kmeans_states[kmeans_state_i][1].cluster_centers[clust]])
                line = Line(cluster_obj.get_center(), translated_point)
                animations4.append(MoveAlongPath(cluster_obj, line))
            self.play(Indicate(text3),animations4, run_time = 2.5)
        self.wait(2)
