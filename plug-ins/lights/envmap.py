import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeName = "MitsubaEnvironmentLight"
kPluginNodeClassify = "light/general"
kPluginNodeId = OpenMaya.MTypeId(0x87032)

class envmap(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mVisibility = OpenMaya.MObject()
        mSource = OpenMaya.MObject()
        mScale = OpenMaya.MObject()
        mAutoGamma = OpenMaya.MObject()
        mSRGB = OpenMaya.MObject()
        mGamma = OpenMaya.MObject()
        mCache = OpenMaya.MObject()
        mSamplingWeight = OpenMaya.MObject()
        mRotate = OpenMaya.MObject()
        mOutColor = OpenMaya.MObject()

    def compute(self, plug, block):
        status = None
        
        if plug == envmap.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)
            
            outColorHandle = block.outputValue( envmap.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            block.setClean( plug )

            status = OpenMaya.kSuccess
        else:
            status = OpenMaya.kUnknownParameter

        return status

def nodeCreator():
    return envmap()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()

    try:
        envmap.mVisibility = nAttr.create("visibility", "visibility", OpenMaya.MFnNumericData.kBoolean, True)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(0)
        nAttr.setWritable(1)

        envmap.mSource = nAttr.createColor("source", "src")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(0)
        nAttr.setWritable(1)

        envmap.mScale = nAttr.create("scale", "scale", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(0)
        nAttr.setWritable(1)

        envmap.mAutoGamma = nAttr.create("autoGamma", "autoGamma", OpenMaya.MFnNumericData.kBoolean, True)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(0)
        nAttr.setWritable(1)

        envmap.mSRGB = nAttr.create("srgb", "srgb", OpenMaya.MFnNumericData.kBoolean, False)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(0)
        nAttr.setWritable(1)

        envmap.mGamma = nAttr.create("gamma", "g", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(0)
        nAttr.setWritable(1)

        envmap.mCache = nAttr.create("cache", "cache", OpenMaya.MFnNumericData.kBoolean, True)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(0)
        nAttr.setWritable(1)

        envmap.mSamplingWeight = nAttr.create("samplingWeight", "sw", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(0)
        nAttr.setWritable(1)

        envmap.mRotate = nAttr.create("rotate", "ro", OpenMaya.MFnNumericData.k3Float)
        nAttr.default = (0.0, 0.0, 0.0)
        nAttr.usedAsColor = False
        nAttr.setKeyable(1) 
        #nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        envmap.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        #nAttr.setHidden(0)
        #nAttr.setReadable(1)
        nAttr.setWritable(0)

    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        envmap.addAttribute(envmap.mVisibility)
        envmap.addAttribute(envmap.mSource)
        envmap.addAttribute(envmap.mGamma)
        envmap.addAttribute(envmap.mAutoGamma)
        envmap.addAttribute(envmap.mSRGB)
        envmap.addAttribute(envmap.mScale)
        envmap.addAttribute(envmap.mCache)
        envmap.addAttribute(envmap.mSamplingWeight)
        envmap.addAttribute(envmap.mRotate)
        envmap.addAttribute(envmap.mOutColor)
    except:
        sys.stderr.write("Failed to add attributes\n")
        raise

    try:
        envmap.attributeAffects (envmap.mRotate, envmap.mOutColor)
    except:
        sys.stderr.write("Failed in setting attributeAffects\n")
        raise

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeName, 
                      kPluginNodeId, 
                      nodeCreator, 
                      nodeInitializer, 
                      OpenMayaMPx.MPxNode.kDependNode, 
                      kPluginNodeClassify )
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
