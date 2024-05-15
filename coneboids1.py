# coneboids1.py

import maya.cmds as cmds
import random
import math
import maya.api.OpenMaya as om2

random.seed( 1234 )
boidNumber = 100
timeMax = 500
turningFactor = 0.2
centringFactor = 0.05
avoidFactor = 0.3
matchingFactor = 0.02
visualRangeSquared = 7**2
minBetweenBoidDistanceSquared = 1**2
boundingBox = [[-10, 0, -10],[10, 20, 10]]
maxInitialVelocityComponent = 1
maxSpeedLimit = 2
margin = 2
positionArray = []
velocityArray = []


#Creates initial boid population
def initialise():
    #Deletes any pre-existing boids
    boidList = cmds.ls( 'boid*' )
    if len( boidList ) > 0:
        cmds.delete( boidList )
    #Creates initial boid as a sphere
    result = cmds.polyCone( sa=20, sh=15, sc=10, r=0.25, h=1, rcp=1, name='boid#' )
    transformName = result[0]
    instanceGroupName = cmds.group( empty=True, name=transformName + '_instance_grp#' )
    #Makes instances of the initial boid with random positions inside the bounding box
    #and random velocities within a pre-defined range. Moves each boid to its chosen position
    #and set a keyframe.
    for boid in range ( 0, boidNumber):
        instanceResult = cmds.instance( transformName, name=transformName + '_instance#' )
        cmds.parent( instanceResult, instanceGroupName )
        positionArray.append( [ random.uniform( boundingBox[0][0]+margin, boundingBox[1][0]-margin ),
        random.uniform( boundingBox[0][1]+margin, boundingBox[1][1]-margin ),
        random.uniform( boundingBox[0][2]+margin, boundingBox[1][2]-margin ) ] )
        velocityArray.append( [ random.uniform( -maxInitialVelocityComponent, maxInitialVelocityComponent ),
        random.uniform( -maxInitialVelocityComponent, maxInitialVelocityComponent ),
        random.uniform( -maxInitialVelocityComponent, maxInitialVelocityComponent ) ] )
        cmds.move (positionArray[boid][0], positionArray[boid][1], positionArray[boid][2], instanceResult)
        cmds.setKeyframe(instanceResult, t=0)
    cmds.hide( transformName )
    cmds.xform( instanceGroupName, centerPivots=True )


#Uses 3D Pythagoras to calculate distance squared between two boids
def distSq(boid, otherBoid):
    distanceSquared = (positionArray[boid][0]-positionArray[otherBoid][0])**2 + (positionArray[boid][1]-positionArray[otherBoid][1])**2 + (positionArray[boid][2]-positionArray[otherBoid][2])**2
    return distanceSquared

#Finds the centre of mass of nearby boids (within a specified visual range).
#Adjusts the velocity of the current boid to move it in the direction of this centre of mass.
#A scaling factor known as centringFactor is applied to this adjustment.
def coherence(boid):
    centreX = 0
    centreY = 0
    centreZ = 0
    neighbourCount = 0
    for otherBoid in range ( 0, boidNumber):
        if otherBoid != boid:
            if distSq(boid, otherBoid) < visualRangeSquared:
                centreX += positionArray[otherBoid][0]
                centreY += positionArray[otherBoid][1]
                centreZ += positionArray[otherBoid][2]
                neighbourCount += 1
    if neighbourCount:
        centreX = centreX/neighbourCount
        centreY = centreY/neighbourCount
        centreZ = centreZ/neighbourCount
        velocityArray[boid][0] += (centreX - positionArray[boid][0]) * centringFactor
        velocityArray[boid][1] += (centreY - positionArray[boid][1]) * centringFactor
        velocityArray[boid][2] += (centreZ - positionArray[boid][2]) * centringFactor

#Finds the very nearby boids then adjusts the velocity components to try to move away from the nearby boids.
#A scaling factor known as avoidFactor is applied to this adjustment.
def avoidOtherBoids(boid):
    moveX = 0
    moveY = 0
    moveZ = 0
    for otherBoid in range ( 0, boidNumber):
        if otherBoid != boid:
            if distSq(boid, otherBoid) < minBetweenBoidDistanceSquared:
                moveX += positionArray[boid][0] - positionArray[otherBoid][0]
                moveY += positionArray[boid][1] - positionArray[otherBoid][1]
                moveZ += positionArray[boid][2] - positionArray[otherBoid][2]
    velocityArray[boid][0] += moveX * avoidFactor
    velocityArray[boid][1] += moveY * avoidFactor
    velocityArray[boid][2] += moveZ * avoidFactor

