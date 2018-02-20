import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginNodeName = "MitsubaHeterogeneousParticipatingMedium"
kPluginNodeClassify = "shader/volume"
kPluginNodeId = OpenMaya.MTypeId(0x87017)

class heterogeneous(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mSamplingMethod = OpenMaya.MObject()

        mDensity = OpenMaya.MObject()
        mAlbedo = OpenMaya.MObject()
        mOrientation = OpenMaya.MObject()

        mScale = OpenMaya.MObject()

        mPhaseFunction = OpenMaya.MObject()
        mPhaseFunctionHGG = OpenMaya.MObject()
        mPhaseFunctionMicroFlakeStdDev = OpenMaya.MObject()

        mOutColor = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == heterogeneous.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)
            
            outColorHandle = block.outputValue( heterogeneous.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter

def nodeCreator():
    return heterogeneous()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()

    try:
        heterogeneous.mSamplingMethod = eAttr.create("samplingMethod", "sm")
        eAttr.setKeyable(1) 
        eAttr.setStorable(1)
        eAttr.setReadable(1)
        eAttr.setWritable(1)

        SamplingMethods = ["Simpson", "Woodcock"]

        for i in range(len(SamplingMethods)):
            eAttr.addField(SamplingMethods[i], i)

        # Default to Skin1
        eAttr.setDefault(1)

        heterogeneous.mDensity = nAttr.create("density","d", OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        heterogeneous.mAlbedo = nAttr.create("albedo","a", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        heterogeneous.mOrientation = nAttr.create("orientation","o", OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        heterogeneous.mScale = nAttr.create("scale","s", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(0) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        heterogeneous.mPhaseFunction = eAttr.create("phaseFunction", "pf")
        eAttr.setKeyable(1) 
        eAttr.setStorable(1)
        eAttr.setReadable(1)
        eAttr.setWritable(1)

        PhaseFunctions = ["Isotropic",
            "Henyey-Greenstein",
            "Rayleigh",
            "Kajiya-Kay",
            "Micro-Flake"
        ]

        for i in range(len(PhaseFunctions)):
            eAttr.addField(PhaseFunctions[i], i)

        # Default to Isotropic
        eAttr.setDefault(0)

        heterogeneous.mPhaseFunctionHGG = nAttr.create("phaseFunctionHGG","pfhgg", OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        heterogeneous.mPhaseFunctionMicroFlakeStdDev = nAttr.create("phaseFunctionMFSD","pfmfsd", OpenMaya.MFnNumericData.kFloat, 0.05)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        heterogeneous.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)

    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        heterogeneous.addAttribute(heterogeneous.mSamplingMethod)

        heterogeneous.addAttribute(heterogeneous.mDensity)
        heterogeneous.addAttribute(heterogeneous.mAlbedo)
        heterogeneous.addAttribute(heterogeneous.mOrientation)

        heterogeneous.addAttribute(heterogeneous.mScale)

        heterogeneous.addAttribute(heterogeneous.mPhaseFunction)
        heterogeneous.addAttribute(heterogeneous.mPhaseFunctionHGG)
        heterogeneous.addAttribute(heterogeneous.mPhaseFunctionMicroFlakeStdDev)

        heterogeneous.addAttribute(heterogeneous.mOutColor)
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
