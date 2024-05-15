import maya.cmds as cmds
import random
import math

class UI:
    def __init__(self):
        window = 'spawn_window'
        title = 'Boid Menu'
        size = (700, 300)

        # Delete any existing window with the same name
        if cmds.window(window, exists=True):
            cmds.deleteUI(window, window=True)

        # Create the main window and layout
        window = cmds.window(window, title=title, widthHeight=size)
        main_layout = cmds.columnLayout(adjustableColumn=True)

        # Create an option menu for selecting collision objects
        self.collision_objects_menu = cmds.optionMenu(
            parent=main_layout,
            label='Select Collision Object or Group:',
        )

        self.update_collision_object_menu()

        # Button to scan the scene and populate the option menu
        cmds.button(label='update full scene', command=self.update_collision_object_menu, parent=main_layout)

        # UI fields for boid parameters
        self.count_field = cmds.intFieldGrp(numberOfFields=1, label='Boid Count', value1=100)
        self.boid_scale_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Scale', value1=0.3)
        self.domain_radius_field = cmds.floatFieldGrp(numberOfFields=1, label='Domain Radius', value1=10.0)
        self.max_time_field = cmds.intFieldGrp(numberOfFields=1, label=' Animation Length (Frames)', value1=500)
        self.turning_factor_field = cmds.floatFieldGrp(numberOfFields=1, label='Turning Factor', value1=0.2)
        self.centring_factor_field = cmds.floatFieldGrp(numberOfFields=1, label='Centering Factor', value1=0.05)
        self.avoid_factor_field = cmds.floatFieldGrp(numberOfFields=1, label='Avoidance Factor', value1=0.3)
        self.matching_factor_field = cmds.floatFieldGrp(numberOfFields=1, label='Velocity Matching Factor', value1=0.02)
        self.visual_range_field = cmds.floatFieldGrp(numberOfFields=1, label='Visual Range', value1=7.0)
        self.min_distance_field = cmds.floatFieldGrp(numberOfFields=1, label='Minimum Boid Distance', value1=1.0)
        self.max_velocity_field = cmds.floatFieldGrp(numberOfFields=1, label='Max Initial Velocity', value1=1.0)
        self.speed_limit_field = cmds.floatFieldGrp(numberOfFields=1, label='Speed Limit', value1=2.0)
        self.boid_colision_radius_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Collision Radius', value1=20)
        self.master_group_name_field = cmds.textFieldGrp(label='Master Group Name', text='FLOCK_group')

        # Initialize the flock_params dictionary with UI field variables
        self.flock_params = {
            'count': self.count_field,
            'boid_scale': self.boid_scale_field,
            'domain_radius': self.domain_radius_field,
            'time_max': self.max_time_field,
            'turning_factor': self.turning_factor_field,
            'centring_factor': self.centring_factor_field,
            'avoid_factor': self.avoid_factor_field,
            'matching_factor': self.matching_factor_field,
            'visual_range': self.visual_range_field,
            'min_distance': self.min_distance_field,
            'max_velocity': self.max_velocity_field,
            'speed_limit': self.speed_limit_field,
            'collision_radius' : self.boid_colision_radius_field,
            'collision_objects': []
        }

        self.flock = None

        cmds.button(label='Create Domain', command=self.create_domain_btn_active)

        # Button to create the flock
        cmds.button(label='Create Flock', command=self.create_flock_btn_active)

        # Button to bake the simulation
        cmds.button(label='Bake Simulation', command=self.bake_simulation_btn_active)

        # Show the main window
        cmds.showWindow()

    def update_collision_object_menu(self, *args):
        # Clear the current items in the option menu
        cmds.optionMenu(self.collision_objects_menu, edit=True, deleteAllItems=True)

        # Get all objects and groups in the scene
        scene_objects = cmds.ls(type='transform')

        # Add the objects and groups to the option menu
        for obj in scene_objects:
            cmds.menuItem(label=obj, parent=self.collision_objects_menu)

    def create_flock_btn_active(self, *args):
        # Handle the 'Create Flock' button press
        self.update_flock_params()

        self.flock = Flock(self.flock_params)
        self.flock.create_flock()


    def bake_simulation_btn_active(self, *args):
        # Handle the 'Bake Simulation' button press
        self.update_flock_params()

        if self.flock is not None:
            self.flock.animate_flock()
        else:
            print("Please create a flock first.")

    def create_domain_btn_active(self, *args):
        # Handle the 'Create Domain' button press
        self.update_flock_params()

        Flock(self.flock_params).create_domain()

    def update_flock_params(self):
        # Update the flock_params dictionary with values from UI fields
        self.flock_params['count'] = cmds.intFieldGrp(self.count_field, query=True, value=True)[0]
        self.flock_params['boid_scale'] = cmds.floatFieldGrp(self.boid_scale_field, query=True, value=True)[0]
        self.flock_params['domain_radius'] = cmds.floatFieldGrp(self.domain_radius_field, query=True, value=True)[0]
        self.flock_params['time_max'] = cmds.intFieldGrp(self.max_time_field, query=True, value=True)[0]
        self.flock_params['turning_factor'] = cmds.floatFieldGrp(self.turning_factor_field, query=True, value=True)[0]
        self.flock_params['centring_factor'] = cmds.floatFieldGrp(self.centring_factor_field, query=True, value=True)[0]
        self.flock_params['avoid_factor'] = cmds.floatFieldGrp(self.avoid_factor_field, query=True, value=True)[0]
        self.flock_params['matching_factor'] = cmds.floatFieldGrp(self.matching_factor_field, query=True, value=True)[0]
        self.flock_params['visual_range'] = cmds.floatFieldGrp(self.visual_range_field, query=True, value=True)[0]
        self.flock_params['min_distance'] = cmds.floatFieldGrp(self.min_distance_field, query=True, value=True)[0]
        self.flock_params['max_velocity'] = cmds.floatFieldGrp(self.max_velocity_field, query=True, value=True)[0]
        self.flock_params['speed_limit'] = cmds.floatFieldGrp(self.speed_limit_field, query=True, value=True)[0]
        self.flock_params['collision_radius'] = cmds.floatFieldGrp(self.boid_colision_radius_field, query=True, value=True)[0]
        self.flock_params['collision_objects'] = cmds.optionMenu(self.collision_objects_menu, query=True, value=True)[0]

