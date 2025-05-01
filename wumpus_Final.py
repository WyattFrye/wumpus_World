import tkinter as tk
import random
import numpy as np
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=6, seed=random.randint(0, 100000))
size = 20
player_x, player_y = size // 2, size // 2
wumpus_x, wumpus_y = None, None

terrain_colors = {0: "black", 1: "white"}
base_map = None

def generate_base_map():
    global base_map

    terrain_map = [[noise([i / size, j / size]) for j in range(size)] for i in range(size)]
    terrain_array = np.array(terrain_map)
    base_map = np.where(terrain_array > 0.2, 0, np.ones((size, size), dtype=int))

    base_map[0, :] = 0
    base_map[-1, :] = 0
    base_map[:, 0] = 0
    base_map[:, -1] = 0

def place_wumpus():
    global wumpus_x, wumpus_y
    walkable_positions = [(i, j) for i in range(size) for j in range(size)
                          if base_map[i][j] == 1 and (j != player_x or i != player_y)]
    wumpus_y, wumpus_x = random.choice(walkable_positions)

def draw_map(canvas, terrain_colors, player_x, player_y):
    canvas.delete("all")

    for i in range(size):
        for j in range(size):
            color = terrain_colors[base_map[i][j]]
            canvas.create_rectangle(j * 20, i * 20, (j + 1) * 20, (i + 1) * 20, fill=color)

    canvas.create_oval(wumpus_x * 20 + 5, wumpus_y * 20 + 5,
                       wumpus_x * 20 + 15, wumpus_y * 20 + 15, fill="green")

    player_screen_x, player_screen_y = player_x * 20, player_y * 20
    canvas.create_oval(player_screen_x, player_screen_y,
                       player_screen_x + 20, player_screen_y + 20, fill="red")

def move_player(event):
    global player_x, player_y

    new_x, new_y = player_x, player_y

    if event.keysym == "w":
        new_y -= 1
    elif event.keysym == "s":
        new_y += 1
    elif event.keysym == "a":
        new_x -= 1
    elif event.keysym == "d":
        new_x += 1

    # Check walkability
    if 0 <= new_x < size and 0 <= new_y < size and base_map[new_y][new_x] == 1:
        player_x, player_y = new_x, new_y

    draw_map(canvas, terrain_colors, player_x, player_y)
    root.update()

    # Wumpus encounter check
    if player_x == wumpus_x and player_y == wumpus_y:
        canvas.create_text(size * 10, size * 10, text="You were eaten by the Wumpus!", fill="red", font=("Arial", 16))
        root.unbind("<KeyPress>")

root = tk.Tk()
root.title("Wumpus World")
canvas = tk.Canvas(root, width=size * 20, height=size * 20)
canvas.pack()

generate_base_map()
place_wumpus()
draw_map(canvas, terrain_colors, player_x, player_y)

root.bind("<KeyPress>", move_player)
root.mainloop()
