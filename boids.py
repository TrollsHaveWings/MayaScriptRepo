import maya.cmds as cmds
import random
import math

master_boid_name = "boid"
boid_size = 10
boid_count = 100
boid_spawn_radius = 1000
velocity = 200  # velocity along Y-axis

main_group_name = "FLOCK_group"

# If the main group exists, delete it
if cmds.objExists(main_group_name):
    cmds.delete(main_group_name)

# Create the main group
cmds.group(empty=True, name=main_group_name)

# Create boids
for i in range(0, boid_count):
    xSpawn = random.uniform(-1 * boid_spawn_radius, boid_spawn_radius)
    ySpawn = random.uniform(-1 * boid_spawn_radius, boid_spawn_radius)
    zSpawn = random.uniform(-1 * boid_spawn_radius, boid_spawn_radius)

    boid_name = master_boid_name + str(i)  # Create a unique name for each boid

    # Use cone GEO to represent boid
    cmds.polyCone(name = boid_name, radius = 1*boid_size, height = 2*boid_size)
    cmds.xform(boid_name, t=[0, 0, 0], ws=True)  # Reset the boid's position

    # Create a group for the boid and move/rotate the group
    ctrl_group_name = "CTRL_" + boid_name
    cmds.group(boid_name, name=ctrl_group_name)
    cmds.xform(ctrl_group_name, t=[xSpawn, ySpawn, zSpawn], ws=True)
    cmds.xform(ctrl_group_name, ro=[xSpawn, ySpawn, zSpawn], os=True)

    # Parent the CTRL_ group to the main group
    cmds.parent(ctrl_group_name, main_group_name)

    # Create an expression to animate the boid
    expression = f"""
        {boid_name}.translateY = {velocity} * time;
    """
    cmds.expression(s=expression)
