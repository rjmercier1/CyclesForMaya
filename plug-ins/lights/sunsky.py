import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeName = "MitsubaSunsky"
kPluginNodeClassify = "light/general"
kPluginNodeId = OpenMaya.MTypeId(0x87031)

class sunsky(OpenMayaMPx.MPxNode):
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        mVisibility = OpenMaya.MObject()
        mUseSun = OpenMaya.MObject()
        mUseSky = OpenMaya.MObject()
        mTurbidity = OpenMaya.MObject()
        mAlbedo = OpenMaya.MObject()
        mDate = OpenMaya.MObject()
        mTime = OpenMaya.MObject()
        mLatitude = OpenMaya.MObject()
        mLongitude = OpenMaya.MObject()
        mTimezone = OpenMaya.MObject()
        mStretch = OpenMaya.MObject()
        mResolution = OpenMaya.MObject()
        mSunScale = OpenMaya.MObject()
        mSkyScale = OpenMaya.MObject()
        mSunRadiusScale = OpenMaya.MObject()
        mOutColor = OpenMaya.MObject()

    def compute(self, plug, block):
        if plug == sunsky.mOutColor:
            resultColor = OpenMaya.MFloatVector(0.0,0.0,0.0)
            
            outColorHandle = block.outputValue( sunsky.mOutColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
        else:
            return OpenMaya.kUnknownParameter

def nodeCreator():
    return sunsky()

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()

    try:
        sunsky.mVisibility = nAttr.create("visibility", "visibility", OpenMaya.MFnNumericData.kBoolean, True)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(0)
        nAttr.setWritable(1)

        sunsky.mUseSun = nAttr.create("useSun", "sun", OpenMaya.MFnNumericData.kBoolean, True)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        sunsky.mUseSky = nAttr.create("useSky", "sky", OpenMaya.MFnNumericData.kBoolean, True)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        sunsky.mTurbidity = nAttr.create("turbidity","turb", OpenMaya.MFnNumericData.kFloat, 3.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        sunsky.mAlbedo = nAttr.createColor("albedo", "alb")
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(.15,.15,.15)

        sunsky.mDate = nAttr.create("date","d", OpenMaya.MFnNumericData.k3Int)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(2010,7,10)

        sunsky.mTime = nAttr.create("time","t", OpenMaya.MFnNumericData.k3Float)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(15.0,00.0,00.0)

        sunsky.mLatitude = nAttr.create("latitude","lat", OpenMaya.MFnNumericData.kFloat, 34.022)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        sunsky.mLongitude = nAttr.create("longitude","lon", OpenMaya.MFnNumericData.kFloat, 118.481)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        sunsky.mTimezone = nAttr.create("timezone","tzone", OpenMaya.MFnNumericData.kFloat, 8.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        sunsky.mStretch = nAttr.create("stretch","stretch", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        sunsky.mResolution = nAttr.create("resolution","res", OpenMaya.MFnNumericData.kInt)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)
        nAttr.setDefault(512)

        sunsky.mSunScale = nAttr.create("sunScale","sunScale", OpenMaya.MFnNumericData.kFloat, 4.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        sunsky.mSkyScale = nAttr.create("skyScale","skyScale", OpenMaya.MFnNumericData.kFloat, 4.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        sunsky.mSunRadiusScale = nAttr.create("sunRadiusScale","sunRadiusScale", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setKeyable(1) 
        nAttr.setStorable(1)
        nAttr.setReadable(1)
        nAttr.setWritable(1)

        sunsky.mOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setReadable(1)
        nAttr.setWritable(0)

    except:
        sys.stderr.write("Failed to create attributes\n")
        raise

    try:
        sunsky.addAttribute(sunsky.mVisibility)
        sunsky.addAttribute(sunsky.mUseSun)
        sunsky.addAttribute(sunsky.mUseSky)
        sunsky.addAttribute(sunsky.mTurbidity)
        sunsky.addAttribute(sunsky.mAlbedo)
        sunsky.addAttribute(sunsky.mDate)
        sunsky.addAttribute(sunsky.mTime)
        sunsky.addAttribute(sunsky.mLatitude)
        sunsky.addAttribute(sunsky.mLongitude)
        sunsky.addAttribute(sunsky.mTimezone)
        sunsky.addAttribute(sunsky.mStretch)
        sunsky.addAttribute(sunsky.mResolution)
        sunsky.addAttribute(sunsky.mSunScale)
        sunsky.addAttribute(sunsky.mSkyScale)
        sunsky.addAttribute(sunsky.mSunRadiusScale)
        sunsky.addAttribute(sunsky.mOutColor)
    except:
        sys.stderr.write("Failed to add attributes\n")
        raise

    try:
        sunsky.attributeAffects (sunsky.mTime, sunsky.mOutColor)
    except:
        sys.stderr.write("Failed in setting attributeAffects\n")
        raise

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeName, kPluginNodeId, nodeCreator, 
                    nodeInitializer, OpenMayaMPx.MPxNode.kDependNode, kPluginClassify )
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
