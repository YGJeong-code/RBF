import maya.cmds as cmds
import maya.mel as mel

def makeGroup():
    cmds.group(em=True, n='rig_setup_GRP')
    cmds.hide('rig_setup_GRP')
    cmds.group(em=True, n='twistSetups_grp', p='rig_setup_GRP')
    cmds.group(em=True, n='poseMasterSetup_grp', p='rig_setup_GRP')

def twistJointLRA():
    cmds.select('upperarm_twist_01_l','upperarm_twist_02_l','lowerarm_twist_01_l','lowerarm_twist_02_l',
                'thigh_twist_01_l','thigh_twist_02_l','calf_twist_01_l','calf_twist_02_l',
                'upperarm_twist_01_r','upperarm_twist_02_r','lowerarm_twist_01_r','lowerarm_twist_02_r',
                'thigh_twist_01_r','thigh_twist_02_r','calf_twist_01_r','calf_twist_02_r',r=True)
    cmds.ToggleLocalRotationAxes()

def makeTwist(myPart, mySide):
    myGroupName = myPart+'_twist_grp'+mySide
    cmds.group(em=True, n=myGroupName, p='twistSetups_grp')

    cmds.createNode('decomposeMatrix', n=myPart+mySide+'_twist_DCM')
    cmds.connectAttr (myPart+mySide+'.parentMatrix[0]', myPart+mySide+'_twist_DCM.inputMatrix', f=True)
    # cmds.connectAttr (myPart+mySide+'.parentMatrix[0]', myPart+mySide+'_twist_DCM.inputMatrix', f=True)
    cmds.connectAttr (myPart+mySide+'_twist_DCM.outputTranslate', myGroupName+'.translate', f=True)
    cmds.connectAttr (myPart+mySide+'_twist_DCM.outputRotate', myGroupName+'.rotate', f=True)

    myIKName = myPart+'_twist'+mySide+'_IK'
    cmds.joint(n=myIKName)
    cmds.parent(myIKName, myGroupName)
    cmds.select(myIKName, myPart+mySide, r=True)
    cmds.MatchTransform()
    cmds.makeIdentity(myIKName, apply=True, t=False, r=True, s=False, n=False, pn=True)

    myList = cmds.listRelatives(myPart+mySide,c=True)
    myChild = ''
    for i in myList:
        if i.split('_')[0] != myPart:
            myChild = i

    myIKEndName = myPart+'_twist'+mySide+'_IK_end'
    cmds.select(myIKName, r=True)
    cmds.joint(n=myIKEndName)
    cmds.select(myIKEndName, myChild, r=True)
    cmds.MatchTransform()
    cmds.setAttr (myIKEndName+".rotateX", 0)
    cmds.setAttr (myIKEndName+".rotateY", 0)
    cmds.setAttr (myIKEndName+".rotateZ", 0)

    mySolver = 'ikRPsolver'
    if myPart == 'calf' or myPart == 'lowerarm':
        mySolver = 'ikSCsolver'

    myIKHandleName = myPart+'_twist'+mySide+'_IK_Handle'
    cmds.ikHandle( n=myIKHandleName, sj=myIKName, ee=myIKEndName, p=1, w=1, solver=mySolver )
    cmds.parent(myIKHandleName, myGroupName)

    cmds.setAttr( myPart+'_twist'+mySide+'_IK_Handle.poleVectorX', 0)
    cmds.setAttr( myPart+'_twist'+mySide+'_IK_Handle.poleVectorY', 0)
    cmds.setAttr( myPart+'_twist'+mySide+'_IK_Handle.poleVectorZ', 0)

    cmds.pointConstraint(myPart+mySide, myIKName)

    if myPart == 'lowerarm' or myPart == 'calf':
        cmds.parentConstraint(myChild, myIKHandleName)
    else:
        cmds.pointConstraint(myChild, myIKHandleName)

    myWeight01 = 0.8
    myWeight02 = 0.2
    myJnt = myIKName
    if myPart == 'thigh' or myPart == 'calf':
        myWeight01 = 1
        myWeight02 = 0
    if myPart == 'calf' or myPart == 'lowerarm':
        myJnt = myIKEndName

    myTwist01 = myPart+'_twist_01'+mySide
    cmds.orientConstraint(myJnt, myTwist01, w=myWeight01, mo=True)
    cmds.orientConstraint(myPart+mySide, myTwist01, w=myWeight02, mo=True)
    cmds.setAttr (myTwist01+"_orientConstraint1.interpType", 2)

    if myPart == 'thigh' or myPart == 'calf':
        myWeight01 = 0.5
        myWeight02 = 0.5
    if myPart == 'calf' or myPart == 'lowerarm':
        myJnt = myIKEndName

    myTwist02 = myPart+'_twist_02'+mySide
    cmds.orientConstraint(myJnt, myTwist02, w=myWeight02, mo=True)
    cmds.orientConstraint(myPart+mySide, myTwist02, w=myWeight01, mo=True)
    cmds.setAttr (myTwist02+"_orientConstraint1.interpType", 2)

    cmds.select(cl=True)

