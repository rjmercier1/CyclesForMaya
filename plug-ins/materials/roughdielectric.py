import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginNodeName = "MitsubaRoughDielectricShader"
kPluginNodeClassify = "/shader/surface"
kPluginNodeId = OpenMaya.MTypeId(0x87009)

class roughdielectric(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mIntIOR = OpenMaya.MObject()
        mExtIOR = OpenMaya.MObject()
        mInteriorMaterial = OpenMaya.MObject()
        mExteriorMaterial = OpenMaya.MObject()

        mAlpha = OpenMaya.MObject()
        mAlpaUV = OpenMaya.MObject()
        mDistribution = OpenMaya.MObject()

        mReflectance = OpenMaya.MObject()
        mTransmittance = OpenMaya.MObject()

        mOutColor = OpenMaya.MObject()
        mOutTransparency = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == roughdielectric.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)
            
            outColorHandle = block.outputValue( roughdielectric.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        elif plug == roughdielectric.mOutTransparency:
            outTransHandle = block.outputValue( roughdielectric.mOutTransparency )
            outTransHandle.setMFloatVector(OpenMaya.MFloatVector(0.75,0.75,0.75))
            outTransHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    return roughdielectric()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()

    try:
        roughdielectric.mDistribution = eAttr.create("distribution", "dist")
        eAttr.setKeyable(1) 
        eAttr.setStorable(1)
        eAttr.setReadable(1)
        eAttr.setWritable(1)

        eAttr.addField("Beckmann", 0)
        eAttr.addField("GGX", 1)
        eAttr.addField("Phong", 2)
        eAttr.addField("Ashikhmin Shirley", 3)

        roughdielectric.mAlpha = nAttr.create("alpha","a", OpenMaya.MFnNumericData.kFloat, 0.1)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        roughdielectric.mAlpaUV = nAttr.create("alphaUV","uv", OpenMaya.MFnNumericData.k2Float)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.1,0.1)

        roughdielectric.mInteriorMaterial = eAttr.create("interiorMaterial", "intmat")
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
        eAttr.setDefault(0)

        roughdielectric.mIntIOR = nAttr.create("interiorIOR","intior", OpenMaya.MFnNumericData.kFloat, 1.5046)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        roughdielectric.mExteriorMaterial = eAttr.create("exteriorMaterial", "extmat")
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
        eAttr.setDefault(0)

        roughdielectric.mExtIOR = nAttr.create("exteriorIOR","extior", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        roughdielectric.mReflectance = nAttr.createColor("specularReflectance", "sr")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(1.0,1.0,1.0)

        roughdielectric.mTransmittance = nAttr.createColor("specularTransmittance","st")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(1.0,1.0,1.0)

        roughdielectric.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)

        roughdielectric.mOutTransparency = nAttr.createColor("outTransparency", "op")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)

    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        roughdielectric.addAttribute(roughdielectric.mDistribution)
        roughdielectric.addAttribute(roughdielectric.mAlpha)
        roughdielectric.addAttribute(roughdielectric.mAlpaUV)
        roughdielectric.addAttribute(roughdielectric.mReflectance)
        roughdielectric.addAttribute(roughdielectric.mTransmittance)
        roughdielectric.addAttribute(roughdielectric.mInteriorMaterial)
        roughdielectric.addAttribute(roughdielectric.mIntIOR)
        roughdielectric.addAttribute(roughdielectric.mExteriorMaterial)
        roughdielectric.addAttribute(roughdielectric.mExtIOR)
        roughdielectric.addAttribute(roughdielectric.mOutColor)
        roughdielectric.addAttribute(roughdielectric.mOutTransparency)
    except:
        sys.stderr.write("Failed to add attributes\n")
        raise

    try:
        roughdielectric.attributeAffects (roughdielectric.mTransmittance, roughdielectric.mOutTransparency)
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
