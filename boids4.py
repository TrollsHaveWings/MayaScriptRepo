# boids4.py - makes a number of instances of spheres with random position and velocity
# Moves all the spheres with constant velocity for each keyframe. 
# When spheres move into the margin near the bounding box, appropriate velocity components are slowed.

import maya.cmds as cmds
import random
import math


random.seed( 1234 )
boidNumber = 20
timeMax = 500
boundingXLower = -10
boundingXUpper = 10
boundingYLower = 0
boundingYUpper = 20
boundingZLower = -10
boundingZUpper = 10
margin = 2


boidList = cmds.ls( 'boid*' )
if len( boidList ) > 0:
    cmds.delete( boidList )

result = cmds.polySphere( r=0.3, name='boid#' )

#print ( 'result: ' + str(result) )

transformName = result[0]

instanceGroupName = cmds.group( empty=True, name=transformName + '_instance_grp#' )

xArray = list()
yArray = list()
zArray = list()
dxArray = list()
dyArray = list()
dzArray = list()


for i in range ( 0, boidNumber):
    xArray.append( random.uniform( boundingXLower+margin, boundingXUpper-margin ) )
    yArray.append( random.uniform( boundingYLower+margin, boundingYUpper-margin ) )
    zArray.append( random.uniform( boundingZLower+margin, boundingZUpper-margin ) )
    dxArray.append( random.uniform( -0.5, 0.5 ) )
    dyArray.append( random.uniform( -0.5, 0.5 ) )
    dzArray.append( random.uniform( -0.5, 0.5 ) )   
     
    instanceResult = cmds.instance( transformName, name=transformName + '_instance#' )
    
    cmds.parent( instanceResult, instanceGroupName )
    
    cmds.move (xArray[i], yArray[i], zArray[i], instanceResult)
    cmds.setKeyframe(instanceResult, t=0)
    
print ( 'xArray: %s' % ( xArray ) ) 
print ( 'yArray: %s' % ( yArray ) ) 
print ( 'zArray: %s' % ( zArray ) ) 
#print ( 'dxArray: %s' % ( dxArray ) ) 
#print ( 'dyArray: %s' % ( dyArray ) ) 
#print ( 'dzArray: %s' % ( dzArray ) ) 

selectedList = cmds.ls('boid1_instance*', type='transform' )
#print( selectedList )

for time in range( 1, timeMax+1 ):
    for i in range ( 0, boidNumber):

        xArray[i] = xArray[i] + dxArray[i]
        if xArray[i] < boundingXLower + margin:
            dxArray[i] = dxArray[i] + 0.1
        elif xArray[i] > boundingXUpper - margin:
            dxArray[i] = dxArray[i] - 0.1        
        yArray[i] = yArray[i] + dyArray[i]
        if yArray[i] < boundingYLower + margin:
            dyArray[i] = dyArray[i] + 0.1
        elif yArray[i] > boundingYUpper - margin:
            dyArray[i] = dyArray[i] - 0.1 
        zArray[i] = zArray[i] + dzArray[i]
        if zArray[i] < boundingZLower + margin:
            dzArray[i] = dzArray[i] + 0.1
        elif zArray[i] > boundingZUpper - margin:
            dzArray[i] = dzArray[i] - 0.1 
        currentObject = selectedList[i]
        #print( 'Current Object: %s' % ( currentObject ) )
        cmds.move (xArray[i], yArray[i], zArray[i], currentObject)
        #print ( 'xArray: %s' % ( xArray[i] ) ) 
        #print ( 'yArray: %s' % ( yArray[i] ) ) 
        #print ( 'zArray: %s' % ( zArray[i] ) ) 
        cmds.setKeyframe(currentObject, t=time)
    
#print ( 'xArray: %s' % ( xArray ) ) 
#print ( 'yArray: %s' % ( yArray ) ) 
#print ( 'zArray: %s' % ( zArray ) ) 
#print ( 'dxArray: %s' % ( dxArray ) ) 
#print ( 'dyArray: %s' % ( dyArray ) ) 
#print ( 'dzArray: %s' % ( dzArray ) ) 
    

    
cmds.hide( transformName )

cmds.xform( instanceGroupName, centerPivots=True )