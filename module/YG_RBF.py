#-*- coding: utf-8 -*-
#==============================
# YG_RBF
# since 2022.08.22
# last update 2022.08.22
# ygjeong@krafton.com
#==============================
import maya.cmds as cmds
import maya.mel as mel

import RBF.module.YG_RBF_def
reload(RBF.module.YG_RBF_def)
YG_RBF_def = RBF.module.YG_RBF_def.YG_RBF_def()

import RBF.module.YG_Twist as YG_Twist
reload(YG_Twist)

import RBF.module.YG_RBF_makePose as YG_RBF_makePose
reload(YG_RBF_makePose)


#class
class YG_RBF(object):
    def __init__(self):
        self.myWin = 'YG_RBF'
        self.size = 150
        self.createWindow()
        self.usd = cmds.internalVar(usd=True)
        self.mayascripts = '%s/%s' % (self.usd.rsplit('/', 3)[0], 'scripts/')
        self.tempPath = self.mayascripts+"RBF/template/SKM_Manny/"
        self.tempFileList = cmds.getFileList( folder=self.tempPath, filespec='*.FBX')
        for i in self.tempFileList:
            cmds.menuItem(label=i)
        self.tempFile = cmds.optionMenu('tempFileMenu', q=True, v=True)
        self.rbfList()

    def createWindow(self):
        if cmds.window(self.myWin, ex=True):
            cmds.deleteUI(self.myWin)

        self.myWin = cmds.window(self.myWin, t=self.myWin+'_v1.1', sizeable=True, resizeToFitChildren=True)
        self.myColor = {'red':[0.6,0,0],'orange':[0.6, 0.2, 0],'yellow':[0.7, 0.6, 0.1],'green':[0.4, 0.6, 0.1]}

        ## template
        cmds.columnLayout( adjustableColumn=True, p=self.myWin )
        cmds.frameLayout( label='Template', collapsable=True, collapse=False, bgc=self.myColor['red'], cc=self.winResize, ec=self.winResize )
        cmds.text(l='Template File:', align='left')
        cmds.rowLayout(numberOfColumns=3, columnWidth3=(self.size, self.size, self.size*0.1), adjustableColumn=2)
        cmds.optionMenu('tempFileMenu', w=self.size)
        cmds.button(label='Import', w=self.size, c=lambda *_:self.tempBtn('import'))
        cmds.button(label='O', w=self.size*0.1, c=lambda *_:self.tempBtn('open'))
        cmds.setParent( '..' )
        cmds.setParent( '..' )

        ## Build...
        ## Step Builder
        cmds.columnLayout( adjustableColumn=True, p=self.myWin )
        self.buildFrame = cmds.frameLayout( label='Build...', collapsable=True, collapse=False, bgc=self.myColor['orange'], cc=self.winResize, ec=self.winResize )
        cmds.columnLayout( adjustableColumn=True, p=self.buildFrame )

        cmds.text(l='Freeze:', align='left')
        cmds.button(label='freeze joint rotate', w=self.size, c=self.freezeJointRotate)

        cmds.text(l='Twist:', align='left')
        self.makeTwistBtn = cmds.button(label='make twist', w=self.size, c=self.makeTwist)
        cmds.button(label='toggle twist joint axis', w=self.size, c=self.toggleTwistAxis)

        cmds.text(l='Step Builder:', align='left')
        # cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(self.size, 25) )
        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=(self.size, self.size), adjustableColumn=1)
        self.clavicle_l_Btn = cmds.button(label='clavicle_l', w=self.size, c=lambda *_:self.rbfBuild('clavicle_l'))
        self.clavicle_l_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('clavicle_l'), enable=False)
        self.upperarm_l_Btn = cmds.button(label='upperarm_l', w=self.size, c=lambda *_:self.rbfBuild('upperarm_l'))
        self.upperarm_l_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('upperarm_l'), enable=False)
        self.lowerarm_l_Btn = cmds.button(label='lowerarm_l', w=self.size, c=lambda *_:self.rbfBuild('lowerarm_l'))
        self.lowerarm_l_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('lowerarm_l'), enable=False)
        self.hand_l_Btn = cmds.button(label='hand_l', w=self.size, c=lambda *_:self.rbfBuild('hand_l'))
        self.hand_l_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('hand_l'), enable=False)
        self.thigh_l_Btn = cmds.button(label='thigh_l', w=self.size, c=lambda *_:self.rbfBuild('thigh_l'))
        self.thigh_l_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('thigh_l'), enable=False)
        self.calf_l_Btn = cmds.button(label='calf_l', w=self.size, c=lambda *_:self.rbfBuild('calf_l'))
        self.calf_l_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('calf_l'), enable=False)
        self.foot_l_Btn = cmds.button(label='foot_l', w=self.size, c=lambda *_:self.rbfBuild('foot_l'))
        self.foot_l_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('foot_l'), enable=False)

        cmds.separator()
        cmds.separator()

        self.clavicle_r_Btn = cmds.button(label='clavicle_r', w=self.size, c=lambda *_:self.rbfBuild('clavicle_r'))
        self.clavicle_r_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('clavicle_r'), enable=False)
        self.upperarm_r_Btn = cmds.button(label='upperarm_r', w=self.size, c=lambda *_:self.rbfBuild('upperarm_r'))
        self.upperarm_r_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('upperarm_r'), enable=False)
        self.lowerarm_r_Btn = cmds.button(label='lowerarm_r', w=self.size, c=lambda *_:self.rbfBuild('lowerarm_r'))
        self.lowerarm_r_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('lowerarm_r'), enable=False)
        self.hand_r_Btn = cmds.button(label='hand_r', w=self.size, c=lambda *_:self.rbfBuild('hand_r'))
        self.hand_r_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('hand_r'), enable=False)
        self.thigh_r_Btn = cmds.button(label='thigh_r', w=self.size, c=lambda *_:self.rbfBuild('thigh_r'))
        self.thigh_r_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('thigh_r'), enable=False)
        self.calf_r_Btn = cmds.button(label='calf_r', w=self.size, c=lambda *_:self.rbfBuild('calf_r'))
        self.calf_r_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('calf_r'), enable=False)
        self.foot_r_Btn = cmds.button(label='foot_r', w=self.size, c=lambda *_:self.rbfBuild('foot_r'))
        self.foot_r_DelBtn = cmds.button(label='delete', w=self.size, c=lambda *_:self.rbfDel('foot_r'), enable=False)

        cmds.columnLayout( adjustableColumn=True, p=self.buildFrame )
        self.aniDelBtn = cmds.button(label='clean (delete ani key)', w=self.size, c=self.aniDel)
        cmds.setParent( '..' )
        cmds.setParent( '..' )

        ## build
        cmds.columnLayout( adjustableColumn=True, p=self.myWin )
        self.buildFrame2 = cmds.frameLayout( label='Build', collapsable=True, collapse=False, bgc=self.myColor['yellow'], cc=self.winResize, ec=self.winResize)
        cmds.columnLayout( adjustableColumn=1, p=self.buildFrame2 )
        cmds.button(label='Build RBF', w=self.size*2, c=self.buildBtn)
        # cmds.button(label='size', w=self.size*2, c=self.getsize)
        cmds.setParent( '..' )
        cmds.setParent( '..' )

        ## window
        cmds.showWindow(self.myWin)

    ############################################################################################################################################################################################################################
    # template
    ############################################################################################################################################################################################################################
    def tempBtn(self, state):
        self.tempFile = cmds.optionMenu('tempFileMenu', q=True, v=True)
        temp = self.tempPath + self.tempFile

        if state == 'import':
            cmds.file(temp, i=True)
        elif state == 'open':
            cmds.file(temp, f=True, save=False, open=True)

    ############################################################################################################################################################################################################################
    # Build...
    ############################################################################################################################################################################################################################
    def createRef(self, FileName):
        filePath = self.mayascripts+"RBF/template/RBF_Target/"
        temp = filePath + 'RBF_' + FileName + '.fbx'
        cmds.file(temp, reference=True, namespace='RBF_'+FileName)

        temp = 'RBF_' + FileName + ':root'
        cmds.setAttr(temp+'.visibility', False )

    def importAnim(self, FileName):
        filePath = self.mayascripts+"RBF/template/RBF_Pose/"
        temp = filePath + 'Manny_' + FileName + '_anim.FBX'
        cmds.file(temp, i=True)

    def removeRef(self, FileName):
        filePath = self.mayascripts+"RBF/template/RBF_Target/"
        temp = filePath + 'RBF_' + FileName + '.fbx'
        cmds.file(temp, removeReference=True)

    def rbfList(self, *args):
        # import YG_RBF_def;reload(YG_RBF_def)
        myList = YG_RBF_def.rbfList()
        if myList:
            for i in myList:
                print i
                # temp = str(i).split('_')[0]
                buildBtn = str(i).replace('_UERBFSolver','_Btn')
                delBtn = str(i).replace('_UERBFSolver','_DelBtn')
                temp = 'cmds.button(self.'+buildBtn+', e=True, enable=False)'
                exec(temp)
                temp = 'cmds.button(self.'+delBtn+', e=True, enable=True)'
                exec(temp)

    def rbfBuild(self, FileName):
        if bool(cmds.listRelatives("root", parent=True)):
            cmds.parent('root', w=True)

        # self.importAnim(FileName)
        YG_RBF_makePose.makePose(FileName)

        # self.createRef(FileName)
        # temp = 'import YG_RBF_'+FileName
        # exec(temp)
        # temp = 'reload(YG_RBF_'+FileName+')'
        # exec(temp)
        # temp = 'YG_RBF_' + FileName + '.run()'
        # exec(temp)

        self.rbfList()

    def rbfDel(self, FileName):
        myJnt = cmds.ls('root',dag=True)
        cmds.cutKey(myJnt, clear=True, time=())

        # reload(RBF.module.YG_RBF_def)
        YG_RBF_makePose.set24fps(24)
        cmds.currentTime( 0, edit=True )

        filePath = self.mayascripts+"RBF/template/RBF_Target/"
        temp = filePath + 'RBF_' + FileName + '.fbx'
        myFileList = cmds.file( q=True, list=True )
        if temp in myFileList:
            self.removeRef(FileName)

        reload(RBF.module.YG_RBF_def)
        myList = YG_RBF_def.rbfList()
        # print myList
        if myList:
            for i in myList:
                # print ('list --> %s' % i)
                if FileName in str(i):
                    # print ('delete --> %s' % i)
                    YG_RBF_def.delRBF(str(i))

        temp = 'cmds.button(self.'+FileName+'_Btn, e=True, enable=True)'
        exec(temp)
        temp = 'cmds.button(self.'+FileName+'_DelBtn, e=True, enable=False)'
        exec(temp)

    def aniDel(self, *args):
        myJnt = cmds.ls('root',dag=True)
        cmds.cutKey(myJnt, clear=True, time=())

        YG_RBF_makePose.set24fps(24)
        cmds.currentTime( 0, edit=True )

        myList = ['clavicle_l','upperarm_l','lowerarm_l','hand_l','thigh_l','calf_l','foot_l',
                'clavicle_r','upperarm_r','lowerarm_r','hand_r','thigh_r','calf_r','foot_r']
        for i in myList:
            filePath = self.mayascripts+"RBF/template/RBF_Target/"
            temp = filePath + 'RBF_' + i + '.fbx'
            myFileList = cmds.file( q=True, list=True )
            if temp in myFileList:
                self.removeRef(i)

    def makeTwist(self, *args):
        if cmds.objExists('rig_setup_GRP'):
            cmds.confirmDialog( message='Aready Twist Exists!!')
        else:
            YG_Twist.makeGroup()
            YG_Twist.makeTwist('upperarm', '_l')
            YG_Twist.makeTwist('lowerarm', '_l')
            YG_Twist.makeTwist('thigh', '_l')
            YG_Twist.makeTwist('calf', '_l')
            YG_Twist.makeTwist('upperarm', '_r')
            YG_Twist.makeTwist('lowerarm', '_r')
            YG_Twist.makeTwist('thigh', '_r')
            YG_Twist.makeTwist('calf', '_r')

            YG_Twist.makePoseMaster('upperarm', '_l')
            YG_Twist.makePoseMaster('lowerarm', '_l')
            YG_Twist.makePoseMaster('thigh', '_l')
            YG_Twist.makePoseMaster('calf', '_l')
            YG_Twist.makePoseMaster('upperarm', '_r')
            YG_Twist.makePoseMaster('lowerarm', '_r')
            YG_Twist.makePoseMaster('thigh', '_r')
            YG_Twist.makePoseMaster('calf', '_r')

    def delTwist(self, *args):
        YG_Twist.delTwist('lowerarm','_l')
        YG_Twist.delTwist('upperarm','_l')
        YG_Twist.delTwist('thigh', '_l')
        YG_Twist.delTwist('calf', '_l')
        cmds.delete('rig_setup_GRP')

    def toggleTwistAxis(self, *args):
        YG_Twist.twistJointLRA()

    def freezeJointRotate(self, *args):
        YG_RBF_def.freezJoint()

    ############################################################################################################################################################################################################################
    # build
    ############################################################################################################################################################################################################################
    def buildBtn(self, *args):
        myConfirm = cmds.confirmDialog( title=u'중요' , message=u'시간이 걸리니 담배 한대 피우고 오세요~~', button=u'시작', defaultButton='Yes', cancelButton='No', dismissString='No')

        if myConfirm == u'시작':
            self.makeTwist()

            self.rbfBuild('clavicle_l')
            self.rbfBuild('upperarm_l')
            self.rbfBuild('lowerarm_l')
            self.rbfBuild('hand_l');self.rbfDel('hand_l');self.rbfBuild('hand_l')
            self.rbfBuild('thigh_l')
            self.rbfBuild('calf_l');self.rbfDel('calf_l');self.rbfBuild('calf_l')
            self.rbfBuild('foot_l');self.rbfDel('foot_l');self.rbfBuild('foot_l')
            self.rbfBuild('clavicle_r')
            self.rbfBuild('upperarm_r')
            self.rbfBuild('lowerarm_r')
            self.rbfBuild('hand_r')
            self.rbfBuild('thigh_r')
            self.rbfBuild('calf_r')
            self.rbfBuild('foot_r')

            # self.delTwist()
            # self.makeTwist()
            self.rbfDel('upperarm_l');self.rbfBuild('upperarm_l')

            self.aniDel()

            myJnt = cmds.ls('root',dag=True,type='joint')
            cmds.select(myJnt, r=True)
            cmds.sets(n='export_cha')

            cmds.dagPose(bindPose=True, reset=True)

            cmds.select(cl=True)
    ############################################################################################################################################################################################################################
    # window resize
    ############################################################################################################################################################################################################################
    def winResize(self, *args):
        cmds.window(self.myWin, e=True, w=50L, h=50L)

    def getsize(self, *args):
        size = cmds.window(self.myWin, q=True, widthHeight=True)
        print size

myTest = YG_RBF()
myTest.winResize()
