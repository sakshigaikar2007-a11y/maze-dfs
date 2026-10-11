import tkinter as tk
import random
import time

ROWS = 12
COLS = 12
CELL_SIZE = 30
START = (0, 0)
FINISH = (ROWS - 1, COLS - 1)

window = tk.Tk()
window.title("Interactive Maze Generator Using DFS")
window.resizable(True, True)

tk.Label(window, text="MAZE GENERATOR USING DFS",
         font=("Arial", 20, "bold")).pack(pady=10)

tk.Label(window, text="Generate and solve a maze using Depth First Search",
         font=("Arial", 11)).pack()

canvas = tk.Canvas(window, width=COLS * CELL_SIZE,
                   height=ROWS * CELL_SIZE, bg="white")
canvas.pack(padx=15, pady=15)

status = tk.Label(window, text="Click Generate Maze to start.",
                  font=("Arial", 11, "bold"))
status.pack(pady=5)

stats = tk.Label(window, text="Moves: 0    Time: 0.00 seconds",
                 font=("Arial", 10))
stats.pack()

walls = {}
maze_generated = False
solving = False
moves = 0
start_time = 0


def reset_walls():
    global walls
    walls = {}
    for r in range(ROWS):
        for c in range(COLS):
            walls[(r, c)] = {
                "top": True, "right": True,
                "bottom": True, "left": True
            }


def draw_maze():
    canvas.delete("all")
    for r in range(ROWS):
        for c in range(COLS):
            x1, y1 = c * CELL_SIZE, r * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            w = walls[(r, c)]

            if w["top"]:
                canvas.create_line(x1, y1, x2, y1, width=2)
            if w["right"]:
                canvas.create_line(x2, y1, x2, y2, width=2)
            if w["bottom"]:
                canvas.create_line(x1, y2, x2, y2, width=2)
            if w["left"]:
                canvas.create_line(x1, y1, x1, y2, width=2)

    sr, sc = START
    canvas.create_rectangle(sc*CELL_SIZE+4, sr*CELL_SIZE+4,
                            (sc+1)*CELL_SIZE-4, (sr+1)*CELL_SIZE-4,
                            fill="green", outline="")
    canvas.create_text(sc*CELL_SIZE+CELL_SIZE//2,
                       sr*CELL_SIZE+CELL_SIZE//2,
                       text="S", fill="white",
                       font=("Arial", 14, "bold"))

    fr, fc = FINISH
    canvas.create_rectangle(fc*CELL_SIZE+4, fr*CELL_SIZE+4,
                            (fc+1)*CELL_SIZE-4, (fr+1)*CELL_SIZE-4,
                            fill="red", outline="")
    canvas.create_text(fc*CELL_SIZE+CELL_SIZE//2,
                       fr*CELL_SIZE+CELL_SIZE//2,
                       text="F", fill="white",
                       font=("Arial", 14, "bold"))


def neighbours(cell):
    r, c = cell
    result = []
    if r > 0:
        result.append((r-1, c))
    if r < ROWS-1:
        result.append((r+1, c))
    if c > 0:
        result.append((r, c-1))
    if c < COLS-1:
        result.append((r, c+1))
    random.shuffle(result)
    return result


def remove_wall(a, b):
    r1, c1 = a
    r2, c2 = b

    if r2 == r1-1:
        walls[a]["top"] = False
        walls[b]["bottom"] = False
    elif r2 == r1+1:
        walls[a]["bottom"] = False
        walls[b]["top"] = False
    elif c2 == c1-1:
        walls[a]["left"] = False
        walls[b]["right"] = False
    elif c2 == c1+1:
        walls[a]["right"] = False
        walls[b]["left"] = False


def generate_maze():
    global maze_generated, moves

    if solving:
        return

    reset_walls()
    visited = {START}
    stack = [START]

    # DFS using a stack
    while stack:
        current = stack[-1]
        choices = [n for n in neighbours(current) if n not in visited]

        if choices:
            nxt = choices[0]
            remove_wall(current, nxt)
            visited.add(nxt)
            stack.append(nxt)
        else:
            stack.pop()

    maze_generated = True
    moves = 0
    draw_maze()
    stats.config(text="Moves: 0    Time: 0.00 seconds")
    status.config(text="Maze generated! Click Solve Maze.")


