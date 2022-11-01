import maya.cmds as cmds
import maya.mel as mel
from epic_pose_wrangler.v2 import main

#class
class YG_RBF_def(object):
    def __init__(self):
        self.myAPIList = []
        self.rbf_api = main.UERBFAPI(view=False)

        self.myMeshList = []
        self.mySkinJntDict = {}
        self.myJntParentDict = {}

        self.usd = cmds.internalVar(usd=True)
        self.mayascripts = '%s/%s' % (self.usd.rsplit('/', 3)[0], 'scripts/')
        self.tempPath = self.mayascripts + "RBF/template/SKM_Manny/"

    def rbfList(self, *args):
        temp = self.rbf_api.rbf_solvers
        if temp:
            for i in temp:
                if i not in self.myAPIList:
                    self.myAPIList.append(i)
        return self.myAPIList

    def delRBF(self, myName):
        mySolver = self.rbf_api.get_rbf_solver_by_name(myName)
        # print ('delete --> %s' % mySolver)
        self.rbf_api.delete_rbf_solver(mySolver)

    def freezJoint(self, *args):
        # save skin
        self.saveSkin()

        # make joint parent dict
        myJnt = cmds.ls('root', dag=True, type='joint')
        for i in myJnt:
            # make dict
            if bool(cmds.listRelatives(i, p=True)):
                myParent = cmds.listRelatives(i, p=True)
                self.myJntParentDict[i]=myParent[0]

        # delete skin
        for i in self.myMeshList:
            cmds.delete(i, constructionHistory = True)

        for i in myJnt:
            # parent world
            cmds.parent(i, world=True)

            # freeze rotate
            cmds.makeIdentity (apply=True, r=True, pn=True)

        # re parent joint
        self.reParentJoint()

        # re skin
        for mesh in list(self.mySkinJntDict):
            skinFileName = cmds.skinCluster(self.mySkinJntDict[mesh], mesh, tsb=True)
            cmds.deformerWeights (mesh+'_skin.xml', im=True, deformer=skinFileName, path=self.tempPath)

    def findMesh(self, *args):
        myShape = cmds.ls(type='geometryShape')
        # print (myShape)
        for i in myShape:
            temp = cmds.listRelatives(i, p=True)[0]
            if temp not in self.myMeshList:
                self.myMeshList.append(temp)

    def saveSkin(self, *args):
        self.findMesh()
        # print(self.myMeshList)
        for mesh in self.myMeshList:
            if bool( mel.eval('findRelatedSkinCluster '+mesh) ):
                skinFileName = mel.eval('findRelatedSkinCluster '+mesh)
                # print('%s -> %s' % (mesh, skinFileName) )

                # make skin joint dict
                self.mySkinJntDict[mesh] = cmds.skinCluster(mesh, q=True, wi=True)
                cmds.deformerWeights (mesh+'_skin.xml', export=True, deformer=skinFileName, path=self.tempPath)

        # print self.myMeshList
        # print self.mySkinJntDict

    def reParentJoint(self, *args):
        # print(self.myJntParentDict)
        for i in self.myJntParentDict:
            # print('%s --> %s' % (i, self.myJntParentDict[i]) )
            cmds.parent(i, self.myJntParentDict[i])