class Boid:
    def __init__(self, boid_id, flock_params):
        self.boid_id = boid_id
        self.flock_params = flock_params
        self.boid_collision_radius = flock_params['collision_radius']

        self.position = [0,0,0]
        self.velocity = [0,0,0]

        # Initialize boid position and velocity
        self.init_position()
        self.init_velocity()

        self.boid_name = f"boid_{boid_id}"

        # Create the boid geometry in Maya
        self.create_boid()

    def init_position(self):
        # Initialize boid position within the domain with a margin
        margin = 2
        self.position[0] = random.uniform(-self.flock_params['domain_radius']+margin, self.flock_params['domain_radius']-margin)
        self.position[1] = random.uniform(-self.flock_params['domain_radius']+margin, self.flock_params['domain_radius']-margin)
        self.position[2] = random.uniform(-self.flock_params['domain_radius']+margin, self.flock_params['domain_radius']-margin)

    def init_velocity(self):
        # Initialize boid velocity within a maximum range
        max_vel = self.flock_params['max_velocity']
        self.velocity[0] = random.uniform(-max_vel, max_vel)
        self.velocity[1] = random.uniform(-max_vel, max_vel)
        self.velocity[2] = random.uniform(-max_vel, max_vel)

    def create_boid(self):
        # Create boid geometry in Maya and set initial position and keyframe
        cmds.polySphere(r=self.flock_params['boid_scale'], name=self.boid_name)
        cmds.move(self.position[0], self.position[1], self.position[2], self.boid_name)
        cmds.setKeyframe(self.boid_name, t=0)

    def check_collision(self, position, velocity):
        collision_object = self.flock_params['collision_objects']

        if cmds.objExists(collision_object):
            # Check if the collision object is a group
            if cmds.objectType(collision_object) == 'transform':
                # If it's a group, get all the objects in the group
                collision_objects = cmds.listRelatives(collision_object, fullPath=True, type='transform')
            else:
                # If it's a single object, create a list with only that object
                collision_objects = [collision_object]

            for obj in collision_objects:
                # Get the position and radius of the collision object
                obj_pos = cmds.xform(obj, q=True, ws=True, rp=True)
                obj_radius = sum(cmds.getAttr(obj + '.boundingBox.boundingBoxSize')) / 3

                # Calculate the future position of the boid based on its current velocity
                future_position = [position[i] + velocity[i] for i in range(3)]

                # Calculate the coefficients of the quadratic equation
                m = velocity
                a = m[0]**2 + m[1]**2 + m[2]**2
                b = 2 * (m[0] * (future_position[0] - obj_pos[0]) + m[1] * (future_position[1] - obj_pos[1]) + m[2] * (future_position[2] - obj_pos[2]))
                c = ((future_position[0] - obj_pos[0])**2 + (future_position[1] - obj_pos[1])**2 + (future_position[2] - obj_pos[2])**2) - (self.boid_collision_radius + obj_radius)**2

                # Check if the discriminant is positive (collision detected)
                discriminant = b**2 - 4 * a * c
                if discriminant >= 0:
                    print(f"Collision detected between {self.boid_name} and {obj}")
                    # Collision detected, calculate the steering force to avoid the collision
                    steering_force = self.avoid_collision(future_position, obj_pos)
                    velocity[0] += steering_force[0]
                    velocity[1] += steering_force[1]
                    velocity[2] += steering_force[2]

        return velocity

    def avoid_collision(self, future_position, obj_pos):
        # Calculate the vector from the boid's future position to the collision object
        avoidance_vector = [future_position[i] - obj_pos[i] for i in range(3)]
        avoidance_vector_length = math.sqrt(sum(x**2 for x in avoidance_vector))
        avoidance_vector = [x / avoidance_vector_length for x in avoidance_vector]

        # Calculate the steering force based on the avoidance vector
        steering_force = [avoidance_vector[i] * self.flock_params['avoid_factor'] for i in range(3)]

        return steering_force


