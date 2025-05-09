import tkinter as tk
import random
import numpy as np
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=6, seed=random.randint(0, 100000))
size = 20
player_x, player_y = size // 2, size // 2
wumpus_x, wumpus_y = None, None
arrows = []
arrow_count = 6

terrain_colors = {0: "black", 1: "white"}
base_map = None
pits = []
bats = []
revealed_pits = set()
game_over = False
wumpus_revealed = False
key_sequence = ""
REVEAL_CODE = "qwerty"


def generate_base_map():
    global base_map, pits, bats

    terrain_map = [
        [noise([i / size, j / size]) for j in range(size)] for i in range(size)
    ]
    terrain_array = np.array(terrain_map)
    base_map = np.where(terrain_array > 0.2, 0, np.ones((size, size), dtype=int))

    base_map[0, :] = 0
    base_map[-1, :] = 0
    base_map[:, 0] = 0
    base_map[:, -1] = 0

    pits = []
    num_pits = 20
    possible_positions = [
        (i, j)
        for i in range(size)
        for j in range(size)
        if base_map[i][j] == 1 and (j != player_x or i != player_y)
    ]
    for _ in range(num_pits):
        y, x = random.choice(possible_positions)
        pits.append((x, y))

    bats = []
    num_bats = 5
    possible_positions = [
        (i, j)
        for i in range(size)
        for j in range(size)
        if base_map[i][j] == 1 and (j, i) != (player_x, player_y) and (j, i) not in pits
    ]
    for _ in range(num_bats):
        y, x = random.choice(possible_positions)
        bats.append((x, y))


def place_wumpus():
    global wumpus_x, wumpus_y
    walkable_positions = [
        (i, j)
        for i in range(size)
        for j in range(size)
        if base_map[i][j] == 1 and (j != player_x or i != player_y)
    ]
    wumpus_y, wumpus_x = random.choice(walkable_positions)


def draw_map(canvas, terrain_colors, player_x, player_y):
    canvas.delete("all")

    for i in range(size):
        for j in range(size):
            color = terrain_colors[base_map[i][j]]
            canvas.create_rectangle(
                j * 20, i * 20, (j + 1) * 20, (i + 1) * 20, fill=color
            )

    canvas.create_oval(
        player_x * 20, player_y * 20, player_x * 20 + 20, player_y * 20 + 20, fill="red"
    )

    for px, py in arrows:
        canvas.create_oval(
            px * 20 + 5, py * 20 + 5, px * 20 + 15, py * 20 + 15, fill="yellow"
        )

    if wumpus_revealed:
        canvas.create_oval(
            wumpus_x * 20 + 5,
            wumpus_y * 20 + 5,
            wumpus_x * 20 + 15,
            wumpus_y * 20 + 15,
            fill="green",
        )

    for pit_x, pit_y in revealed_pits:
        canvas.create_oval(
            pit_x * 20 + 2,
            pit_y * 20 + 2,
            pit_x * 20 + 18,
            pit_y * 20 + 18,
            fill="gray",
            outline="black",
            width=1,
        )

    if wumpus_revealed:
        for bat_x, bat_y in bats:
            canvas.create_oval(
                bat_x * 20 + 6,
                bat_y * 20 + 6,
                bat_x * 20 + 14,
                bat_y * 20 + 14,
                fill="purple",
                outline="black",
                width=1,
            )


def is_near_pit(x, y):
    return any(
        (x + dx, y + dy) in pits
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1]
        if (dx, dy) != (0, 0)
    )


def is_near_wumpus(x, y):
    return any(
        (x + dx, y + dy) == (wumpus_x, wumpus_y)
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1]
        if (dx, dy) != (0, 0)
    )


def is_near_bats(x, y):
    return any(
        (x + dx, y + dy) in bats
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1]
        if (dx, dy) != (0, 0)
    )


def teleport_player():
    global player_x, player_y

    safe_positions = [
        (j, i)
        for i in range(size)
        for j in range(size)
        if base_map[i][j] == 1 and (j, i) != (player_x, player_y)
    ]
    player_x, player_y = random.choice(safe_positions)
    draw_map(canvas, terrain_colors, player_x, player_y)


