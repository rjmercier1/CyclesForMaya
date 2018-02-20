import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginNodeName = "MitsubaConductorShader"
kPluginNodeClassify = "/shader/surface"
kPluginNodeId = OpenMaya.MTypeId(0x87002)

class conductor(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mTwoSided = OpenMaya.MObject()
        mMaterial = OpenMaya.MObject()
        mExtEta = OpenMaya.MObject()
        mSpecularReflectance = OpenMaya.MObject()

        mOutColor = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == conductor.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.5,0.5,0.5)
            
            outColorHandle = block.outputValue( conductor.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter

        return None

def nodeCreator():
    return conductor()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()

    try:
        conductor.mTwoSided = nAttr.create("twosided", "tw", OpenMaya.MFnNumericData.kBoolean, True)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        conductor.mMaterial = eAttr.create("material", "mat")
        eAttr.setKeyable(1) 
        eAttr.setStorable(1)
        eAttr.setReadable(1)
        eAttr.setWritable(1)

        eAttr.addField("100\% reflecting mirror", 0)
        eAttr.addField("Amorphous carbon", 1)
        eAttr.addField("Silver", 2)
        eAttr.addField("Aluminium", 3)
        eAttr.addField("Cubic aluminium arsenide", 4)
        eAttr.addField("Cubic aluminium antimonide", 5)
        eAttr.addField("Gold",  6)
        eAttr.addField("Polycrystalline beryllium", 7)
        eAttr.addField("Chromium", 8)
        eAttr.addField("Cubic caesium iodide", 9)
        eAttr.addField("Copper", 10)
        eAttr.addField("Copper (I) oxide", 11)
        eAttr.addField("Copper (II) oxide", 12)
        eAttr.addField("Cubic diamond", 13)
        eAttr.addField("Mercury", 14)
        eAttr.addField("Mercury telluride", 15)
        eAttr.addField("Iridium", 16)
        eAttr.addField("Polycrystalline potassium", 17)
        eAttr.addField("Lithium", 18)
        eAttr.addField("Polycrystalline potassium", 19)
        eAttr.addField("Magnesium oxide", 20)
        eAttr.addField("Molybdenum", 21)
        eAttr.addField("Sodium", 22)
        eAttr.addField("Niobium", 23)
        eAttr.addField("Nickel", 24)
        eAttr.addField("Rhodium", 25)
        eAttr.addField("Selenium", 26)
        eAttr.addField("Hexagonal silicon carbide", 27)
        eAttr.addField("Tin telluride", 28)
        eAttr.addField("Tantalum", 29)
        eAttr.addField("Trigonal tellurium", 30)
        eAttr.addField("Polycryst. thorium (IV) fuoride", 31)
        eAttr.addField("Polycrystalline titanium carbide", 32)
        eAttr.addField("Titanium nitride", 33)
        eAttr.addField("Tetragonal titan. dioxide", 34)
        eAttr.addField("Vanadium carbide", 35)
        eAttr.addField("Vanadium", 36)
        eAttr.addField("Vanadium nitride", 37)
        eAttr.addField("Tungsten", 38)

        conductor.mExtEta = nAttr.create("extEta","ee", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        conductor.mSpecularReflectance = nAttr.createColor("specularReflectance", "sr")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(1.0,1.0,1.0)

        conductor.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)
        nAttr.setDefault(0.5,0.5,0.0)

    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        conductor.addAttribute(conductor.mTwoSided)
        conductor.addAttribute(conductor.mMaterial)
        conductor.addAttribute(conductor.mExtEta)
        conductor.addAttribute(conductor.mSpecularReflectance)
        conductor.addAttribute(conductor.mOutColor)
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
