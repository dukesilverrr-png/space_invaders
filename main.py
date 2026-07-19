from graphics import Canvas
import time

DELAY = 0.02

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

SHIP_SPEED = 10
SHIP_MOVE_LEFT = -SHIP_SPEED
SHIP_MOVE_RIGHT = SHIP_SPEED

LASER_WIDTH = 4
LASER_HEIGHT = 12


ENEMY_WIDTH = 60
ENEMY_HEIGHT = 34
ENEMY_COUNT = 5
ENEMY_SPACING = 12
ENEMY_START_Y = 70
ENEMY_SPEED =3
ENEMY_DROP_DISTANCE = 15

def main():

    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    keys_held = set()
    canvas.bind(
        "<KeyRelease>",
        lambda event: keys_held.discard(event.keysym)
    )

    draw_background(canvas)

    player_ship = draw_player_ship(canvas)
    
    enemies = draw_enemy_fleet(canvas)

    enemy_dx = ENEMY_SPEED

    lasers = []
    
    game_over = False
    game_over_title = None
    game_over_frames = 0

    while True:
        if game_over:
            game_over_frames += 1

            if game_over_frames % 15 == 0:
                if (game_over_frames // 15) % 2 == 0:
                    canvas.set_fill_color(game_over_title, "dark red")
                else:
                    canvas.set_fill_color(game_over_title, "red")
         
            canvas.update()
            time.sleep(DELAY)
            continue

        keys_pressed = canvas.get_new_key_presses()

        for key in keys_pressed:
            if key.keysym == "a":
                keys_held.add("a")

            elif key.keysym == "d":
                keys_held.add("d")

            elif key.keysym == "space" and "space" not in keys_held:
                keys_held.add("space")

                if len(lasers) < 3:
                    lasers.append(fire_laser(canvas, player_ship))

        if "a" in keys_held:
            move_player_ship(
                canvas,
                player_ship,
                SHIP_MOVE_LEFT
            )

        if "d" in keys_held:
            move_player_ship(
                canvas,
                player_ship,
                SHIP_MOVE_RIGHT
            )

        for laser in lasers[:]:
            canvas.move(laser, 0, -10)

            laser_left_x = canvas.get_left_x(laser)
            laser_right_x = laser_left_x + LASER_WIDTH
            laser_top_y = canvas.get_top_y(laser)
            laser_bottom_y = laser_top_y + LASER_HEIGHT

            collisions = canvas.find_overlapping(
                laser_left_x,
                laser_top_y,
                laser_right_x,
                laser_bottom_y
            )

            collided_enemy = None

            for enemy in enemies:
                if any(part in collisions for part in enemy):
                    collided_enemy = enemy
                    break

            if collided_enemy is not None:
                canvas.delete(laser)
                lasers.remove(laser)

                for part in collided_enemy:
                    canvas.delete(part)

                enemies.remove(collided_enemy)
                continue

            if laser_top_y < 0:
                canvas.delete(laser)
                lasers.remove(laser)

        move_enemy_row(canvas, enemies, enemy_dx)

        if enemy_row_hit_edge(canvas, enemies):
            enemy_dx = -enemy_dx
            move_enemy_row_down(canvas, enemies)

        if enemies_reached_player(canvas, enemies, player_ship):
            game_over = True
            game_over_title = draw_game_over(canvas)

        canvas.update()
        time.sleep(DELAY)


def draw_game_over(canvas):
    canvas.create_text(
        CANVAS_WIDTH / 2 + 3,
        CANVAS_HEIGHT / 2 + 3,
        "GAME OVER",
        "center",
        ("Arial", 36, "bold"),
        "dark red"
    )

    game_over_title = canvas.create_text(
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2,
        "GAME OVER",
        "center",
        ("Arial", 36, "bold"),
        "red"
    )

    canvas.create_text(
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2 + 45,
        "THE INVASION WAS SUCCESSFUL",
        "center",
        ("Arial", 12, "bold"),
        "white"
    )

    return game_over_title

def fire_laser(canvas, player_ship):
    laser_left_x = canvas.get_left_x(player_ship[6])  # Get the left x-coordinate of the nose cannon tip
    laser_top_y = canvas.get_top_y(player_ship[6]) 
    laser_right_x = laser_left_x + LASER_WIDTH 
    laser_bottom_y = laser_top_y + LASER_HEIGHT
    laser = canvas.create_rectangle(laser_left_x, laser_top_y, laser_right_x, laser_bottom_y, "red")# Spawn the laser at the nose cannon tip

    return laser

def move_player_ship(canvas,player_ship,dx):

    for ship_part in player_ship:
        canvas.move(ship_part, dx, 0)

    player_ship_left_x = canvas.get_left_x(player_ship[11])
    player_ship_right_x = canvas.get_left_x(player_ship[13]) + 30

    if player_ship_left_x < 0:
        correction = -player_ship_left_x

        for ship_part in player_ship:
            canvas.move(ship_part, correction,0)
    
    if player_ship_right_x > CANVAS_WIDTH:
        correction = CANVAS_WIDTH - player_ship_right_x

        for ship_part in player_ship:
            canvas.move(ship_part, correction,0)    

def draw_background(canvas):
    # Black space
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, "black")

    # Stars
    canvas.create_oval(50, 40, 54, 44, "white")
    canvas.create_oval(120, 90, 124, 94, "white")
    canvas.create_oval(200, 55, 204, 59, "white")
    canvas.create_oval(310, 130, 314, 134, "white")
    canvas.create_oval(420, 70, 424, 74, "white")
    canvas.create_oval(80, 180, 84, 184, "white")
    canvas.create_oval(260, 210, 264, 214, "white")
    canvas.create_oval(460, 190, 464, 194, "white")

