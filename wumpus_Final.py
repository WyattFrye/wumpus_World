import tkinter as tk
import random
import numpy as np
from perlin_noise import PerlinNoise


noise = PerlinNoise(octaves=6, seed=random.randint(0, 100000))
size = 20
player_x, player_y = size // 2, size // 2
world_x, world_y = 0, 0


terrain_colors = {0: "blue", 1: "green", 2: "brown"}

def generate_map(offset_x, offset_y):
    terrain_map = [[noise([(i + offset_x) / size, (j + offset_y) / size]) for j in range(size)] for i in range(size)]
    terrain_array = np.array(terrain_map)
    return np.where(terrain_array > 0.3, 2, np.where(terrain_array > 0.1, 1, 0))  # Mountain, Grass, Water

def draw_map(canvas, terrain_colors, world_x, world_y):
    canvas.delete("all")
    terrain_map = generate_map(world_x, world_y)

    for i in range(size):
        for j in range(size):
            color = terrain_colors[terrain_map[i][j]]
            canvas.create_rectangle(j * 20, i * 20, (j + 1) * 20, (i + 1) * 20, fill=color)

    center_x, center_y = (size // 2) * 20, (size // 2) * 20
    canvas.create_oval(center_x, center_y, center_x + 20, center_y + 20, fill="red")

def move_player(event):
    global world_x, world_y

    if event.keysym == "a":
        world_y -= 1
    elif event.keysym == "d":
        world_y += 1
    elif event.keysym == "w":
        world_x -= 1
    elif event.keysym == "s":
        world_x += 1

    draw_map(canvas, terrain_colors, world_x, world_y)


root = tk.Tk()
root.title("Wumpus World")
canvas = tk.Canvas(root, width=size * 20, height=size * 20)
canvas.pack()


draw_map(canvas, terrain_colors, world_x, world_y)

root.bind("<KeyPress>", move_player)

root.mainloop()