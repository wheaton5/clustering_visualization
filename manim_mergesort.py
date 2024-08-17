from manim import *
import data_generation
import random
import numpy as np
from colour import Color
from manim import config
config.max_files_cached = 1000

import math

class PlayMergesort(Scene):

    def construct(self):
        playsection0 = True
        playsection1 = True
        playsection2 = True
        playsection3 = True
        playsection4 = True
        playsection5 = True
        playsection6 = True
        playsection7 = True
        
        
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

        n = 16
        max = 100
        seed = 7
        data = data_generation.generate_linear(n,max, seed)
        array_y_location = [0,2.25,0]
        side_length = 0.5
        buffer = side_length
        text_scale = 0.65
        number_scale = 0.5
        title = Tex("Mergesort: textbook divide and conquer")
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
                     

        self.next_section(skip_animations=not playsection0)
        text1 = Tex("1. Recursively split data in half until the data are singletons.").shift(DOWN*3.5).scale(text_scale)
        self.play(create_text(text1))


        # SECTION 1
        self.next_section(skip_animations=not playsection1)

        square_objects_level2 = []
        animations = []
        ybuff = DOWN*1.15
        xbuff = RIGHT*1.75
        for x in range(n):
            square = Square(side_length=side_length)
            #loc = array_y_location + DOWN*1
            square_objects_level2.append(square)
            square.move_to(array_y_location)
            square.shift(get_x_shift(x,n,side_length))
            self.add(square)
            xdirection = -1
            if x > n/2-1:
                xdirection = 1
            line = Line(square.get_center(), square.get_center()+ybuff+xbuff*xdirection)
            animations.append(MoveAlongPath(square, line))
            animations.append(MoveAlongPath(number_objects[x], line))

        xshiftdivider = 2.5
        self.play(animations, run_time=2)
        self.wait()
        


        # SECTION 2
        self.next_section(skip_animations=not playsection2)

        square_objects_level3 = []
        animations = [] 
        for x in range(n):
            square = Square(side_length=side_length)
            square_objects_level3.append(square)
            square.move_to(square_objects_level2[x].get_center())
            xdirection = -1/xshiftdivider
            if x % (n/2) > n/4-1:
                xdirection = 1/xshiftdivider
            print(x, "x % (n/2)", x % (n/2), "n/4-1", xdirection)
            line = Line(square.get_center(), square.get_center()+ybuff+xbuff*xdirection)
            animations.append(MoveAlongPath(square, line))
            animations.append(MoveAlongPath(number_objects[x], line))
        
        self.play(animations, run_time=2)
        self.wait()



        # SECTION 3
        self.next_section(skip_animations=not playsection3)

        square_objects_level4 = []
        animations = []
        for x in range(n):
            square = Square(side_length=side_length)
            square_objects_level4.append(square)
            square.move_to(square_objects_level3[x])
            xdirection = -1/xshiftdivider/xshiftdivider
            if x % (n/4) > n/8-1:
                xdirection = 1/xshiftdivider/xshiftdivider
            line = Line(square.get_center(), square.get_center()+ybuff+xbuff*xdirection)
            animations.append(MoveAlongPath(square, line))
            animations.append(MoveAlongPath(number_objects[x], line))

        self.play(animations, run_time=2)
        self.wait()

    
    
        #SECTION 4
        self.next_section(skip_animations=not playsection4)    

        square_objects_level5 = []
        animations = []
        for x in range(n):
            square = Square(side_length=side_length)
            square_objects_level5.append(square)
            square.move_to(square_objects_level4[x])
            xdirection = -1/xshiftdivider/xshiftdivider/xshiftdivider
            if x % (n/8) > n/16-1:
                xdirection = 1/xshiftdivider/xshiftdivider/xshiftdivider
            line = Line(square.get_center(), square.get_center()+ybuff+xbuff*xdirection)
            animations.append(MoveAlongPath(square, line))
            animations.append(MoveAlongPath(number_objects[x], line))

        self.play(animations, run_time=2)
        self.wait()


        #SECTION 5
        self.next_section(skip_animations=not playsection5)

        self.play(FadeOut(text1))
        text2 = Tex("Merge subarrays in a sorted manner. Consider the two subarrays on the left.").move_to(text1.get_center()).scale(text_scale)
        #text3 = Tex("Consider the two subarrays on the left").move_to(text1.get_center()).scale(text_scale)
        self.play(create_text(text2))
        self.wait()
        rectangle = SurroundingRectangle(VGroup(square_objects_level5[0], square_objects_level5[1]))
        self.play(FadeIn(rectangle))
        self.play(FadeOut(text2))


        # SECTION 6
        self.next_section(skip_animations= not playsection6)

        text3 = Tex(r"{15cm}Put a pointer at the first element of each array. We will denote those by colored squares.", tex_environment="minipage").move_to(text1.get_center()).scale(text_scale)
        self.play(create_text(text3))
        self.play(FadeToColor(square_objects_level5[0], "#FF0000"), FadeToColor(square_objects_level5[1], "#0000FF"))
        self.wait()
        self.play(FadeOut(text3))
        text4 = Tex(r"{15cm}Compare the values at these pointers and add the smaller one to the merged array", tex_environment="minipage").move_to(text1.get_center()).scale(text_scale)
        self.play(create_text(text4))
        self.wait()
        
        compare = Tex(str(data[1]) + " $<$ "+str(data[0])).move_to(rectangle).scale(text_scale).shift(DOWN*0.65)
        self.play(FadeIn(compare))
        line = Line(number_objects[1].get_center(), square_objects_level4[0].get_center())
        self.play(MoveAlongPath(number_objects[1], line), FadeToColor(square_objects_level5[1], WHITE), FadeOut(compare))
        self.play(FadeOut(text4))
        text5 = Tex(r"{15cm}Move the pointer from the minimum element forward. In this case it is the end of the array.", tex_environment="minipage").scale(text_scale).move_to(text1.get_center())
        compare2 = Tex(str(data[0]) + " $< \infty$ ").move_to(rectangle).scale(text_scale).shift(DOWN*0.65)
        self.play(create_text(text5))
        self.play(FadeToColor(square_objects_level5[0], WHITE), FadeIn(compare2))
        line = Line(number_objects[0].get_center(), square_objects_level4[1].get_center())
        self.play(MoveAlongPath(number_objects[0], line), FadeToColor(square_objects_level5[0], WHITE), FadeOut(compare2))
        self.play(FadeOut(text5))

        #SECTION 7
        self.next_section(skip_animations=not playsection7)
        text6 = Tex("And the same for the rest")
        swap(data, 0, 1)
        swap(number_objects, 0, 1)
        
        animations1 = [] 
        animations2 = []
        for i in range(1,n//2):
            start = i*2
            next = start + 1
            mindex = np.argmin(data[start:next+1])+start
            maxdex = np.argmax(data[start:next+1])+start
            loc = (square_objects_level5[start].get_center() + square_objects_level5[next].get_center())/2
            compare = Tex(str(data[mindex]) + " $<$ "+str(data[maxdex])).move_to(loc).scale(text_scale).shift(DOWN*0.65)
            animations1.append(FadeIn(compare))
            line = Line(number_objects[mindex].get_center(), square_objects_level4[start].get_center())
            animations2.append(MoveAlongPath(number_objects[mindex], line))
        self.play(animations1)
        self.wait()
        self.play(animations2)
        self.wait()
        

