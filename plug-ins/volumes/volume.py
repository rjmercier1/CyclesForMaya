import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeName = "MitsubaVolume"
kPluginNodeClassify = "shader/volume"
kPluginNodeId = OpenMaya.MTypeId(0x87033)

class volume(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mSourcefile = OpenMaya.MObject()
        mGridDims = OpenMaya.MObject()
        mOutColor = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == volume.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)
            
            outColorHandle = block.outputValue( volume.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    return volume()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()

    try:
        volume.mSourcefile = nAttr.createColor("sourceFile", "sf")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        #nAttr.setDefault(50,50,50)
        volume.mGridDims = nAttr.create("gridDimensions", "gd", OpenMaya.MFnNumericData.k3Float)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        volume.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        volume.addAttribute(volume.mSourcefile)
        volume.addAttribute(volume.mGridDims)
        volume.addAttribute(volume.mOutColor)
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
