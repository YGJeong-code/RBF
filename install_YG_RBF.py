import maya.cmds as cmds
import maya.mel as mel

gShelfTopLevel = mel.eval("$tmpVar=$gShelfTopLevel")
myTap = cmds.tabLayout(gShelfTopLevel, query=True, selectTab=True)
myCommand = '''import RBF.module.YG_RBF
from imp import reload
reload(RBF.module.YG_RBF)'''
usd = cmds.internalVar(usd=True)
mayascripts = '%s/%s' % (usd.rsplit('/', 3)[0], 'scripts/')
tempPath = mayascripts+"RBF/icon/"
cmds.shelfButton(command=myCommand,
                 annotation="YG_RBF",
                 label='YG_RBF',
                 image=tempPath+'YG_RBF.bmp',
                 parent=myTap)


