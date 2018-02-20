import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeName = "MitsubaSSSDipoleShader"
kPluginNodeClassify = "shader/volume"
kPluginNodeId = OpenMaya.MTypeId(0x87016)

class dipole(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        mMaterial = OpenMaya.MObject()
        mUseSigmaSA = OpenMaya.MObject()
        mSigmaS = OpenMaya.MObject()
        mSigmaA = OpenMaya.MObject()
        mUseSigmaTAlbedo = OpenMaya.MObject()
        mSigmaT = OpenMaya.MObject()
        mAlbedo = OpenMaya.MObject()
        mScale = OpenMaya.MObject()
        mInteriorMaterial = OpenMaya.MObject()
        mIntIOR = OpenMaya.MObject()
        mExteriorMaterial = OpenMaya.MObject()
        mExtIOR = OpenMaya.MObject()
        mIrrSamples = OpenMaya.MObject()

        mOutColor = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == dipole.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)
            
            outColorHandle = block.outputValue( dipole.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter

def nodeCreator():
    return dipole()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()

    try:
        dipole.mMaterial = eAttr.create("material", "mat")
        eAttr.setKeyable(1) 
        eAttr.setStorable(1)
        eAttr.setReadable(1)
        eAttr.setWritable(1)

        Materials = ["Apple",
            "Cream",
            "Skimmilk",
            "Spectralon",
            "Chicken1",
            "Ketchup",
            "Skin1",
            "Wholemilk",
            "Chicken2",
            "Potato",
            "Skin2",
            "Lowfat Milk",
            "Reduced Milk",
            "Regular Milk",
            "Espresso",
            "Mint Mocha Coffee",
            "Lowfat Soy Milk",
            "Regular Soy Milk",
            "Lowfat Chocolate Milk",
            "Regular Chocolate Milk",
            "Coke",
            "Pepsi Sprite", 
            "Gatorade",
            "Chardonnay",
            "White Zinfandel",
            "Merlot",
            "Budweiser Beer",
            "Coors Light Beer",
            "Clorox",
            "Apple Juice",
            "Cranberry Juice",
            "Grape Juice",
            "Ruby Grapefruit Juice",
            "White Grapefruit Juice",
            "Shampoo",
            "Strawberry Shampoo",
            "Head & Shoulders Shampoo",
            "Lemon Tea Powder",
            "Orange Juice Powder",
            "Pink Lemonade Powder",
            "Cappuccino Powder",
            "Salt Powder",
            "Sugar Powder",
            "Suisse Mocha"
        ]

        for i in range(len(Materials)):
            eAttr.addField(Materials[i], i)

        # Default to Skin1
        eAttr.setDefault(6)

        dipole.mUseSigmaSA = nAttr.create("useSigmaSA","ussa", OpenMaya.MFnNumericData.kBoolean, False)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        dipole.mSigmaS = nAttr.createColor("sigmaS", "ss")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        dipole.mSigmaA = nAttr.createColor("sigmaA", "sa")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        dipole.mUseSigmaTAlbedo = nAttr.create("useSigmaTAlbedo","usta", OpenMaya.MFnNumericData.kBoolean, False)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        dipole.mSigmaT = nAttr.createColor("sigmaT", "st")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        dipole.mAlbedo = nAttr.createColor("albedo", "albedo")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        dipole.mScale = nAttr.create("scale","sc", OpenMaya.MFnNumericData.kFloat, 1000.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        dipole.mInteriorMaterial = eAttr.create("interiorMaterial", "intmat")
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

        dipole.mIntIOR = nAttr.create("interiorIOR","intior", OpenMaya.MFnNumericData.kFloat, 1.3)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        dipole.mExteriorMaterial = eAttr.create("exteriorMaterial", "extmat")
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

        dipole.mExtIOR = nAttr.create("exteriorIOR","extior", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        dipole.mIrrSamples = nAttr.create("irrSamples","irrs", OpenMaya.MFnNumericData.kInt, 16)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)


        dipole.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)
    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        dipole.addAttribute(dipole.mMaterial)
        dipole.addAttribute(dipole.mUseSigmaSA)
        dipole.addAttribute(dipole.mSigmaS)
        dipole.addAttribute(dipole.mSigmaA)
        dipole.addAttribute(dipole.mUseSigmaTAlbedo)
        dipole.addAttribute(dipole.mSigmaT)
        dipole.addAttribute(dipole.mAlbedo)
        dipole.addAttribute(dipole.mScale)
        dipole.addAttribute(dipole.mInteriorMaterial)
        dipole.addAttribute(dipole.mIntIOR)
        dipole.addAttribute(dipole.mExteriorMaterial)
        dipole.addAttribute(dipole.mExtIOR)
        dipole.addAttribute(dipole.mIrrSamples)

        dipole.addAttribute(dipole.mOutColor)
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
