import maya.cmds as cmds
import random
import math
import maya.api.OpenMaya as om2

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
            'speed_limit': self.speed_limit_field
        }

        self.flock = None

        cmds.button(label='Create Domain', command=self.create_domain_btn_active)

        # Button to create the flock
        cmds.button(label='Create Flock', command=self.create_flock_btn_active)

        # Button to bake the simulation
        cmds.button(label='Bake Simulation', command=self.bake_simulation_btn_active)

        # Show the main window
        cmds.showWindow()

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

class Boid:
    def __init__(self, boid_id, flock_params):
        self.boid_id = boid_id
        self.flock_params = flock_params

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
        # Create boid geometry (cone) in Maya and set initial position and keyframe
        cmds.polyCone(r=self.flock_params['boid_scale']*0.5, h=self.flock_params['boid_scale'], sa=20, sh=15, sc=10, name=self.boid_name)
        cmds.move(self.position[0], self.position[1], self.position[2], self.boid_name)
        cmds.setKeyframe(self.boid_name, t=0)

    def update_rotation(self):
        # Update boid rotation based on velocity
        initial_rotation_vector = om2.MVector([0, 1, 0])
        final_rotation_vector = om2.MVector(self.velocity)

        cross = initial_rotation_vector ^ final_rotation_vector
        cross_length = om2.MVector.length(cross)
        dot = initial_rotation_vector * final_rotation_vector

        # Create a z matrix
        row1 = [0, -cross[2], cross[1], 0]
        row2 = [cross[2], 0, -cross[0], 0]
        row3 = [-cross[1], cross[0], 0, 0]
        row4 = [0, 0, 0, 0]
        mat_list = [row1, row2, row3, row4]
        z = om2.MMatrix(mat_list)

        identity4 = om2.MMatrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        rotation_matrix = (identity4 + z + z * z * (1 - dot) * (1 / cross_length ** 2))
        m_matrix_tr = om2.MTransformationMatrix(rotation_matrix)
        m_euler_rot = m_matrix_tr.rotation()

        cmds.rotate(0, 0, 0, self.boid_name)
        cmds.rotate(math.degrees(-m_euler_rot.x), math.degrees(-m_euler_rot.y), math.degrees(-m_euler_rot.z), self.boid_name)


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
        # Update boid position based on velocity and set keyframe in Maya
        boid.position[0] += boid.velocity[0]
        boid.position[1] += boid.velocity[1]
        boid.position[2] += boid.velocity[2]
        cmds.move(boid.position[0], boid.position[1], boid.position[2], boid.boid_name)

        # Update boid rotation
        boid.update_rotation()

        cmds.setKeyframe(boid.boid_name, t=frame)

    def dist_sq(self, boid1, boid2):
        # Calculate squared distance between two boids
        return (
            (boid1.position[0] - boid2.position[0])**2 +
            (boid1.position[1] - boid2.position[1])**2 +
            (boid1.position[2] - boid2.position[2])**2
        )

UI()