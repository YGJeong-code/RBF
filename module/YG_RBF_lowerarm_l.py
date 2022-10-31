import maya.cmds as cmds
from epic_pose_wrangler.v2 import main
import RBF.module.YG_RBF_def
reload(RBF.module.YG_RBF_def)
YG_RBF_def = RBF.module.YG_RBF_def.YG_RBF_def()

def transform2RBF():
    cmds.select('lowerarm_out_l','RBF_lowerarm_l:lowerarm_out_l')
    cmds.MatchTransform()
    cmds.select('lowerarm_in_l','RBF_lowerarm_l:lowerarm_in_l')
    cmds.MatchTransform()
    cmds.select('lowerarm_fwd_l','RBF_lowerarm_l:lowerarm_fwd_l')
    cmds.MatchTransform()
    cmds.select('lowerarm_bck_l','RBF_lowerarm_l:lowerarm_bck_l')
    cmds.MatchTransform()
    cmds.select('upperarm_bicep_l','RBF_lowerarm_l:upperarm_bicep_l')
    cmds.MatchTransform()
    cmds.select('upperarm_tricep_l','RBF_lowerarm_l:upperarm_tricep_l')
    cmds.MatchTransform()

def run():
    YG_RBF_def.set24fps(8)

    cmds.currentTime( 2, edit=True )
    rbf_api = main.UERBFAPI(view=False)
    rbf_api.create_rbf_solver(solver_name="lowerarm_l_UERBFSolver", drivers=['lowerarm_l']) # create solver

    mySolver = rbf_api.get_rbf_solver_by_name('lowerarm_l_UERBFSolver') # solver
    myDriven = ['lowerarm_out_l','lowerarm_in_l','lowerarm_fwd_l','lowerarm_bck_l','upperarm_bicep_l','upperarm_tricep_l'] # driven
    rbf_api.add_driven_transforms(driven_nodes=myDriven, solver=mySolver, edit=False) # driven transform
    rbf_api.edit_solver(edit=True, solver=mySolver) # edit solver
    transform2RBF()
    rbf_api.update_pose("default", solver=mySolver) # update pose


    cmds.currentTime( 0, edit=True )
    rbf_api.create_pose("lowerarm_l_in_110", solver=mySolver) # create pose
    transform2RBF()
    rbf_api.update_pose("lowerarm_l_in_110", solver=mySolver) # update pose

    cmds.currentTime( 1, edit=True )
    rbf_api.create_pose("lowerarm_l_in_35", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_l_in_35", solver=mySolver) # update pose

    cmds.currentTime( 3, edit=True )
    rbf_api.create_pose("lowerarm_l_out_35", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_l_out_35", solver=mySolver) # update pose

    cmds.currentTime( 4, edit=True )
    rbf_api.create_pose("lowerarm_l_in_50", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_l_in_50", solver=mySolver) # update pose

    cmds.currentTime( 5, edit=True )
    rbf_api.create_pose("lowerarm_l_in_75", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_l_in_75", solver=mySolver) # update pose

    cmds.currentTime( 6, edit=True )
    rbf_api.create_pose("lowerarm_l_out_10", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_l_out_10", solver=mySolver) # update pose

    cmds.currentTime( 7, edit=True )
    rbf_api.create_pose("lowerarm_l_in_90", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_l_in_90", solver=mySolver) # update pose

    cmds.currentTime( 8, edit=True )
    rbf_api.create_pose("lowerarm_l_in_10", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("lowerarm_l_in_10", solver=mySolver) # update pose

    cmds.currentTime( 2, edit=True )
    rbf_api.edit_solver(edit=False, solver=mySolver) # edit solver
    #rbf_api.get_solver_edit_status(solver=mySolver)

    cmds.setAttr('%s.radius'%mySolver, 58)
    cmds.setAttr('%s.distanceMethod'%mySolver, 2)
    cmds.setAttr('%s.normalizeMethod'%mySolver, 1)
    cmds.setAttr('%s.functionType'%mySolver, 0)
