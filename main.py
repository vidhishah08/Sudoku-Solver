from tkinter import *
import tkinter as tk



def ValidateNumber(P):
    out = (P.isdigit() or P == "") and len(P) < 2
    return out

root = tk.Tk()
root.title("Sudoku Solver")
root.configure(bg="#194972")
root.geometry("650x320")

font_ = ("Bookman Old Style", 9)
font01 = ("Comic Sans MS", 10)
font02 = ("Cambria", 9)
font03 = ("Comic Sans MS", 12, "bold")

frame01 = tk.Frame(root, padx=10, pady=10)
frame01.configure(bg="#194972")
cells = {}
stack = []


reg = root.register(ValidateNumber)

def draw3x3Grid(row, coloum, bgcolour):
    for i in range(3):
        for j in range(3):
            e = Entry(frame01, width=5, bg=bgcolour, justify="center", validate="key", validatecommand=(reg, "%P"))
            e.grid(row=row+i+1, column=coloum+j+1, sticky="nsew", padx=1, pady=1, ipady=5)
            cells[(row+i+1, coloum+j+1)] = e

def draw9x9Grid():
    color = "#F0FFFF"
    for rowNo in range(1, 10, 3):
        for colNo in range(0, 9, 3):
            draw3x3Grid(rowNo, colNo, color)
            if color == "#F0FFFF":
                color = "#4194FF"
            else:
                color = "#F0FFFF"

draw9x9Grid()

frame = tk.Frame(root, padx=10, pady=10)
frame.configure(bg="#194972")
cells02 = {}

def draw3x3Grid01(row, column, bgcolor):
    for i in range(3):
        if i == 0:
            y = i+1
        elif i == 1:
            y = i+3
        else:
            y = i+5
        for j in range(3):
            x = y+j
            b = Button(frame, text=x, width=4, bg=bgcolor, relief="groove", activebackground="#dce3ed", justify="center", font=font_, fg="black", command=lambda x=x: button_click(x))
            b.grid(row=row+i+1, column=column+j+1, sticky="nsew", padx=1, pady=1, ipady=5)
            cells02[(row+i+1, column+j+1)] = b

draw3x3Grid01(0, 0, "#eaeef4")

def button_click(button_text):
    a = root.focus_get()
    if isinstance(a, tk.Entry):
        b = a.get()
        stack.append((a,b))
        a.delete(0, tk.END)
        a.insert(tk.END, b + str(button_text))

def button_click01(button_text):
    a = root.focus_get()
    if isinstance(a, tk.Entry):
        b = a.get()
        stack.append((a,b))
        a.delete(0, tk.END)

def clear_entry():
    for b, a in cells.items():
        a.delete(0, tk.END)

def undo():
    if stack:
        entry, text = stack.pop()
        entry.delete(0, tk.END)
        entry.insert(tk.END, text)

def solve_cell():
    a = root.focus_get()
    if isinstance(a, tk.Entry):
        b = a.get()
        board = []
        for row in range(2, 11):
            rows = []
            for col in range(1, 10):
                val = cells[(row, col)].get()
                if val == "":
                    rows.append(0)
                else:
                    rows.append(int(val))
            board.append(rows)

        i, j = int(a.grid_info()["row"]), int(a.grid_info()["column"])

        if solve_sudoku(board):
            a.delete(0, tk.END)
            a.insert(tk.END, str(board[i - 2][j - 1]))
        else:
            print("Cannot solve cell. Check your input.")

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def solve_sudoku(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num

                        if solve_sudoku(board):
                            return True

                        board[i][j] = 0

                return False

    return True
def solve_sudoku_ui():
    board = []
    for row in range(2, 11):
        rows = []
        for col in range(1, 10):
            val = cells[(row, col)].get()
            if val == "":
                rows.append(0)
            else:
                rows.append(int(val))
        board.append(rows)

    if solve_sudoku(board):
        for row in range(2, 11):
            for col in range(1, 10):
                cells[(row, col)].delete(0, END)
                cells[(row, col)].insert(0, str(board[row - 2][col - 1]))
    else:
        print("Cannot solve Sudoku. Check your input.")

b1 = Button(root, text="Solve Cell", width=10, bg="#a8a8aa", justify=CENTER, relief="groove", activebackground="#dce3ed", font=font01, fg="black",command=solve_cell)
b2 = Button(root, text="Clear", width=10, bg="#a8a8aa", justify=CENTER, relief="groove", activebackground="#dce3ed", font=font01, fg="black", command=clear_entry)
b3 = Button(root, text="Undo", width=10, bg="#a8a8aa", justify=CENTER, relief="groove", activebackground="#dce3ed", font=font01, fg="black",command=undo)
b4 = Button(root, text="Remove", width=10, bg="#a8a8aa", justify=CENTER, relief="groove", activebackground="#dce3ed", font=font01, fg="black", command=lambda X=X: button_click01(X))
b5 = Button(root, text="Solve", width=22, height=1, bg="#5a7bc0", justify=CENTER, relief="groove", activebackground="#dce3ed", font=font03, fg="White", command=solve_sudoku_ui)

L1 = Label(root, text="Functions:", justify=LEFT, font=font02, fg="White", bg="#194972")

frame01.place(x=20, y=10)
L1.place(x=400, y=10)
b1.place(x=400, y=30)
b2.place(x=500, y=30)
b3.place(x=400, y=70)
b4.place(x=500, y=70)
frame.place(x=420, y=110)
b5.place(x=380, y=270)

root.mainloop()