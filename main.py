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
ENEMY_SPEED = 3
ENEMY_DROP_DISTANCE = 15


# TODO: Increase enemy speed as enemies are destroyed.
# TODO: Add multiple rows of enemies.
# TODO: Add a special saucer with a visible alien pilot.
# TODO: Make the special saucer drop an upgrade when destroyed.
# TODO: Allow the player to catch falling upgrades.
# TODO: Add an upgrade that increases the on-screen laser limit.
# TODO: Add larger and stronger enemies in later levels.
# TODO: Add a score system.
# TODO: Add player lives.
# TODO: Add a high score system.
# TODO: Add a title screen.
# TODO: Add a level system.
# TODO: Add a pause feature.
# TODO: Add sound effects and music.

def main():
    # Create the game window
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    # Track which movement and firing keys are currently held down
    keys_held = set()

    # Stop tracking a key when the player releases it
    canvas.bind(
        "<KeyRelease>",
        lambda event: keys_held.discard(event.keysym)
    )

    # Draw the background and create the starting game objects
    draw_background(canvas)
    
    player_ship = draw_player_ship(canvas)
    
    enemies = draw_enemy_fleet(canvas)

    # Set the enemies' starting horizontal speed and direction
    enemy_dx = ENEMY_SPEED

    # Store the Canvas object ID of every active laser
    lasers = []
    
    # Track the game-over screen and its title animation
    game_over = False
    game_over_title = None
    game_over_frames = 0

    # Track the victory screen and its title animation
    game_won = False
    victory_title = None
    victory_frames = 0

    # Run the main game loop
    while True:

        # Handle the retry and quit controls after the game ends
        if game_over or game_won:
            game_over_keys_pressed = canvas.get_new_key_presses()

            for key in game_over_keys_pressed:
                
                # Quit the game or reset everything for a new round
                if key.keysym == "q":
                    canvas.winfo_toplevel().destroy()
                    return
                elif key.keysym == "r":
                    canvas.clear()
                    draw_background(canvas)

                    player_ship = draw_player_ship(canvas)
                    enemies = draw_enemy_fleet(canvas)

                    lasers = []
                    enemy_dx = ENEMY_SPEED
                    keys_held.clear()

                    game_over = False
                    game_over_title = None
                    game_over_frames = 0

                    game_won = False
                    victory_title = None
                    victory_frames = 0
                    break

            if not game_over and not game_won:
                canvas.update()
                time.sleep(DELAY)

            # Choose the colors and frame counter for the active ending screen
            if game_over:
                game_over_frames += 1
                active_title = game_over_title
                active_frames = game_over_frames
                first_color = "dark red"
                second_color = "red"
            else:
                victory_frames += 1
                active_title = victory_title
                active_frames = victory_frames
                first_color = "dark green"
                second_color = "lime green"

            if active_frames % 15 == 0:

                # Switch the title color every 15 frames to create a flashing effect
                if (active_frames // 15) % 2 == 0:
                    canvas.set_fill_color(
                        active_title,
                        first_color
                    )
                else:
                    canvas.set_fill_color(
                        active_title,
                        second_color
                    )

            canvas.update()
            time.sleep(DELAY)

            # Skip the normal gameplay code while an ending screen is active
            continue
        
        # Collect any keys pressed during this frame
        keys_pressed = canvas.get_new_key_presses()

        # Begin tracking movement keys and fire one laser per spacebar press
        for key in keys_pressed:
            if key.keysym == "a":
                keys_held.add("a")

            elif key.keysym == "d":
                keys_held.add("d")

            elif key.keysym == "space" and "space" not in keys_held:
                keys_held.add("space")

                if len(lasers) < 3:
                    lasers.append(fire_laser(canvas, player_ship))

        # Move the ship while a movement key remains held down
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

        # Move each laser and check whether it hits an enemy
        for laser in lasers[:]:
            canvas.move(laser, 0, -10)

            # Calculate the laser's boundaries for collision detection
            laser_left_x = canvas.get_left_x(laser)
            laser_right_x = laser_left_x + LASER_WIDTH
            laser_top_y = canvas.get_top_y(laser)
            laser_bottom_y = laser_top_y + LASER_HEIGHT

            # Find every canvas object currently touching the laser
            collisions = canvas.find_overlapping(
                laser_left_x,
                laser_top_y,
                laser_right_x,
                laser_bottom_y
            )

            # Search the overlapping objects for an enemy ship part
            collided_enemy = None

            for enemy in enemies:
                if any(part in collisions for part in enemy):
                    collided_enemy = enemy
                    break
            
            # Remove both the laser and the entire enemy when a hit occurs
            if collided_enemy is not None:
                canvas.delete(laser)
                lasers.remove(laser)

                for part in collided_enemy:
                    canvas.delete(part)

                enemies.remove(collided_enemy)

                continue
            # Remove lasers after they travel beyond the top of the canvas
            if laser_top_y < 0:
                canvas.delete(laser)
                lasers.remove(laser)

        # Trigger victory after the final enemy is destroyed
        if len(enemies) == 0 and not game_won:
            game_won = True
            victory_title = draw_victory(canvas)

        # Move the enemy fleet horizontally
        move_enemy_row(canvas, enemies, enemy_dx)

        # Reverse the fleet and move it downward when it reaches an edge
        if enemy_row_hit_edge(canvas, enemies):
            enemy_dx = -enemy_dx
            move_enemy_row_down(canvas, enemies)

        # Trigger game over if any enemy reaches the player's ship height
        if enemies_reached_player(canvas, enemies, player_ship):
            game_over = True
            game_over_title = draw_game_over(canvas)

        canvas.update()
        time.sleep(DELAY)

# Draw the victory screen and its text
def draw_victory(canvas):

    # Draw the "VICTORY" title with a shadow effect
    canvas.create_text(
        CANVAS_WIDTH / 2 + 3,
        CANVAS_HEIGHT / 2 + 3,
        "VICTORY",
        "center",
        ("Arial", 36, "bold"),
        "dark green"
    )

    # Draw the "VICTORY" title in front of the shadow
    victory_title = canvas.create_text(
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2,
        "VICTORY",
        "center",
        ("Arial", 36, "bold"),
        "lime green"
    )

    # Draw the victory message
    canvas.create_text(
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2 + 45,
        "THE INVASION HAS BEEN REPELLED",
        "center",
        ("Arial", 12, "bold"),
        "white"
    )
    # Draw the retry and quit instructions below the victory message
    canvas.create_text(
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2 + 68,
        "Press 'r' to retry",
        "center",
        ("Arial", 12, "bold"),
        "white"
    )
    # Draw the quit instructions below the retry instructions
    canvas.create_text(
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2 + 90,
        "Press 'q' to quit",
        "center",
        ("Arial", 12, "bold"),
        "white"
    )

    return victory_title

# Draw the game over screen and its text
def draw_game_over(canvas):
    
    # Draw the "GAME OVER" title with a shadow effect
    canvas.create_text(
        CANVAS_WIDTH / 2 + 3,
        CANVAS_HEIGHT / 2 + 3,
        "GAME OVER",
        "center",
        ("Arial", 36, "bold"),
        "dark red"
    )

    # Draw the "GAME OVER" title in front of the shadow
    game_over_title = canvas.create_text(
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2,
        "GAME OVER",
        "center",
        ("Arial", 36, "bold"),
        "red"
    )

    # Draw the game over message and instructions for retrying or quitting
    canvas.create_text(
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2 + 45,
        "THE INVASION WAS SUCCESSFUL",
        "center",
        ("Arial", 12, "bold"),
        "white"
    )
    
    # Draw the retry and quit instructions below the game over message
    canvas.create_text(
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2 + 68,
        "Press 'r' to retry",
        "center",
        ("Arial", 12, "bold"),
        "white"
    )

    # Draw the quit instructions below the retry instructions
    canvas.create_text(
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2 + 90,
        "Press 'q' to quit",
        "center",
        ("Arial", 12, "bold"),
        "white"
    )

    return game_over_title

# Fire a laser from the player's ship and return the laser's rectangle object
def fire_laser(canvas, player_ship):
    laser_left_x = canvas.get_left_x(player_ship[6])  # Get the left x-coordinate of the nose cannon tip
    laser_top_y = canvas.get_top_y(player_ship[6]) 
    laser_right_x = laser_left_x + LASER_WIDTH 
    laser_bottom_y = laser_top_y + LASER_HEIGHT
    laser = canvas.create_rectangle(laser_left_x, laser_top_y, laser_right_x, laser_bottom_y, "red") # Spawn the laser at the nose cannon tip

    return laser

# Move the player's ship horizontally by dx pixels, while keeping it within the canvas boundaries
def move_player_ship(canvas,player_ship,dx):

    # Move each part of the player's ship by dx pixels
    for ship_part in player_ship:
        canvas.move(ship_part, dx, 0)

    player_ship_left_x = canvas.get_left_x(player_ship[11])
    player_ship_right_x = canvas.get_left_x(player_ship[13]) + 30

    # Move each part of the player's ship back to the right bounary
    if player_ship_left_x < 0:
        correction = -player_ship_left_x

        # Move each ship part back inside the left boundary if it goes beyond the left edge of the canvas
        for ship_part in player_ship:
            canvas.move(ship_part, correction,0)
    
    # Correct the ship's position if it goes beyond the right edge of the canvas
    if player_ship_right_x > CANVAS_WIDTH:
        correction = CANVAS_WIDTH - player_ship_right_x

        # Move each part of the player's ship back to the right edge of the canvas
        for ship_part in player_ship:
            canvas.move(ship_part, correction,0)    

# Draw the background, including black space and stars
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

# Check if any enemy has reached the player's ship height, indicating a game over condition
def enemies_reached_player(canvas, enemies, player_ship):
    player_top_y = canvas.get_top_y(player_ship[6])

    # Check each enemy's bottom y-coordinate to see if it has reached or passed the player's ship top y-coordinate
    for enemy in enemies:
        enemy_bottom_y = (
            canvas.get_top_y(enemy[-1]) + 7
        )

        # If any enemy's bottom y-coordinate is greater than or equal to the player's ship top y-coordinate, return True (game over)
        if enemy_bottom_y >= player_top_y:
            return True

    return False

# Draw the player's ship on the canvas and return a list of its parts
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

# Check if the enemy row has hit the left or right edge of the canvas
def enemy_row_hit_edge(canvas, enemies):

    # If there are no enemies left, return False (no edge hit)
    if len(enemies) == 0:
        return False
    
    # Calculate the leftmost and rightmost x-coordinates of the enemy row so we can determine if it has hit the canvas edges
    left_edge = canvas.get_left_x(enemies[0][1])
    right_edge = (canvas.get_left_x(enemies[-1][1]) + ENEMY_WIDTH)

    return left_edge <= 0 or right_edge >= CANVAS_WIDTH

# Move the entire row of enemies horizontally by dx pixels so that they move together as a fleet
def move_enemy_row(canvas, enemies, dx):
    
    # Move each part of every enemy ship in the row by dx pixels
    for enemy in enemies:
        for enemy_part in enemy:
            canvas.move(enemy_part, dx, 0)

# Move the entire row of enemies downward by a fixed distance when they reach the edge of the canvas
def move_enemy_row_down(canvas, enemies):
    for enemy in enemies:
        for enemy_part in enemy:
            canvas.move(enemy_part,0,ENEMY_DROP_DISTANCE)

# Draw a centered enemy row and return a list of its ships
def draw_enemy_fleet(canvas):
    enemies = []

    # Calculate the total width of the enemy fleet, including spacing between ships, so we can center it on the canvas
    fleet_width = (ENEMY_COUNT * ENEMY_WIDTH + (ENEMY_COUNT - 1) * ENEMY_SPACING)
    
    # Calculate the starting x-coordinate for the first enemy ship to center the fleet horizontally on the canvas
    enemy_start_x = (CANVAS_WIDTH - fleet_width) / 2

    # Draw each enemy ship in the fleet, spaced evenly apart, and add them to the enemies list
    for i in range(ENEMY_COUNT):
        enemy_x = enemy_start_x + i * (ENEMY_WIDTH + ENEMY_SPACING)
        enemy = draw_enemy(canvas, enemy_x, ENEMY_START_Y)
        enemies.append(enemy)

    return enemies

# Draw a single enemy ship at the specified (enemy_x, enemy_y) position on the canvas and return a list of its parts
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