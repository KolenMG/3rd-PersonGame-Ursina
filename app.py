from ursina import *
app = Ursina()
from environment import InfiniteTerrain
from player import setup_player
from animations import setup_animations, update_animations, handle_input
from menu import main_menu
from inventory import Inventory
from hotbar import Hotbar
from ursina.shaders import lit_with_shadows_shader


Entity.default_shader = lit_with_shadows_shader
hotbar = Hotbar()

editor_camera = EditorCamera(enabled=False)
player, inventory_ui = setup_player()
terrain = InfiniteTerrain(camera=player, inventory_ui=inventory_ui)
editor_camera.target_z = -1000  # Initialize target_z with a default value


setup_animations(player)
main_menu(player)

def update():
    update_animations(player)
    terrain.update_chunks()

    
    editor_camera.enabled = held_keys['tab']

def input(key):
    handle_input(key, player, inventory_ui)
    hotbar.input_handler_function(key)   # Call the hotbar input handler

app.run()
