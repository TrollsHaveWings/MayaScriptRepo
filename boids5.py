# boids5.py - makes a number of instances of spheres with random position and velocity
# 

import maya.cmds as cmds
import random
import math


random.seed( 1234 )
boidNumber = 20
timeMax = 2
turningFactor = 0.2
centringFactor = 0.005
visualRangeSquared = 10**2
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

        #Checks to see if the current boid has gone into the margin near the bounding box.
        #If so, the appropriate velocity component is adjusted by the turningFactor.
        if xArray[i] < boundingXLower + margin:
            dxArray[i] += turningFactor
        elif xArray[i] > boundingXUpper - margin:
            dxArray[i] -= turningFactor        
        if yArray[i] < boundingYLower + margin:
            dyArray[i] += turningFactor
        elif yArray[i] > boundingYUpper - margin:
            dyArray[i] -= turningFactor 
        if zArray[i] < boundingZLower + margin:
            dzArray[i] += turningFactor
        elif zArray[i] > boundingZUpper - margin:
            dzArray[i] -= turningFactor 
        
        #Finds the centre of mass of nearby boids and adjusts the velocity of the current boid
        #to move slightly towards the centre of mass.
        centreX = 0
        centreY = 0
        centreZ = 0
        neighbourCount = 0
        
        for otherBoid in range ( 0, i):
            distanceSquared = (xArray[i]-xArray[otherBoid])**2 + (yArray[i]-yArray[otherBoid])**2 + (zArray[i]-zArray[otherBoid])**2
            if distanceSquared < visualRangeSquared:
                centreX += xArray[otherBoid]
                centreY += yArray[otherBoid]
                centreZ += zArray[otherBoid]
                neighbourCount += 1
                
        for otherBoid in range ( i+1, boidNumber):
            distanceSquared = (xArray[i]-xArray[otherBoid])**2 + (yArray[i]-yArray[otherBoid])**2 + (zArray[i]-zArray[otherBoid])**2
            if distanceSquared < visualRangeSquared:
                centreX += xArray[otherBoid]
                centreY += yArray[otherBoid]
                centreZ += zArray[otherBoid]
                neighbourCount += 1
                
        if neighbourCount:
            centreX = centreX/neighbourCount        
            centreY = centreY/neighbourCount        
            centreZ = centreZ/neighbourCount
            
            dxArray[i] += (centreX - xArray[i]) * centringFactor        
            dyArray[i] += (centreY - yArray[i]) * centringFactor        
            dzArray[i] += (centreZ - zArray[i]) * centringFactor
            
            print ( 'centre: %s %s %s neightbours: %s' % ( centreX, centreY, centreZ, neighbourCount ) ) 
        
        
                
        
        
       
            
                    
        xArray[i] += dxArray[i]
        yArray[i] += dyArray[i]
        zArray[i] += dzArray[i]


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