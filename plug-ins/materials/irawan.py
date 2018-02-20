import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeName = "MitsubaIrawanShader"
kPluginNodeClassify = "shader/surface"
kPluginNodeId = OpenMaya.MTypeId(0x87020)

class irawan(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mOutColor = OpenMaya.MObject()
        mTwoSided = OpenMaya.MObject()

        mFilename = OpenMaya.MObject()

        mRepeatU = OpenMaya.MObject()
        mRepeatV = OpenMaya.MObject()

        mWarpKd = OpenMaya.MObject()
        mWarpKs = OpenMaya.MObject()
        mWeftKd = OpenMaya.MObject()
        mWeftKs = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == irawan.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)
            
            repeatU = block.inputValue( irawan.mRepeatU ).asFloat()
            repeatV = block.inputValue( irawan.mRepeatV ).asFloat()

            resultColor.x = repeatU
            resultColor.y = repeatV
            resultColor.z = 0

            outColorHandle = block.outputValue( irawan.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    return irawan()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()
    sAttr = OpenMaya.MFnTypedAttribute()

    try:
        irawan.mTwoSided = nAttr.create("twosided", "tw", OpenMaya.MFnNumericData.kBoolean, True)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        irawan.mFilename = sAttr.create("filename", "f", OpenMaya.MFnData.kString )
        sAttr.setStorable(1)
        sAttr.setReadable(1)

        irawan.mRepeatU = nAttr.create("repeatu", "ru", OpenMaya.MFnNumericData.kFloat, 100.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)

        irawan.mRepeatV = nAttr.create("repeatv", "rv", OpenMaya.MFnNumericData.kFloat, 100.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)

        irawan.mWarpKd = nAttr.createColor("warpkd", "wpkd")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)

        irawan.mWarpKs = nAttr.createColor("warpks", "wpks")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)

        irawan.mWeftKd = nAttr.createColor("weftkd", "wfkd")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)

        irawan.mWeftKs = nAttr.createColor("weftks", "wfks")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)

        irawan.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)

    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        irawan.addAttribute(irawan.mTwoSided)
        irawan.addAttribute(irawan.mFilename)
        irawan.addAttribute(irawan.mRepeatU)
        irawan.addAttribute(irawan.mRepeatV)
        irawan.addAttribute(irawan.mWarpKs)
        irawan.addAttribute(irawan.mWarpKd)
        irawan.addAttribute(irawan.mWeftKs)
        irawan.addAttribute(irawan.mWeftKd)
        irawan.addAttribute(irawan.mOutColor)
    except:
        sys.stderr.write("Failed to add attributes\n")
        raise

    try:
        irawan.attributeAffects (irawan.mRepeatU, irawan.mOutColor)
        irawan.attributeAffects (irawan.mRepeatV, irawan.mOutColor)
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
