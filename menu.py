from ursina import *

def main_menu(player):
    # Check if a menu already exists and avoid creating duplicates
    if hasattr(main_menu, "menu") and main_menu.menu is not None:
        return  # Menu is already active, so don't create a new one

    def start_game():
        destroy(main_menu.menu)  # Destroy the menu
        main_menu.menu = None   # Reset the menu reference
        player.enabled = True   # Enable the player
        mouse.locked = True     # Lock the mouse
        mouse.visible = False

    # Create the menu entity
    main_menu.menu = Entity(parent=camera.ui, model='quad', scale=(2, 1.5), color=color.black66)
    Text("Main Menu", origin=(0, 0), scale=2, position=(0, 0.4), parent=main_menu.menu, color=color.white)
    Button("Start Game", scale=(0.2, 0.1), position=(0, 0.2), on_click=start_game, parent=main_menu.menu)
    Button("Quit", scale=(0.2, 0.1), position=(0, 0), on_click=application.quit, parent=main_menu.menu)
