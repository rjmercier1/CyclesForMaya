import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeName = "MitsubaObjectAreaLightShader"
kPluginNodeClassify = "shader/surface"
kPluginNodeId = OpenMaya.MTypeId(0x87024)

class arealight(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mOutColor = OpenMaya.MObject()
        mRadiance = OpenMaya.MObject()
        mSamplingWeight = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == arealight.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)
            
            outColorHandle = block.outputValue( arealight.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    return arealight()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()

    try:
        arealight.mRadiance = nAttr.createColor("radiance", "rd")
        nAttr.setDefault(1.0, 1.0, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        arealight.mSamplingWeight = nAttr.create("samplingWeight", "sw", OpenMaya.MFnNumericData.kInt, 1)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        arealight.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)

    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        arealight.addAttribute(arealight.mRadiance)
        arealight.addAttribute(arealight.mSamplingWeight)
        arealight.addAttribute(arealight.mOutColor)
    except:
        sys.stderr.write("Failed to add attributes\n")
        raise

    try:
        arealight.attributeAffects (arealight.mRadiance, arealight.mOutColor)
    except:
        sys.stderr.write("Failed in setting attributeAffects\n")
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
