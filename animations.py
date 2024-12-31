from direct.actor.Actor import Actor
from ursina import *
from menu import main_menu
from minerals import Mineral
from player import setup_player
player = setup_player()
from inventory import Inventory
from hotbar import Hotbar
hotbar = Hotbar()



frame_ranges = {
    'idle': (60, 100),
    'walk': (20, 50),
    'mine': (150, 200),
    'jump': (100, 150),
}

animation_state = {
    'current_action': None,
    'interrupted_action': None,
    'is_playing': False
}


def setup_animations(player):
    """Set up the player model and animations."""
    player.actor = Actor("2/untitled.glb")  # Load your model
    player.actor.reparent_to(player)
    player.actor.set_scale(0.9)  # Scale the model
    player.actor.setHpr(180,0,0)
    


    


def play_animation(actor, from_frame, to_frame, loop=False, speed=1.25, action_name=None):
    """Play an animation on the actor."""
    global animation_state

    # Prevent restarting the same animation
    if animation_state['current_action'] == action_name:
        print(f"Animation {action_name} already playing.")
        return

    print(f"Playing animation: {action_name} (frames {from_frame}-{to_frame}, loop={loop})")
    actor.stop()  # Stop any current animations

    # Play the requested animation
    if loop:
        print(f"Looping animation from frame {from_frame} to {to_frame}")
        actor.loop('Armature|AllAnim|BaseLayer', fromFrame=from_frame, toFrame=to_frame)
    else:
        print(f"Playing animation from frame {from_frame} to {to_frame}")
        actor.loop('Armature|AllAnim|BaseLayer', fromFrame=from_frame, toFrame=to_frame)

    # Update the animation state
    animation_state['current_action'] = action_name
    animation_state['is_playing'] = not loop



def update_animations(player):
    """Update player animations based on input."""
    global animation_state

    if player.enabled:
        # Check for movement keys
        if any(held_keys[key] for key in ['w', 's', 'a', 'd']):
            if animation_state['current_action'] != 'walk':
                play_animation(player.actor, *frame_ranges['walk'], loop=True, action_name='walk')
        else:
            # Default to idle if no keys are held
            if animation_state['current_action'] != 'idle':
                play_animation(player.actor, *frame_ranges['idle'], loop=True, action_name='idle')
        if held_keys['left mouse']:
            if animation_state['current_action'] != 'mine':
                play_animation(player.actor, *frame_ranges['mine'], loop=True, action_name='mine')
                animation_state['current_action'] = 'mine'
        if held_keys['space']:
            if animation_state['current_action'] != 'jump':
                play_animation(player.actor, *frame_ranges['jump'], loop=True, action_name='jump')
                animation_state['current_action'] = 'jump'
        if hotbar.slots[hotbar.selected_slot].item:
            print(f"Selected item: {hotbar.slots[hotbar.selected_slot].item}")




def handle_input(key, player, 
                 #minerals
                 inventory_ui
                 ):
    if key == 'space':
        print("Spacebar pressed")  # Debugging print
        play_animation(player.actor, *frame_ranges['jump'], loop=True, action_name='jump')
    elif key == 'left mouse down' and player.enabled:
        ray = raycast(
            origin=player.position + Vec3(0, 1.3, 0),  
            direction=camera.forward,               
            distance=3,                             
            ignore=(player,),                       
            debug=True                              
        )
        if ray.hit and isinstance(ray.entity, Mineral):  # Ensure the hit entity is a Mineral
            ray.entity.mine()  
    if key == 'escape':  
        if hasattr(main_menu, "menu") and main_menu.menu is not None:
            destroy(main_menu.menu)  
            main_menu.menu = None
            player.enabled = True 
            mouse.locked = True
 
        else:
            player.enabled = False  
            mouse.locked = False

                   
            main_menu(player)
            inventory_ui.visible = False
        


    scroll_speed = 1  # Sensitivity for zoom default was 0.2 / 0.5
    max_distance = -20  # Maximum camera distance behind player
    min_distance = 1  # Minimum camera distance
    #default_height = 2.5  # Minimum height for camera pivot - no longer used

    if key == 'scroll down' or held_keys['g']:  # Scroll up to zoom out
        if player.camera_pivot.z > max_distance:  
            player.camera_pivot.z -= scroll_speed  # A (z-axis)
            player.camera_pivot.y += scroll_speed * 0.5  
    elif key == 'scroll up' or held_keys['t']:  # Scroll down to zoom in
        if player.camera_pivot.z < min_distance:  
            player.camera_pivot.z += scroll_speed  
            player.camera_pivot.y -= scroll_speed * 0.5 

    if key == 'i':  # Assuming 'i' toggles the inventory
        print("Toggling inventory visibility")
        inventory_ui.toggle_visibility()