def makePoseMaster(myPart, mySide):
    myStand = '_pm_pm'
    myGroup = cmds.group(em=True, n=myPart+mySide+myStand+'_cmpnt', p='poseMasterSetup_grp')

    cmds.select(myGroup, myPart+mySide, r=True)
    cmds.MatchTransform()

    myParent = cmds.listRelatives(myPart+mySide, p=True)
    cmds.parentConstraint(myParent, myGroup, mo=True)

    myInput = myPart+mySide+myStand+'_input'
    cmds.group(em=True, n=myInput, p=myGroup)
    cmds.addAttr (myInput, longName="twistIsolation", attributeType='float', min=0, max=1, defaultValue=1)
    cmds.setAttr(myInput+'.twistIsolation', e=True, keyable=True)
    cmds.addAttr (myInput, longName="poseMasterFollow", attributeType='float', min=0, max=1, defaultValue=0.5)
    cmds.setAttr(myInput+'.poseMasterFollow', e=True, keyable=True)
    cmds.addAttr (myInput, longName="sourceMatrix", attributeType='matrix')
    cmds.addAttr(myInput, longName='driverRotate', numberOfChildren=3, attributeType='compound' )
    cmds.addAttr( longName='driverRotateX', attributeType='double', parent='driverRotate' )
    cmds.addAttr( longName='driverRotateY', attributeType='double', parent='driverRotate' )
    cmds.addAttr( longName='driverRotateZ', attributeType='double', parent='driverRotate' )

    myOutput = cmds.group(em=True, n=myPart+mySide+myStand+'_output', p=myGroup)
    cmds.addAttr(myOutput, longName='driverFinalRot', numberOfChildren=3, attributeType='compound' )
    cmds.addAttr( longName='driverFinalRotX', attributeType='double', parent='driverFinalRot' )
    cmds.addAttr( longName='driverFinalRotY', attributeType='double', parent='driverFinalRot' )
    cmds.addAttr( longName='driverFinalRotZ', attributeType='double', parent='driverFinalRot' )
    cmds.addAttr(myOutput, longName='twistRaw', numberOfChildren=3, attributeType='compound' )
    cmds.addAttr( longName='twistRawX', attributeType='double', parent='twistRaw' )
    cmds.addAttr( longName='twistRawY', attributeType='double', parent='twistRaw' )
    cmds.addAttr( longName='twistRawZ', attributeType='double', parent='twistRaw' )
    cmds.addAttr(myOutput, longName='twistRedistribution', numberOfChildren=3, attributeType='compound' )
    cmds.addAttr( longName='twistRedistributionX', attributeType='double', parent='twistRedistribution' )
    cmds.addAttr( longName='twistRedistributionY', attributeType='double', parent='twistRedistribution' )
    cmds.addAttr( longName='twistRedistributionZ', attributeType='double', parent='twistRedistribution' )

    ###
    myLogic = cmds.group(em=True, n=myPart+mySide+myStand+'_logic', p=myGroup)

    myPoseMasterJnt = cmds.joint(n=myPart+mySide+myStand+'_poseMasterJnt')
    myFinalRotJnt = cmds.joint(n=myPart+mySide+myStand+'_finalRotJnt')
    cmds.parent(myFinalRotJnt, myLogic)
    myFinalTwistJnt = cmds.joint(n=myPart+mySide+myStand+'_finalTwistJnt')
    cmds.setAttr(myFinalTwistJnt+'.translateX', 1)

    myFinalRotOriCon = cmds.createNode('orientConstraint', n=myPart+mySide+myStand+'_finalRot')
    cmds.parent(myFinalRotOriCon, myLogic)
    myTwistRedistributionAmountOriCon = cmds.createNode('orientConstraint', n=myPart+mySide+myStand+'_twistRedistributionAmount')
    cmds.parent(myTwistRedistributionAmountOriCon, myLogic)

    ###
    myStand = '_pm_twistreader'
    myTwistreader = cmds.group(em=True, n=myPart+mySide+myStand+'_cmpnt', p=myGroup)
    myTwistInput = cmds.group(em=True, n=myPart+mySide+myStand+'_input', p=myTwistreader)
    cmds.addAttr (myTwistInput, longName="sourceMatrix", attributeType='matrix')

    myTwistOutput = cmds.group(em=True, n=myPart+mySide+myStand+'_output', p=myTwistreader)
    cmds.addAttr(myTwistOutput, longName='aimConstraintRotate', numberOfChildren=3, attributeType='compound' )
    cmds.addAttr( longName='aimConstraintRotateX', attributeType='double', parent='aimConstraintRotate' )
    cmds.addAttr( longName='aimConstraintRotateY', attributeType='double', parent='aimConstraintRotate' )
    cmds.addAttr( longName='aimConstraintRotateZ', attributeType='double', parent='aimConstraintRotate' )
    cmds.addAttr(myTwistOutput, longName='twist', numberOfChildren=3, attributeType='compound' )
    cmds.addAttr( longName='twistX', attributeType='double', parent='twist' )
    cmds.addAttr( longName='twistY', attributeType='double', parent='twist' )
    cmds.addAttr( longName='twistZ', attributeType='double', parent='twist' )
    myTwistJnt = cmds.joint(n=myPart+mySide+myStand+'_twist')
    myAimGrp = cmds.group(em=True, n=myPart+mySide+myStand+'_aimGrp', p=myTwistreader)

    myStartLoc = myPart+mySide+myStand+'_aimStart'
    cmds.spaceLocator(n=myStartLoc)
    cmds.parent(myStartLoc, myAimGrp)
    cmds.select(myStartLoc, myAimGrp, r=True)
    cmds.MatchTransform()

    myEndLoc = myPart+mySide+myStand+'_aimEnd'
    cmds.spaceLocator(n=myEndLoc)
    cmds.parent(myEndLoc, myAimGrp)
    cmds.select(myEndLoc, myAimGrp, r=True)
    cmds.MatchTransform()
    cmds.setAttr(myEndLoc+'.translateX', 1)

    myAimStartCon = cmds.aimConstraint(myEndLoc, myStartLoc, worldUpType='None')

    cmds.parentConstraint(myTwistJnt, myEndLoc, mo=True)
    myTwistreaderOriCon = cmds.createNode('orientConstraint', n=myPart+mySide+myStand+'_oc')
    cmds.parent(myTwistreaderOriCon, myTwistreader)

    ###
    cmds.connectAttr(myPart+mySide+'.rotate', myInput+'.driverRotate')
    cmds.connectAttr(myPart+mySide+'.worldMatrix', myInput+'.sourceMatrix')
    cmds.connectAttr(myInput+'.sourceMatrix', myTwistInput+'.sourceMatrix')

    myTwistPCMult = cmds.createNode('multMatrix', n=myPart+mySide+myStand+'_twist_pc')
    cmds.connectAttr(myTwistInput+'.sourceMatrix', myTwistPCMult+'.matrixIn[0]')
    cmds.connectAttr(myTwistJnt+'.parentInverseMatrix[0]', myTwistPCMult+'.matrixIn[1]')

    myTwistPCOutput = cmds.createNode('decomposeMatrix', n=myPart+mySide+myStand+'_twist_pc_output')
    cmds.connectAttr(myTwistPCMult+'.matrixSum', myTwistPCOutput+'.inputMatrix')
    cmds.connectAttr(myTwistPCOutput+'.outputTranslate', myTwistJnt+'.translate')
    cmds.connectAttr(myTwistPCOutput+'.outputRotate', myTwistJnt+'.rotate')
    cmds.connectAttr(myTwistPCOutput+'.outputTranslate', myAimGrp+'.translate')

    myTwistWeight = cmds.createNode('pairBlend', n=myPart+mySide+myStand+'_rawTwistWeight')
    cmds.connectAttr (myInput+'.twistIsolation', myTwistWeight+'.weight', f=True)
    cmds.connectAttr(myTwistWeight+'.outRotate', myFinalRotOriCon+'.target[0].targetRotate')
    cmds.connectAttr(myTwistOutput+'.twist', myTwistWeight+'.inRotate1')

    cmds.connectAttr(myTwistOutput+'.aimConstraintRotate', myFinalRotOriCon+'.target[0].targetJointOrient')
    cmds.connectAttr(myAimStartCon[0]+'.constraintRotate', myTwistOutput+'.aimConstraintRotate')
    cmds.connectAttr(myAimStartCon[0]+'.matrix', myTwistreaderOriCon+'.target[0].targetParentMatrix')
    cmds.connectAttr(myAimStartCon[0]+'.constraintRotate', myTwistreaderOriCon+'.constraintJointOrient')
    cmds.connectAttr(myTwistJnt+'.rotate', myAimStartCon[0]+'.rotate')
    cmds.connectAttr(myTwistreaderOriCon+'.constraintRotate', myTwistOutput+'.twist')
    cmds.connectAttr(myFinalRotOriCon+'.constraintRotate', myFinalRotJnt+'.rotate')
    cmds.connectAttr (myFinalRotOriCon+'.constraintRotate', myTwistRedistributionAmountOriCon+'.constraintJointOrient')
    cmds.connectAttr (myFinalRotOriCon+'.constraintRotate', myOutput+'.driverFinalRot')
    cmds.connectAttr (myTwistOutput+'.twist', myOutput+'.twistRaw')
    cmds.connectAttr (myTwistRedistributionAmountOriCon+'.constraintRotate', myOutput+'.twistRedistribution')
    cmds.connectAttr (myTwistRedistributionAmountOriCon+'.constraintRotate', myFinalTwistJnt+'.rotate')
    cmds.connectAttr (myInput+'.driverRotate', myTwistRedistributionAmountOriCon+'.target[0].targetRotate')

    myPoseMasterWeight = cmds.createNode('pairBlend', n=myPart+mySide+myStand+'_poseMasterJnt_poseMasterWeight')
    cmds.setAttr (myPoseMasterWeight+".rotInterpolation", 1)
    cmds.connectAttr (myInput+'.poseMasterFollow', myPoseMasterWeight+'.weight', f=True)
    cmds.connectAttr (myFinalRotJnt+'.rotate', myPoseMasterWeight+'.inRotate2')
    cmds.connectAttr (myPoseMasterWeight+'.outRotate', myPoseMasterJnt+'.rotate')

    myInputpcin = cmds.createNode('multMatrix', n=myPart+mySide+myStand+'_input_pcIn')
    cmds.connectAttr (myInput+'.sourceMatrix', myInputpcin+'.matrixIn[0]')
    cmds.connectAttr (myPoseMasterJnt+'.parentInverseMatrix[0]', myInputpcin+'.matrixIn[1]')

    myInputpcout = cmds.createNode('decomposeMatrix', n=myPart+mySide+myStand+'_input_pcOut')
    cmds.connectAttr (myInputpcin+'.matrixSum', myInputpcout+'.inputMatrix')
    cmds.connectAttr (myInputpcout+'.outputTranslate', myPoseMasterJnt+'.translate')

    myInputpcin1 = cmds.createNode('multMatrix', n=myPart+mySide+myStand+'_input_pcIn1')
    cmds.connectAttr (myInput+'.sourceMatrix', myInputpcin1+'.matrixIn[0]')
    cmds.connectAttr (myFinalRotJnt+'.parentInverseMatrix[0]', myInputpcin1+'.matrixIn[1]')

    myInputpcout1 = cmds.createNode('decomposeMatrix', n=myPart+mySide+myStand+'_input_pcOut1')
    cmds.connectAttr (myInputpcin1+'.matrixSum', myInputpcout1+'.inputMatrix')
    cmds.connectAttr (myInputpcout1+'.outputTranslate', myFinalRotJnt+'.translate')

    cmds.parentConstraint(myPoseMasterJnt, myPart+'_correctiveRoot'+mySide)

def delTwist(myPart, mySide):
    mel.eval('CBdeleteConnection "%s_twist_01%s.rx";'%(myPart,mySide))
    mel.eval('CBdeleteConnection "%s_twist_01%s.ry";'%(myPart,mySide))
    mel.eval('CBdeleteConnection "%s_twist_01%s.rz";'%(myPart,mySide))

    mel.eval('CBdeleteConnection "%s_twist_02%s.rx";'%(myPart,mySide))
    mel.eval('CBdeleteConnection "%s_twist_02%s.ry";'%(myPart,mySide))
    mel.eval('CBdeleteConnection "%s_twist_02%s.rz";'%(myPart,mySide))
