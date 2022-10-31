import maya.cmds as cmds
from epic_pose_wrangler.v2 import main
import RBF.module.YG_RBF_def
reload(RBF.module.YG_RBF_def)
YG_RBF_def = RBF.module.YG_RBF_def.YG_RBF_def()

def transform2RBF():
    cmds.select('clavicle_scap_r','RBF_clavicle_r:clavicle_scap_r')
    cmds.MatchTransform()
    cmds.select('clavicle_out_r','RBF_clavicle_r:clavicle_out_r')
    cmds.MatchTransform()
    cmds.select('spine_04_latissimus_r','RBF_clavicle_r:spine_04_latissimus_r')
    cmds.MatchTransform()
    cmds.select('clavicle_pec_r','RBF_clavicle_r:clavicle_pec_r')
    cmds.MatchTransform()

def run():
    YG_RBF_def.set24fps(4)

    cmds.currentTime( 0, edit=True )
    rbf_api = main.UERBFAPI(view=False)
    rbf_api.create_rbf_solver(solver_name="clavicle_r_UERBFSolver", drivers=['clavicle_r']) # create solver

    mySolver = rbf_api.get_rbf_solver_by_name('clavicle_r_UERBFSolver') # solver
    myDriven = ['clavicle_scap_r','clavicle_out_r','spine_04_latissimus_r','clavicle_pec_r'] # driven
    rbf_api.add_driven_transforms(driven_nodes=myDriven, solver=mySolver, edit=False) # driven transform
    rbf_api.edit_solver(edit=True, solver=mySolver) # edit solver
    transform2RBF()
    rbf_api.update_pose("default", solver=mySolver) # update pose

    cmds.currentTime( 1, edit=True )
    rbf_api.create_pose("clavicle_r_fwd_30", solver=mySolver) # create pose
    transform2RBF()
    rbf_api.update_pose("clavicle_r_fwd_30", solver=mySolver) # update pose

    cmds.currentTime( 2, edit=True )
    rbf_api.create_pose("clavicle_r_down_20", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("clavicle_r_down_20", solver=mySolver) # update pose

    cmds.currentTime( 3, edit=True )
    rbf_api.create_pose("clavicle_r_back_30", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("clavicle_r_back_30", solver=mySolver) # update pose

    cmds.currentTime( 4, edit=True )
    rbf_api.create_pose("clavicle_r_up_40", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("clavicle_r_up_40", solver=mySolver) # update pose

    cmds.currentTime( 0, edit=True )
    rbf_api.edit_solver(edit=False, solver=mySolver) # edit solver
    #rbf_api.get_solver_edit_status(solver=mySolver)

    cmds.setAttr('%s.radius'%mySolver, 51)
    cmds.setAttr('%s.distanceMethod'%mySolver, 2)
    cmds.setAttr('%s.normalizeMethod'%mySolver, 1)
    cmds.setAttr('%s.functionType'%mySolver, 0)