def enemies_reached_player(canvas, enemies, player_ship):
    player_top_y = canvas.get_top_y(player_ship[6])

    for enemy in enemies:
        enemy_bottom_y = (
            canvas.get_top_y(enemy[-1]) + 7
        )

        if enemy_bottom_y >= player_top_y:
            return True

    return False

def draw_player_ship(canvas):
    player_ship = []

    # Ship body
    outer_body = canvas.create_oval(227, 449, 273, 486, "dark gray")
    middle_body = canvas.create_oval(233, 453, 267, 481, "gray")
    inner_body = canvas.create_oval(241, 459, 259, 475, "light gray")
    player_ship.append(outer_body)
    player_ship.append(middle_body)
    player_ship.append(inner_body)

    # Cockpit glass
    cockpit_glass = canvas.create_oval(241, 451, 259, 467, "cyan")
    cockpit_highlight = canvas.create_oval(245, 454, 255, 462, "light blue")
    player_ship.append(cockpit_glass)
    player_ship.append(cockpit_highlight)

    # Nose cannon
    nose_cannon_base = canvas.create_rectangle(247, 430, 253, 454, "light gray")
    nose_cannon_tip = canvas.create_rectangle(248, 420, 252, 432, "white")
    player_ship.append(nose_cannon_base)
    player_ship.append(nose_cannon_tip)

    # Side cannons
    left_cannon_base = canvas.create_rectangle(222, 460, 230, 476, "gray")
    right_cannon_base = canvas.create_rectangle(270, 460, 278, 476, "gray")
    left_cannon_tip = canvas.create_rectangle(224, 451, 229, 462, "light gray")
    right_cannon_tip = canvas.create_rectangle(271, 451, 276, 462, "light gray")
    player_ship.append(left_cannon_base)
    player_ship.append(right_cannon_base)
    player_ship.append(left_cannon_tip)
    player_ship.append(right_cannon_tip)

    # Left wing
    left_wing_base = canvas.create_rectangle(207, 466, 230, 477, "dark gray")
    left_wing_highlight = canvas.create_rectangle(211, 469, 225, 474, "light gray")
    player_ship.append(left_wing_base)
    player_ship.append(left_wing_highlight)

    # Right wing
    right_wing_base = canvas.create_rectangle(270, 466, 293, 477, "dark gray")
    right_wing_highlight = canvas.create_rectangle(275, 469, 289, 474, "light gray")
    player_ship.append(right_wing_base)
    player_ship.append(right_wing_highlight)

    # Engine bases
    left_engine_base = canvas.create_rectangle(235, 479, 247, 490, "gray")
    right_engine_base = canvas.create_rectangle(253, 479, 265, 490, "gray")
    left_engine_nozzle = canvas.create_rectangle(239, 486, 243, 494, "light gray")
    right_engine_nozzle = canvas.create_rectangle(257, 486, 261, 494, "light gray")
    player_ship.append(left_engine_base)
    player_ship.append(right_engine_base)
    player_ship.append(left_engine_nozzle)
    player_ship.append(right_engine_nozzle)

    # Engine flames
    left_outer_flame = canvas.create_oval(235, 489, 247, 500, "orange")
    right_outer_flame = canvas.create_oval(253, 489, 265, 500, "orange")
    left_inner_flame = canvas.create_oval(238, 493, 244, 500, "yellow")
    right_inner_flame = canvas.create_oval(256, 493, 262, 500, "yellow")
    player_ship.append(left_outer_flame)
    player_ship.append(right_outer_flame)
    player_ship.append(left_inner_flame)
    player_ship.append(right_inner_flame)

    # Small armor panels
    left_upper_armor_panel = canvas.create_rectangle(
        234, 467, 240, 472, "dark gray"
    )
    right_upper_armor_panel = canvas.create_rectangle(
        260, 467, 266, 472, "dark gray"
    )
    left_lower_armor_panel = canvas.create_rectangle(
        238, 475, 244, 479, "black"
    )
    right_lower_armor_panel = canvas.create_rectangle(
        256, 475, 262, 479, "black"
    )
    player_ship.append(left_upper_armor_panel)
    player_ship.append(right_upper_armor_panel)
    player_ship.append(left_lower_armor_panel)
    player_ship.append(right_lower_armor_panel)

    return player_ship

