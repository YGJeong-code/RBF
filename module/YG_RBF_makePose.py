import maya.cmds as cmds
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
        print myJnt
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

# def makeMirrorPose(myName, mySide):
#     makeLoc(myName, mySide)
#
# def makeLocDriver(myName, mySide):
#     cmds.select(cl=True)
#     myLocJnt = cmds.joint(n=myName+mySide+'_jnt')
#
#     myJnt = myName + mySide
#     myLoc = cmds.spaceLocator(n=myJnt+'_loc')
#     cmds.parent(myLoc, myLocJnt)
#
#     cmds.select(myLoc, myJnt)
#     cmds.MatchTransform()
#     cmds.setKeyframe(myLoc)
#
#     myMirror = cmds.mirrorJoint(myLocJnt, mirrorYZ=True,mirrorBehavior=True,searchReplace=('_l_', '_r_') )
#     cmds.select(myMirror)
#     myMirrorList = cmds.ls(sl=True, type='transform')
#     cmds.delete(myLocJnt)
#
#     myJnt = myName + '_r'
#     print myJnt
#     cmds.select(myJnt, myMirrorList[1])
#     cmds.MatchTransform()
#     cmds.setKeyframe(myJnt)
#
#     cmds.delete(myMirror)
#     cmds.select(cl=True)
#
# def makeMirrorDirverAni(myName, mySide, myTime, myBase):
#     for i in range(myTime+1):
#         cmds.currentTime( i, edit=True )
#         makeLocDriver(myName, mySide)
#     cmds.currentTime( myBase, edit=True )
#
#     myJnt = myName + mySide
#     # print myJnt
#     cmds.cutKey(myJnt, clear=True, time=())

def set24fps(maxFrame):
    cmds.currentUnit( time='film' )
    cmds.currentTime( 0, edit=True )
    cmds.playbackOptions( e=True, min=0, max=maxFrame, aet=maxFrame )

def makePose(FileName):
    myPartsDict = YG_RBF_poseDict.myPoseDict[FileName]
    set24fps( list( myPartsDict )[-1] )

    for frame in myPartsDict:
        cmds.currentTime( frame, edit=True )
        for axis in myPartsDict[frame]:
            cmds.setAttr( FileName + '.' + axis, myPartsDict[frame][axis] )
            cmds.setKeyframe( FileName )
