import maya.cmds as cmds
import random
import math


class UI:
    def create_main_UI (self):
        self.window = 'ui_window'
        self.title = 'flock/boids UI'
        self.size = (500, 300)

        # If an old version of the window exists, delete it.
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        # Create the window and the main layout.
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        self.main_layout = cmds.columnLayout(adjustableColumn=True)

        # UI fields for the boid variables
        self.count_field = cmds.intFieldGrp(numberOfFields=1, label='Boid Count', value1=500)
        self.scale_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Scale', value1=10)
        self.domain_radius_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Domain Radius', value1=1000)

        cmds.button (label='Create Flock', command=self.create_flock_btn_active)

        cmds.showWindow()

    def create_flock_btn_active(self, *args):
        # This method is called when the 'Create Flock' button is pressed.

        master_group_name = "FLOCK_group"

        # Get the values from the UI fields and capture them in variables.
        count = cmds.intFieldGrp(self.count_field, query=True, value=True)[0]
        scale = cmds.floatFieldGrp(self.scale_field, query=True, value=True)[0]
        domain_radius = cmds.floatFieldGrp(self.domain_radius_field, query=True, value=True)[0]

        # Pack the values into a tuples to pass to the create_flock and create_boid functions.
        packed_boid_values = (master_group_name, scale, domain_radius)
        packed_flock_values = (master_group_name, count, domain_radius)

        Flock().create_flock(packed_flock_values, packed_boid_values)


class Boid:
    def create_boid (self, boid_id, packed_boid_values):
        # This method creates a single boid.
        master_group_name, scale, domain_radius = packed_boid_values

        # Create a unique name for the boid.
        boid_name = "boid_" + str(boid_id)

        spawn_radius = domain_radius * 0.75
        # The boid will spawn within 75% of the domain radius.
        self.X = random.uniform(-1*spawn_radius, spawn_radius)
        self.Y = random.uniform(-1*spawn_radius, spawn_radius)
        self.Z = random.uniform(-1*spawn_radius, spawn_radius)

        # TEMP --- Create a cone to represent the boid for testing purposes.
        cmds.polyCone(name=boid_name, radius=scale, height=scale*2)

        cmds.xform(boid_name, translation=(self.X, self.Y, self.Z))
        cmds.xform(boid_name, rotation=(self.X, self.Y, self.Z))

        return boid_name


class Flock:
    def create_flock(self, packed_flock_values, packed_boid_values):
        # This function creates the flock of boids.
        master_group_name, count, domain_radius = packed_flock_values

        # Check if the master group exists and delete it if it does then create a new one.
        if cmds.objExists(master_group_name):
            cmds.delete(master_group_name)
        cmds.group(empty=True, name=master_group_name)

        # Create the boids and parent them to the master group.
        for i in range(count):
            boid_id = i + 1
            boid_name = Boid().create_boid(boid_id, packed_boid_values)
            cmds.parent(boid_name, master_group_name)


# Call the UI class to create the main UI.
UI().create_main_UI()
