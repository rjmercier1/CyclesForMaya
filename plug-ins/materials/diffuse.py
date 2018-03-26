import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeName = "CyclesDiffuseShader"
kPluginNodeClassify = "shader/surface"
kPluginNodeId = OpenMaya.MTypeId(0x87003)

class diffuse(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mDiffuse = OpenMaya.MObject()
        mRoughness = OpenMaya.MObject()
        
        mOutColor = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == diffuse.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)
            
            outColorHandle = block.outputValue( diffuse.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter

        return None

def nodeCreator():
    return diffuse()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()

    try:
        diffuse.mDiffuse = nAttr.createColor("color", "dr")
        nAttr.setKeyable(1)
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.7, 0.5, 0.3)
        
        diffuse.mRoughness = nAttr.create("roughness","drf", OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.setKeyable(1)
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        diffuse.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)

    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        diffuse.addAttribute(diffuse.mDiffuse)
        diffuse.addAttribute(diffuse.mRoughness)
        diffuse.addAttribute(diffuse.mOutColor)
    except:
        sys.stderr.write("Failed to add attributes\n")
        raise

    #try:
    #    diffuse.attributeAffects (diffuse.mReflectance, diffuse.mOutColor)
    #except:
    #    sys.stderr.write("Failed in setting attributeAffects\n")
    #    raise


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
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Cycles")
    try:
        mplugin.deregisterNode( kPluginNodeId )
    except:
        sys.stderr.write( "Failed to deregister node: %s" % kPluginNodeName )
        raise
