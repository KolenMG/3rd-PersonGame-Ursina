#from ursina import *
#from perlin_noise import PerlinNoise
#def create_environment():
#    noise = PerlinNoise(octaves=3, seed=12312124124141142414141)
#    amp = 6
#    freq = 24
#
#    terrain_width = 40
#    for i in range(terrain_width*terrain_width):
#        cube = Entity(model = 'cube', texture = 'grass', collider = 'mesh')
#        cube.x = floor(i/terrain_width)
#        cube.z = floor(i%terrain_width)
#        cube.y = floor(noise([cube.x/freq, cube.z/freq])*amp)
#    # Terrain
#    #Entity(model='plane', collider='box', scale=(100, 1, 150), texture='grass', texture_scale=(50, 50), color=color.green)
#
#    # Water
#    #Entity(model='plane', scale=(10, 1, 10), position=(10, 0.1, 10), texture='water', texture_scale=(10, 10), color=color.blue.tint(-0.3))
#
#    # Lighting and sky
#    sun = DirectionalLight()
#    sun.look_at(Vec3(2, -4, -1))
#    Sky()

from ursina import *
import random
from player import setup_player
player, inventory = setup_player()

# Chunk render logic to manage visibility based on player position
class Chunkrender(Entity):
    def __init__(self, position=(0, 0, 0), child=Entity()):
        super().__init__(
            position=position,
            child=child
        )

    def update(self):
        # Distance range to render chunks
        rendrange = 100
        # Access player's position directly
        pposx = player.x  # Directly use player's x position
        pposz = player.z  # Directly use player's z position
        
        rlimitxP = pposx + rendrange
        rlimitxN = pposx - rendrange
        rlimitzP = pposz + rendrange
        rlimitzN = pposz - rendrange
        chunkx = self.position[0]
        chunkz = self.position[2]

        # Enable chunk visibility if within render range
        if chunkx < rlimitxP and chunkx > rlimitxN and chunkz < rlimitzP and chunkz > rlimitzN:
            self.child.enable()
        else:
            self.child.disable()


# Function to generate a random world seed for variety
def gen_god():
    god = random.randint(1000, 9999)
    random.seed(god)
    print(god)

# Function to spawn different types of objects in the world
def spawn_shroom(x, y, chunknode):
    # Spawn mushrooms as cubes (no texture)
    Entity(model="cube", color=color.orange, position=(x * 10, -.6, y * 10), parent=chunknode)
    Entity(model="cube", color=color.orange, position=((x * 10)-3, -.6, y * 10), parent=chunknode)
    Entity(model="cube", color=color.orange, position=((x * 10)-3, -.6, (y * 10)-3), parent=chunknode)

def spawn_oak(x, y, chunknode):
    # Spawn oak trees as cubes (no texture)
    Entity(model="tree.obj", color=color.green, position=(x * 5, 0, y * 5), parent=chunknode)

def spawn_pine(x, y, chunknode):
    # Spawn the pine tree model
    level = Entity(
        model="map.glb",  # Complex model
        texture="/2/textures/PP_Color_Palette.png",
        position=(x * 5, 18, y * 5),
        parent=chunknode,
        scale=1,
        collider = 'mesh'
    )
    level.mesh_collider.collider = 'mesh'
    level.mesh_collider.visible = False



#def spawn_pine(x, y, chunknode):
#    # Spawn pine trees as cubes (no texture)
#    entity = Entity(
#        model="map.glb",
#        texture="/2/textures/PP_Color_Palette.png",
#        position=(x * 5, 25, y * 5),
#        parent=chunknode,
#        collider='box',  # Use a 'box' collider by default
#        scale=1
#    )
#    
#    # Now add a custom BoxCollider to the entity (adjust size and offset as needed)
#    entity.collider = BoxCollider(entity, size=(100, 2, 100))  # Adjust size as needed



# Generate a chunk with objects like trees and mushrooms
def gen_chunk(chunkx, chunkz):
    chunknode = Entity(position=(chunkx, 0, chunkz), enabled=False)
    rendnode = Chunkrender(position=(chunkx, 0, chunkz), child=chunknode)
    chunk = Entity(texture = 'grass',color=color.green, scale=(100, 2, 100), collider='cube', position=(chunkx, -1, chunkz), parent=chunknode)
    #chunk = Entity(model="map.fbx",           # color=color.green,            texture = "/2/textures/PP_Color_Palette.png",            position=(chunkx, -1, chunkz), parent=chunknode)

    
    #mapsize = 2
    #for x in range(mapsize):
    #    for y in range(mapsize):
    #        chance = random.randint(0, 9)
    #        if chance == 8:
    #            spawn_oak(x, y, chunknode)
    #        elif chance == 1:
    #            spawn_pine(x, y, chunknode)
    #        elif chance == 1 or chance == 0:
    #            spawn_shroom(x, y, chunknode)

# Generate a world with multiple chunks
def gen_world():
    worldlimit = 10
    for cx in range(-worldlimit, worldlimit + 1):
        for cy in range(-worldlimit, worldlimit + 1):
            gen_chunk(cx * 50, cy * 50)

# Update player position to determine chunk visibility range
def update():
    global pposx, pposz
    pposx = player.getX()
    pposz = player.getZ()

# Function to create the environment and spawn world
def create_environment():
    gen_god()  # Generate the random seed for the world
    gen_world()  # Generate the chunks around the player
    
    Entity(
        model="map.glb",
        texture="/2/textures/PP_Color_Palette.png",
        position=(1 * 5, 28, 1 * 5),
        scale=1
    )
    # Lighting and sky
    sun = DirectionalLight()
    sun.look_at(Vec3(2, -4, -1))
    Sky()
