import maya.cmds as cmds
from epic_pose_wrangler.v2 import main

def transform2RBF():
    cmds.select('upperarm_fwd_r','RBF_upperarm_r:upperarm_fwd_r')
    cmds.MatchTransform()
    cmds.select('upperarm_bck_r','RBF_upperarm_r:upperarm_bck_r')
    cmds.MatchTransform()
    cmds.select('upperarm_in_r','RBF_upperarm_r:upperarm_in_r')
    cmds.MatchTransform()
    cmds.select('upperarm_out_r','RBF_upperarm_r:upperarm_out_r')
    cmds.MatchTransform()

def set24fps(maxFrame):
    cmds.currentUnit( time='film' )
    cmds.currentTime( 0, edit=True )
    cmds.playbackOptions( e=True, min=0, max=maxFrame, aet=maxFrame )

def run():
    set24fps(15)

    cmds.currentTime( 4, edit=True )
    rbf_api = main.UERBFAPI(view=False)
    rbf_api.create_rbf_solver(solver_name="upperarm_r_UERBFSolver", drivers=['upperarm_r']) # create solver

    mySolver = rbf_api.get_rbf_solver_by_name('upperarm_r_UERBFSolver') # solver
    myDriven = ['upperarm_fwd_r','upperarm_bck_r','upperarm_in_r','upperarm_out_r'] # driven
    rbf_api.add_driven_transforms(driven_nodes=myDriven, solver=mySolver, edit=False) # driven transform
    rbf_api.edit_solver(edit=True, solver=mySolver) # edit solver
    transform2RBF()
    rbf_api.update_pose("default", solver=mySolver) # update pose


    cmds.currentTime( 0, edit=True )
    rbf_api.create_pose("upperarm_r_back_45", solver=mySolver) # create pose
    transform2RBF()
    rbf_api.update_pose("upperarm_r_back_45", solver=mySolver) # update pose

    cmds.currentTime( 1, edit=True )
    rbf_api.create_pose("upperarm_r_out_55", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_out_55", solver=mySolver) # update pose

    cmds.currentTime( 2, edit=True )
    rbf_api.create_pose("upperarm_r_out110_twist_in_70", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_out110_twist_in_70", solver=mySolver) # update pose

    cmds.currentTime( 3, edit=True )
    rbf_api.create_pose("lowerarm_r_in_35", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_r_in_35", solver=mySolver) # update pose

    cmds.currentTime( 5, edit=True )
    rbf_api.create_pose("upperarm_r_out_85", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_out_85", solver=mySolver) # update pose

    cmds.currentTime( 6, edit=True )
    rbf_api.create_pose("upperarm_r_fwd_110", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_fwd_110", solver=mySolver) # update pose

    cmds.currentTime( 7, edit=True )
    rbf_api.create_pose("upperarm_r_in_10", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_in_10", solver=mySolver) # update pose

    cmds.currentTime( 8, edit=True )
    rbf_api.create_pose("upperarm_r_out110_twist_out_70", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_out110_twist_out_70", solver=mySolver) # update pose

    cmds.currentTime( 9, edit=True )
    rbf_api.create_pose("upperarm_r_out_twist_a", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_out_twist_a", solver=mySolver) # update pose

    cmds.currentTime( 10, edit=True )
    rbf_api.create_pose("upperarm_r_fwd_15", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_fwd_15", solver=mySolver) # update pose

    cmds.currentTime( 11, edit=True )
    rbf_api.create_pose("upperarm_r_out_15", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_out_15", solver=mySolver) # update pose

    cmds.currentTime( 12, edit=True )
    rbf_api.create_pose("upperarm_r_back_10", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_back_10", solver=mySolver) # update pose

    cmds.currentTime( 13, edit=True )
    rbf_api.create_pose("upperarm_r_out110", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_out110", solver=mySolver) # update pose

    cmds.currentTime( 14, edit=True )
    rbf_api.create_pose("upperarm_r_fwd_twist_in_a", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_fwd_twist_in_a", solver=mySolver) # update pose

    cmds.currentTime( 15, edit=True )
    rbf_api.create_pose("upperarm_r_fwd_90", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("upperarm_r_fwd_90", solver=mySolver) # update pose

    cmds.currentTime( 4, edit=True )
    rbf_api.edit_solver(edit=False, solver=mySolver) # edit solver
    #rbf_api.get_solver_edit_status(solver=mySolver)

    cmds.setAttr('%s.radius'%mySolver, 74)
    cmds.setAttr('%s.distanceMethod'%mySolver, 1)
    cmds.setAttr('%s.normalizeMethod'%mySolver, 1)
    cmds.setAttr('%s.functionType'%mySolver, 0)
