from ursina import Entity, Vec3
import random
from inventory import Inventory
from hotbar import Hotbar

hotbar = Hotbar()
inventory_ui = Inventory()  # Correct, where 5 and 8 are numeric
class Mineral(Entity):
    ore_type_to_model = {
        'Iron': '2/picksandores3.glb',
        'Gold': '2/picksandores2.glb',
        'Diamond': 'Wolf_With_Baked_Action_Animations_For_Export_One_Mesh.obj'
    }

    def __init__(self, position, ore_type, texture, inventory_ui):
        super().__init__(
            model=self.ore_type_to_model[ore_type],
            scale=1,
            collider='box',
            position=position
        )
        self.ore_type = ore_type
        self.texture_name = texture
        self.inventory_ui = inventory_ui

    def mine(self):
        print(f"Mined {self.ore_type}!")
        self.inventory_ui.append(self.texture_name)  # Add item to the inventory
        self.disable()  # Disable the mineral after it's mined



def create_minerals(inventory_ui):
    return [
        Mineral(
            position=Vec3(random.uniform(-20, 20), 0.1, random.uniform(-20, 20)),
            ore_type=random.choice(['Iron', 'Gold', 'Diamond']),
            texture=random.choice(['bag', 'gem', 'orb']),  # Replace these with actual texture paths
            
        )
        for _ in range(10)
    ]
