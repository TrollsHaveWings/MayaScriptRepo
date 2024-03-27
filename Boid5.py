import maya.cmds as cmds
import random
import itertools
import math

class UI:
    def __init__ (self):
        self.window = 'BoidWindow'
        self.title = 'Boidssss'
        self.size = (500, 300)

        BOID_COLORS_RGB = [
        # Used in the Boids class __init__ method to give each boid a unique color
            (255, 97, 136),  # FF6188
            (169, 220, 118),  # A9DC76
            (255, 216, 102),  # FFD866
            (120, 220, 232),  # 78DCE8
            (171, 157, 242)  # AB9DF2
        ]

        # Normalize colors to range 0-1 and create a cycle iterator
        BOID_COLORS = [(r/255.0, g/255.0, b/255.0) for r, g, b in BOID_COLORS_RGB]
        self.colors = itertools.cycle(BOID_COLORS)

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

        # UI fields for baking/playing the simulation

        # Get the default frame range and use it as the default values to initilize our frame range field
        self.default_frame_range = (cmds.playbackOptions(query=True, minTime=True), cmds.playbackOptions(query=True, maxTime=True))
        self.frame_range_field = cmds.intFieldGrp(numberOfFields=2, label='Frame Range', value1=self.default_frame_range[0], value2=self.default_frame_range[1])

        # Create flock button
        cmds.button (label='Create Flock', command=self.create_flock_btn_active)
        # Bake simulation button
        cmds.button (label='Bake Simulation', command=self.bake_simulation_btn_active)

        cmds.showWindow()

    def create_flock_btn_active(self, *args):
        # master_group_name = "FLOCK_group"
        master_group_name = "FLOCK_group"

        # Retrieve the values from the UI elements
        count = cmds.intFieldGrp(self.count_field, query=True, value=True)[0]
        size = cmds.floatFieldGrp(self.size_field, query=True, value=True)[0]
        min_speed = cmds.floatFieldGrp(self.min_speed_field, query=True, value=True)[0]
        max_speed = cmds.floatFieldGrp(self.max_speed_field, query=True, value=True)[0]
        domain_radius = cmds.floatFieldGrp(self.domain_radius_field, query=True, value=True)[0]

        # Pack the variables appropriately
        boid_vars = (master_group_name, size, min_speed, max_speed, domain_radius, self.colors)
        flock_vars = (master_group_name, count, domain_radius)

        # Call create_flock and create_domain
        self.flock_instance = Flock(boid_vars, flock_vars)
        self.flock_instance.create_domain()
        self.flock_instance.create_flock()

    def bake_simulation_btn_active(self, *args):
        # Retrive the values from the bake fields
        frame_range = cmds.intFieldGrp(self.frame_range_field, query=True, value=True)[0]



class Boids:
    def __init__ (self, boid_vars):
        # Unpack boids variables
        self.master_group_name, self.size, self.min_speed, self.max_speed, self.spawn_radius, self.colors = boid_vars

    def create_boid (self, id):
        # Initilize the instanced boid's ID and name
        boid_id = id
        boid_name = f"boid{boid_id}"
        # Initilize Variables for the instanced boid's position
        self.X = random.uniform(-1 * self.spawn_radius, self.spawn_radius)
        self.Y = random.uniform(-1 * self.spawn_radius, self.spawn_radius)
        self.Z = random.uniform(-1 * self.spawn_radius, self.spawn_radius)
        # Initilize Variables for the instanced boid's ΔPosition
        self.dX = 10
        self.dY = 5
        self.dZ = 9

        # Create the boid and give it a random debug color
        cmds.polyCone(name=boid_name, radius=self.size, height=2*self.size)
        cmds.polyColorPerVertex(boid_name, rgb=next(self.colors), colorDisplayOption=True)

        # Create the boid's control group and position it in the scene
        self.ctrl_group_name = f"CTRL_{boid_name}"

        cmds.group(boid_name, name=self.ctrl_group_name)
        cmds.xform(self.ctrl_group_name, t=[self.X, self.Y, self.Z], ws=True)
        cmds.xform(self.ctrl_group_name, ro=[self.X, self.Y, self.Z], os=True)

        cmds.parent(self.ctrl_group_name, self.master_group_name)

        return self

    def update_boid (self, id):
        self.X += self.dX
        self.Y += self.dY
        self.Z += self.dZ
        cmds.xform(self.ctrl_group_name, t=[self.X, self.Y, self.Z], ws=True)



class Flock:
    def __init__ (self, boid_vars, flock_vars):
        # Unpack flock variables
        self.master_group_name, self.count, self.domain_radius = flock_vars
        self.boid_vars = boid_vars

    def create_domain (self):
        # If the domain obj already exists, delete it
        if cmds.objExists("FLOCK_domain"):
            cmds.delete("FLOCK_domain")

        # Create the domain obj for visual reference
        cmds.polyCube(name="FLOCK_domain", width=self.domain_radius*2, height=self.domain_radius*2, depth=self.domain_radius*2)
        cmds.polyColorPerVertex("FLOCK_domain", rgb=(0, 0, 0), colorDisplayOption=True)

        # Uses the template display type for wireframe and no selection
        cmds.setAttr("FLOCK_domain.overrideEnabled", 1)
        cmds.setAttr("FLOCK_domain.overrideDisplayType", 1)

        cmds.xform("FLOCK_domain", t=[0, 0, 0], ws=True)

    def create_flock (self):
        self.flock_array = []

        if cmds.objExists(self.master_group_name):
            cmds.delete(self.master_group_name)
        cmds.group(empty=True, name=self.master_group_name)

        for i in range(self.count):
            boid_instance = Boids(self.boid_vars)
            boid = boid_instance.create_boid(i)
            self.flock_array.append(boid)

    def update_flock (self):
        for boid in self.flock_array:
            boid.update_boid(0)


# Run the UI class to start the program
UI ()
