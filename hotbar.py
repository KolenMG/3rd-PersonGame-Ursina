from ursina import *

class Hotbar(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)  # Attach to the UI layer

        self.slots = []
        self.hotkey_texts = []  # List to store text for hotkeys
        self.selected_slot = 0

        for i in range(7):  # 7 slots for the specified keys
            # Slot itself
            slot = Entity(
                parent=self,
                model='quad',
                texture=None,
                color=color.gray,
                scale=(0.05, 0.05),
                position=(i * 0.12 - 0.36, -0.45),  # Adjust for 7 slots
                item=None  # Holds the item assigned to the slot
            )
            self.slots.append(slot)
            
            # Add a border for each slot
            border = Entity(
                parent=slot,
                model='quad',
                texture=None,
                color=color.black,
                scale=(1.1, 1.1),  # Slightly larger than the slot
                position=(0, 0),
                z=-0.01  # Keep it in the background of the slot
            )
            slot.border = border

        # Highlight for the selected slot
        self.selector = Entity(
            parent=self,
            model='quad',
            texture=None,
            color=color.white,
            scale=(0.065, 0.065),
            position=self.slots[self.selected_slot].position,
            z=-0.02
        )

        # Initialize the first slot as selected
        self.update_slot_highlight()

        # Input handling for hotbar
        self.input_handler = self.input_handler_function

    def input_handler_function(self, key):
        # Key-to-slot mapping
        key_to_slot = {
            '1': 0,
            '2': 1,
            '3': 2,
            '4': 3,
            'f1': 4,
            'f2': 5,
            'f3': 6,
        }

        if key in key_to_slot:
            self.select_slot(key_to_slot[key])

    def select_slot(self, index):
        """Update the selected slot."""
        self.selected_slot = index
        self.update_slot_highlight()

    def update_slot_highlight(self):
        """Update the selector and slot colors to reflect the selected slot."""
        for i, slot in enumerate(self.slots):
            if i == self.selected_slot:
                slot.color = color.white  # Highlight selected slot
                slot.border.color = color.white  # Highlight the border of the selected slot
            else:
                slot.color = color.gray  # Reset other slots to gray
                slot.border.color = color.black  # Reset the border color for non-selected slots
        self.selector.position = self.slots[self.selected_slot].position

    def set_item(self, slot_index, item):
        """
        Assign an item to a specific slot.
        :param slot_index: Index of the slot
        :param item: The item entity or representation
        """
        if 0 <= slot_index < len(self.slots):
            self.slots[slot_index].item = item
            self.slots[slot_index].color = color.white if item else color.gray
