from ursina import *
from ursina import Entity, Vec3
import random

class Inventory(Entity):
    def __init__(self, width=5, height=8, **kwargs):
        super().__init__(
            parent=camera.ui,
            model=Quad(radius=.015),
            texture=None,
            texture_scale=(width, height),
            scale=(width * .1, height * .1),
            origin=(-.5, .5),
            position=(-.3, .4),
            color=color.hsv(0, 0, .1, .9),
            visible=False
        )

        self.width = width
        self.height = height
        self.items = []  # List to store item textures or identifiers
        self.free_spots = [(x, y) for x in range(self.width) for y in range(self.height)]  # Track available spots

        for key, value in kwargs.items():
            setattr(self, key, value)

    def find_free_spot(self):
        """Find a free spot in the inventory grid."""
        if not self.free_spots:
            return None  # Inventory is full
        return self.free_spots.pop(0)  # Get the first available spot and remove it from the list

    def add_free_spot(self, x, y):
        """Add a free spot back when an item is removed."""
        self.free_spots.append((x, y))

    def append(self, item):
        """Append an item to the inventory."""
        if len(self.children) >= self.width * self.height:
            print('Inventory is full!')
            error_message = Text('<red>Inventory is full!', origin=(0, -1.5), x=-.5, scale=2)
            destroy(error_message, delay=1)
            return

        # Find a free spot
        spot = self.find_free_spot()
        if spot is None:
            print("No free spot available!")
            return

        x, y = spot
        scale_factor = 0.1  # Adjust for smaller item size

        # Create the draggable icon
        icon = Draggable(
            parent=self,
            model='quad',
            texture=item,
            color=color.white,
            scale=(1 / self.texture_scale[0]) * scale_factor,  # Adjust item scale
            origin=(-.5, .5),
            x=(x + 0.5) * 1 / self.width,  # Grid-based X position, adjusted for scale
            y=-(y + 0.5) * 1 / self.height,  # Grid-based Y position, adjusted for scale
            z=-.5,
        )

        # Adding tooltip and rarity
        name = item.replace('_', ' ').title()
        if random.random() < .25:
            icon.color = color.gold
            name = '<orange>Rare ' + name
        icon.tooltip = Tooltip(name)
        icon.tooltip.background.color = color.hsv(0, 0, 0, .8)

        # Drag functionality
        def drag():
            icon.org_pos = (icon.x, icon.y)
            icon.z -= .01  # Ensure the dragged item overlaps the rest

        def drop():
            # Snap item back to grid if dropped within boundaries
            icon.x = int((icon.x + (icon.scale_x / 2)) * self.width) / self.width
            icon.y = int((icon.y - (icon.scale_y / 2)) * self.height) / self.height
            icon.z += .01

            # Ensure correct placement in the grid (within boundaries)
            if icon.x < 0 or icon.x >= 1 or icon.y > 0 or icon.y <= -1:
                icon.position = icon.org_pos
                return

            # Prevent overlapping by checking if the spot is already occupied
            for c in self.children:
                if c == icon:
                    continue
                if c.x == icon.x and c.y == icon.y:
                    print('Position already occupied, finding a new spot.')
                    new_spot = self.find_free_spot()  # Find a new free spot
                    if new_spot:
                        icon.x = (new_spot[0] + 0.5) * 1 / self.width
                        icon.y = -(new_spot[1] + 0.5) * 1 / self.height
                        break

        icon.drag = drag
        icon.drop = drop

    def toggle_visibility(self):
        """Toggle the visibility of the inventory."""
        self.visible = not self.visible

        if self.visible:
            mouse.locked = False
            mouse.visible = True
        else:
            mouse.locked = True
            mouse.visible = False
