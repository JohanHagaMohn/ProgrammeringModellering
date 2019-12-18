from tkinter import *
from tkinter.font import Font
import math
from decimal import Decimal

root = Tk()
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
frame = Frame(root)
frame.grid(row=0, column=0, sticky=N+S+E+W)

for row_index in range(7):
    Grid.rowconfigure(frame, row_index, weight=1)
for col_index in range(5):
    Grid.columnconfigure(frame, col_index, weight=1)

helv36 = Font(family="Times", size=36)
title = Button(frame, text="Calculator", highlightcolor="black", highlightbackground="black", fg="gray23", font=("Times", 52, "bold"),
               command=root.quit, bd="0", highlightthickness=30)
v = StringVar()
entry = Entry(frame, font=helv36, textvariable=v, justify="right", highlightcolor="gray80", fg="gray23",
              bd="0", highlightthickness=0)
title.grid(row=0, column=0, sticky=N+S+E+W, columnspan=5)
entry.grid(row=1, column=0, sticky=N+S+E+W, columnspan=5)
v.set(0)


def colours(colour):
    if colour < 4 or colour % 5 == 0:
        return "gray20"
    elif colour % 5 == 4 or colour == 23:
        return "darkorange"
    else:
        return "gray40"


def colors(color):
    if color % 5 == 4 or color == 23:
        return "gray95"
    else:
        return "gray23"


number1 = "0"
operator = ""
number2 = ""
display_number = "0"
numbers_received = 0
decimal_counter = 0
boolean_value = False
is_pi = False
equal = False


def normalizing(d):
    normalized = d.normalize()
    sign, digit, exponent = normalized.as_tuple()
    return normalized if exponent <= 0 else normalized.quantize(1)


def length(variable):
    if len(str(variable)) > len(str(normalizing(Decimal(variable)))):
        return str(normalizing(Decimal(variable)))
    else:
        return str(variable)


def factorial(num):
    if num == 1:
        return num
    else:
        return num * factorial(num - 1)


def button_maker(text, y):
    def operation():
        global v
        global equal
        global is_pi
        global number1
        global operator
        global number2
        global display_number
        global numbers_received
        global decimal_counter
        global boolean_value
        if boolean_value is False:
            if isinstance(text, int) or text == "π" or text == ",":
                if text == "π" and display_number != "0":
                    display_number = length(float(display_number) * float(math.pi))
                    is_pi = True
                elif text == "π":
                    display_number = length(float(math.pi))
                    is_pi = True
                elif is_pi is True:
                    if text == ",":
                        pass
                    else:
                        display_number = length(float(display_number) * float(text))
                elif text == "," and decimal_counter == 0:
                    if numbers_received == 2:
                        display_number = "0."
                        decimal_counter += 1
                    else:
                        display_number += "."
                        decimal_counter += 1
                elif text == ",":
                    pass
                elif display_number.startswith("0") and "0." not in display_number:
                    display_number = length(text)
                else:
                    if numbers_received == 2 and "." not in display_number:
                        display_number = length(text)
                        numbers_received += 1
                    elif equal is True:
                        display_number = length(text)
                        number1 = length(text)
                        equal = False
                    else:
                        display_number += length(text)
            elif text == "±":
                display_number = length(float(display_number) * float(-1))
                v.set(display_number)
                number1 = display_number
                numbers_received = 1
            elif text == "!":
                if int(display_number) < 27:
                    display_number = length(factorial(int(display_number)))
                else:
                    display_number = "Error"
                    boolean_value = True
                number1 = display_number
                numbers_received = 1
            elif text == "%":
                display_number = length(float(display_number) / float(100))
                number1 = display_number
                numbers_received = 1
            elif text == "AC":
                number1 = ""
                operator = ""
                number2 = ""
                display_number = "0"
                numbers_received = 0
                decimal_counter = 0
                boolean_value = False
                is_pi = False
            else:
                is_pi = False
                equal = False
                if numbers_received == 0:
                    number1 = display_number
                    numbers_received += 1
                if numbers_received == 3:
                    number2 = display_number
                    print(str(number1) + str(operator) + str(number2))
                    if operator == "+":
                        display_number = length(float(number1) + float(number2))
                    elif operator == "-":
                        display_number = length(float(number1) - float(number2))
                    elif operator == "x":
                        display_number = length(float(number1) * float(number2))
                    elif operator == "÷":
                        try:
                            display_number = length(float(number1) / float(number2))
                        except ZeroDivisionError:
                            display_number = "Error"
                            boolean_value = True
                    elif operator == "^":
                        display_number = length(float(number1) ** float(number2))
                    elif operator == "√":
                        display_number = length(float(number1) ** (float(1)/float(number2)))
                    elif operator == ">":
                        display_number = str((float(number1) > float(number2)))
                    numbers_received = 1
                    number1 = display_number
                    number2 = ""
                    operator = ""
                    if text != "=" and operator != "<" and operator != ">":
                        display_number = text
                        operator = display_number
                        numbers_received = 2
                    else:
                        equal = True
                else:
                    display_number = text
                    if numbers_received == 1:
                        operator = display_number
                        numbers_received += 1
            if "." not in display_number:
                decimal_counter = 0
            v.set(display_number)
            print(numbers_received)
        elif text == "AC":
            number1 = ""
            operator = ""
            number2 = ""
            display_number = "0"
            numbers_received = 0
            decimal_counter = 0
            boolean_value = False
            is_pi = False

    num = Button(frame, text=text, highlightcolor=colours(x), highlightbackground=colours(x),
                 fg=colors(x), font=helv36, command=operation, highlightthickness=0, borderwidth=0)
    if y < 21:
        num.grid(row=math.floor(y / 5) + 2, column=y % 5, sticky=N+S+E+W)
    elif y == 21:
        num.grid(row=math.floor(y / 5) + 2, column=y % 5, sticky=N+S+E+W, columnspan=2)
    else:
        num.grid(row=math.floor((y + 1) / 5) + 2, column=(y + 1) % 5, sticky=N+S+E+W)


symbols = ["AC", "√", "^", "%", "÷", "π", 7, 8, 9, "x", "!", 4, 5, 6, "-", "±", 1, 2, 3, "+", ">", 0, ",", "="]
for x in range(0, 24):
    button_maker(symbols[x], x)

root.mainloop()
