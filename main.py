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

def main():

    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    keys_held = set()
    canvas.bind(
        "<KeyRelease>",
        lambda event: keys_held.discard(event.keysym)
    )

    draw_background(canvas)

    player_ship = draw_player_ship(canvas)
    
    enemy = draw_enemy(canvas, 215, 70)

    lasers = []
    
    while True:
        keys_pressed = canvas.get_new_key_presses()#Get the new key presses since the last iteration

        for key in keys_pressed:#Check for key presses and add them to the keys_held set            
            if key.keysym == "a":
                keys_held.add("a")
            elif key.keysym == "d":
                keys_held.add("d")
            elif key.keysym == "space" and "space" not in keys_held:
                keys_held.add("space")
                if len(lasers) < 3:  # Limit the number of lasers on screen to 3
                    lasers.append(fire_laser(canvas, player_ship))
        
        if "a" in keys_held:
            move_player_ship(canvas, player_ship, SHIP_MOVE_LEFT)
        if "d" in keys_held:
            move_player_ship(canvas, player_ship, SHIP_MOVE_RIGHT)

        for laser in lasers[:]:#Make a copy of the lasers list to avoid modifying it while iterating
            canvas.move(laser, 0, -10)

            laser_left_x = canvas.get_left_x(laser)
            laser_right_x = laser_left_x + LASER_WIDTH
            laser_top_y = canvas.get_top_y(laser)
            laser_bottom_y = laser_top_y + LASER_HEIGHT

            collisions = canvas.find_overlapping(laser_left_x, laser_top_y, laser_right_x, laser_bottom_y) #Check for collisions with the enemy ship
            if any(part in collisions for part in enemy): #If the laser collides with any part of the enemy ship, remove the laser and the enemy ship from the canvas
                canvas.delete(laser)
                lasers.remove(laser)
                for part in enemy:
                    canvas.delete(part)
                enemy = []  # Clear the enemy list to indicate that the enemy has been destroyed
                break  # Exit the loop since the laser has been removed

            laser_top_y = canvas.get_top_y(laser)

            if laser_top_y < 0: #If the laser has moved off the top of the canvas, remove it from the canvas and the lasers list
                canvas.delete(laser)
                lasers.remove(laser)
                
        canvas.update()
        time.sleep(DELAY)    


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