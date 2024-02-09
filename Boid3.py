import maya.cmds as cmds
import random
import math

master_group_name = "FLOCK_group"

class main:
    def __init__(self):
        BoidUI()
main()

class BoidUI:
    def __init__(self):
        # Set the window variables.
        self.window = 'BoidWindow'
        self.title = 'Boidssss'
        self.size = (500, 300)

        # If the old version of the window exists, delete it.
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        # Create the window and the main layout.
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        self.main_layout = cmds.columnLayout(adjustableColumn=True)

        # UI fields for the boid variables 
        self.boid_count_field = cmds.intFieldGrp(numberOfFields=1, label='Boid Count', value1=500)
        self.boid_size_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Size', value1=10)
        self.boid_min_speed_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Min Speed', value1=100)
        self.boid_max_speed_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Max Speed', value1=200)
        self.boid_spawn_radius_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Spawn Radius', value1=1000)

        # UI fields for the flock variables
        self.flock_count_field = cmds.intFieldGrp(numberOfFields=1, label='Flock Count', value1=1)

        # Create flock button
        cmds.button(label='Create Flock', command=lambda *args: (self.pass_boid_variables(), self.create_flock()))

        cmds.showWindow()

    def pass_boid_variables(self):
        boid_size = cmds.floatFieldGrp(self.boid_size_field, query=True, value1=True)
        boid_min_speed = cmds.floatFieldGrp(self.boid_min_speed_field, query=True, value1=True)
        boid_max_speed = cmds.floatFieldGrp(self.boid_max_speed_field, query=True, value1=True)
        boid_spawn_radius = cmds.floatFieldGrp(self.boid_spawn_radius_field, query=True, value1=True)

        self.boid = Boid(boid_size, boid_min_speed, boid_max_speed, boid_spawn_radius)

    def create_flock(self, *args):
        flock_count = cmds.intFieldGrp(self.flock_count_field, query=True, value1=True)

        Flock(flock_count, self.boid)

# ---------------------------

class Boid:
    def __init__(self, size, min_speed, max_speed, spawn_radius):
        self.master_group_name = master_group_name
        self.boid_size = size
        self.boid_min_speed = min_speed
        self.boid_max_speed = max_speed
        self.boid_spawn_radius = spawn_radius

    def create_boid(self, id):
        # Set the boid's id.
        self.boid_id = id
        # Variables for the boid's position, ΔPosition, and name.
        self.X = random.uniform(-1 * self.boid_spawn_radius, self.boid_spawn_radius)
        self.Y = random.uniform(-1 * self.boid_spawn_radius, self.boid_spawn_radius)
        self.Z = random.uniform(-1 * self.boid_spawn_radius, self.boid_spawn_radius)

        self.dX = random.uniform(-1, 1)
        self.dY = random.uniform(-1, 1)
        self.dZ = random.uniform(-1, 1)

        self.boid_name = f"boid{self.boid_id}"

        # Create the boid and the control group for the boid to go in.
        cmds.polyCone(name=self.boid_name, radius=self.boid_size, height=2*self.boid_size)
        cmds.xform(self.boid_name, t=[0, 0, 0], ws=True)

        self.ctrl_group_name = f"CTRL_{self.boid_name}"

        cmds.group(self.boid_name, name=self.ctrl_group_name)
        cmds.xform(self.ctrl_group_name, t=[self.X, self.Y, self.Z], ws=True)
        cmds.xform(self.ctrl_group_name, ro=[self.X, self.Y, self.Z], os=True)

        cmds.parent(self.ctrl_group_name, self.master_group_name)
        

# ---------------------------

class Boid__Behavior:
    def __init__(self, boid):
        self.boid = boid
        self.boid_speed = random.uniform(self.boid.boid_min_speed, self.boid.boid_max_speed)

    def move_boid(self):
        self.boid_X += self.boid_dX * self.boid_speed
        self.boid_Y += self.boid_dY * self.boid_speed
        self.boid_Z += self.boid_dZ * self.boid_speed

        self.boid.X = self.boid_X; self.boid.dX = self.boid_dX
        self.boid.Y = self.boid_Y; self.boid.dY = self.boid_dY
        self.boid.Z = self.boid_Z; self.boid.dZ = self.boid_dZ

        cmds.xform(self.boid.boid_name, t=[self.boid_X, self.boid_Y, self.boid_Z], ws=True)

    def turn_boid(self):
        pass

    def cohesion(self):
        pass

    def separation(self):
        pass

    def alignment(self):
        pass

    def collision_avoidance(self):
        pass

    def tellwitnessiwasmurdered(self):
        pass

# ---------------------------

class Flock:
    def __init__(self, flock_count):
        self.master_group_name = master_group_name
        self.flock_count = flock_count
        self.boid = boid
        self.flock_array = []
        try:
            self.create_flock()
        except Exception as e:
            print(f"Error creating flock: {e}")
            raise

    def create_flock(self):
        if cmds.objExists(self.master_group_name):
            cmds.delete(self.master_group_name)

        cmds.group(empty=True, name=self.master_group_name)
        for i in range(self.flock_count):
            self.flock_array.append(boid.create_boid(i))

# --------------------------- 

