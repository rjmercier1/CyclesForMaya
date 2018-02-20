import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginNodeName = "MitsubaSmoothCoatingShader"
kPluginNodeClassify = "/shader/surface"
kPluginNodeId = OpenMaya.MTypeId(0x8700E)

class coating(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mIntIOR = OpenMaya.MObject()
        mExtIOR = OpenMaya.MObject()
        mInteriorMaterial = OpenMaya.MObject()
        mExteriorMaterial = OpenMaya.MObject()

        mThickness = OpenMaya.MObject()
        mSigmaA = OpenMaya.MObject()
        mReflectance = OpenMaya.MObject()

        mBSDF = OpenMaya.MObject()

        mOutColor = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == coating.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)

            outColorHandle = block.outputValue( coating.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    return coating()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()

    try:
        coating.mInteriorMaterial = eAttr.create("interiorMaterial", "intmat")
        eAttr.setKeyable(1) 
        eAttr.setStorable(1)
        eAttr.setReadable(1)
        eAttr.setWritable(1)

        eAttr.addField("Use Value", 0)
        eAttr.addField("Vacuum - 1.0", 1)
        eAttr.addField("Helum - 1.00004", 2)
        eAttr.addField("Hydrogen - 1.00013", 3)
        eAttr.addField("Air - 1.00028", 4)
        eAttr.addField("Carbon Dioxide - 1.00045", 5)
        eAttr.addField("Water - 1.3330", 6)
        eAttr.addField("Acetone - 1.36", 7)
        eAttr.addField("Ethanol - 1.361", 8)
        eAttr.addField("Carbon Tetrachloride - 1.461", 9)
        eAttr.addField("Glycerol - 1.4729", 10)
        eAttr.addField("Benzene - 1.501", 11)
        eAttr.addField("Silicone Oil - 1.52045", 12)
        eAttr.addField("Bromine - 1.661", 13)
        eAttr.addField("Water Ice - 1.31", 14)
        eAttr.addField("Fused Quartz - 1.458", 15)
        eAttr.addField("Pyrex - 1.470", 16)
        eAttr.addField("Acrylic Glass - 1.49", 17)
        eAttr.addField("Polypropylene - 1.49", 18)
        eAttr.addField("BK7 - 1.5046", 19)
        eAttr.addField("Sodium Chloride - 1.544", 20)
        eAttr.addField("Amber - 1.55", 21)
        eAttr.addField("Pet - 1.575", 22)
        eAttr.addField("Diamond - 2.419", 23)

        # Default to 
        eAttr.setDefault(19)

        coating.mIntIOR = nAttr.create("interiorIOR","intior", OpenMaya.MFnNumericData.kFloat, 1.5046)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        coating.mExteriorMaterial = eAttr.create("exteriorMaterial", "extmat")
        eAttr.setKeyable(1) 
        eAttr.setStorable(1)
        eAttr.setReadable(1)
        eAttr.setWritable(1)

        eAttr.addField("Use Value", 0)
        eAttr.addField("Vacuum - 1.0", 1)
        eAttr.addField("Helum - 1.00004", 2)
        eAttr.addField("Hydrogen - 1.00013", 3)
        eAttr.addField("Air - 1.00028", 4)
        eAttr.addField("Carbon Dioxide - 1.00045", 5)
        eAttr.addField("Water - 1.3330", 6)
        eAttr.addField("Acetone - 1.36", 7)
        eAttr.addField("Ethanol - 1.361", 8)
        eAttr.addField("Carbon Tetrachloride - 1.461", 9)
        eAttr.addField("Glycerol - 1.4729", 10)
        eAttr.addField("Benzene - 1.501", 11)
        eAttr.addField("Silicone Oil - 1.52045", 12)
        eAttr.addField("Bromine - 1.661", 13)
        eAttr.addField("Water Ice - 1.31", 14)
        eAttr.addField("Fused Quartz - 1.458", 15)
        eAttr.addField("Pyrex - 1.470", 16)
        eAttr.addField("Acrylic Glass - 1.49", 17)
        eAttr.addField("Polypropylene - 1.49", 18)
        eAttr.addField("BK7 - 1.5046", 19)
        eAttr.addField("Sodium Chloride - 1.544", 20)
        eAttr.addField("Amber - 1.55", 21)
        eAttr.addField("Pet - 1.575", 22)
        eAttr.addField("Diamond - 2.419", 23)

        # Default to 
        eAttr.setDefault(4)

        coating.mExtIOR = nAttr.create("exteriorIOR","extior", OpenMaya.MFnNumericData.kFloat, 1.000277)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        coating.mThickness = nAttr.create("thickness","th", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        coating.mSigmaA = nAttr.createColor("sigmaA", "sa")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        coating.mReflectance = nAttr.createColor("specularReflectance", "sr")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(1.0,1.0,1.0)

        coating.mBSDF = nAttr.createColor("bsdf", "bsdf")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        coating.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)

    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        coating.addAttribute(coating.mThickness)
        coating.addAttribute(coating.mSigmaA)
        coating.addAttribute(coating.mReflectance)
        coating.addAttribute(coating.mInteriorMaterial)
        coating.addAttribute(coating.mIntIOR)
        coating.addAttribute(coating.mExteriorMaterial)
        coating.addAttribute(coating.mExtIOR)
        coating.addAttribute(coating.mBSDF)
        coating.addAttribute(coating.mOutColor)
    except:
        sys.stderr.write("Failed to add attributes\n")
        raise

    try:
        coating.attributeAffects(coating.mBSDF, coating.mOutColor)
        # print "attr affects"
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
