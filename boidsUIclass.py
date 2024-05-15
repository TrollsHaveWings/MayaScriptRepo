import maya.cmds as cmds
import random
import math



class UI:
    def __init__(self):
        window = 'spawn_window'
        title = 'Boidify Menu'
        size = (500, 300)

        # Delete any existing window with the same name
        if cmds.window(window, exists=True):
            cmds.deleteUI(window, window=True)

        # Create the main window and layout
        window = cmds.window(window, title=title, widthHeight=size)
        main_layout = cmds.columnLayout(adjustableColumn=True)

        # UI fields for boid parameters
        self.count_field = cmds.intFieldGrp(numberOfFields=1, labelThis='Boid Count', value1=100)
        self.boid_scale_field = cmds.floatFieldGrp(numberOfFields=1, labelThis='Boid Scale', value1=0.3)
        self.domain_radius_field = cmds.floatFieldGrp(numberOfFields=1, labelThis='Domain Radius', value1=10.0)
        self.max_time_field = cmds.intFieldGrp(numberOfFields=1, labelThis='Animation Length (Frames)', value1=500)
        self.turning_factor_field = cmds.floatFieldGrp(numberOfFields=1, labelThis='Turning Factor', value1=0.2)
        self.centring_factor_field = cmds.floatFieldGrp(numberOfFields=1, labelThis='Centering Factor', value1=0.05)
        self.avoid_factor_field = cmds.floatFieldGrp(numberOfFields=1, labelThis='Avoidance Factor', value1=0.3)
        self.matching_factor_field = cmds.floatFieldGrp(numberOfFields=1, labelThis='Velocity Matching Factor', value1=0.02)
        self.visual_range_field = cmds.floatFieldGrp(numberOfFields=1, labelThis='Visual Range', value1=7.0)
        self.min_distance_field = cmds.floatFieldGrp(numberOfFields=1, labelThis='Minimum Boid Distance', value1=1.0)
        self.max_velocity_field = cmds.floatFieldGrp(numberOfFields=1, labelThis='Max Initial Velocity', value1=1.0)
        self.speed_limit_field = cmds.floatFieldGrp(numberOfFields=1, labelThis='Speed Limit', value1=2.0)

        # Button to create the flock
        cmds.button(label='Create Flock', command=self.create_flock_btn_active)

        # Show the main window
        cmds.showWindow()

    def create_flock_btn_active(self, *args):
        # Get parameter values from UI fields
        count = cmds.intFieldGrp(self.count_field, query=True, value=True)[0]
        boid_scale = cmds.floatFieldGrp(self.boid_scale_field, query=True, value=True)[0]
        domain_radius = cmds.floatFieldGrp(self.domain_radius_field, query=True, value=True)[0]
        time_max = cmds.intFieldGrp(self.max_time_field, query=True, value=True)[0]
        turning_factor = cmds.floatFieldGrp(self.turning_factor_field, query=True, value=True)[0]
        centring_factor = cmds.floatFieldGrp(self.centring_factor_field, query=True, value=True)[0]
        avoid_factor = cmds.floatFieldGrp(self.avoid_factor_field, query=True, value=True)[0]
        matching_factor = cmds.floatFieldGrp(self.matching_factor_field, query=True, value=True)[0]
        visual_range = cmds.floatFieldGrp(self.visual_range_field, query=True, value=True)[0]
        min_distance = cmds.floatFieldGrp(self.min_distance_field, query=True, value=True)[0]
        max_velocity = cmds.floatFieldGrp(self.max_velocity_field, query=True, value=True)[0]
        speed_limit = cmds.floatFieldGrp(self.speed_limit_field, query=True, value=True)[0]

        # Pack parameter values into a dictionary
        flock_params = {
            'count': count,
            'boid_scale': boid_scale,
            'domain_radius': domain_radius,
            'time_max': time_max,
            'turning_factor': turning_factor,
            'centring_factor': centring_factor,
            'avoid_factor': avoid_factor,
            'matching_factor': matching_factor,
            'visual_range': visual_range,
            'min_distance': min_distance,
            'max_velocity': max_velocity,
            'speed_limit': speed_limit
        }

        # Create and animate the flock
        flock = Flock(flock_params)
        flock.create()
        flock.animate()