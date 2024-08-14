from manim import *
import data_generation
import random
from colour import Color

import math

class PlayQuicksort(Scene):

    def construct(self):
        def create_text(text_object):
            return Create(text_object, run_time = 0.1*len(text_object[0]))
    
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

        def partitioning_subarray_helper(start, pivot, new_indices):
            return (pivot + start, [new_indices[i] + start for i in range(len(new_indices))])

        def partitioning_in_place(x, pivot_index):
            partitioning_index = []
            newx = x.copy()
            newx.append(math.inf)
            newx_index = [i for i in range(len(x))]
            # swap pivot index to 0
            tmp_data = newx[pivot_index]
            newx[pivot_index] = newx[0]
            newx[0] = tmp_data
            tmp_index = newx_index[pivot_index]
            newx_index[pivot_index] = 0
            newx_index[0] = tmp_index
            low = 0
            high = len(newx) - 1
            while high > low:
                
                while newx[low] <= x[pivot_index]:
                    low += 1 
                
                while newx[high] > x[pivot_index] and high > 0:
                    high -= 1
                if high > low:
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
            return (new_pivot, newx_index)
            

        n = 16
        max = 100
        seed = 6
        data = data_generation.generate_linear(n,max, seed)
        array_y_location = [0,2,0]
        side_length = 0.75
        buffer = side_length
        text_scale = 0.75
        title = Tex("Quicksort: the god of all sorting methods")
        title.scale(1.25)
        
        title.to_edge(UP)
        title.shift(DOWN*0.25)
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
        text1 = Tex("High level process")
        text2 = Tex("1. Choose an element often called the pivot")
        text3 = Tex("2. Reorder the array such that all elements less than the pivot\n are on the left and all elements that are greater than the pivot are on the right")
        text4 = Tex("This is known as \"partitioning\" the array.")
        text45 = Tex("Note that the pivot is now in its final sorted position. \n All elements to the left are less and all elements to the right are greater.") 
        text5 = Tex("3. Recursively repeat 1-2 on the subarrays to the left and right\n of the pivot until the subarrays are length 1")
        text_group = VGroup(text1, text2, text3, text4, text45, text5).arrange(DOWN, buff=0.2)
        text_group.scale(0.7)
        text_group.shift(DOWN*1.5)
        #self.play(Create(text1), run_time=2)
        self.play(create_text(text1))
        self.wait(1)
        #self.play(Create(text2), run_time=3)
        self.play(create_text(text2))
        self.wait(0.25)
        rand = random.Random()
        rand.seed(seed)
        pivot = rand.randint(0,n-1)
        newsquare = Square(side_length = side_length)
        newsquare.move_to(array_y_location)
        newsquare.shift(get_x_shift(pivot,n,side_length))
        self.add(newsquare)
        self.play(FadeToColor(number_objects[pivot], "#FF0000"), FadeToColor(newsquare, "#FF0000"))
        self.play(create_text(text3))
        (new_pivot, new_indices) = partitioning_in_place(data, pivot)
        animations1 = []
        new_data = []
        new_number_objects = []
        #new_square_objects = []
        
        for (index, new_index) in enumerate(new_indices):
            line = Line(number_objects[new_index].get_center(), number_objects[index].get_center())
            animations1.append(MoveAlongPath(number_objects[new_index], line))
            new_data.append(data[new_index])
            new_number_objects.append(number_objects[new_index])
        line = Line(new_number_objects[new_pivot].get_center(), number_objects[new_pivot].get_center())
        animations1.append(MoveAlongPath(newsquare, line))
        textmagic = Text("Magic we will explain later")
        textmagic.scale(0.35)
        textmagic.move_to(array_y_location+DOWN*0.75)
        self.play(FadeIn(textmagic))
        self.play(animations1,run_time = 4)
        self.play(FadeOut(textmagic))
        self.play(Create(text4, run_time=4))
        self.wait(1)
        text45.align_to(text4, direction=UP) 
        text5.align_to(text4, direction=UP)
        self.play(FadeOut(text4))
        self.wait()
        #self.play(Create(text45), run_time=8)
        self.play(create_text(text45))
        self.wait(2)
        self.play(FadeOut(text45))
        self.wait()
        #self.play(Create(text5), run_time=8)
        self.play(create_text(text5))
        self.wait(1)
        faded_grey = "#484848"
        self.play(FadeToColor(new_number_objects[new_pivot], get_blue(new_data[new_pivot]/max)), FadeToColor(newsquare, faded_grey))
        brace_shift = 0.3
        brace1 = BraceBetweenPoints(new_number_objects[0].get_center()+LEFT*side_length*1, new_number_objects[new_pivot-1].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        brace2 = BraceBetweenPoints(new_number_objects[new_pivot+1].get_center()+LEFT*side_length*1, new_number_objects[n-1].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        self.play(FadeIn(brace1), FadeIn(brace2), run_time=3)
        self.wait(2)

        pivot2 = 2#rand.randint(0, new_pivot-1)
        pivot3 = new_pivot+3#rand.randint(new_pivot+1,n-1)
        animations = []
        animations.append(FadeToColor(new_number_objects[pivot2], "#FF0000"))
        animations.append(FadeToColor(new_number_objects[pivot3], "#FF0000"))
        newsquare2 = Square(side_length = side_length)
        newsquare2.move_to(array_y_location)
        newsquare2.shift(get_x_shift(pivot2,n,side_length))
        self.add(newsquare2)
        animations.append(FadeToColor(newsquare2, "#FF0000"))
        newsquare3 = Square(side_length = side_length)
        newsquare3.move_to(array_y_location)
        newsquare3.shift(get_x_shift(pivot3,n,side_length))
        self.add(newsquare3)
        animations.append(FadeToColor(newsquare3, "#FF0000"))
        animations.append(Indicate(text2))
        self.play(animations,run_time=3)
        self.wait()
        
            
        (new_pivot2, new_indices2) = partitioning_in_place(new_data[0:new_pivot], pivot2)
        (new_pivot3, new_indices3) = partitioning_in_place(new_data[new_pivot+1:n], pivot3-new_pivot-1)
        (new_pivot3, new_indices3) = partitioning_subarray_helper(new_pivot+1, new_pivot3, new_indices3)
        
        new_indices = new_indices2 + [new_pivot] + new_indices3
        animations = []
        data = new_data.copy()
        number_objects = new_number_objects.copy()
        #square_objects = new_square_objects.copy()
        new_data = []
        new_number_objects = []
        #new_square_objects = []
        for (index, new_index) in enumerate(new_indices):
            line = Line(number_objects[new_index].get_center(), number_objects[index].get_center())
            animations.append(MoveAlongPath(number_objects[new_index], line))
            new_data.append(data[new_index])
            new_number_objects.append(number_objects[new_index])
            #new_square_objects.append(square_objects[new_index])
        #        line = Line(new_number_objects[new_pivot].get_center(), number_objects[new_pivot].get_center())
        line = Line(number_objects[pivot2].get_center(), number_objects[new_pivot2].get_center())
        animations.append(MoveAlongPath(newsquare2, line))
        line = Line(number_objects[pivot3].get_center(), number_objects[new_pivot3].get_center())
        animations.append(MoveAlongPath(newsquare3, line))
        animations.append(Indicate(text3))
        self.play(animations, run_time=3)
        self.wait(2)
        self.play(FadeOut(brace1), FadeOut(brace2), FadeToColor(new_number_objects[new_pivot2],get_blue(new_data[new_pivot2]/max)), 
            FadeToColor(new_number_objects[new_pivot3], get_blue(new_data[new_pivot3]/max)), FadeToColor(newsquare3, faded_grey), 
            FadeToColor(newsquare2, faded_grey))
        brace1 = BraceBetweenPoints(new_number_objects[0].get_center()+LEFT*side_length*1, new_number_objects[new_pivot2-1].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        brace2 = BraceBetweenPoints(new_number_objects[new_pivot2+1].get_center()+LEFT*side_length*1, new_number_objects[new_pivot-1].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        brace3 = BraceBetweenPoints(new_number_objects[new_pivot+1].get_center()+LEFT*side_length*1, new_number_objects[new_pivot3-1].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        brace4 = BraceBetweenPoints(new_number_objects[new_pivot3+1].get_center()+LEFT*side_length*1, new_number_objects[n-1].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        self.play(FadeIn(brace1), FadeIn(brace2), FadeIn(brace3), FadeIn(brace4), run_time=3)
       
        pivot4 = 0
        pivot5 = 4
        pivot6 = 8
        pivot7 = 14

        animations = []
        animations.append(FadeToColor(new_number_objects[pivot4], "#FF0000"))
        animations.append(FadeToColor(new_number_objects[pivot5], "#FF0000"))
        newsquare4 = Square(side_length = side_length)
        newsquare4.move_to(array_y_location)
        newsquare4.shift(get_x_shift(pivot4,n,side_length))
        self.add(newsquare4)
        animations.append(FadeToColor(newsquare4, "#FF0000"))
        newsquare5 = Square(side_length = side_length)
        newsquare5.move_to(array_y_location)
        newsquare5.shift(get_x_shift(pivot5,n,side_length))
        self.add(newsquare5)
        animations.append(FadeToColor(newsquare5, "#FF0000"))
        newsquare6 = Square(side_length=side_length)
        newsquare6.move_to(array_y_location)
        newsquare6.shift(get_x_shift(pivot6,n,side_length))
        animations.append(FadeToColor(new_number_objects[pivot6], "#FF0000"))
        animations.append(FadeToColor(new_number_objects[pivot7], "#FF0000"))
        self.add(newsquare6)
        animations.append(FadeToColor(newsquare6, "#FF0000"))
        newsquare7 = Square(side_length=side_length)
        newsquare7.move_to(array_y_location)
        newsquare7.shift(get_x_shift(pivot7,n,side_length))
        self.add(newsquare7)
        animations.append(FadeToColor(newsquare7, "#FF0000"))
        animations.append(Indicate(text2))
        self.play(animations,run_time=3)
        self.wait()

        (new_pivot4, new_indices4) = partitioning_in_place(new_data[0:new_pivot2], pivot4)
        (new_pivot5, new_indices5) = partitioning_in_place(new_data[new_pivot2+1:new_pivot], pivot5-new_pivot2-1)
        (new_pivot5, new_indices5) = partitioning_subarray_helper(new_pivot2+1, new_pivot5, new_indices5)
        (new_pivot6, new_indices6) = partitioning_in_place(new_data[new_pivot+1:new_pivot3], pivot6-new_pivot-1)
        (new_pivot6, new_indices6) = partitioning_subarray_helper(new_pivot+1, new_pivot6, new_indices6)
        (new_pivot7, new_indices7) = partitioning_in_place(new_data[new_pivot3+1:n], pivot7-new_pivot3-1)
        (new_pivot7, new_indices7) = partitioning_subarray_helper(new_pivot3+1, new_pivot7, new_indices7)
    
        new_indices = new_indices4 + [new_pivot2] + new_indices5 + [new_pivot] + new_indices6 + [new_pivot3] + new_indices7
        # yes this makes no sense. oh wait, it makes perfect sense. you are the dumb one!!!!
        
        data = new_data.copy()
        number_objects = new_number_objects.copy()
        print(len(number_objects))
        new_data = []
        new_number_objects = []
        animations = []
        animations.append(Indicate(text3))
        for (index, new_index) in enumerate(new_indices):
            print(new_index, index)
            line = Line(number_objects[new_index].get_center(), number_objects[index].get_center())
            animations.append(MoveAlongPath(number_objects[new_index], line))
            new_data.append(data[new_index])
            new_number_objects.append(number_objects[new_index])
            #new_square_objects.append(square_objects[new_index])
        line = Line(number_objects[pivot4].get_center(), number_objects[new_pivot4].get_center())
        animations.append(MoveAlongPath(newsquare4, line))
        self.play(animations, run_time=3)
        self.wait(1)
        
        #brace1 = BraceBetweenPoints(new_number_objects[0].get_center()+LEFT*side_length*1, new_number_objects[new_pivot2-1].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        self.play(FadeOut(brace1), FadeOut(brace2), FadeOut(brace3), FadeOut(brace4))
        
        brace1 = BraceBetweenPoints(new_number_objects[0].get_center()+LEFT*side_length*1, new_number_objects[new_pivot4-1].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        done1 = Tex("Done!").move_to(brace1.get_center()).shift(DOWN*0.3).scale(0.5)
        brace2 = BraceBetweenPoints(new_number_objects[3].get_center()+LEFT*side_length*1, new_number_objects[3].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        done2 = Tex("Done!").move_to(brace2.get_center()).shift(DOWN*0.3).scale(0.5)
        brace3 = BraceBetweenPoints(new_number_objects[5].get_center()+LEFT*side_length*1, new_number_objects[5].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        done3 = Tex("Done!").move_to(brace3.get_center()).shift(DOWN*0.3).scale(0.5)

        brace4 = BraceBetweenPoints(new_number_objects[7].get_center()+LEFT*side_length*1, new_number_objects[7].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        done4 = Tex("Done!").move_to(brace4, DOWN).shift(DOWN*0.3).scale(0.5)
        brace5 = BraceBetweenPoints(new_number_objects[9].get_center()+LEFT*side_length*1, new_number_objects[11].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        brace6 = BraceBetweenPoints(new_number_objects[13].get_center()+LEFT*side_length*1, new_number_objects[13].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        
        done6 = Tex("Done!").move_to(brace6.get_center()).shift(DOWN*0.3).scale(0.5)
        brace7 = BraceBetweenPoints(new_number_objects[15].get_center()+LEFT*side_length*1, new_number_objects[15].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        
        done7 = Tex("Done!").move_to(brace7.get_center()).shift(DOWN*0.3).scale(0.5)
        self.play(FadeIn(brace1), FadeIn(brace2), FadeIn(brace3), FadeIn(brace4), FadeIn(brace5), FadeIn(brace6), FadeIn(brace7))
        self.play(FadeIn(done1), FadeIn(done2), FadeIn(done3), FadeIn(done4), FadeIn(done6), FadeIn(done7))
        self.wait()
        animations = [FadeToColor(x, faded_grey) for x in [newsquare4, newsquare5, newsquare6, newsquare7]]
        animations.extend([FadeToColor(new_number_objects[x], get_blue(new_data[x]/max)) for x in [new_pivot4, new_pivot5, new_pivot5, new_pivot6, new_pivot7]])
        self.play(animations)
        self.wait()
        animations = []
        animations.extend([FadeOut(brace1), FadeOut(brace2), FadeOut(brace3), FadeOut(brace4), FadeOut(brace5), FadeOut(brace6), FadeOut(brace7)])
        animations.extend([FadeOut(x) for x in [done1,done2,done3,done4, done6,done7]])
        animations.extend([FadeToColor(square_objects[x], faded_grey) for x in [0,3,5, 7, 13,15]])
        self.play(animations)
        self.wait()
        brace1 = BraceBetweenPoints(new_number_objects[9].get_center()+LEFT*side_length*1, new_number_objects[11].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        self.play(FadeIn(brace1))
        self.wait()

        pivotlast = 11
        
        animations = []
        newsquarelast = Square(side_length=side_length)
        newsquarelast.move_to(array_y_location)
        newsquarelast.shift(get_x_shift(pivotlast,n,side_length))
        self.add(newsquarelast)
        animations.append(FadeToColor(newsquarelast, "#FF0000"))
        animations.append(Indicate(text2))
        self.play(animations,run_time=3)
        self.wait()


        self.wait()
        (new_pivotlast, new_indiceslast) = partitioning_in_place(new_data[9:12], 2)
        (new_pivotlast, new_indiceslast) = partitioning_subarray_helper(9, new_pivotlast, new_indiceslast)
        
        
        data = new_data.copy()
        number_objects = new_number_objects.copy()
        new_data = []
        new_number_objects = []
        animations = []
        animations.append(Indicate(text3))
        for (index, new_index) in enumerate(new_indiceslast):
            index = index + 9
            line = Line(number_objects[new_index].get_center(), number_objects[index].get_center())
            animations.append(MoveAlongPath(number_objects[new_index], line))
            new_data.append(data[new_index])
            new_number_objects.append(number_objects[new_index])
        line = Line(square_objects[11].get_center(), square_objects[10].get_center())
        animations.append(MoveAlongPath(newsquarelast, line))
        self.play(animations, run_time=3)
        self.wait()
        animations = []
        animations.append(FadeOut(brace1))
        animations.append(FadeToColor(newsquarelast,faded_grey))
        self.play(animations)
        self.wait()
        brace1 = BraceBetweenPoints(new_number_objects[0].get_center()+LEFT*side_length*1, new_number_objects[0].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        done1 = Tex("Done!").move_to(brace1, DOWN).shift(DOWN*0.3).scale(0.5)
        brace2 = BraceBetweenPoints(new_number_objects[2].get_center()+LEFT*side_length*1, new_number_objects[2].get_center()).shift(DOWN*brace_shift+side_length*RIGHT*0.5)
        done2 = Tex("Done!").move_to(brace2, DOWN).shift(DOWN*0.3).scale(0.5)
        self.play(FadeIn(brace1), FadeIn(brace2), FadeIn(done1), FadeIn(done2))
        self.wait(2)
        self.play(FadeOut(brace1), FadeOut(brace2), FadeOut(done1), FadeOut(done2))
        self.wait()
        animations = [FadeToColor(square_objects[x], faded_grey) for x in [9,10,11]]
        animations.append(FadeToColor(newsquarelast, faded_grey))
        self.play(animations)
        self.wait()
        self.play(FadeOut(text1), FadeOut(text2), FadeOut(text3), FadeOut(text4), FadeOut(text5))
        self.wait()
        text = Tex("Array Sorted!\nBut now for the details about accomplishing\nthe partitioning process efficiently")
        text.move_to(text2.get_center())
        text.scale(0.65)
        self.play(create_text(text))
        text55 = Tex("So let's go back to the beginning")
        text55.move_to(text3.get_center())
        self.play(create_text(text55))
        animations = [FadeOut(x) for x in number_objects]
        self.play(animations)
        print(data)
        self.wait(3)

