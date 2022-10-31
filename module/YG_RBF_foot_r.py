import maya.cmds as cmds
from epic_pose_wrangler.v2 import main
import RBF.module.YG_RBF_def
reload(RBF.module.YG_RBF_def)
YG_RBF_def = RBF.module.YG_RBF_def.YG_RBF_def()

def transform2RBF():
    cmds.select('ankle_bck_r','RBF_foot_r:ankle_bck_r')
    cmds.MatchTransform()
    cmds.select('ankle_fwd_r','RBF_foot_r:ankle_fwd_r')
    cmds.MatchTransform()

def run():
    YG_RBF_def.set24fps(2)

    cmds.currentTime( 0, edit=True )
    rbf_api = main.UERBFAPI(view=False)
    rbf_api.create_rbf_solver(solver_name="foot_r_UERBFSolver", drivers=['foot_r']) # create solver

    mySolver = rbf_api.get_rbf_solver_by_name('foot_r_UERBFSolver') # solver
    myDriven = ['ankle_bck_r','ankle_fwd_r'] # driven
    rbf_api.add_driven_transforms(driven_nodes=myDriven, solver=mySolver, edit=False) # driven transform
    rbf_api.edit_solver(edit=True, solver=mySolver) # edit solver
    transform2RBF()
    rbf_api.update_pose("default", solver=mySolver) # update pose


    cmds.currentTime( 1, edit=True )
    rbf_api.create_pose("foot_r_down_60", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("foot_r_down_60", solver=mySolver) # update pose

    cmds.currentTime( 2, edit=True )
    rbf_api.create_pose("foot_r_up_35", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("foot_r_up_35", solver=mySolver) # update pose

    cmds.currentTime( 0, edit=True )
    rbf_api.edit_solver(edit=False, solver=mySolver) # edit solver
    #rbf_api.get_solver_edit_status(solver=mySolver)

    cmds.setAttr('%s.radius'%mySolver, 32.5)
    cmds.setAttr('%s.distanceMethod'%mySolver, 2)
    cmds.setAttr('%s.normalizeMethod'%mySolver, 1)
    cmds.setAttr('%s.functionType'%mySolver, 0)
