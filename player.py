from ursina import Entity, BoxCollider, Vec3, color
from ursina.prefabs.first_person_controller import FirstPersonController
from inventory import Inventory
from hotbar import Hotbar
hotbar = Hotbar()
terrain_width = 40

def setup_player():
    # Create player
    player = FirstPersonController(origin=(0, 30, 0), rotation=(0, 180, 0), collider = 'mesh', speed = 5)
    player.camera_pivot.z = -3.5
    player.camera_pivot.y = 2.5
    player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))
    player.enabled = False  # Disabled until the game starts
    player.crosshair = Entity(model = "quad", color = color.black, parent = player, position = (0, 0, 1), scale = (0.01, 0.01, 0.01))

    # Create inventory and attach it to player
    player.inventory = Inventory()  # Attach inventory to player

    return player, player.inventory  # Return both player and inventory
