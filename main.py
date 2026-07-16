from graphics import Canvas

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

def main():

    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    draw_background(canvas)

    player_ship = draw_player_ship(canvas)

    input("Press Enter to close the window...")

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