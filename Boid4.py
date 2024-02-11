import maya.cmds as cmds
import random
import itertools
import math

class Main:
    def __init__ (self):
        Boid_UI ()

class Boid_UI:
    def __init__ (self):
        self.window = 'BoidWindow'
        self.title = 'Boidssss'
        self.size = (500, 300)

        # If the old version of the window exists, delete it.
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        # Create the window and the main layout.
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        self.main_layout = cmds.columnLayout(adjustableColumn=True)

        # UI fields for the flock variables
        self.count_field = cmds.intFieldGrp(numberOfFields=1, label='Boid Count', value1=500)
        
        # UI fields for the boid variables 
        self.size_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Size', value1=10)
        self.min_speed_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Min Speed', value1=100)
        self.max_speed_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Max Speed', value1=200)
        self.domain_radius_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Domain Radius', value1=1000)

        # Create flock button
        cmds.button (label='Create Flock', command=self.create_flock_btn_active)

        cmds.showWindow()

    def create_flock_btn_active(self, *args):
        # Retrieve the values from the UI elements
        count = cmds.intFieldGrp(self.count_field, query=True, value=True)[0]
        size = cmds.floatFieldGrp(self.size_field, query=True, value=True)[0]
        min_speed = cmds.floatFieldGrp(self.min_speed_field, query=True, value=True)[0]
        max_speed = cmds.floatFieldGrp(self.max_speed_field, query=True, value=True)[0]
        domain_radius = cmds.floatFieldGrp(self.domain_radius_field, query=True, value=True)[0]

        # Create a Boids instance and create the flock
        self.boids_instance = Boids(size, min_speed, max_speed, domain_radius)
        self.boids_instance.create_flock(count)
        self.boids_instance.create_domain(domain_radius)

class Boids:
    # Used in the Boids class __init__ method to give each boid a unique color
    BOID_COLORS_RGB = [
        (255, 97, 136),  # FF6188
        (169, 220, 118),  # A9DC76
        (255, 216, 102),  # FFD866
        (120, 220, 232),  # 78DCE8
        (171, 157, 242)  # AB9DF2
    ]

    def __init__ (self, size, min_speed, max_speed, domain_radius):
        self.master_group_name = "FLOCK_group"
        self.size = size
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.spawn_radius = domain_radius

        # Normalize colors to range 0-1 and create a cycle iterator
        BOID_COLORS = [(r/255.0, g/255.0, b/255.0) for r, g, b in BOID_COLORS_RGB]
        self.colors = itertools.cycle(BOID_COLORS)

    def create_boid (self, id):
        # Initilize the instanced boid's ID and name
        self.boid_id = id
        self.boid_name = f"boid{self.boid_id}"
        # Initilize Variables for the instanced boid's position
        self.X = random.uniform(-1 * self.spawn_radius, self.spawn_radius)
        self.Y = random.uniform(-1 * self.spawn_radius, self.spawn_radius)
        self.Z = random.uniform(-1 * self.spawn_radius, self.spawn_radius)
        # Initilize Variables for the instanced boid's ΔPosition
        self.dX = 0
        self.dY = 0
        self.dZ = 0

        # Create the boid and give it a random debug color
        cmds.polyCone(name=self.boid_name, radius=self.size, height=2*self.size)
        cmds.polyColorPerVertex(self.boid_name, rgb=next(self.colors), colorDisplayOption=True)

        # Create the boid's control group and position it in the scene
        self.ctrl_group_name = f"CTRL_{self.boid_name}"

        cmds.group(self.boid_name, name=self.ctrl_group_name)
        cmds.xform(self.ctrl_group_name, t=[self.X, self.Y, self.Z], ws=True)
        cmds.xform(self.ctrl_group_name, ro=[self.X, self.Y, self.Z], os=True)

        cmds.parent(self.ctrl_group_name, self.master_group_name)

    def pilot (self):
        pass

    def cohesion (self):
        pass

    def separation (self):
        pass

    def alignment (self):
        pass

    def collisions (self):
        pass

    def constraints (self):
        pass

    def create_flock (self, count):
        self.flock_array = []
        
        if cmds.objExists(self.master_group_name):
            cmds.delete(self.master_group_name)

        cmds.group(empty=True, name=self.master_group_name)
        for i in range(count):
            self.flock_array.append(self.create_boid(i))

    def create_domain (self, domain_radius):
        # If the domain obj already exists, delete it
        if cmds.objExists("FLOCK_domain"):
            cmds.delete("FLOCK_domain")
        
        # Create the domain obj for visual reference
        cmds.polyCube(name="FLOCK_domain", width=domain_radius*2, height=domain_radius*2, depth=domain_radius*2)
        cmds.polyColorPerVertex("FLOCK_domain", rgb=(0, 0, 0), colorDisplayOption=True)

        # Uses the template display type for wireframe and no selection
        cmds.setAttr("FLOCK_domain.overrideEnabled", 1)
        cmds.setAttr("FLOCK_domain.overrideDisplayType", 1)

        cmds.xform("FLOCK_domain", t=[0, 0, 0], ws=True)

# Run the main class to start the program
Main ()