def accessible(cell):
    r, c = cell
    result = []
    w = walls[cell]

    if r > 0 and not w["top"]:
        result.append((r-1, c))
    if r < ROWS-1 and not w["bottom"]:
        result.append((r+1, c))
    if c > 0 and not w["left"]:
        result.append((r, c-1))
    if c < COLS-1 and not w["right"]:
        result.append((r, c+1))

    return result


def solve_maze():
    global solving, moves, start_time

    if not maze_generated:
        status.config(text="Generate a maze first.")
        return
    if solving:
        return

    solving = True
    moves = 0
    start_time = time.time()

    visited = {START}
    stack = [(START, [START])]
    path = []

    # DFS to find a path
    while stack:
        current, current_path = stack.pop()

        if current == FINISH:
            path = current_path
            break

        choices = accessible(current)
        random.shuffle(choices)

        for nxt in choices:
            if nxt not in visited:
                visited.add(nxt)
                stack.append((nxt, current_path + [nxt]))

    if path:
        animate_solution(path, 0)
    else:
        solving = False
        status.config(text="No path found.")


def animate_solution(path, index):
    global moves, solving

    if index >= len(path):
        elapsed = time.time() - start_time
        stats.config(text=f"Moves: {moves}    Time: {elapsed:.2f} seconds")
        status.config(text="Maze solved! DFS reached the finish.")
        solving = False
        return

    r, c = path[index]

    if (r, c) != START and (r, c) != FINISH:
        canvas.create_rectangle(
            c*CELL_SIZE+8, r*CELL_SIZE+8,
            (c+1)*CELL_SIZE-8, (r+1)*CELL_SIZE-8,
            fill="blue", outline="")
    moves += 1
    elapsed = time.time() - start_time
    stats.config(text=f"Moves: {moves}    Time: {elapsed:.2f} seconds")

    window.after(60, lambda: animate_solution(path, index+1))


def reset_maze():
    global maze_generated, solving, moves

    if solving:
        return

    maze_generated = False
    moves = 0
    reset_walls()

    canvas.delete("all")

    for r in range(ROWS):
        for c in range(COLS):
            canvas.create_rectangle(
                c*CELL_SIZE, r*CELL_SIZE,
                (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
                outline="lightgray"
            )

    sr, sc = START
    canvas.create_rectangle(sc*CELL_SIZE+4, sr*CELL_SIZE+4,
                            (sc+1)*CELL_SIZE-4, (sr+1)*CELL_SIZE-4,
                            fill="green", outline="")
    canvas.create_text(sc*CELL_SIZE+CELL_SIZE//2,
                       sr*CELL_SIZE+CELL_SIZE//2,
                       text="S", fill="white",
                       font=("Arial", 14, "bold"))

    fr, fc = FINISH
    canvas.create_rectangle(fc*CELL_SIZE+4, fr*CELL_SIZE+4,
                            (fc+1)*CELL_SIZE-4, (fr+1)*CELL_SIZE-4,
                            fill="red", outline="")
    canvas.create_text(fc*CELL_SIZE+CELL_SIZE//2,
                       fr*CELL_SIZE+CELL_SIZE//2,
                       text="F", fill="white",
                       font=("Arial", 14, "bold"))

    stats.config(text="Moves: 0    Time: 0.00 seconds")
    status.config(text="Board reset. Click Generate Maze.")


buttons = tk.Frame(window)
buttons.pack(pady=10)

tk.Button(buttons, text="Generate Maze", width=15,
          font=("Arial", 11, "bold"),
          command=generate_maze).grid(row=0, column=0, padx=5)

tk.Button(buttons, text="Solve Maze", width=15,
          font=("Arial", 11, "bold"),
          command=solve_maze).grid(row=0, column=1, padx=5)

tk.Button(buttons, text="Reset", width=15,
          font=("Arial", 11, "bold"),
          command=reset_maze).grid(row=0, column=2, padx=5)

reset_maze()
window.mainloop()