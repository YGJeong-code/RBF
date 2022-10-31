import maya.cmds as cmds
from epic_pose_wrangler.v2 import main
import RBF.module.YG_RBF_def
reload(RBF.module.YG_RBF_def)
YG_RBF_def = RBF.module.YG_RBF_def.YG_RBF_def()

def transform2RBF():
    cmds.select('thigh_in_l','RBF_thigh_l:thigh_in_l')
    cmds.MatchTransform()
    cmds.select('thigh_out_l','RBF_thigh_l:thigh_out_l')
    cmds.MatchTransform()
    cmds.select('thigh_fwd_l','RBF_thigh_l:thigh_fwd_l')
    cmds.MatchTransform()
    cmds.select('thigh_bck_l','RBF_thigh_l:thigh_bck_l')
    cmds.MatchTransform()
    cmds.select('thigh_fwd_lwr_l','RBF_thigh_l:thigh_fwd_lwr_l')
    cmds.MatchTransform()
    cmds.select('thigh_bck_lwr_l','RBF_thigh_l:thigh_bck_lwr_l')
    cmds.MatchTransform()

def run():
    YG_RBF_def.set24fps(13)

    cmds.currentTime( 4, edit=True )
    rbf_api = main.UERBFAPI(view=False)
    rbf_api.create_rbf_solver(solver_name="thigh_l_UERBFSolver", drivers=['thigh_l']) # create solver

    mySolver = rbf_api.get_rbf_solver_by_name('thigh_l_UERBFSolver') # solver
    myDriven = ['thigh_in_l','thigh_out_l','thigh_fwd_l','thigh_bck_l','thigh_fwd_lwr_l','thigh_bck_lwr_l'] # driven
    rbf_api.add_driven_transforms(driven_nodes=myDriven, solver=mySolver, edit=False) # driven transform
    rbf_api.edit_solver(edit=True, solver=mySolver) # edit solver
    transform2RBF()
    rbf_api.update_pose("default", solver=mySolver) # update pose


    cmds.currentTime( 0, edit=True )
    rbf_api.create_pose("thigh_l_bck_10", solver=mySolver) # create pose
    transform2RBF()
    rbf_api.update_pose("thigh_l_bck_10", solver=mySolver) # update pose

    cmds.currentTime( 1, edit=True )
    rbf_api.create_pose("thigh_l_fwd_10", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("thigh_l_fwd_10", solver=mySolver) # update pose

    cmds.currentTime( 2, edit=True )
    rbf_api.create_pose("thigh_l_in_45_out_90", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("thigh_l_in_45_out_90", solver=mySolver) # update pose

    cmds.currentTime( 3, edit=True )
    rbf_api.create_pose("thigh_l_out_55", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("thigh_l_out_55", solver=mySolver) # update pose

    cmds.currentTime( 5, edit=True )
    rbf_api.create_pose("thigh_l_bck_90", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("thigh_l_bck_90", solver=mySolver) # update pose

    cmds.currentTime( 6, edit=True )
    rbf_api.create_pose("thigh_l_bck_50", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("thigh_l_bck_50", solver=mySolver) # update pose

    cmds.currentTime( 7, edit=True )
    rbf_api.create_pose("thigh_l_out_110", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("thigh_l_out_110", solver=mySolver) # update pose

    cmds.currentTime( 8, edit=True )
    rbf_api.create_pose("thigh_l_out_10", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("thigh_l_out_10", solver=mySolver) # update pose

    cmds.currentTime( 9, edit=True )
    rbf_api.create_pose("thigh_l_fwd_45", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("thigh_l_fwd_45", solver=mySolver) # update pose

    cmds.currentTime( 10, edit=True )
    rbf_api.create_pose("thigh_l_in_50", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("thigh_l_in_50", solver=mySolver) # update pose

    cmds.currentTime( 11, edit=True )
    rbf_api.create_pose("thigh_l_fwd_110", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("thigh_l_fwd_110", solver=mySolver) # update pose

    cmds.currentTime( 12, edit=True )
    rbf_api.create_pose("thigh_l_fwd_90", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("thigh_l_fwd_90", solver=mySolver) # update pose

    cmds.currentTime( 13, edit=True )
    rbf_api.create_pose("thigh_l_out_85", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("thigh_l_out_85", solver=mySolver) # update pose

    cmds.currentTime( 4, edit=True )
    rbf_api.edit_solver(edit=False, solver=mySolver) # edit solver
    #rbf_api.get_solver_edit_status(solver=mySolver)

    cmds.setAttr('%s.radius'%mySolver, 48)
    cmds.setAttr('%s.distanceMethod'%mySolver, 1)
    cmds.setAttr('%s.normalizeMethod'%mySolver, 1)
    cmds.setAttr('%s.functionType'%mySolver, 0)