class Flock:
    def __init__(self, flock_params):
        self.flock_params = flock_params
        self.boids = []

        # Precalculate derived parameter values for efficiency
        self.visual_range_sq = self.flock_params['visual_range'] ** 2
        self.min_distance_sq = self.flock_params['min_distance'] ** 2
        self.domain = [
            [-self.flock_params['domain_radius'], -self.flock_params['domain_radius'], -self.flock_params['domain_radius']],
            [self.flock_params['domain_radius'], self.flock_params['domain_radius'], self.flock_params['domain_radius']]
        ]

    def create_domain(self):
        # Create a domain object for visual reference
        if cmds.objExists("FLOCK_domain"):
            cmds.delete("FLOCK_domain")

        cmds.polyCube(name="FLOCK_domain", width=self.flock_params['domain_radius']*2, height=self.flock_params['domain_radius']*2, depth=self.flock_params['domain_radius']*2)
        cmds.polyColorPerVertex("FLOCK_domain", rgb=(0,0,0), colorDisplayOption=True)

        # Uses the template display type for wireframe and no selection
        cmds.setAttr("FLOCK_domain.overrideEnabled", 1)
        cmds.setAttr("FLOCK_domain.overrideDisplayType", 1)

    def create_flock(self):

        # Create the specified number of boids
        for i in range(self.flock_params['count']):
            boid = Boid(i, self.flock_params)
            self.boids.append(boid)

    def animate_flock(self):
        print(f"Boids: {[boid.boid_name for boid in self.boids]}")
        # Simulate flock behavior over the specified number of frames
        for frame in range(1, self.flock_params['time_max']+1):
            print(f"Frame: {frame}")
            for boid in self.boids:
                print(f"Applying rules for {boid.boid_name}")
                self.apply_rules(boid)
                print(f"Updating boid {boid.boid_name}")
                self.update_boid(boid, frame)

    def apply_rules(self, boid):
        # Apply flocking rules to the boid
        self.cohesion(boid)
        self.avoidance(boid)
        self.alignment(boid)
        self.limit_speed(boid)
        self.bound_position(boid)

    def cohesion(self, boid):
        # Rule 1: Boids try to fly towards the center of mass of neighboring boids
        center = [0,0,0]
        count = 0
        for other in self.boids:
            if other != boid:
                if self.dist_sq(boid, other) < self.visual_range_sq:
                    center[0] += other.position[0]
                    center[1] += other.position[1]
                    center[2] += other.position[2]
                    count += 1
        if count > 0:
            center[0] /= count
            center[1] /= count
            center[2] /= count

            boid.velocity[0] += (center[0] - boid.position[0]) * self.flock_params['centring_factor']
            boid.velocity[1] += (center[1] - boid.position[1]) * self.flock_params['centring_factor']
            boid.velocity[2] += (center[2] - boid.position[2]) * self.flock_params['centring_factor']

    def avoidance(self, boid):
        # Rule 2: Boids try to keep a small distance away from other boids
        move = [0,0,0]
        for other in self.boids:
            if other != boid:
                if self.dist_sq(boid, other) < self.min_distance_sq:
                    move[0] += boid.position[0] - other.position[0]
                    move[1] += boid.position[1] - other.position[1]
                    move[2] += boid.position[2] - other.position[2]

        boid.velocity[0] += move[0] * self.flock_params['avoid_factor']
        boid.velocity[1] += move[1] * self.flock_params['avoid_factor']
        boid.velocity[2] += move[2] * self.flock_params['avoid_factor']

    def alignment(self, boid):
        # Rule 3: Boids try to match velocity with neighboring boids
        avg_vel = [0,0,0]
        count = 0
        for other in self.boids:
            if other != boid:
                if self.dist_sq(boid, other) < self.visual_range_sq:
                    avg_vel[0] += other.velocity[0]
                    avg_vel[1] += other.velocity[1]
                    avg_vel[2] += other.velocity[2]
                    count += 1
        if count > 0:
            avg_vel[0] /= count
            avg_vel[1] /= count
            avg_vel[2] /= count

            boid.velocity[0] += (avg_vel[0] - boid.velocity[0]) * self.flock_params['matching_factor']
            boid.velocity[1] += (avg_vel[1] - boid.velocity[1]) * self.flock_params['matching_factor']
            boid.velocity[2] += (avg_vel[2] - boid.velocity[2]) * self.flock_params['matching_factor']

    def limit_speed(self, boid):
        # Limit the speed of the boid
        speed_sq = (
            boid.velocity[0]**2 +
            boid.velocity[1]**2 +
            boid.velocity[2]**2
        )

        if speed_sq > self.flock_params['speed_limit']**2:
            speed = math.sqrt(speed_sq)
            boid.velocity[0] = (boid.velocity[0] / speed) * self.flock_params['speed_limit']
            boid.velocity[1] = (boid.velocity[1] / speed) * self.flock_params['speed_limit']
            boid.velocity[2] = (boid.velocity[2] / speed) * self.flock_params['speed_limit']

    def bound_position(self, boid):
        # Keep the boid within the defined domain
        margin = 2

        min_x = self.domain[0][0] + margin
        max_x = self.domain[1][0] - margin
        min_y = self.domain[0][1] + margin
        max_y = self.domain[1][1] - margin
        min_z = self.domain[0][2] + margin
        max_z = self.domain[1][2] - margin

        if boid.position[0] < min_x:
            boid.velocity[0] += self.flock_params['turning_factor']
        elif boid.position[0] > max_x:
            boid.velocity[0] -= self.flock_params['turning_factor']

        if boid.position[1] < min_y:
            boid.velocity[1] += self.flock_params['turning_factor']
        elif boid.position[1] > max_y:
            boid.velocity[1] -= self.flock_params['turning_factor']

        if boid.position[2] < min_z:
            boid.velocity[2] += self.flock_params['turning_factor']
        elif boid.position[2] > max_z:
            boid.velocity[2] -= self.flock_params['turning_factor']

    def update_boid(self, boid, frame):
        # Check for collisions and update the velocity if necessary
        new_velocity = boid.check_collision(boid.position, boid.velocity)

        # Update boid position based on the updated velocity and set keyframe in Maya
        boid.position[0] += new_velocity[0]
        boid.position[1] += new_velocity[1]
        boid.position[2] += new_velocity[2]
        cmds.move(boid.position[0], boid.position[1], boid.position[2], boid.boid_name)
        cmds.setKeyframe(boid.boid_name, t=frame)

        # Update the boid's velocity after updating its position
        boid.velocity = new_velocity

    def dist_sq(self, boid1, boid2):
        # Calculate squared distance between two boids
        return (
            (boid1.position[0] - boid2.position[0])**2 +
            (boid1.position[1] - boid2.position[1])**2 +
            (boid1.position[2] - boid2.position[2])**2
        )



UI()