from graphics import Canvas

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
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

    # Player ship
    ship_left_x = 225
    ship_top_y = 440
    ship_right_x = 275
    ship_bottom_y = 480

    # Ship body
    canvas.create_oval(220, 435, 280, 482, "dark gray")
    canvas.create_oval(228, 440, 272, 476, "gray")
    canvas.create_oval(238, 448, 262, 468, "light gray")

    # Cockpit glass
    canvas.create_oval(238, 438, 262, 458, "cyan")
    canvas.create_oval(244, 442, 256, 452, "light blue")

    # Nose cannon
    canvas.create_rectangle(246, 410, 254, 442, "light gray")
    canvas.create_rectangle(248, 398, 252, 412, "white")

    # Side cannons
    canvas.create_rectangle(214, 450, 224, 470, "gray")
    canvas.create_rectangle(276, 450, 286, 470, "gray")
    canvas.create_rectangle(216, 440, 222, 452, "light gray")
    canvas.create_rectangle(278, 440, 284, 452, "light gray")

    # Left wing
    canvas.create_rectangle(195, 458, 225, 472, "dark gray")
    # canvas.create_rectangle(185, 466, 215, 480, "gray")
    canvas.create_rectangle(200, 462, 218, 468, "light gray")

    # Right wing
    canvas.create_rectangle(275, 458, 305, 472, "dark gray")
    canvas.create_rectangle(282, 462, 300, 468, "light gray")

    # Engine base
    canvas.create_rectangle(230, 474, 245, 486, "gray")
    canvas.create_rectangle(255, 474, 270, 486, "gray")
    canvas.create_rectangle(235, 478, 240, 488, "light gray")
    canvas.create_rectangle(260, 478, 265, 488, "light gray")

    # Engine flames
    canvas.create_oval(230, 485, 245, 500, "orange")
    canvas.create_oval(255, 485, 270, 500, "orange")
    canvas.create_oval(234, 490, 241, 500, "yellow")
    canvas.create_oval(259, 490, 266, 500, "yellow")

    # Small armor panels
    canvas.create_rectangle(230, 460, 238, 466, "dark gray")
    canvas.create_rectangle(262, 460, 270, 466, "dark gray")
    canvas.create_rectangle(235, 470, 242, 475, "black")
    canvas.create_rectangle(258, 470, 265, 475, "black")
    
    input("Press Enter to close the window...")
if __name__ == "__main__":
    main()