def move_player(event):
    global player_x, player_y, game_over, key_sequence, wumpus_revealed

    if game_over:
        return

    if event.char.isalpha():
        key_sequence += event.char.lower()
        if len(key_sequence) > len(REVEAL_CODE):
            key_sequence = key_sequence[-len(REVEAL_CODE) :]

        if key_sequence == REVEAL_CODE:
            wumpus_revealed = True
            revealed_pits.update(pits)
            message_label.config(text="Everything has been revealed!")
            draw_map(canvas, terrain_colors, player_x, player_y)
            return

    dx = {"w": 0, "s": 0, "a": -1, "d": 1}.get(event.keysym, 0)
    dy = {"w": -1, "s": 1, "a": 0, "d": 0}.get(event.keysym, 0)
    new_x, new_y = player_x + dx, player_y + dy

    if 0 <= new_x < size and 0 <= new_y < size and base_map[new_y][new_x] == 1:
        player_x, player_y = new_x, new_y

    if (player_x, player_y) in pits:
        revealed_pits.add((player_x, player_y))
        message_label.config(text="You fell into a pit!")
        player_x, player_y = size // 2, size // 2
    elif (player_x, player_y) == (wumpus_x, wumpus_y):
        wumpus_revealed = True
        message_label.config(
            text="You were eaten by the Wumpus!\nPress SPACE to tray again."
        )
        game_over = True
    elif (player_x, player_y) in bats:
        message_label.config(
            text="A giant bat grabs you!\nIt drops you in a random location."
        )
        teleport_player()
    elif is_near_pit(player_x, player_y) and is_near_wumpus(player_x, player_y):
        message_label.config(
            text="You feel a cool breeze... and smell something awful."
        )
    elif is_near_pit(player_x, player_y):
        message_label.config(text="You feel a cool breeze...")
    elif is_near_wumpus(player_x, player_y):
        message_label.config(text="You smell something awful.")
    elif is_near_bats(player_x, player_y):
        message_label.config(text="You hear a flapping in the distance.")
    else:
        message_label.config(text="")

    draw_map(canvas, terrain_colors, player_x, player_y)


def shoot(event):
    global arrow_count

    if arrow_count <= 0:
        return

    direction = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}.get(
        event.keysym
    )
    if direction:
        dx, dy = direction
        arrows.append((player_x + dx, player_y + dy))
        arrow_count -= 1
        update_arrow_count()
        update_arrows()


def update_arrow_count():
    arrow_label.config(text=f"Arrows: {arrow_count}")


def update_arrows():
    global arrows, wumpus_x, wumpus_y, game_over, wumpus_revealed

    new_arrows = []
    for px, py in arrows:
        if 0 <= px < size and 0 <= py < size and base_map[py][px] == 1:
            if (px, py) == (wumpus_x, wumpus_y):
                wumpus_revealed = True
                message_label.config(
                    text="You killed the Wumpus!\nPress SPACE to play again."
                )
                game_over = True
                draw_map(canvas, terrain_colors, player_x, player_y)
                return
            new_arrows.append((px, py))

    arrows = new_arrows
    draw_map(canvas, terrain_colors, player_x, player_y)
    root.after(100, update_arrows)


def restart_game(event):
    global player_x, player_y, wumpus_x, wumpus_y, arrows
    global game_over, revealed_pits, wumpus_revealed, key_sequence, arrow_count

    if not game_over:
        return

    wumpus_revealed = False
    revealed_pits.clear()
    key_sequence = ""
    arrows = []
    arrow_count = 6
    player_x, player_y = size // 2, size // 2

    generate_base_map()
    place_wumpus()

    game_over = False
    message_label.config(text="")
    update_arrow_count()
    draw_map(canvas, terrain_colors, player_x, player_y)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wumpus World")
    root.geometry("800x600")

    frame = tk.Frame(root)
    frame.pack()

    canvas = tk.Canvas(frame, width=size * 20, height=size * 20)
    canvas.grid(row=0, column=0)

    info_frame = tk.Frame(root)
    info_frame.pack()

    arrow_label = tk.Label(
        info_frame, text=f"Arrows: {arrow_count}", font=("Arial", 12), fg="blue"
    )
    arrow_label.pack()

    message_label = tk.Label(
        frame, text="", font=("Arial", 12), fg="blue", width=50, anchor="w"
    )
    message_label.grid(row=1, column=0, padx=10)

    generate_base_map()
    place_wumpus()
    draw_map(canvas, terrain_colors, player_x, player_y)

    root.bind("<KeyPress>", move_player)
    root.bind("<KeyPress-Up>", shoot)
    root.bind("<KeyPress-Down>", shoot)
    root.bind("<KeyPress-Left>", shoot)
    root.bind("<KeyPress-Right>", shoot)
    root.bind("<KeyPress-space>", restart_game)

    root.mainloop()
