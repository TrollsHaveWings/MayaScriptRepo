import maya.cmds as cmds
import random
import math


class UI:
    def __init__ (self):
        window = 'spawn_window'
        title = 'Boidify Menu'
        size = (500, 300)

        # If an old version of the window exists, delete it.
        if cmds.window(window, exists=True):
            cmds.deleteUI(window, window=True)

        # Create the window and the main layout.
        window = cmds.window(window, title=title, widthHeight=size)
        main_layout = cmds.columnLayout(adjustableColumn=True)

        # UI fields for the boid variables
        self.count_field = cmds.intFieldGrp(numberOfFields=1, label='Boid Count', value1=100)
        self.boid_scale_field = cmds.floatFieldGrp(numberOfFields=1, label='Boid Scale', value1=0.3)
        self.domain_radius_field = cmds.floatFieldGrp(numberOfFields=1, label='Domain Radius', value1=10.0)
        self.max_time_field = cmds.intFieldGrp(numberOfFields=1, label='Animation Length (Frames)', value1=500)
        self.turning_factor_field = cmds.floatFieldGrp(numberOfFields=1, label='Turning Factor', value1=0.2)
        self.centring_factor_field = cmds.floatFieldGrp(numberOfFields=1, label='Centering Factor', value1=0.05)
        self.avoid_factor_field = cmds.floatFieldGrp(numberOfFields=1, label='Avoidance Factor', value1=0.3)
        self.matching_factor_field = cmds.floatFieldGrp(numberOfFields=1, label='Velocity Matching Factor', value1=0.02)
        self.visual_range_field = cmds.floatFieldGrp(numberOfFields=1, label='Visual Range', value1=7.0)
        self.min_distance_field = cmds.floatFieldGrp(numberOfFields=1, label='Minimum Boid Distance', value1=1.0)
        self.max_velocity_field = cmds.floatFieldGrp(numberOfFields=1, label='Max Initial Velocity', value1=1.0)
        self.speed_limit_field = cmds.floatFieldGrp(numberOfFields=1, label='Speed Limit', value1=2.0)

        cmds.button(label='Create Flock', command=self.create_flock_btn_active)

        cmds.showWindow()

    def create_flock_btn_active(self, *args):
        # Get the values from the UI fields
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

        # Pack the values into a dict to pass to the Flock class
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

        flock = Flock(flock_params)
        flock.create()
        flock.animate()


class Boid:
    def __init__(self, boid_id, flock_params):
        self.boid_id = boid_id
        self.flock_params = flock_params

        self.position = [0,0,0]
        self.velocity = [0,0,0]

        self.init_position()
        self.init_velocity()

        self.boid_name = f"boid_{boid_id}"
        self.create_boid()

    def init_position(self):
        margin = 2
        self.position[0] = random.uniform(-self.flock_params['domain_radius']+margin, self.flock_params['domain_radius']-margin)
        self.position[1] = random.uniform(-self.flock_params['domain_radius']+margin, self.flock_params['domain_radius']-margin)
        self.position[2] = random.uniform(-self.flock_params['domain_radius']+margin, self.flock_params['domain_radius']-margin)

    def init_velocity(self):
        max_vel = self.flock_params['max_velocity']
        self.velocity[0] = random.uniform(-max_vel, max_vel)
        self.velocity[1] = random.uniform(-max_vel, max_vel)
        self.velocity[2] = random.uniform(-max_vel, max_vel)

    def create_boid(self):
        cmds.polySphere(r=self.flock_params['boid_scale'], name=self.boid_name)
        cmds.move(self.position[0], self.position[1], self.position[2], self.boid_name)
        cmds.setKeyframe(self.boid_name, t=0)


class Flock:
    def __init__(self, flock_params):
        self.flock_params = flock_params
        self.boids = []

        # Derived parameter values
        self.visual_range_sq = self.flock_params['visual_range'] ** 2
        self.min_distance_sq = self.flock_params['min_distance'] ** 2
        self.domain = [
            [-self.flock_params['domain_radius'], -self.flock_params['domain_radius'], -self.flock_params['domain_radius']],
            [self.flock_params['domain_radius'], self.flock_params['domain_radius'], self.flock_params['domain_radius']]
        ]

    def create(self):
        for i in range(self.flock_params['count']):
            boid = Boid(i, self.flock_params)
            self.boids.append(boid)

    def animate(self):
        for frame in range(1, self.flock_params['time_max']+1):
            print(f"Frame: {frame}")
            for boid in self.boids:
                self.apply_rules(boid)
                self.update_boid(boid, frame)

    def apply_rules(self, boid):
        self.cohesion(boid)
        self.avoidance(boid)
        self.alignment(boid)
        self.limit_speed(boid)
        self.bound_position(boid)

    def cohesion(self, boid):
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
        boid.position[0] += boid.velocity[0]
        boid.position[1] += boid.velocity[1]
        boid.position[2] += boid.velocity[2]
        cmds.move(boid.position[0], boid.position[1], boid.position[2], boid.boid_name)
        cmds.setKeyframe(boid.boid_name, t=frame)

    def dist_sq(self, boid1, boid2):
        return (
            (boid1.position[0] - boid2.position[0])**2 +
            (boid1.position[1] - boid2.position[1])**2 +
            (boid1.position[2] - boid2.position[2])**2
        )


UI()