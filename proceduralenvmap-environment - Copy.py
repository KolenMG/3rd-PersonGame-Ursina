from ursina import *
import numpy as np
from noise import pnoise2
import random
from minerals import Mineral


class InfiniteTerrain(Entity): ########### inspired by https://github.com/Vxtzq/Openworld
    def __init__(self, camera, **kwargs):
        super().__init__()
        self.camera = camera  # This is the FirstPersonController object
        
        self.chunks = {}
        self.chunk_size = 16
        self.terrain_scale = 100
        self.height_scale = 8
        self.chunk_distance = 2
        self.biome1 = ["tree","tree4", "tree5", #"tree6"
                       ]
        self.entities = []
        self.grass_distance = 1 * 16

        # Perlin noise settings for additional detail
        self.detail_scale = 20
        self.detail_height = 2
        
        # Perlin noise settings for mountains
        self.mountain_scale = 300
        self.mountain_height = 50
        self.mountain_threshold = 0

        self.octaves = 4
        self.persistence = 0.5
        self.lacunarity = 2.0
        self.seed = np.random.randint(0, 100)
        self.sun = DirectionalLight(shadow_map_resolution=(8192, 8192))
        self.sun.look_at(Vec3(-10, -1, -10))
        self.sun.position = Vec3(0, 10, 0)
        skybox_image = load_texture("skybox.jpg")
        Sky(texture=skybox_image)
        

        self.water = Entity(model='plane', color=color.color(160, 1, .8, .5), position=(0, -1, 0), scale=500, rotation=(0, 0, 0), double_sided=True)

        # Load the shader

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.update_chunks()

    def update(self):
        self.update_chunks()

    def generate_chunk(self, x, z):       
        vertices = []
        triangles = []
        uvs = []
        colors = []
        normals = []
        heightmap = []
        chunk_size_plus_one = self.chunk_size + 1

        for i in range(chunk_size_plus_one):
            for j in range(chunk_size_plus_one):
                world_x = x * self.chunk_size + i
                world_z = z * self.chunk_size + j
                
                # Base terrain layer
                base_height = pnoise2(world_x / self.terrain_scale, world_z / self.terrain_scale, 
                                      octaves=self.octaves, persistence=self.persistence, lacunarity=self.lacunarity, 
                                      repeatx=1024, repeaty=1024, base=self.seed) * self.height_scale

                # Detail layer
                detail_height = pnoise2(world_x / self.detail_scale, world_z / self.detail_scale, 
                                        octaves=self.octaves, persistence=self.persistence, lacunarity=self.lacunarity, 
                                        repeatx=1024, repeaty=1024, base=self.seed) * self.detail_height

                # Mountain layer
                mountain_noise = pnoise2(world_x / self.mountain_scale, world_z / self.mountain_scale, 
                                         octaves=self.octaves, persistence=self.persistence, lacunarity=self.lacunarity, 
                                         repeatx=1024, repeaty=1024, base=self.seed)
                mountain_height = (mountain_noise > self.mountain_threshold) * mountain_noise * self.mountain_height
                
                # Combine the heights
                height = base_height + detail_height + mountain_height
                heightmap.append(height)
                vertices.append((i, height, j))
                uvs.append((i / self.chunk_size, j / self.chunk_size))
                normals.append((0, 1, 0))  # Placeholder normals
                
                # Assign colors based on height
                if height < -.3:
                    colors.append(color.rgb32(255, 230, 146))
                elif height > 10:
                    colors.append(color.gray)
                elif height > 15:
                    colors.append(color.white)
                elif height > -.3 and height < 10:
                    colors.append(color.rgb32(51, 130, 10))

        for i in range(self.chunk_size):
            for j in range(self.chunk_size):
                idx = i * chunk_size_plus_one + j
                triangles.append((idx, idx + chunk_size_plus_one, idx + 1))
                triangles.append((idx + 1, idx + chunk_size_plus_one, idx + chunk_size_plus_one + 1))

        return vertices, triangles, colors, heightmap

    def update_chunks(self):
        """Updates chunks based on the player's current position."""
        player_chunk_x = int(self.camera.x // self.chunk_size)  # Access x, y, z directly from FirstPersonController
        player_chunk_z = int(self.camera.z // self.chunk_size)

        new_chunks = {}
        
        # Loop over the chunk grid around the player
        for x in range(player_chunk_x - self.chunk_distance, player_chunk_x + self.chunk_distance + 1):
            for z in range(player_chunk_z - self.chunk_distance, player_chunk_z + self.chunk_distance + 1):
                if (x, z) not in self.chunks:
                    print(f"Generating chunk at ({x}, {z})")  # Debugging chunk generation
                    vertices, triangles, colors, heightmap = self.generate_chunk(x, z)

                    new_chunk = Entity(
                        model=Mesh(vertices=vertices, triangles=triangles, colors=colors, mode='triangle', static=True),
                        collider='mesh', 
                        position=(x * self.chunk_size, 0, z * self.chunk_size),
                        shader=self.shader,
                        shadow_receiver=True,
                    )

                    # Add random objects like trees and grass
                    for i in range(1, self.chunk_size,4):
                        for j in range(1, self.chunk_size,4):
                            if random.randint(0, 100) > 90:
                                if heightmap[i * (self.chunk_size + 1) + j] > 1 and heightmap[i * (self.chunk_size + 1) + j - 16] - 1 < 6:
                                    Entity(model="2/grass_patches.glb",scale = 0.025, position=(i, heightmap[i * (self.chunk_size - 1) + j - 16] + 0.3, j), #was grasstest
                                          rotation=(0, random.randint(0, 360), 0), color=color.green, parent=new_chunk, double_sided=True)


                    for i in range(1, self.chunk_size,2):
                        for j in range(1, self.chunk_size,2):
                            if random.randint(0, 100) > 99:
                                if heightmap[i * (self.chunk_size + 1) + j] > 1 and heightmap[i * (self.chunk_size + 1) + j - 16] - 1 < 7:
                                    Entity(model=random.choice(self.biome1), position=(i, heightmap[i * (self.chunk_size + 1) + j - 16] - 1, j), 
                                           rotation=(0, random.randint(0, 360), 0), color=color.green, parent=new_chunk, double_sided=True)
                    for i in range(1, self.chunk_size, 4):
                        for j in range(1, self.chunk_size, 4):
                            if random.randint(0, 100) > 99:
                                # Check if height is appropriate for mineral placement
                                if heightmap[i * (self.chunk_size + 1) + j] > 1 and heightmap[i * (self.chunk_size + 1) + j - 16] - 1 < 6:
                                    # Procedural mineral spawning, use the Mineral class here
                                    ore_type = random.choice(['Iron', 'Gold', 'Diamond'])
                                    texture = random.choice(['bag', 'gem', 'orb'])

                                    # Create the mineral using the Mineral class from minerals.py
                                    mineral = Mineral(
                                        position=(i, heightmap[i * (self.chunk_size - 1) + j - 16] + 0.4, j),
                                        ore_type=ore_type,
                                        texture=texture,
                                        inventory_ui=self.inventory_ui,  # Ensure inventory UI is passed
                                        
                                    )
                                    mineral.parent = new_chunk  # Add the mineral to the chunk 

                    new_chunk.set_shader_input("light_direction", Vec3(1, -1, -1))
                    self.chunks[(x, z)] = new_chunk
                new_chunks[(x, z)] = self.chunks[(x, z)]

        self.water.position = (self.camera.x, -1, self.camera.z)

        # Remove old chunks that are no longer needed
        for chunk in list(self.chunks.keys()):
            if chunk not in new_chunks:
                destroy(self.chunks[chunk])
                del self.chunks[chunk]

        self.chunks = new_chunks
        self.sun.update_bounds(entity=scene)
