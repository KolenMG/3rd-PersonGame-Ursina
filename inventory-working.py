from ursina import Entity, camera, Quad, color, Tooltip

class Inventory(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent=camera.ui,
            model='quad',
            scale=(.5, .8),
            origin=(-.5, .5),
            position=(-.3, .4),
            texture=None,
            texture_scale=(5, 8),
            color=color.dark_gray,
            visible=False  # Hidden by default
        )
        self.item_parent = Entity(parent=self, scale=(1/5, 1/8))  # Grid of slots
        self.items = []  # To store inventory items

    def toggle_visibility(self):
        # Toggle inventory visibility (on/off)
        self.visible = not self.visible

    def add_item(self, item_name):
    # Add item to the inventory
        self.items.append(item_name)  # Add item to the list

        # Calculate the position of the new item in the grid
        rows = 8  # Number of rows in the inventory
        cols = 5  # Number of columns in the inventory
        index = len(self.items) - 1
        row = index // cols
        col = index % cols

        # Create a new slot for the item
        slot = Entity(
            parent=self.item_parent,
            model='quad',
            texture=item_name,
            position=(col * 1 + 0.5, -row * 1 - 0.38),  # Adjust the spacing between slots
            scale=(1, 1),  # Adjust slot size
            color=color.white
        )

        # Optional: Add a tooltip for the item
        Tooltip(f"Item: {item_name}", parent=slot)