import tkinter as tk
import random
import numpy as np
from perlin_noise import PerlinNoise


noise = PerlinNoise(octaves=6, seed=random.randint(0, 100000))
size = 20
player_x, player_y = size // 2, size // 2
world_x, world_y = 0, 0


terrain_colors = {0: "black", 1: "white"}

def generate_map(offset_x, offset_y):
    terrain_map = [[noise([(i + offset_x) / size, (j + offset_y) / size]) for j in range(size)] for i in range(size)]
    terrain_array = np.array(terrain_map)

    new_map = np.ones((size, size), dtype=int)

    new_map[0, :] = 0
    new_map[-1, :] = 0
    new_map[:, 0] = 0
    new_map[:, -1] = 0

    return new_map

def draw_map(canvas, terrain_colors, world_x, world_y):
    canvas.delete("all")
    terrain_map = generate_map(world_x, world_y)

    for i in range(size):
        for j in range(size):
            color = terrain_colors[terrain_map[i][j]]
            canvas.create_rectangle(j * 20, i * 20, (j + 1) * 20, (i + 1) * 20, fill=color)

    player_screen_x, player_screen_y = player_x * 20, player_y * 20
    canvas.create_oval(player_screen_x, player_screen_y, player_screen_x + 20, player_screen_y + 20, fill="red")


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

    terrain_map = generate_map(new_x, new_y)
    if terrain_map[new_x][new_y] == 1:
        player_x, player_y = new_x, new_y

    draw_map(canvas, terrain_colors, player_x, player_y)


root = tk.Tk()
root.title("Wumpus World")
canvas = tk.Canvas(root, width=size * 20, height=size * 20)
canvas.pack()


draw_map(canvas, terrain_colors, world_x, world_y)

root.bind("<KeyPress>", move_player)

root.mainloop()