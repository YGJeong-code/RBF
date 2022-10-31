import maya.cmds as cmds
from epic_pose_wrangler.v2 import main
import RBF.module.YG_RBF_def
reload(RBF.module.YG_RBF_def)
YG_RBF_def = RBF.module.YG_RBF_def.YG_RBF_def()

def transform2RBF():
    cmds.select('lowerarm_out_r','RBF_lowerarm_r:lowerarm_out_r')
    cmds.MatchTransform()
    cmds.select('lowerarm_in_r','RBF_lowerarm_r:lowerarm_in_r')
    cmds.MatchTransform()
    cmds.select('lowerarm_fwd_r','RBF_lowerarm_r:lowerarm_fwd_r')
    cmds.MatchTransform()
    cmds.select('lowerarm_bck_r','RBF_lowerarm_r:lowerarm_bck_r')
    cmds.MatchTransform()
    cmds.select('upperarm_bicep_r','RBF_lowerarm_r:upperarm_bicep_r')
    cmds.MatchTransform()
    cmds.select('upperarm_tricep_r','RBF_lowerarm_r:upperarm_tricep_r')
    cmds.MatchTransform()

def run():
    YG_RBF_def.set24fps(8)

    cmds.currentTime( 2, edit=True )
    rbf_api = main.UERBFAPI(view=False)
    rbf_api.create_rbf_solver(solver_name="lowerarm_r_UERBFSolver", drivers=['lowerarm_r']) # create solver

    mySolver = rbf_api.get_rbf_solver_by_name('lowerarm_r_UERBFSolver') # solver
    myDriven = ['lowerarm_out_r','lowerarm_in_r','lowerarm_fwd_r','lowerarm_bck_r','upperarm_bicep_r','upperarm_tricep_r'] # driven
    rbf_api.add_driven_transforms(driven_nodes=myDriven, solver=mySolver, edit=False) # driven transform
    rbf_api.edit_solver(edit=True, solver=mySolver) # edit solver
    transform2RBF()
    rbf_api.update_pose("default", solver=mySolver) # update pose


    cmds.currentTime( 0, edit=True )
    rbf_api.create_pose("lowerarm_r_in_110", solver=mySolver) # create pose
    transform2RBF()
    rbf_api.update_pose("lowerarm_r_in_110", solver=mySolver) # update pose

    cmds.currentTime( 1, edit=True )
    rbf_api.create_pose("lowerarm_r_in_35", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_r_in_35", solver=mySolver) # update pose

    cmds.currentTime( 3, edit=True )
    rbf_api.create_pose("lowerarm_r_out_35", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_r_out_35", solver=mySolver) # update pose

    cmds.currentTime( 4, edit=True )
    rbf_api.create_pose("lowerarm_r_in_50", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_r_in_50", solver=mySolver) # update pose

    cmds.currentTime( 5, edit=True )
    rbf_api.create_pose("lowerarm_r_in_75", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_r_in_75", solver=mySolver) # update pose

    cmds.currentTime( 6, edit=True )
    rbf_api.create_pose("lowerarm_r_out_10", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_r_out_10", solver=mySolver) # update pose

    cmds.currentTime( 7, edit=True )
    rbf_api.create_pose("lowerarm_r_in_90", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_r_in_90", solver=mySolver) # update pose

    cmds.currentTime( 8, edit=True )
    rbf_api.create_pose("lowerarm_r_in_10", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_r_in_10", solver=mySolver) # update pose

    cmds.currentTime( 2, edit=True )
    rbf_api.edit_solver(edit=False, solver=mySolver) # edit solver
    #rbf_api.get_solver_edit_status(solver=mySolver)

    cmds.setAttr('%s.radius'%mySolver, 58)
    cmds.setAttr('%s.distanceMethod'%mySolver, 2)
    cmds.setAttr('%s.normalizeMethod'%mySolver, 1)
    cmds.setAttr('%s.functionType'%mySolver, 0)
