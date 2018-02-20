import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginNodeName = "MitsubaTwoSidedShader"
kPluginNodeClassify = "/shader/surface"
kPluginNodeId = OpenMaya.MTypeId(0x87013)

class twosided(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mFrontBSDF = OpenMaya.MObject()
        mBackBSDF = OpenMaya.MObject()
        mOutColor = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == twosided.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)

            outColorHandle = block.outputValue( twosided.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            block.setClean( plug )
        else:
            return OpenMaya.kUnknownParameter

        return None

def nodeCreator():
    return twosided()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()

    try:
        twosided.mFrontBSDF = nAttr.createColor("frontBSDF", "fbsdf")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        twosided.mBackBSDF = nAttr.createColor("backBSDF", "bbsdf")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        twosided.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)
        nAttr.setDefault(0.5,0.5,0.0)

    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        twosided.addAttribute(twosided.mFrontBSDF)
        twosided.addAttribute(twosided.mBackBSDF)
        twosided.addAttribute(twosided.mOutColor)
    except:
        sys.stderr.write("Failed to add attributes\n")
        raise

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeName, kPluginNodeId, nodeCreator, 
                    nodeInitializer, OpenMayaMPx.MPxNode.kDependNode, kPluginNodeClassify )
    except:
        sys.stderr.write( "Failed to register node: %s" % kPluginNodeName )
        raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( kPluginNodeId )
    except:
        sys.stderr.write( "Failed to deregister node: %s" % kPluginNodeName )
        raise
