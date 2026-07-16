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

    input("Press Enter to close the window...")
if __name__ == "__main__":
    main()