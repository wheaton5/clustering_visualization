from manim import *
import data_generation
import random
from colour import Color

import math

class PlayQuicksort(Scene):

    def construct(self):
        def get_x_shift(index, n, side_length):
            return (n/2 - (index+1/2))*LEFT*side_length
    
        def get_blue(p):
            light_blue = Color("#cadeef")
            dark_blue = Color("#090088")
            low_red = light_blue.get_red()
            low_green = light_blue.get_green()
            low_blue = light_blue.get_blue()
            high_red = dark_blue.get_red()
            high_green = dark_blue.get_green()
            high_blue = dark_blue.get_blue()
            new_red = (high_red-low_red)*p+low_red
            new_green = (high_green-low_green)*p+low_green
            new_blue = (high_blue-low_blue)*p+low_blue
            c = Color()
            c.set_red(new_red)
            c.set_green(new_green)
            c.set_blue(new_blue)
            print(c.get_hex_l())
            return c


        def partitioning_in_place(x, pivot_index):
            print("pivot", pivot_index, "value",x[pivot_index])
            partitioning_index = []
            newx = []
            newx_index = []
            newx.append(x[pivot_index])
            newx_index.append(pivot_index)
            for (index, blah) in enumerate(x):
                if index != pivot_index:
                    newx.append(blah)
                    newx_index.append(index)
            newx.append(math.inf)
            low = 1
            high = len(newx) - 1
            while high > low:
                while newx[high] >= x[pivot] and high > 0:
                    high -= 1
                while newx[low] < x[pivot]:
                    low += 1
                if newx[high] < newx[low] and high > low:
                    tmp = newx[low]
                    newx[low] = newx[high]
                    newx[high] = tmp
                    tmp = newx_index[low]
                    newx_index[low] = newx_index[high]
                    newx_index[high] = tmp
            tmp = newx[0]
            newx[0]=newx[high] 
            newx[high] = tmp
            tmp = newx_index[0]
            newx_index[0] = newx_index[high]
            newx_index[high] = tmp
            new_pivot = high
            print("data")
            print(x)
            print("new data")
            print(newx)
            print("new indices")
            print(newx_index)
            return (new_pivot, newx_index)
            

        n = 16
        max = 100
        seed = 6
        data = data_generation.generate_linear(n,max, seed)
        array_y_location = [0,2,0]
        side_length = 0.75
        buffer = side_length
        text_scale = 0.75
        title = Text("Quicksort: the god of all sorting methods")
        title.to_edge(UP)
        self.add(title)
        number_objects = []
        square_objects = []
        for x in range(n):
            blah = Square(side_length=side_length)
            square_objects.append(blah)
            loc = array_y_location
            blah.move_to(loc)
            blah.shift(get_x_shift(x,n,side_length))
            text = Text(str(data[x]))
            number_objects.append(text)
            text.move_to(loc)
            text.shift(get_x_shift(x,n,side_length))
            text.scale(text_scale)
            self.add(text)
            self.add(blah)
            
            text.set_color(get_blue(data[x]/max))    
        text1 = Text("High level process")
        text2 = Text("1. Choose an element often called the pivot")
        text3 = Paragraph("2. Rearrange the array such that all elements less than the pivot", "are on the left and all elements that are greater than the pivot are on the right", alignment="center")
        text4 = Paragraph("This is known as \"partitioning\" the array.", alignment="center")
        text5 = Text("3. Repeat 1-2 on the subarrays to the left and right of the pivot until the subarrays are length 1")
        text_group = VGroup(text1, text2, text3, text4, text5).arrange(DOWN, buff=0.5)
        text_group.scale(0.5)
        text_group.shift(DOWN*1)
        self.play(Create(text1), run_time=2)
        self.wait(1)
        self.play(Create(text2), run_time=3)
        self.wait(2)
        rand = random.Random()
        rand.seed(seed)
        pivot = rand.randint(0,n-1)
        newsquare = Square(side_length = side_length)
        newsquare.move_to(array_y_location)
        newsquare.shift(get_x_shift(pivot,n,side_length))
        self.add(newsquare)
        self.play(FadeToColor(number_objects[pivot], "#FF0000"), FadeToColor(newsquare, "#FF0000"))
        self.play(Create(text3), run_time=7)
        (new_pivot, new_indices) = partitioning_in_place(data, pivot)
        animations1 = []
        new_data = []
        new_number_objects = []
        print("new indices", new_indices)
        print("old pivot",pivot, data[pivot])
        
        for (index, new_index) in enumerate(new_indices):
            line = Line(number_objects[new_index].get_center(), number_objects[index].get_center())
            animations1.append(MoveAlongPath(number_objects[new_index], line))
            new_data.append(data[new_index])
            new_number_objects.append(number_objects[new_index])
        print("new pivot", new_pivot, "new pivot", new_data[new_pivot])
        print(new_data)
        line = Line(new_number_objects[new_pivot].get_center(), number_objects[new_pivot].get_center())
        animations1.append(MoveAlongPath(newsquare, line))
        self.play(animations1,run_time = 8)
        self.wait(1)
        self.play(Create(text4, run_time=4))
        self.wait(1)
        text5.move_to(text4.get_center())
        self.play(FadeOut(text4))
        self.play(Create(text5), run_time=3)
        self.wait(1)
        self.play(FadeToColor(new_number_objects[new_pivot], GREY), FadeToColor(newsquare, "#636363"))
        brace_shift = 0.3
        brace1 = BraceBetweenPoints(new_number_objects[0].get_center(), new_number_objects[new_pivot-1].get_center()).shift(DOWN*brace_shift)
        brace2 = BraceBetweenPoints(new_number_objects[new_pivot+1].get_center(), new_number_objects[n-1].get_center()).shift(DOWN*brace_shift)
        self.play(Create(brace1), Create(brace2), run_time=3)
        self.wait(2)

