import heapq
import sys
from collections import defaultdict
import turtle
from tkinter import *
from tkinter import ttk
import os

'''
Huffman('String with more than 2 unique characters')

Huffman.print_info() -> print info 
Huffman.draw_tree() -> draws huffman tree (using turtle)
'''


class Huffman:
    def __init__(self, data) -> None:
        self.data = data
        self.origin = 0, 250

        if len(set(data)) <= 2:
            raise ValueError('not enough unique characters')

    def encode(self, frequency):
        heap = [[weight, [symbol, '']] for symbol, weight in frequency.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

    def extract_info(self):
        frequency = defaultdict(int)
        for symbol in self.data:
            frequency[symbol] += 1

        huff = self.encode(frequency)
        return frequency, huff

    def print_info(self):
        frequency, huff = self.extract_info()
        print("Symbol".ljust(10) + "Weight".ljust(10) + "Huffman Code")
        label_symbol = Label()
        for p in huff:
            if p[0] == ' ':
                print("space".ljust(10) + str(frequency[p[0]]).ljust(10) + p[1])
                continue
            print(p[0].ljust(10) + str(frequency[p[0]]).ljust(10) + p[1])

    ###drawing stuff###
    def turtle_space(self):
        turtle.penup()
        turtle.forward(20)
        turtle.pendown()

    def down_lt_branch(self, a, length):
        branch_length = length * (length * 6 / 2 ** a)
        turtle.forward(10)
        turtle.right(90)
        turtle.forward(branch_length)
        turtle.left(90)
        turtle.forward(10)
        self.turtle_space()

    def down_rt_branch(self, a, length):
        branch_length = length * (length * 6 / 2 ** a)
        turtle.forward(10)
        turtle.left(90)
        turtle.forward(branch_length)
        turtle.right(90)
        turtle.forward(10)
        self.turtle_space()

    def write_uncircled(self, character, size):
        turtle.penup()
        turtle.left(90)
        turtle.backward(size * 2)
        turtle.pendown()
        turtle.write(character, font=("Helvetica", 10, "normal"))
        turtle.penup()
        turtle.forward(size * 2)
        turtle.right(90)
        turtle.pendown()

    def write_circled(self, character, size):
        turtle.penup()
        turtle.left(90)
        turtle.backward(size * 3)
        turtle.pendown()
        turtle.write(character, font=("Helvetica", 10, "normal"))
        turtle.penup()
        turtle.forward(size * 3)
        turtle.pendown()
        turtle.circle(10)
        turtle.right(90)

    def init_turtle_screen(self):
        turtle.title('huffman tree')
        # turtle.tracer(0) #to make it instantaneous
        turtle.speed(0)
        turtle.color("white")
        turtle.bgcolor("black")
        turtle.setup(width=1.0, height=1.0)

    def tp(self):
        turtle.penup()
        turtle.goto(self.origin)
        turtle.pendown()

    ###end of drawing stuff###

    # data processing
    def huffman_tree_info(self):
        frequency, huff = self.extract_info()

        huff_frequency = [[frequency[symbol], binary] for symbol, binary in huff]  # making addition simpler
        parent_nodes = []  # for drawing the parent nodes

        huff_frequency.sort(key=lambda x: len(x[1]), reverse=True)

        current_binary_value = huff_frequency[0]

        while len(huff_frequency) > 2:
            for freq, binary in huff_frequency:
                if binary[:-1] == current_binary_value[1][:-1] and binary != current_binary_value[1]:
                    parent_value = freq + current_binary_value[0]
                    huff_frequency.append([parent_value, binary[:-1]])

                    parent_nodes.append([parent_value, binary[:-1]])  # objective

                    huff_frequency.remove(current_binary_value)
                    huff_frequency.remove([freq, binary])
            current_binary_value = huff_frequency[0]
            huff_frequency.sort(key=lambda x: len(x[1]), reverse=True)

        huffman_tree_data = huff + parent_nodes
        '''
        if first element of list is str: it's a character
        if first element of list is int: it's a parent node
        '''
        return huffman_tree_data

    def draw_tree(self):
        self.init_turtle_screen()

        _, huff = self.extract_info()

        length = len(huff[len(huff) - 1][1])

        huffman_tree_data = self.huffman_tree_info()

        # starting off with main branch
        self.tp()
        turtle.right(90)
        self.write_circled(len(self.data), 2)

        for char, binary_code in huffman_tree_data:
            for index, bit in enumerate(binary_code):
                if bit == '0':
                    self.down_lt_branch(index, length)
                else:
                    self.down_rt_branch(index, length)

            if type(char) is str:
                if char == ' ':
                    self.write_uncircled("space", 5)
                self.write_uncircled(char, len(char))
            else:
                self.write_circled(char, len(str(char)))
            self.tp()

        turtle.penup()
        turtle.goto(0, 300)
        turtle.pendown()
        turtle.write(self.data, font=("Helvetica", 15, "normal"), align='center')

        turtle.hideturtle()
        turtle.mainloop()


def restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def gui():
    root = Tk()
    root.title("Huffman coding")
    frm = ttk.Frame(root, padding=30)

    frm.grid()

    label = Label(frm, text="Insert text to encode: ")
    entry_field = Entry(frm, width=30)
    encode_button = Button(frm, text="Encode!", command=lambda: algorithm(entry_field.get()))
    label2 = Label(frm, text="Text to encode:")
    text_field = Label(frm, width=25, height=1)
    reset_button = Button(frm, text="Reset", command=restart)
    quit_button = Button(frm, text="Quit", command=root.destroy)
    # row 0
    label.grid(column=0, row=0)
    entry_field.grid(column=1, row=0)
    encode_button.grid(column=3, row=0)
    quit_button.grid(column=5, row=0)
    reset_button.grid(column=4, row=0)
    # row 1
    label2.grid(column=0, row=1)
    text_field.grid(column=1, row=1)
    # row 2
    root.mainloop()


def algorithm(text):
    huffman = Huffman(text)
    huffman.print_info()
    huffman.draw_tree()


if __name__ == '__main__':
    gui()
