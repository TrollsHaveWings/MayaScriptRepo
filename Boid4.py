import maya.cmds as cmds
import random
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
        self.spawn_radius_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Spawn Radius', value1=1000)

        # Create flock button
        cmds.button (label='Create Flock', command=self.create_flock)

        cmds.showWindow()

    def create_flock_btn_active(self, *args):
        # Retrieve the values from the UI elements
        count = cmds.intFieldGrp(self.count_field, query=True, value=True)[0]
        size = cmds.floatFieldGrp(self.size_field, query=True, value=True)[0]
        min_speed = cmds.floatFieldGrp(self.min_speed_field, query=True, value=True)[0]
        max_speed = cmds.floatFieldGrp(self.max_speed_field, query=True, value=True)[0]
        spawn_radius = cmds.floatFieldGrp(self.spawn_radius_field, query=True, value=True)[0]

        # Create a Boids instance and create the flock
        self.boids_instance = Boids(size, min_speed, max_speed, spawn_radius)
        self.boids_instance.Create_Flock(count)

class Boids:
    def __init__ (self, size, min_speed, max_speed, spawn_radius):
        self.master_group_name = "FLOCK_group"
        self.cb_size = size
        self.cb_min_speed = min_speed
        self.cb_max_speed = max_speed
        self.cb_spawn_radius = spawn_radius

    def create_boid (self, id):
        # Initilize the boid's ID.
        self.boid_id = id
        # Initilize Variables for the boid's position and ΔPosition.
        self.X = random.uniform(-1 * self.cb_spawn_radius, self.cb_spawn_radius)
        self.Y = random.uniform(-1 * self.cb_spawn_radius, self.cb_spawn_radius)
        self.Z = random.uniform(-1 * self.cb_spawn_radius, self.cb_spawn_radius)
        self.dX = random.uniform(-1, 1)
        self.dY = random.uniform(-1, 1)
        self.dZ = random.uniform(-1, 1)
        # Initilize boid name
        self.boid_name = f"boid{self.boid_id}"

        # Create the boid and the control group for the boid to go in.
        cmds.polyCone(name=self.boid_name, radius=self.cb_size, height=2*self.cb_size)
        cmds.xform(self.boid_name, t=[0, 0, 0], ws=True)

        self.ctrl_group_name = f"CTRL_{self.boid_name}"

        cmds.group(self.boid_name, name=self.ctrl_group_name)
        cmds.xform(self.ctrl_group_name, t=[self.X, self.Y, self.Z], ws=True)
        cmds.xform(self.ctrl_group_name, ro=[self.X, self.Y, self.Z], os=True)

        cmds.parent(self.ctrl_group_name, self.master_group_name)

    def boid_behavior (self):
        pass

    def create_flock (self, cf_count):
        self.flock_array = []
        
        if cmds.objExists(self.master_group_name):
            cmds.delete(self.master_group_name)

        cmds.group(empty=True, name=self.master_group_name)
        for i in range(cf_count):
            self.flock_array.append(self.create_boid(i))

Main ()
