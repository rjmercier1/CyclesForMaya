import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginNodeName = "MitsubaMixtureShader"
kPluginNodeClassify = "/shader/surface"
kPluginNodeId = OpenMaya.MTypeId(0x87011)

class mixture(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mBSDF1 = OpenMaya.MObject()
        mWeight1 = OpenMaya.MObject()
        mBSDF2 = OpenMaya.MObject()
        mWeight2 = OpenMaya.MObject()
        mBSDF3 = OpenMaya.MObject()
        mWeight3 = OpenMaya.MObject()
        mBSDF4 = OpenMaya.MObject()
        mWeight4 = OpenMaya.MObject()

        mOutColor = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == mixture.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)
            
            outColorHandle = block.outputValue( mixture.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    return mixture()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()

    try:
        mixture.mBSDF1 = nAttr.createColor("bsdf1", "b1")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        mixture.mWeight1 = nAttr.create("weight1","w1", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        mixture.mBSDF2 = nAttr.createColor("bsdf2", "b2")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        mixture.mWeight2 = nAttr.create("weight2","w2", OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        mixture.mBSDF3 = nAttr.createColor("bsdf3", "b3")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        mixture.mWeight3 = nAttr.create("weight3","w3", OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        mixture.mBSDF4 = nAttr.createColor("bsdf4", "b4")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        mixture.mWeight4 = nAttr.create("weight4","w4", OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        mixture.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)
    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        mixture.addAttribute(mixture.mBSDF1)
        mixture.addAttribute(mixture.mWeight1)
        mixture.addAttribute(mixture.mBSDF2)
        mixture.addAttribute(mixture.mWeight2)
        mixture.addAttribute(mixture.mBSDF3)
        mixture.addAttribute(mixture.mWeight3)
        mixture.addAttribute(mixture.mBSDF4)
        mixture.addAttribute(mixture.mWeight4)

        mixture.addAttribute(mixture.mOutColor)
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
