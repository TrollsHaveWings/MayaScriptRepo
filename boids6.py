# boids6.py

import maya.cmds as cmds
import random
import math
from array import *

random.seed( 1234 )
boidNumber = 20
timeMax = 200
turningFactor = 0.2
centringFactor = 0.1
visualRangeSquared = 5**2
boundingBox = [[-10, 0, -10],[10, 20, 10]]
maxInitialVelocity = 0.5
margin = 2
positionArray = []
velocityArray = []

def initialise():
    #Deletes any pre-existing boids
    boidList = cmds.ls( 'boid*' )
    if len( boidList ) > 0:
        cmds.delete( boidList )
    result = cmds.polySphere( r=0.3, name='boid#' )
    transformName = result[0]
    instanceGroupName = cmds.group( empty=True, name=transformName + '_instance_grp#' )   
    for i in range ( 0, boidNumber):
        instanceResult = cmds.instance( transformName, name=transformName + '_instance#' )
        cmds.parent( instanceResult, instanceGroupName )
        positionArray.append( [ random.uniform( boundingBox[0][0]+margin, boundingBox[1][0]-margin ), 
        random.uniform( boundingBox[0][1]+margin, boundingBox[1][1]-margin ), 
        random.uniform( boundingBox[0][2]+margin, boundingBox[1][2]-margin ) ] )  
        velocityArray.append( [ random.uniform( -maxInitialVelocity, maxInitialVelocity ), 
        random.uniform( -maxInitialVelocity, maxInitialVelocity ), 
        random.uniform( -maxInitialVelocity, maxInitialVelocity ) ] )  
        cmds.move (positionArray[i][0], positionArray[i][1], positionArray[i][2], instanceResult)
        cmds.setKeyframe(instanceResult, t=0)    
        print('Position: %s %s %s ' % (positionArray[i][0],positionArray[i][1],positionArray[i][2]) )
        print('Velcoity: %s %s %s ' % (velocityArray[i][0],velocityArray[i][1],velocityArray[i][2]) )
    cmds.hide( transformName )
    cmds.xform( instanceGroupName, centerPivots=True )
    
def stayInBoundingBox(boid):
        if positionArray[boid][0] < boundingBox[0][0] + margin:
            velocityArray[boid][0] += turningFactor
        elif positionArray[boid][0] > boundingBox[1][0] - margin:
            velocityArray[boid][0] -= turningFactor        
        if positionArray[boid][1] < boundingBox[0][1] + margin:
            velocityArray[boid][1] += turningFactor
        elif positionArray[boid][1] > boundingBox[1][1] - margin:
            velocityArray[boid][1] -= turningFactor 
        if positionArray[boid][2] < boundingBox[0][2] + margin:
            velocityArray[boid][2] += turningFactor
        elif positionArray[boid][2] > boundingBox[1][2] - margin:
            velocityArray[boid][2] -= turningFactor

def updateBoidPosition(boid):
        positionArray[boid][0] += velocityArray[boid][0]
        positionArray[boid][1] += velocityArray[boid][1]
        positionArray[boid][2] += velocityArray[boid][2]
        currentObject = selectedList[boid]
        cmds.move (positionArray[boid][0], positionArray[boid][1], positionArray[boid][2], currentObject)
        cmds.setKeyframe(currentObject, t=time)



    
#Main loop  
initialise()
selectedList = cmds.ls('boid1_instance*', type='transform' )

for time in range( 1, timeMax+1 ):
    for boid in range ( 0, boidNumber):
        stayInBoundingBox(boid)
        updateBoidPosition(boid)

   

