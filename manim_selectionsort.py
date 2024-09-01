from manim import *
import data_generation
import random
import numpy as np
from colour import Color
from manim import config
config.max_files_cached = 1000

import math

class PlaySelectionsort(Scene):

    def construct(self):
        playsections = [True for _ in range(12)]
        #playsections[4] = True
        #playsections[5] = True
        #playsections[6] = True
        #playsections[7] = True
        #playsections[8] = True
        #playsections[9] = True
        #playsections[10] = True
        playsections[11] = True
        
        def swap(array, i, j):
            tmp = array[i]
            array[i] = array[j]
            array[j] = tmp
        
        def create_text(text_object):
            return Create(text_object, run_time = 0.065*len(text_object[0]))
    
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
            return c

        self.next_section(skip_animations=False)
        n = 8
        max = 75
        seed = 9
        data = data_generation.generate_linear(n,50, seed)
        print(data)
        array_y_location = [0,1.5,0]
        side_length = 0.75
        buffer = side_length
        text_scale = 0.65
        number_scale = 0.5
        title = Tex("Selection sort")
        title.scale(1.15)
        
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
            text.scale(number_scale)
            self.add(text)
            self.add(blah)
            text.set_color(get_blue(data[x]/max))    
                     
        def swap(arr, i, j):
            tmp = arr[i]
            arr[i] = arr[j]
            arr[j] = tmp

        ###section 0
        self.next_section(skip_animations=False)
        text1 = Tex("Selection sort works by selecting the minimum element from the array, and swapping it with the first index.")
        text2 = Tex("Iterate through the array and keep track of the minimum so far.")
        text3 = Tex("And swap the minimum element with the first index.")
        text4 = Tex("Now the elements on the left of the line are in sorted order.")
        text5 = Tex("We continue to select the minimum element from the subarray right of the line and swapping with the first index of the subarray.") 
        textgroup = VGroup(text1, text2, text3, text4, text5).arrange(DOWN, buff=0.5).scale(text_scale).shift(DOWN*2)
    
        #### SECTION 1
        self.next_section(skip_animations=False)
        self.play(create_text(text1))
        pointer = 0
        self.play(create_text(text2))
        pointertext = Tex("$i$").scale(text_scale).move_to(square_objects[0]).shift(DOWN*0.65)
        mindexsofar = 0
        mintext = Tex("Min").scale(text_scale).move_to(square_objects[0].get_center()+UP*0.65)
        minsquare = Square(side_length=side_length, color="#FF0000").move_to(square_objects[0]).scale(0.9)
        self.play(FadeIn(mintext), FadeIn(minsquare), FadeIn(pointertext))
        for i in range(1,n):
            line = Line(pointertext.get_center(), pointertext.get_center()+RIGHT*side_length)
            #self.play(MoveAlongPath(pointertext, line))
            animations = [] 
            minsofar = data[mindexsofar]
            if data[i] < data[mindexsofar]:
                mindexsofar = i
                cmp = " $<$ "
                line1 = Line(mintext.get_center(), square_objects[i].get_center()+UP*0.65)
                line2 = Line(minsquare.get_center(), square_objects[i].get_center())
                animations.extend([MoveAlongPath(mintext, line1), MoveAlongPath(minsquare, line2)])
            else:
                cmp = " $\geq$ "
                
            cmptext = Tex(str(data[i]) + cmp + str(minsofar)).scale(text_scale).move_to(pointertext.get_center()+RIGHT*side_length).shift(DOWN*0.45)
            self.play(FadeIn(cmptext), MoveAlongPath(pointertext, line))
            if len(animations) > 0:
                self.play(animations)
            self.play(FadeOut(cmptext))
        self.play(FadeOut(pointertext), create_text(text3)) 

        self.next_section(skip_animations=False)
        
        line1 = Line(square_objects[0].get_center(), square_objects[mindexsofar].get_center())
        line2 = Line(square_objects[mindexsofar].get_center(), square_objects[0].get_center())
        partition_line = Line(square_objects[0].get_center()+RIGHT*side_length*0.5 + DOWN*0.5, square_objects[0].get_center()+RIGHT*side_length*0.5 + UP*0.5, color=WHITE).scale(1.25)
        self.play(MoveAlongPath(number_objects[0], line1), MoveAlongPath(number_objects[mindexsofar], line2), FadeOut(minsquare), FadeOut(mintext), Create(partition_line))
        swap(data, 0, mindexsofar)
        swap(number_objects,0, mindexsofar)
        self.wait()

        ####SECTION 2
        self.next_section(skip_animations=False)
        self.play(create_text(text4))
        self.wait(0.5)
        self.play(create_text(text5))
        self.wait(0.5)

        self.next_section(skip_animations=False)
        for i in range(1,n-1):
            pointer1 = i
            pointertext.move_to(square_objects[i].get_center()+DOWN*0.6)
            minsquare.move_to(square_objects[i].get_center())
            mintext.move_to(square_objects[i].get_center()+UP*0.6)
            self.play(FadeIn(pointertext), FadeIn(minsquare), FadeIn(mintext))
            mindexsofar = pointer1
            minsofar = data[pointer1]
            for j in range(i+1, n):
                minsofar = data[mindexsofar]
                if data[j] < data[mindexsofar]:
                    cmp = " $<$ "
                    mindexsofar = j
                else:
                    cmp = " $\geq$ "
                cmptext = Tex(str(data[j]) + cmp + str(minsofar)).scale(text_scale).move_to(pointertext.get_center()+RIGHT*side_length).shift(DOWN*0.45)
                line = Line(pointertext.get_center(), pointertext.get_center()+RIGHT*side_length)
                self.play(FadeIn(cmptext), MoveAlongPath(pointertext, line))
                if data[j] < minsofar:
                    line1 = Line(minsquare.get_center(), square_objects[j].get_center())
                    line2 = Line(mintext.get_center(), square_objects[j].get_center()+UP*0.6)
                    self.play(MoveAlongPath(minsquare, line1), MoveAlongPath(mintext, line2), FadeOut(cmptext))
                else:
                    self.play(FadeOut(cmptext))
            line1 = Line(square_objects[i].get_center(), square_objects[mindexsofar].get_center())
            line2 = Line(square_objects[mindexsofar].get_center(), square_objects[i].get_center())
            line3 = Line(partition_line.get_center(), partition_line.get_center()+RIGHT*side_length)
            self.play(FadeOut(pointertext), FadeOut(mintext), FadeOut(minsquare), MoveAlongPath(number_objects[i], line1), MoveAlongPath(number_objects[mindexsofar], line2), MoveAlongPath(partition_line, line3))
            swap(data, i, mindexsofar)
            swap(number_objects, i, mindexsofar)
