from graphics import Canvas

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, "black")
    input("Press Enter to close the window...")
if __name__ == "__main__":
    main()