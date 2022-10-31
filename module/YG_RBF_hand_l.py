import maya.cmds as cmds
from epic_pose_wrangler.v2 import main

def transform2RBF():
    cmds.select('wrist_outer_l','RBF_hand_l:wrist_outer_l')
    cmds.MatchTransform()
    cmds.select('wrist_inner_l','RBF_hand_l:wrist_inner_l')
    cmds.MatchTransform()

def set24fps(maxFrame):
    cmds.currentUnit( time='film' )
    cmds.currentTime( 0, edit=True )
    cmds.playbackOptions( e=True, min=0, max=maxFrame, aet=maxFrame )

def run():
    set24fps(3)

    cmds.currentTime( 0, edit=True )
    rbf_api = main.UERBFAPI(view=False)
    rbf_api.create_rbf_solver(solver_name="hand_l_UERBFSolver", drivers=['hand_l']) # create solver

    mySolver = rbf_api.get_rbf_solver_by_name('hand_l_UERBFSolver') # solver
    myDriven = ['wrist_outer_l','wrist_inner_l'] # driven
    rbf_api.add_driven_transforms(driven_nodes=myDriven, solver=mySolver, edit=False) # driven transform
    rbf_api.edit_solver(edit=True, solver=mySolver) # edit solver
    transform2RBF()
    rbf_api.update_pose("default", solver=mySolver) # update pose


    cmds.currentTime( 1, edit=True )
    rbf_api.create_pose("hand_l_down_90", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("hand_l_down_90", solver=mySolver) # update pose

    cmds.currentTime( 2, edit=True )
    rbf_api.create_pose("hand_l_up_20", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("hand_l_up_20", solver=mySolver) # update pose

    cmds.currentTime( 3, edit=True )
    rbf_api.create_pose("hand_l_up_90", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("hand_l_up_90", solver=mySolver) # update pose

    cmds.currentTime( 0, edit=True )
    rbf_api.edit_solver(edit=False, solver=mySolver) # edit solver
    #rbf_api.get_solver_edit_status(solver=mySolver)

    cmds.setAttr('%s.radius'%mySolver, 93)
    cmds.setAttr('%s.distanceMethod'%mySolver, 2)
    cmds.setAttr('%s.normalizeMethod'%mySolver, 1)
    cmds.setAttr('%s.functionType'%mySolver, 0)
