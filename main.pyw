import heapq
from collections import defaultdict
import turtle
from tkinter import *
import os
from scipy.stats import entropy


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
        global ent
        global av_len
        global tab

        frequency, huff = self.extract_info()
        prob_table = []

        av_len = 0
        tab = [("Symbol".ljust(10) + "Waga".ljust(10) + "Prawdopodobieństwo [%]".ljust(25) + "Kod Huffmana")]
        for p in huff:
            prob = frequency[p[0]] / sum(frequency.values()) * 100
            av_len = av_len + (prob / 100 * len(p[1]))
            prob_table.append(prob)

            if p[0] == ' ':
                tab.append(("spacja".ljust(10) + str(frequency[p[0]]).ljust(10) + '{0:.2f}'.format(prob).ljust(25) +
                            str(p[1])).ljust(10))
                continue
            tab.append((str(p[0]).ljust(10) + str(frequency[p[0]]).ljust(10) + '{0:.2f}'.format(prob).ljust(25) +
                        str(p[1])).ljust(10))

        ent = entropy(prob_table, base=2)

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
        turtle.title('Drzewo Huffmana')
        turtle.speed(0)
        turtle.color("#ccffcc")
        turtle.bgcolor("#006600")
        turtle.setup(width=1.0, height=1.0)

    def tp(self):
        turtle.penup()
        turtle.goto(self.origin)
        turtle.pendown()

    def huffman_tree_info(self):
        frequency, huff = self.extract_info()

        huff_frequency = [[frequency[symbol], binary] for symbol, binary in huff]
        parent_nodes = []

        huff_frequency.sort(key=lambda x: len(x[1]), reverse=True)

        current_binary_value = huff_frequency[0]

        while len(huff_frequency) > 2:
            for freq, binary in huff_frequency:
                if binary[:-1] == current_binary_value[1][:-1] and binary != current_binary_value[1]:
                    parent_value = freq + current_binary_value[0]
                    huff_frequency.append([parent_value, binary[:-1]])

                    parent_nodes.append([parent_value, binary[:-1]])

                    huff_frequency.remove(current_binary_value)
                    huff_frequency.remove([freq, binary])
            current_binary_value = huff_frequency[0]
            huff_frequency.sort(key=lambda x: len(x[1]), reverse=True)

        huffman_tree_data = huff + parent_nodes

        return huffman_tree_data

    def draw_tree(self):
        self.init_turtle_screen()

        _, huff = self.extract_info()

        length = len(huff[len(huff) - 1][1])

        huffman_tree_data = self.huffman_tree_info()

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


def restart(root):
    root.destroy()
    os.startfile("main.pyw")


def algorithm(text):
    encode_button.config(bg="#ffcccc", state=DISABLED, text="Zakodowano.")
    reset_button.config(bg="#ccffcc")
    draw_tree_button.config(state=NORMAL)
    huffman = Huffman(text)
    huffman.print_info()

    label3.config(text='Entropia:  ' + '{0:.2f}'.format(ent))
    label4.config(text=' Średnia długość słowa kodowego:  ' + '{0:.2f}'.format(av_len))
    text_field.config(text=entry_field.get())

    scroll_bar = Scrollbar(root)
    scroll_bar.pack(side=RIGHT, fill=Y)

    t = Text(root, padx=10, width=55, height=25, wrap=NONE, yscrollcommand=scroll_bar.set)

    for i in tab:
        t.insert(END, i + "\n")

    t.configure(state=DISABLED)
    t.pack(side=TOP, fill=X)
    scroll_bar.config(command=t.yview)

    label3.pack()
    label4.pack()
    text_field.pack()


def drawTree(text):
    draw_tree_button.config(state=DISABLED, text="Drzewo narysowane.")
    huffman = Huffman(text)
    huffman.print_info()
    huffman.draw_tree()


root = Tk()
root.geometry('500x500')
#root.resizable(True, False)
root.title("Kodowanie Huffmana")

frm = Frame(root, width=450, height=45)

label = Label(root, text="Wprowadź tekst do zakodowania: ")
entry_field = Entry(root, width=30)
label2 = Label(root, text="Tekst do zakodowania:")
text_field = Label(root, fg="blue", height=1, padx=5)
label3 = Label(root)
label4 = Label(root)

encode_button = Button(root, bg="#ccffcc", text="Zakoduj!", width=50, command=lambda: algorithm(entry_field.get()))
reset_button = Button(root, text="Reset", width=50, command=lambda: restart(root))
draw_tree_button = Button(root, state=DISABLED, text="Rysuj drzewo", width=50,
                          command=lambda: drawTree(entry_field.get()))
quit_button = Button(root, text="Wyjście", width=50, command=root.destroy)

label.pack()
entry_field.pack()
label2.pack()
text_field.pack()

label3.pack()
label4.pack()
encode_button.pack()
draw_tree_button.pack()
reset_button.pack()
quit_button.pack()

root.mainloop()
