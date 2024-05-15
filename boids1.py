# boids1.py

import maya.cmds as cmds
import random

random.seed( 1234 )

boidList = cmds.ls( 'boid*' )
if len( boidList ) > 0:
    cmds.delete( boidList )

result = cmds.polyCone( r=0.3, h=1, name='boid#' )

#print ( 'result: ' + str(result) )

transformName = result[0]

instanceGroupName = cmds.group( empty=True, name=transformName + '_instance_grp#' )

for i in range ( 0, 100):
    
    instanceResult = cmds.instance( transformName, name=transformName + '_instance#' )
    
    cmds.parent( instanceResult, instanceGroupName )
    
    #print ( 'instanceResult: ' + str(instanceResult) )
    
    x = random.uniform( -10, 10 )
    y = random.uniform( 0, 20 )
    z = random.uniform( -10, 10 )
    
    cmds.move (x, y, z, instanceResult)

    xRot = random.uniform( 0, 360 )
    #yRot = random.uniform( 0, 360 )
    zRot = random.uniform( 0, 360 )
    
    cmds.rotate (xRot, 0, zRot, instanceResult)

    
cmds.hide( transformName )

cmds.xform( instanceGroupName, centerPivots=True )