def enemy_row_hit_edge(canvas, enemies):
    if len(enemies) == 0:
        return False

    left_edge = canvas.get_left_x(enemies[0][1])
    right_edge = (canvas.get_left_x(enemies[-1][1]) + ENEMY_WIDTH)

    return left_edge <= 0 or right_edge >= CANVAS_WIDTH

def move_enemy_row(canvas, enemies, dx):
    for enemy in enemies:
        for enemy_part in enemy:
            canvas.move(enemy_part, dx, 0)

def move_enemy_row_down(canvas, enemies):
    for enemy in enemies:
        for enemy_part in enemy:
            canvas.move(enemy_part,0,ENEMY_DROP_DISTANCE)

def draw_enemy_fleet(canvas):
    enemies = []

    fleet_width = (ENEMY_COUNT * ENEMY_WIDTH + (ENEMY_COUNT - 1) * ENEMY_SPACING)
    
    enemy_start_x = (CANVAS_WIDTH - fleet_width) / 2

    for i in range(ENEMY_COUNT):
        enemy_x = enemy_start_x + i * (ENEMY_WIDTH + ENEMY_SPACING)
        enemy = draw_enemy(canvas, enemy_x, ENEMY_START_Y)
        enemies.append(enemy)

    return enemies

def draw_enemy(canvas, enemy_x, enemy_y):
    enemy_ship = []

    # Dark underside
    underside = canvas.create_oval(
        enemy_x + 6,
        enemy_y + 16,
        enemy_x + 54,
        enemy_y + 32,
        "dark gray"
    )
    enemy_ship.append(underside)

    # Main silver disc
    main_disc = canvas.create_oval(
        enemy_x,
        enemy_y + 10,
        enemy_x + 60,
        enemy_y + 27,
        "light gray"
    )
    enemy_ship.append(main_disc)

    # Metallic rim
    outer_rim = canvas.create_rectangle(
        enemy_x + 3,
        enemy_y + 16,
        enemy_x + 57,
        enemy_y + 22,
        "gray"
    )
    inner_rim = canvas.create_rectangle(
        enemy_x + 7,
        enemy_y + 17,
        enemy_x + 53,
        enemy_y + 20,
        "white"
    )
    enemy_ship.append(outer_rim)
    enemy_ship.append(inner_rim)

    # Glass cockpit dome
    dome = canvas.create_oval(
        enemy_x + 16,
        enemy_y + 1,
        enemy_x + 44,
        enemy_y + 20,
        "dark turquoise"
    )
    dome_glass = canvas.create_oval(
        enemy_x + 20,
        enemy_y + 4,
        enemy_x + 40,
        enemy_y + 17,
        "cyan"
    )
    dome_highlight = canvas.create_oval(
        enemy_x + 23,
        enemy_y + 5,
        enemy_x + 29,
        enemy_y + 9,
        "white"
    )
    enemy_ship.append(dome)
    enemy_ship.append(dome_glass)
    enemy_ship.append(dome_highlight)

    # Running lights
    left_light = canvas.create_oval(
        enemy_x + 8,
        enemy_y + 19,
        enemy_x + 13,
        enemy_y + 24,
        "red"
    )
    left_middle_light = canvas.create_oval(
        enemy_x + 20,
        enemy_y + 21,
        enemy_x + 25,
        enemy_y + 26,
        "yellow"
    )
    right_middle_light = canvas.create_oval(
        enemy_x + 35,
        enemy_y + 21,
        enemy_x + 40,
        enemy_y + 26,
        "yellow"
    )
    right_light = canvas.create_oval(
        enemy_x + 47,
        enemy_y + 19,
        enemy_x + 52,
        enemy_y + 24,
        "red"
    )
    enemy_ship.append(left_light)
    enemy_ship.append(left_middle_light)
    enemy_ship.append(right_middle_light)
    enemy_ship.append(right_light)

    # Glowing propulsion reactor
    reactor = canvas.create_oval(
        enemy_x + 23,
        enemy_y + 25,
        enemy_x + 37,
        enemy_y + 32,
        "purple"
    )
    reactor_glow = canvas.create_oval(
        enemy_x + 27,
        enemy_y + 27,
        enemy_x + 33,
        enemy_y + 34,
        "magenta"
    )
    enemy_ship.append(reactor)
    enemy_ship.append(reactor_glow)

    return enemy_ship


if __name__ == "__main__":
    main()