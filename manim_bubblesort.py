from manim import *
import data_generation
import random
import numpy as np
from colour import Color
from manim import config
config.max_files_cached = 1000

import math

class PlayBubblesort(Scene):

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

        self.next_section(skip_animations=True)
        n = 8
        max = 50
        seed = 7
        data = data_generation.generate_linear(n,max, seed)
        print(data)
        array_y_location = [0,2.25,0]
        side_length = 0.75
        buffer = side_length
        text_scale = 0.65
        number_scale = 0.5
        title = Tex("Bubble sort")
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

        self.next_section(skip_animations=not playsections[0])
        text1 = Tex("1. Make two pointers i and j at positions 0 and 1.")
        text2 = Tex("2. Compare the values at those indices and swap if arr[i] $>$ arr[j].")
        text3 = Tex("3. Move both pointers forward by 1.") 
        text4 = Tex("4. Continue 2-3 until at the end of the array.")
        text5 = Tex("5. Repeat 1-4 n times or until one pass results in no changes.")
        textgroup = VGroup(text1, text2, text3, text4, text5).arrange(DOWN, buff=0.5).scale(text_scale).shift(DOWN*1.5)
        self.play(create_text(text1))
        pointer1 = 0
        pointer2 = 1
        pointer1text = Tex("$i$").scale(text_scale).move_to(square_objects[0]).shift(DOWN*0.65)
        pointer2text = Tex("$j$").scale(text_scale).move_to(square_objects[1]).shift(DOWN*0.65)
        self.play(Create(pointer1text), Create(pointer2text), run_time=1)
        self.play(create_text(text2))
        if data[pointer1] <= data[pointer2]:
            cmp = " $\leq$ "
        else:
            cmp = " $>$ "
        comptext = Tex(str(data[pointer1]) + cmp +str(data[pointer2])).scale(text_scale).move_to((square_objects[pointer1].get_center() + square_objects[pointer2].get_center())/2.0).shift(DOWN*1.2)
        self.play(FadeIn(comptext))
        if data[pointer1] > data[pointer2]:
            line1 = Line(number_objects[pointer1].get_center(),number_objects[pointer2].get_center())
            line2 = Line(number_objects[pointer2].get_center(),number_objects[pointer1].get_center())
            
            self.play(MoveAlongPath(number_objects[pointer1],line1), MoveAlongPath(number_objects[pointer2], line2))
            swap(data, pointer1, pointer2)
            swap(number_objects, pointer1, pointer2)
        self.play(FadeOut(comptext))
        self.play(create_text(text3))
        self.wait(0.5)
        self.play(create_text(text4))

        self.next_section(skip_animations=False)
        
        for i in range(1, n-1):
            line1 = Line(pointer1text.get_center(),pointer1text.get_center()+RIGHT*side_length)
            line2 = Line(pointer2text.get_center(),pointer2text.get_center()+RIGHT*side_length)
            self.play(MoveAlongPath(pointer1text, line1), MoveAlongPath(pointer2text, line2), Indicate(text3), run_time=1.25)
            self.wait(0.5)
            pointer1 = i
            pointer2 = i+1
            if data[pointer1] <= data[pointer2]:
                cmp = " $\leq$ "
            else:
                cmp = " $>$ "
            cmptext = Tex(str(data[pointer1])+cmp+str(data[pointer2])).scale(text_scale).move_to((square_objects[pointer1].get_center()+square_objects[pointer2].get_center())/2.0).shift(DOWN*1.2)
            self.play(Indicate(text2), FadeIn(cmptext),run_time=1.5)
            if data[pointer1] > data[pointer2]:
                line1 = Line(square_objects[pointer1].get_center(), square_objects[pointer2].get_center())
                line2 = Line(square_objects[pointer2].get_center(), square_objects[pointer1].get_center())
                self.play(MoveAlongPath(number_objects[pointer1], line1), MoveAlongPath(number_objects[pointer2], line2))
                swap(data, pointer1, pointer2)
                swap(number_objects, pointer1, pointer2)
            self.play(FadeOut(cmptext))


        self.next_section(skip_animations=False)
        self.play(create_text(text5)) 
        for iteration in range(n):
            anychange = False
            pointer1 = 0
            pointer2 = 1
            line1 = Line(pointer1text.get_center(), square_objects[pointer1].get_center()+DOWN*0.65)
            line2 = Line(pointer2text.get_center(), square_objects[pointer2].get_center()+DOWN*0.65)
            
            self.play(Indicate(text5))            
            self.play(Indicate(text1), MoveAlongPath(pointer1text, line1), MoveAlongPath(pointer2text, line2), run_time=1.5) 
            for i in range(n-1):
                if not i == 0:
                    line1 = Line(pointer1text.get_center(),pointer1text.get_center()+RIGHT*side_length)
                    line2 = Line(pointer2text.get_center(),pointer2text.get_center()+RIGHT*side_length)
                    self.play(MoveAlongPath(pointer1text, line1), MoveAlongPath(pointer2text, line2), Indicate(text3), run_time=1.25)
                    self.wait(0.5)
                pointer1 = i
                pointer2 = i+1
                if data[pointer1] <= data[pointer2]:
                    cmp = " $\leq$ "
                else:
                    cmp = " $>$ "
                cmptext = Tex(str(data[pointer1])+cmp+str(data[pointer2])).scale(text_scale).move_to((square_objects[pointer1].get_center()+square_objects[pointer2].get_center())/2.0).shift(DOWN*1.2)
                self.play(Indicate(text2), FadeIn(cmptext), run_time=1.5)
                if data[pointer1] > data[pointer2]:
                    line1 = Line(square_objects[pointer1].get_center(), square_objects[pointer2].get_center())
                    line2 = Line(square_objects[pointer2].get_center(), square_objects[pointer1].get_center())
                    self.play(MoveAlongPath(number_objects[pointer1], line1), MoveAlongPath(number_objects[pointer2], line2))
                    swap(data, pointer1, pointer2)
                    swap(number_objects, pointer1, pointer2)
                    anychange = True
                self.play(FadeOut(cmptext))         
            if not anychange:
                break
        
        


