# boids2.py - makes a number of instances of spheres with random position and velocity
# Moves all the spheres and takes 2 keyframes.

import maya.cmds as cmds
import random
import math


random.seed( 1234 )

boidList = cmds.ls( 'boid*' )
if len( boidList ) > 0:
    cmds.delete( boidList )

result = cmds.polySphere( r=0.3, name='boid#' )

#print ( 'result: ' + str(result) )

transformName = result[0]

instanceGroupName = cmds.group( empty=True, name=transformName + '_instance_grp#' )

boidNumber = 20
xArray = list()
yArray = list()
zArray = list()
dxArray = list()
dyArray = list()
dzArray = list()


for i in range ( 0, boidNumber):
    xArray.append( random.uniform( -10, 10 ) )
    yArray.append( random.uniform( 0, 20 ) )
    zArray.append( random.uniform( -10, 10 ) )
    dxArray.append( random.uniform( -0.5, 0.5 ) )
    dyArray.append( random.uniform( -0.5, 0.5 ) )
    dzArray.append( random.uniform( -0.5, 0.5 ) )   
     
    instanceResult = cmds.instance( transformName, name=transformName + '_instance#' )
    
    cmds.parent( instanceResult, instanceGroupName )
    
    print ( 'instanceResult: %s' % ( instanceResult ) )
    
    #x = random.uniform( -10, 10 )
    #y = random.uniform( 0, 20 )
    #z = random.uniform( -10, 10 )
    
    cmds.move (xArray[i], yArray[i], zArray[i], instanceResult)
    cmds.setKeyframe(instanceResult, t=0)
    
print ( 'xArray: %s' % ( xArray ) ) 
print ( 'yArray: %s' % ( yArray ) ) 
print ( 'zArray: %s' % ( zArray ) ) 
print ( 'dxArray: %s' % ( dxArray ) ) 
print ( 'dyArray: %s' % ( dyArray ) ) 
print ( 'dzArray: %s' % ( dzArray ) ) 

selectedList = cmds.ls('boid1_instance*', type='transform' )
print( selectedList )

for i in range ( 0, boidNumber):

    xArray[i] = xArray[i] + dxArray[i]
    yArray[i] = yArray[i] + dyArray[i]
    zArray[i] = zArray[i] + dzArray[i]
    currentObject = selectedList[i]
    print( 'Current Object: %s' % ( currentObject ) )
    cmds.move (xArray[i], yArray[i], zArray[i], currentObject)
    print ( 'xArray: %s' % ( xArray[i] ) ) 
    print ( 'yArray: %s' % ( yArray[i] ) ) 
    print ( 'zArray: %s' % ( zArray[i] ) ) 
    cmds.setKeyframe(currentObject, t=1)
    
print ( 'xArray: %s' % ( xArray ) ) 
print ( 'yArray: %s' % ( yArray ) ) 
print ( 'zArray: %s' % ( zArray ) ) 
#print ( 'dxArray: %s' % ( dxArray ) ) 
#print ( 'dyArray: %s' % ( dyArray ) ) 
#print ( 'dzArray: %s' % ( dzArray ) ) 
    

    
cmds.hide( transformName )

cmds.xform( instanceGroupName, centerPivots=True )