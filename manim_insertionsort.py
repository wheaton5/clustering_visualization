from manim import *
import data_generation
import random
import numpy as np
from colour import Color
from manim import config
config.max_files_cached = 1000

import math

class PlayInsertionsort(Scene):

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
        seed = 15
        data = data_generation.generate_linear(n,50, seed)
        print(data)
        array_y_location = [0,2.25,0]
        side_length = 0.75
        buffer = side_length
        text_scale = 0.65
        number_scale = 0.5
        title = Tex("Insertion sort")
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
        text1 = Tex("Insertion sort works by maintaining the invariant that a subarray on the left is in-order and each new element we insert it to its sorted order in that subarray.")
        text2 = Tex("To begin, a subarray of length 1 on the left is already sorted.")
        text3 = Tex("We consider the first element to the right of the sorted subarray, store it in a temporary variable.")
        text4 = Tex("Find the position in which it should be inserted and shift all items over to make space for it.")
        text5 = Tex("Continue this process expanding the length of the sorted subarray each time.") 
        textgroup = VGroup(text1, text2, text3, text4, text5).arrange(DOWN, buff=0.4).scale(text_scale).shift(DOWN*1.85)
    
        #### SECTION 1
        self.next_section(skip_animations=False)
        self.play(create_text(text1))
        pointer = 1
        self.play(create_text(text2))
        partitionline = Line(square_objects[0].get_center()+RIGHT*side_length/2.0+UP*0.75, square_objects[0].get_center()+RIGHT*side_length/2.0+DOWN*0.75)
        self.play(Create(partitionline))
        self.play(create_text(text3))
        tmpsquare = Square(side_length=side_length).move_to(array_y_location+DOWN*1.65)
        tmptext = Tex("tmp").scale(text_scale).move_to(tmpsquare.get_center()+UP*0.6)
        square_interest = square_objects[1].copy().set_color("#FF0000").scale(0.9)
        self.play(Create(tmpsquare), FadeIn(tmptext),FadeIn(square_interest))
        newnumber = number_objects[pointer].copy().move_to(tmpsquare.get_center())
        newsquare = square_interest.copy().move_to(tmpsquare.get_center())
        self.play(Transform(number_objects[pointer], newnumber), Transform(square_interest, newsquare))
        self.play(Transform(partitionline, partitionline.copy().shift(RIGHT*side_length)))
        self.play(create_text(text4))
        number1 = number_objects[pointer].copy()
        number1_target = number1.copy().move_to(square_objects[0].get_center()).shift(DOWN*0.7 +LEFT*0.4)
        if data[pointer] < data[0]:
            cmptext = Tex(" $<$ ")
        else:
            cmptext = Tex(" $\geq$ ")
        cmptext.scale(text_scale).move_to(square_objects[0].get_center()+DOWN*0.7)
        number2 = number_objects[0].copy()
        number2_target = number2.copy().move_to(square_objects[0].get_center()).shift(DOWN*0.7+RIGHT*0.4)
        self.add(number1, number2)
        self.play(Transform(number1, number1_target, path_arc=-PI/2.5), Transform(number2, number2_target, path_arc=-PI/2.5), FadeIn(cmptext), run_time=1.5) 
        number1_target = number1.copy().shift(LEFT*side_length)
        infty = Tex("$-\infty$").scale(text_scale).move_to(square_objects[0].get_center()+LEFT*side_length)#+RIGHT*0.4+DOWN*0.7)
        infty_target = infty.copy().shift(RIGHT*0.4+DOWN*0.7)
        cmptext2 = Tex("$\geq$").scale(text_scale).move_to(square_objects[0].get_center()+LEFT*side_length+DOWN*0.7)
        self.wait()
        self.add(infty)
        self.play(Transform(number1, number1_target, path_arc = -PI/2.5), Transform(infty, infty_target, path_arc=-PI/2.5), FadeOut(cmptext), FadeIn(cmptext2), FadeOut(number2), run_time=1.5)
        self.wait()
        self.play(Transform(number_objects[0], number_objects[0].copy().shift(RIGHT*side_length)))
        
        self.play(Transform(number_objects[1], number_objects[1].copy().move_to(square_objects[0]), path_arc=-PI/2.5),
                Transform(square_interest, square_interest.copy().move_to(square_objects[0]), path_arc=-PI/2.5),
                FadeOut(number1), FadeOut(cmptext2), FadeOut(infty))
        swap(data, 0, pointer)
        swap(number_objects, 0, pointer)
        self.play(create_text(text5))
        print([i for i in range(2,n)])
        for i in range(2, n):
            pointer = i
            print("pointer", i)
            square_interest.move_to(square_objects[pointer])
            self.play(FadeIn(square_interest))
            self.wait(0.5)
            self.play(Transform(number_objects[pointer], number_objects[pointer].copy().move_to(tmpsquare), path_arc=PI/2),
                    Transform(square_interest, square_interest.copy().move_to(tmpsquare),path_arc=PI/2))
            self.play(Transform(partitionline, partitionline.copy().shift(RIGHT*side_length)))
            compare_pointer = pointer
            
            
            number1 = number_objects[pointer].copy()
            self.add(number1)
            print("we added number 1 at pointer ", pointer,"but havent moved anything yet")
            print("while ", data[pointer] ," < ", data[compare_pointer])
            while data[pointer] <= data[compare_pointer]:
                compare_pointer -= 1
                compare_pointer_loc = square_objects[compare_pointer].get_center() if compare_pointer >= 0 else square_objects[0].get_center() + LEFT*side_length
                compare_number = str(data[compare_pointer]) if compare_pointer >= 0 else "$-\infty$"
                if compare_pointer < 0:
                    number2color = WHITE
                    compare_operator = "$\geq$"
                else:
                    number2color = get_blue(int(compare_number)/max)
                    if data[pointer] < data[compare_pointer]:
                        compare_operator = "$<$"
                    else:
                        compare_operator = "$\geq$" 
                number1_target = number1.copy().move_to(compare_pointer_loc+DOWN*0.7+LEFT*0.4)
                number2 = Tex(compare_number, color=number2color).scale(text_scale).move_to(compare_pointer_loc)#+DOWN*0.7+RIGHT*0.4)
                
                self.add(number2)
                number2_target = number2.copy().shift(DOWN*0.7+RIGHT*0.4)
                compare_text = Tex(compare_operator).scale(text_scale).move_to(compare_pointer_loc+DOWN*0.7)
                self.play(Transform(number1, number1_target, path_arc=-PI/2.5),
                        Transform(number2, number2_target, path_arc=-PI/2.5),
                        FadeIn(compare_text))
                self.wait()
                if compare_pointer >= 0 and data[pointer] < int(compare_number):
                    self.play(FadeOut(compare_text), FadeOut(number2))
                else:
                    print("loop ", [i in range(pointer-1, compare_pointer, -1)])
                    print("trying to loop from ", pointer-1, " to ", compare_pointer)
                    print(type(pointer), type(compare_pointer))
                    new_data = [-1 for _ in range(len(data))]
                    new_number_objects = [None for _ in range(len(data))]
                    
                    for i in range(pointer-1, compare_pointer,-1):
                        target = number_objects[i].copy().shift(RIGHT*side_length)
                        self.play(Transform(number_objects[i], target))
                        print("storing ",data[i], " at ",i+1)
                        new_data[i+1] = data[i]
                        print("so far new data", new_data)
                        new_number_objects[i+1] = number_objects[i]
                    self.play(Transform(number_objects[pointer], number_objects[pointer].copy().move_to(square_objects[compare_pointer+1]),path_arc=-PI/2.5))
                    print("now storing ", data[pointer], "at", compare_pointer+1)
                    new_data[compare_pointer+1] = data[pointer]
                    print("new data", new_data)
                    print("is this none", number_objects[pointer])
                    new_number_objects[compare_pointer+1] = number_objects[pointer]
                    print("new number objects", new_number_objects)
                    print("new data small", new_data[(compare_pointer+1):(pointer+1)])
                    print("new number objects small", new_number_objects[(compare_pointer+1):(pointer+1)])
                    data[(compare_pointer+1):(pointer+1)] = new_data[(compare_pointer+1):(pointer+1)]
                    print(data)
                    number_objects[(compare_pointer+1):(pointer+1)] = new_number_objects[(compare_pointer+1):(pointer+1)]
                    print(number_objects)
                    self.play(FadeOut(compare_text), FadeOut(number2), FadeOut(number1))
                    
                
        
                
        self.wait(3)
