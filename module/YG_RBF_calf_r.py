import maya.cmds as cmds
from epic_pose_wrangler.v2 import main

def transform2RBF():
    cmds.select('calf_knee_r','RBF_calf_r:calf_knee_r')
    cmds.MatchTransform()
    cmds.select('calf_kneeBack_r','RBF_calf_r:calf_kneeBack_r')
    cmds.MatchTransform()
    cmds.select('calf_twistCor_02_r','RBF_calf_r:calf_twistCor_02_r')
    cmds.MatchTransform()
    cmds.select('thigh_twistCor_01_r','RBF_calf_r:thigh_twistCor_01_r')
    cmds.MatchTransform()
    cmds.select('thigh_twistCor_02_r','RBF_calf_r:thigh_twistCor_02_r')
    cmds.MatchTransform()

def set24fps(maxFrame):
    cmds.currentUnit( time='film' )
    cmds.currentTime( 0, edit=True )
    cmds.playbackOptions( e=True, min=0, max=maxFrame, aet=maxFrame )

def run():
    set24fps(4)

    cmds.currentTime( 0, edit=True )
    rbf_api = main.UERBFAPI(view=False)
    rbf_api.create_rbf_solver(solver_name="calf_r_UERBFSolver", drivers=['calf_r']) # create solver

    mySolver = rbf_api.get_rbf_solver_by_name('calf_r_UERBFSolver') # solver
    myDriven = ['calf_knee_r','calf_kneeBack_r','calf_twistCor_02_r','thigh_twistCor_01_r','thigh_twistCor_02_r'] # driven
    rbf_api.add_driven_transforms(driven_nodes=myDriven, solver=mySolver, edit=False) # driven transform
    rbf_api.edit_solver(edit=True, solver=mySolver) # edit solver
    transform2RBF()
    rbf_api.update_pose("default", solver=mySolver) # update pose


    cmds.currentTime( 1, edit=True )
    rbf_api.create_pose("calf_r_back_50", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("calf_r_back_50", solver=mySolver) # update pose

    cmds.currentTime( 2, edit=True )
    rbf_api.create_pose("calf_r_back_120", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("calf_r_back_120", solver=mySolver) # update pose

    cmds.currentTime( 3, edit=True )
    rbf_api.create_pose("calf_r_back_90", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("calf_r_back_90", solver=mySolver) # update pose

    cmds.currentTime( 4, edit=True )
    rbf_api.create_pose("calf_r_back_150", solver=mySolver)
    transform2RBF()
    rbf_api.update_pose("calf_r_back_150", solver=mySolver) # update pose

    cmds.currentTime( 0, edit=True )
    rbf_api.edit_solver(edit=False, solver=mySolver) # edit solver
    #rbf_api.get_solver_edit_status(solver=mySolver)

    cmds.setAttr('%s.radius'%mySolver, 50)
    cmds.setAttr('%s.distanceMethod'%mySolver, 2)
    cmds.setAttr('%s.normalizeMethod'%mySolver, 1)
    cmds.setAttr('%s.functionType'%mySolver, 0)
