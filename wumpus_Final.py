import tkinter as tk
import random
import numpy as np
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=6, seed=random.randint(0, 100000))
size = 20
player_x, player_y = size // 2, size // 2
wumpus_x, wumpus_y = None, None
projectiles = []

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

    pits = []
    num_pits = 5
    possible_positions = [(i, j) for i in range(size) for j in range(size)
                          if base_map[i][j] == 1 and (j != player_x or i != player_y)]
    for _ in range(num_pits):
        y, x = random.choice(possible_positions)
        pits.append((x, y))

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

    for px, py in projectiles:
        canvas.create_oval(px * 20 + 5, py * 20 + 5, px * 20 + 15, py * 20 + 15, fill="yellow")

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

    if 0 <= new_x < size and 0 <= new_y < size and base_map[new_y][new_x] == 1:
        player_x, player_y = new_x, new_y

    draw_map(canvas, terrain_colors, player_x, player_y)
    root.update()

    if player_x == wumpus_x and player_y == wumpus_y:
        canvas.create_text(size * 10, size * 10, text="You were eaten by the Wumpus!", fill="red", font=("Arial", 16))
        root.unbind("<KeyPress>")

def shoot(event):
    if event.keysym == "Up":
        projectiles.append((player_x, player_y - 1))
    elif event.keysym == "Down":
        projectiles.append((player_x, player_y + 1))
    elif event.keysym == "Left":
        projectiles.append((player_x - 1, player_y))
    elif event.keysym == "Right":
        projectiles.append((player_x + 1, player_y))

    update_projectiles()

def update_projectiles():
    global projectiles, wumpus_x, wumpus_y
    new_projectiles = []

    for px, py in projectiles:
        if 0 <= px < size and 0 <= py < size and base_map[py][px] == 1:
            if px == wumpus_x and py == wumpus_y:
                canvas.create_text(size * 10, size * 10, text="You killed the Wumpus!", fill="green", font=("Arial", 16))
                root.unbind("<KeyPress>")
                return
            new_projectiles.append((px, py))

    projectiles = new_projectiles
    draw_map(canvas, terrain_colors, player_x, player_y)
    root.after(100, update_projectiles)

root = tk.Tk()
root.title("Wumpus World")
canvas = tk.Canvas(root, width=size * 20, height=size * 20)
canvas.pack()

generate_base_map()
place_wumpus()
draw_map(canvas, terrain_colors, player_x, player_y)

root.bind("<KeyPress>", move_player)
root.bind("<KeyPress-Up>", shoot)
root.bind("<KeyPress-Down>", shoot)
root.bind("<KeyPress-Left>", shoot)
root.bind("<KeyPress-Right>", shoot)

root.mainloop()