#Calculates the average velocity of the boids within the visual range and adjusts current boid velocity
#to move towards that value.
#A scaling factor known as matchFactor is applied to this adjustment.
def velocityMatching(boid):
    averagedX = 0
    averagedY = 0
    averagedZ = 0
    neighbourCount = 0
    for otherBoid in range ( 0, boidNumber):
        if otherBoid != boid:
            if distSq(boid, otherBoid) < visualRangeSquared:
                averagedX += velocityArray[otherBoid][0]
                averagedY += velocityArray[otherBoid][1]
                averagedZ += velocityArray[otherBoid][2]
                neighbourCount += 1
    if neighbourCount:
        averagedX = averagedX/neighbourCount
        averagedY = averagedY/neighbourCount
        averagedZ = averagedZ/neighbourCount
        velocityArray[boid][0] += (averagedX - velocityArray[boid][0]) * matchingFactor
        velocityArray[boid][1] += (averagedY - velocityArray[boid][1]) * matchingFactor
        velocityArray[boid][2] += (averagedZ - velocityArray[boid][2]) * matchingFactor

#Applies a maximum overall velocity to each boid.
def speedLimit(boid):
    boidSpeed = math.sqrt(velocityArray[boid][0]**2 + velocityArray[boid][1]**2 + velocityArray[boid][2]**2)
    if (boidSpeed > maxSpeedLimit):
        velocityArray[boid][0] = (velocityArray[boid][0]/boidSpeed)*maxSpeedLimit
        velocityArray[boid][1] = (velocityArray[boid][1]/boidSpeed)*maxSpeedLimit
        velocityArray[boid][2] = (velocityArray[boid][2]/boidSpeed)*maxSpeedLimit

#Checks to see if any boid has strayed into the margin region of the bounding box.
#If it has, the particular velocity component of that boid is adjusted to return it to the bounding box.
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

#Updates the position matrix of the boid and moves the object then set a keyframe.
def updateBoidPosition(boid):
    positionArray[boid][0] += velocityArray[boid][0]
    positionArray[boid][1] += velocityArray[boid][1]
    positionArray[boid][2] += velocityArray[boid][2]
    currentObject = selectedList[boid]
    cmds.move (positionArray[boid][0], positionArray[boid][1], positionArray[boid][2], currentObject)
    #This is the start of the rotation calculation - it needs maya.api.OpenMaya import
    Initial_Rotation_Vector=om2.MVector([0,1,0])
    Final_Rotation_Vector=om2.MVector([velocityArray[boid][0],velocityArray[boid][1],velocityArray[boid][2]])
    cross=Initial_Rotation_Vector^Final_Rotation_Vector
    crossLength = om2.MVector.length(cross)
    dot=Initial_Rotation_Vector*Final_Rotation_Vector
    # Create a z matrix
    row1 = [0,-cross[2],cross[1],0]
    row2 = [cross[2],0,-cross[0],0]
    row3 = [-cross[1],cross[0],0,0]
    row4 = [0, 0, 0, 0]
    matList = [row1,row2,row3,row4]
    z = om2.MMatrix(matList)

    Identity4 = om2.MMatrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    rotationMatrix = (Identity4 + z + z*z *(1-d)*(1/crossLength**2))
    m_matrixTr = om2.MTransformationMatrix(rotationMatrix)
    m_eulerRot = m_matrixTr.rotation()
    #This is the end of the rotation calculation
    cmds.rotate (0, 0, 0, currentObject)
    cmds.rotate (math.degrees(-m_eulerRot.x), math.degrees(-m_eulerRot.y), math.degrees(-m_eulerRot.z), currentObject)
    cmds.setKeyframe(currentObject, t=time)

#Main loop
initialise()
selectedList = cmds.ls('boid1_instance*', type='transform' )

for time in range( 1, timeMax+1 ):
    print ( 'Time: %s' % ( time ) )
    for boid in range ( 0, boidNumber):
        coherence(boid)
        avoidOtherBoids(boid)
        velocityMatching(boid)
        speedLimit(boid)
        stayInBoundingBox(boid)
        updateBoidPosition(boid)



