import maya.cmds as cmds
from imp import reload
import RBF.module.YG_RBF_poseDict as YG_RBF_poseDict
reload(YG_RBF_poseDict)

def makeLoc(myName, mySide):
    cmds.select(cl=True)
    myTarget = YG_RBF_poseDict.myList[myName]
    myLocJnt = cmds.joint(n=myName+mySide+'_jnt')
    myJntList = []
    for i in myTarget:
        myJnt = i + mySide
        myJntList.append(myJnt)
        myLoc = cmds.spaceLocator(n=myJnt+'_loc')
        cmds.parent(myLoc, myLocJnt)

    for i in myJntList:
        myLoc = i + '_loc'
        cmds.select(myLoc, i)
        cmds.MatchTransform()
        cmds.setKeyframe(myLoc)

    myMirror = cmds.mirrorJoint(myLocJnt, mirrorYZ=True,mirrorBehavior=True,searchReplace=('_l_', '_r_') )
    cmds.select(myMirror)
    myMirrorList = cmds.ls(sl=True, type='transform')
    cmds.delete(myLocJnt)

    for i in range(1,len(myMirrorList)):
        myJnt = myMirrorList[i].replace('l_loc1', "r")
        print (myJnt)
        cmds.select(myJnt, myMirrorList[i])
        cmds.MatchTransform()
        cmds.setKeyframe(myJnt)

    cmds.delete(myMirror)
    cmds.select(cl=True)

def makeMirror(myName, mySide, myTime, myBase):
    for i in range(myTime+1):
        cmds.currentTime( i, edit=True )
        makeLoc(myName, mySide)
    cmds.currentTime( myBase, edit=True )

    myTarget = YG_RBF_poseDict.myList[myName]
    for i in myTarget:
        myJnt = i + mySide
        # print myJnt
        cmds.cutKey(myJnt, clear=True, time=())

def set24fps(maxFrame):
    cmds.currentUnit( time='film' )
    cmds.currentTime( 0, edit=True )
    cmds.playbackOptions( e=True, min=0, max=maxFrame, aet=maxFrame )

def makePose(PartsName):
    myPartsDict = YG_RBF_poseDict.myPoseDict[PartsName]
    myCorrectiveDict = YG_RBF_poseDict.myCorrectiveDict[PartsName]
    set24fps( list( myPartsDict )[-1] )

    for frame in myPartsDict:
        cmds.currentTime( frame, edit=True )
        for partsAxis in myPartsDict[frame]:
            cmds.setAttr( PartsName + '.' + partsAxis, myPartsDict[frame][partsAxis] )
            cmds.setKeyframe( PartsName )
        for correctiveJoint in myCorrectiveDict:
            # print('corrective Joint : %s' % correctiveJoint)
            axisList = myCorrectiveDict[correctiveJoint][frame]
            for axis in axisList:
                # print('%s -> %s' % (axis, axisList[axis]))
                cmds.setAttr( correctiveJoint + '.' + axis, axisList[axis] )
                cmds.setKeyframe( correctiveJoint )
