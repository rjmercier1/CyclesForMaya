import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginNodeName = "MitsubaHKShader"
kPluginNodeClassify = "/shader/surface"
kPluginNodeId = OpenMaya.MTypeId(0x87015)

class hk(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mMaterial = OpenMaya.MObject()
        mUseSigmaSA = OpenMaya.MObject()
        mSigmaS = OpenMaya.MObject()
        mSigmaA = OpenMaya.MObject()
        mUseSigmaTAlbedo = OpenMaya.MObject()
        mSigmaT = OpenMaya.MObject()
        mAlbedo = OpenMaya.MObject()
        mThickness = OpenMaya.MObject()

        mPhaseFunction = OpenMaya.MObject()
        mPhaseFunctionHGG = OpenMaya.MObject()
        mPhaseFunctionMicroFlakeStdDev = OpenMaya.MObject()

        mOutColor = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == hk.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)
            
            outColorHandle = block.outputValue( hk.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    return hk()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()

    try:
        hk.mMaterial = eAttr.create("material", "mat")
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

        hk.mUseSigmaSA = nAttr.create("useSigmaSA","ussa", OpenMaya.MFnNumericData.kBoolean, False)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        hk.mSigmaS = nAttr.createColor("sigmaS", "ss")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        hk.mSigmaA = nAttr.createColor("sigmaA", "sa")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        hk.mUseSigmaTAlbedo = nAttr.create("useSigmaTAlbedo","usta", OpenMaya.MFnNumericData.kBoolean, False)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        hk.mSigmaT = nAttr.createColor("sigmaT", "st")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        hk.mAlbedo = nAttr.createColor("albedo", "albedo")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(0.0,0.0,0.0)

        hk.mThickness = nAttr.create("thickness","t", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        hk.mThickness = nAttr.create("thickness","t", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        hk.mPhaseFunction = eAttr.create("phaseFunction", "pf")
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

        hk.mPhaseFunctionHGG = nAttr.create("phaseFunctionHGG","pfhgg", OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        hk.mPhaseFunctionMicroFlakeStdDev = nAttr.create("phaseFunctionMFSD","pfmfsd", OpenMaya.MFnNumericData.kFloat, 0.05)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        hk.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)
    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        hk.addAttribute(hk.mMaterial)
        hk.addAttribute(hk.mUseSigmaSA)
        hk.addAttribute(hk.mSigmaS)
        hk.addAttribute(hk.mSigmaA)
        hk.addAttribute(hk.mUseSigmaTAlbedo)
        hk.addAttribute(hk.mSigmaT)
        hk.addAttribute(hk.mAlbedo)
        hk.addAttribute(hk.mThickness)
        hk.addAttribute(hk.mPhaseFunction)
        hk.addAttribute(hk.mPhaseFunctionHGG)
        hk.addAttribute(hk.mPhaseFunctionMicroFlakeStdDev)
        hk.addAttribute(hk.mOutColor)
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
