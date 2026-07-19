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


def main():

    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    keys_held = set()
    canvas.bind(
        "<KeyRelease>",
        lambda event: keys_held.discard(event.keysym)
    )

    draw_background(canvas)

    player_ship = draw_player_ship(canvas)

    lasers = []
    
    while True:
        keys_pressed = canvas.get_new_key_presses()

        for key in keys_pressed:            
            if key.keysym == "a":
                keys_held.add("a")
            elif key.keysym == "d":
                keys_held.add("d")
            elif key.keysym == "space":
                lasers.append(fire_laser(canvas, player_ship))
        
        if "a" in keys_held:
            move_player_ship(canvas, player_ship, SHIP_MOVE_LEFT)
        if "d" in keys_held:
            move_player_ship(canvas, player_ship, SHIP_MOVE_RIGHT)

        for laser in lasers[:]:#Make a copy of the lasers list to avoid modifying it while iterating
            canvas.move(laser, 0, -10)
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
    outer_body = canvas.create_oval(220, 435, 280, 482, "dark gray")
    middle_body = canvas.create_oval(228, 440, 272, 476, "gray")
    inner_body = canvas.create_oval(238, 448, 262, 468, "light gray")
    player_ship.append(outer_body)
    player_ship.append(middle_body)
    player_ship.append(inner_body)


    # Cockpit glass
    cockpit_glass = canvas.create_oval(238, 438, 262, 458, "cyan")
    cockpit_highlight = canvas.create_oval(244, 442, 256, 452, "light blue")
    player_ship.append(cockpit_glass)
    player_ship.append(cockpit_highlight)

    # Nose cannon
    nose_cannon_base = canvas.create_rectangle(246, 410, 254, 442, "light gray")
    nose_cannon_tip = canvas.create_rectangle(248, 398, 252, 412, "white")
    player_ship.append(nose_cannon_base)
    player_ship.append(nose_cannon_tip)

    # Side cannons
    left_cannon_base = canvas.create_rectangle(214, 450, 224, 470, "gray")
    right_cannon_base = canvas.create_rectangle(276, 450, 286, 470, "gray")
    left_cannon_tip = canvas.create_rectangle(216, 440, 222, 452, "light gray")
    right_cannon_tip = canvas.create_rectangle(278, 440, 284, 452, "light gray")
    player_ship.append(left_cannon_base)
    player_ship.append(right_cannon_base)
    player_ship.append(left_cannon_tip)
    player_ship.append(right_cannon_tip)

    # Left wing
    left_wing_base = canvas.create_rectangle(195, 458, 225, 472, "dark gray")
    left_wing_highlight = canvas.create_rectangle(200, 462, 218, 468, "light gray")
    player_ship.append(left_wing_base)
    player_ship.append(left_wing_highlight)

    # Right wing
    right_wing_base = canvas.create_rectangle(275, 458, 305, 472, "dark gray")
    right_wing_highlight = canvas.create_rectangle(282, 462, 300, 468, "light gray")
    player_ship.append(right_wing_base)
    player_ship.append(right_wing_highlight)

    # Engine base
    left_engine_base = canvas.create_rectangle(230, 474, 245, 486, "gray")
    right_engine_base = canvas.create_rectangle(255, 474, 270, 486, "gray")
    left_engine_nozzle = canvas.create_rectangle(235, 478, 240, 488, "light gray")
    right_engine_nozzle = canvas.create_rectangle(260, 478, 265, 488, "light gray")
    player_ship.append(left_engine_base)
    player_ship.append(right_engine_base)
    player_ship.append(left_engine_nozzle)
    player_ship.append(right_engine_nozzle)

    # Engine flames
    left_outer_flame = canvas.create_oval(230, 485, 245, 500, "orange")
    right_outer_flame = canvas.create_oval(255, 485, 270, 500, "orange")
    left_inner_flame = canvas.create_oval(234, 490, 241, 500, "yellow")
    right_inner_flame = canvas.create_oval(259, 490, 266, 500, "yellow")
    player_ship.append(left_outer_flame)
    player_ship.append(right_outer_flame)
    player_ship.append(left_inner_flame)
    player_ship.append(right_inner_flame)

    # Small armor panels
    left_upper_armor_panel = canvas.create_rectangle(230, 460, 238, 466, "dark gray")
    right_upper_armor_panel = canvas.create_rectangle(262, 460, 270, 466, "dark gray")
    left_lower_armor_panel = canvas.create_rectangle(235, 470, 242, 475, "black")
    right_lower_armor_panel = canvas.create_rectangle(258, 470, 265, 475, "black")
    player_ship.append(left_upper_armor_panel)
    player_ship.append(right_upper_armor_panel)
    player_ship.append(left_lower_armor_panel)
    player_ship.append(right_lower_armor_panel)

    return player_ship

if __name__ == "__main__":
    main()