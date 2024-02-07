import maya.cmds as cmds
import random
import math

class BoidUI:
    def __init__(self):
        self.window = 'BoidWindow'
        self.title = 'Boid Creator'
        self.size = (500, 300)

        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)

        self.main_layout = cmds.columnLayout(adjustableColumn=True)

        self.boid_count_field = cmds.intFieldGrp(numberOfFields=1, label='Boid Count', value1=50)
        self.boid_size_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Size', value1=1.0)
        self.boid_max_speed_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Max Speed', value1=10.0)
        self.boid_spawn_radius_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Spawn Radius', value1=100.0)

        cmds.button(label='Create Flock', command=self.create_flock)

        cmds.showWindow()

    def create_flock(self, *args):
        boid_count = cmds.intFieldGrp(self.boid_count_field, query=True, value1=True)
        boid_size = cmds.floatFieldGrp(self.boid_size_field, query=True, value1=True)
        boid_max_speed = cmds.floatFieldGrp(self.boid_max_speed_field, query=True, value1=True)
        boid_spawn_radius = cmds.floatFieldGrp(self.boid_spawn_radius_field, query=True, value1=True)

        flock = Flock(boid_count, boid_size, boid_max_speed, boid_spawn_radius)

# Create the UI
BoidUI()

# ---------------------------

class Boid:
    def __init__(self, id, size, max_speed, spawn_radius, master_group_name):
        self.id = id
        self.size = size
        self.max_speed = max_speed
        self.spawn_radius = spawn_radius
        self.master_group_name = master_group_name
        try:
            self.create_boid()
        except Exception as e:
            print(f"Error creating boid {self.id}: {e}")
            raise

    def create_boid(self):
        # Variables for the boid's position, ΔPosition, and name.
        self.X = random.uniform(-self.spawn_radius, self.spawn_radius)
        self.Y = random.uniform(-self.spawn_radius, self.spawn_radius)
        self.Z = random.uniform(-self.spawn_radius, self.spawn_radius)

        self.dX = random.uniform(-1, 1)
        self.dY = random.uniform(-1, 1)
        self.dZ = random.uniform(-1, 1)

        self.boid_name = f"boid{self.id}"

        # Create the boid and the control group for the boid to go in.
        cmds.polyCone(name=self.boid_name, radius=self.size, height=2*self.size)
        cmds.xform(self.boid_name, t=[0, 0, 0], ws=True)

        ctrl_group_name = f"CTRL_{self.boid_name}"

        cmds.group(self.boid_name, name=ctrl_group_name)
        cmds.xform(ctrl_group_name, t=[self.X, self.Y, self.Z], ws=True)
        cmds.xform(ctrl_group_name, ro=[self.X, self.Y, self.Z], os=True)

        cmds.parent(ctrl_group_name, self.master_group_name)

# ---------------------------

class Flock:
    def __init__(self, boid_count, boid_size, boid_max_speed, boid_spawn_radius):
        self.master_group_name = "FLOCK_group"
        self.boid_count = boid_count
        self.boid_size = boid_size
        self.boid_max_speed = boid_max_speed
        self.boid_spawn_radius = boid_spawn_radius
        self.boids = []
        try:
            self.create_flock()
        except Exception as e:
            print(f"Error creating flock: {e}")
            raise

    def create_flock(self):
        if cmds.objExists(self.master_group_name):
            cmds.delete(self.master_group_name)

        cmds.group(empty=True, name=self.master_group_name)
        for i in range(self.boid_count):
            self.boids.append(Boid(i, self.boid_size, self.boid_max_speed, self.boid_spawn_radius, self.master_group_name))
