import os
import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginNodeName = "CyclesRenderSettings"
kPluginNodeId = OpenMaya.MTypeId(0x87021)

# Command
class CyclesRenderSetting(OpenMayaMPx.MPxNode):
    # Class variables
    mCyclesPath = OpenMaya.MObject()
    mOIIOToolPath = OpenMaya.MObject()

    # Integrator variables
    mIntegrator = OpenMaya.MObject()

    # Sampler variables
    mSampler = OpenMaya.MObject()
    mSampleCount = OpenMaya.MObject()
    mSamplerDimension = OpenMaya.MObject()
    mSamplerScramble = OpenMaya.MObject()

    # Reconstruction Filter variables
    mReconstructionFilter = OpenMaya.MObject()

    # Overall controls
    mKeepTempFiles = OpenMaya.MObject()
    mVerbose = OpenMaya.MObject()
    mWritePartialResults = OpenMaya.MObject()
    mWritePartialResultsInterval = OpenMaya.MObject()
    mBlockSize = OpenMaya.MObject()
    mThreads = OpenMaya.MObject()

    # Integrator - Path Tracer variables
    mPathTracerUseInfiniteDepth = OpenMaya.MObject()
    mPathTracerMaxDepth = OpenMaya.MObject()
    mPathTracerRRDepth = OpenMaya.MObject()
    mPathTracerStrictNormals = OpenMaya.MObject()
    mPathTracerHideEmitters = OpenMaya.MObject()

    # Integrator - Bidirectional Path Tracer variables
    mBidrectionalPathTracerUseInfiniteDepth = OpenMaya.MObject()
    mBidrectionalPathTracerMaxDepth = OpenMaya.MObject()
    mBidrectionalPathTracerRRDepth = OpenMaya.MObject()
    mBidrectionalPathTracerLightImage = OpenMaya.MObject()
    mBidrectionalPathTracerSampleDirect = OpenMaya.MObject()

    # Integrator - Ambient Occlusion variables
    mAmbientOcclusionShadingSamples = OpenMaya.MObject()
    mAmbientOcclusionUseAutomaticRayLength = OpenMaya.MObject()
    mAmbientOcclusionRayLength = OpenMaya.MObject()

    # Integrator - Direct Illumination variables
    mDirectIlluminationShadingSamples = OpenMaya.MObject()
    mDirectIlluminationUseEmitterAndBSDFSamples = OpenMaya.MObject()
    mDirectIlluminationEmitterSamples = OpenMaya.MObject()
    mDirectIlluminationBSDFSamples = OpenMaya.MObject()
    mDirectIlluminationStrictNormals = OpenMaya.MObject()
    mDirectIlluminationHideEmitters = OpenMaya.MObject()

    # Integrator - Simple Volumetric Path Tracer variables
    mSimpleVolumetricPathTracerUseInfiniteDepth = OpenMaya.MObject()
    mSimpleVolumetricPathTracerMaxDepth = OpenMaya.MObject()
    mSimpleVolumetricPathTracerRRDepth = OpenMaya.MObject()
    mSimpleVolumetricPathTracerStrictNormals = OpenMaya.MObject()
    mSimpleVolumetricPathTracerHideEmitters = OpenMaya.MObject()

    # Integrator - Volumetric Path Tracer variables
    mVolumetricPathTracerUseInfiniteDepth = OpenMaya.MObject()
    mVolumetricPathTracerMaxDepth = OpenMaya.MObject()
    mVolumetricPathTracerRRDepth = OpenMaya.MObject()
    mVolumetricPathTracerStrictNormals = OpenMaya.MObject()
    mVolumetricPathTracerHideEmitters = OpenMaya.MObject()

    # Integrator - Photon Map variables
    mPhotonMapDirectSamples = OpenMaya.MObject()
    mPhotonMapGlossySamples = OpenMaya.MObject()
    mPhotonMapUseInfiniteDepth = OpenMaya.MObject()
    mPhotonMapMaxDepth = OpenMaya.MObject()
    mPhotonMapGlobalPhotons = OpenMaya.MObject()
    mPhotonMapCausticPhotons = OpenMaya.MObject()
    mPhotonMapVolumePhotons = OpenMaya.MObject()
    mPhotonMapGlobalLookupRadius = OpenMaya.MObject()
    mPhotonMapCausticLookupRadius = OpenMaya.MObject()
    mPhotonMapLookupSize = OpenMaya.MObject()
    mPhotonMapGranularity = OpenMaya.MObject()
    mPhotonMapHideEmitters = OpenMaya.MObject()
    mPhotonMapRRDepth = OpenMaya.MObject()

    # Integrator - Progressive Photon Map variables
    mProgressivePhotonMapUseInfiniteDepth = OpenMaya.MObject()
    mProgressivePhotonMapMaxDepth = OpenMaya.MObject()
    mProgressivePhotonMapPhotonCount = OpenMaya.MObject()
    mProgressivePhotonMapInitialRadius = OpenMaya.MObject()
    mProgressivePhotonMapAlpha = OpenMaya.MObject()
    mProgressivePhotonMapGranularity = OpenMaya.MObject()
    mProgressivePhotonMapRRDepth = OpenMaya.MObject()
    mProgressivePhotonMapMaxPasses = OpenMaya.MObject()

    # Integrator - Stochastic Progressive Photon Map variables
    mStochasticProgressivePhotonMapUseInfiniteDepth = OpenMaya.MObject()
    mStochasticProgressivePhotonMapMaxDepth = OpenMaya.MObject()
    mStochasticProgressivePhotonMapPhotonCount = OpenMaya.MObject()
    mStochasticProgressivePhotonMapInitialRadius = OpenMaya.MObject()
    mStochasticProgressivePhotonMapAlpha = OpenMaya.MObject()
    mStochasticProgressivePhotonMapGranularity = OpenMaya.MObject()
    mStochasticProgressivePhotonMapRRDepth = OpenMaya.MObject()
    mStochasticProgressivePhotonMapMaxPasses = OpenMaya.MObject()

    # Integrator - Primary Sample Space Metropolis Light Transport variables
    mPrimarySampleSpaceMetropolisLightTransportBidirectional = OpenMaya.MObject()
    mPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth = OpenMaya.MObject()
    mPrimarySampleSpaceMetropolisLightTransportMaxDepth = OpenMaya.MObject()
    mPrimarySampleSpaceMetropolisLightTransportDirectSamples = OpenMaya.MObject()
    mPrimarySampleSpaceMetropolisLightTransportRRDepth = OpenMaya.MObject()
    mPrimarySampleSpaceMetropolisLightTransportLuminanceSamples = OpenMaya.MObject()
    mPrimarySampleSpaceMetropolisLightTransportTwoStage = OpenMaya.MObject()
    mPrimarySampleSpaceMetropolisLightTransportPLarge = OpenMaya.MObject()

    # Integrator - Path Space Metropolis Light Transport variables
    mPathSpaceMetropolisLightTransportUseInfiniteDepth = OpenMaya.MObject()
    mPathSpaceMetropolisLightTransportMaxDepth = OpenMaya.MObject()
    mPathSpaceMetropolisLightTransportDirectSamples = OpenMaya.MObject()
    mPathSpaceMetropolisLightTransportLuminanceSamples = OpenMaya.MObject()
    mPathSpaceMetropolisLightTransportTwoStage = OpenMaya.MObject()
    mPathSpaceMetropolisLightTransportBidirectionalMutation = OpenMaya.MObject()
    mPathSpaceMetropolisLightTransportLensPurturbation = OpenMaya.MObject()
    mPathSpaceMetropolisLightTransportMultiChainPurturbation = OpenMaya.MObject()
    mPathSpaceMetropolisLightTransportCausticPurturbation = OpenMaya.MObject()
    mPathSpaceMetropolisLightTransportManifoldPurturbation = OpenMaya.MObject()
    mPathSpaceMetropolisLightTransportLambda = OpenMaya.MObject()

    # Integrator - Energy Redistribution Path Tracing variables
    mEnergyRedistributionPathTracingUseInfiniteDepth = OpenMaya.MObject()
    mEnergyRedistributionPathTracingMaxDepth = OpenMaya.MObject()
    mEnergyRedistributionPathTracingNumChains = OpenMaya.MObject()
    mEnergyRedistributionPathTracingMaxChains = OpenMaya.MObject()
    mEnergyRedistributionPathTracingChainLength = OpenMaya.MObject()
    mEnergyRedistributionPathTracingDirectSamples = OpenMaya.MObject()
    mEnergyRedistributionPathTracingLensPerturbation = OpenMaya.MObject()
    mEnergyRedistributionPathTracingMultiChainPerturbation = OpenMaya.MObject()
    mEnergyRedistributionPathTracingCausticPerturbation = OpenMaya.MObject()
    mEnergyRedistributionPathTracingManifoldPerturbation = OpenMaya.MObject()
    mEnergyRedistributionPathTracingLambda = OpenMaya.MObject()

    # Integrator - Adjoint Particle Tracer variables
    mAdjointParticleTracerUseInfiniteDepth = OpenMaya.MObject()
    mAdjointParticleTracerMaxDepth = OpenMaya.MObject()
    mAdjointParticleTracerRRDepth = OpenMaya.MObject()
    mAdjointParticleTracerGranularity = OpenMaya.MObject()
    mAdjointParticleTracerBruteForce = OpenMaya.MObject()

    # Integrator - Virtual Point Light variables
    mVirtualPointLightUseInfiniteDepth = OpenMaya.MObject()
    mVirtualPointLightMaxDepth = OpenMaya.MObject()
    mVirtualPointLightShadowMapResolution = OpenMaya.MObject()
    mVirtualPointLightClamping = OpenMaya.MObject()

    # Sensor variables
    mSensorOverride = OpenMaya.MObject()

    # Sensor - Perspective Rdist variables
    mPerspectiveRdistKc2 = OpenMaya.MObject()
    mPerspectiveRdistKc4 = OpenMaya.MObject()

    # Film variables
    mFilm = OpenMaya.MObject()

    # Film - HDR variables
    mHDRFilmFileFormat = OpenMaya.MObject()
    mHDRFilmPixelFormat = OpenMaya.MObject()
    mHDRFilmComponentFormat = OpenMaya.MObject()
    mHDRFilmAttachLog = OpenMaya.MObject()
    mHDRFilmBanner = OpenMaya.MObject()
    mHDRFilmHighQualityEdges = OpenMaya.MObject()

    # Film - Tiled HDR variables
    mTiledHDRFilmPixelFormat = OpenMaya.MObject()
    mTiledHDRFilmComponentFormat = OpenMaya.MObject()

    # Film - LDR variables
    mLDRFilmFileFormat = OpenMaya.MObject()
    mLDRFilmPixelFormat = OpenMaya.MObject()
    mLDRFilmTonemapMethod = OpenMaya.MObject()
    mLDRFilmGamma = OpenMaya.MObject()
    mLDRFilmExposure = OpenMaya.MObject()
    mLDRFilmKey = OpenMaya.MObject()
    mLDRFilmBurn = OpenMaya.MObject()
    mLDRFilmBanner = OpenMaya.MObject()
    mLDRFilmHighQualityEdges = OpenMaya.MObject()

    # Film - Math variables
    mMathFilmFileFormat = OpenMaya.MObject()
    mMathFilmPixelFormat = OpenMaya.MObject()
    mMathFilmDigits = OpenMaya.MObject()
    mMathFilmVariable = OpenMaya.MObject()
    mMathFilmHighQualityEdges = OpenMaya.MObject()

    # Metaintegrator variables
    mMetaIntegrator = OpenMaya.MObject()

    # Metaintegrator - Adaptive variables
    mAdaptiveMaxError = OpenMaya.MObject()
    mAdaptivePValue = OpenMaya.MObject()
    mAdaptiveMaxSampleFactor = OpenMaya.MObject()

    # Metaintegrator - Irradiance Cache variables
    mIrradianceCacheResolution = OpenMaya.MObject()
    mIrradianceCacheQuality = OpenMaya.MObject()
    mIrradianceCacheGradients = OpenMaya.MObject()
    mIrradianceCacheClampNeighbor = OpenMaya.MObject()
    mIrradianceCacheClampScreen = OpenMaya.MObject()
    mIrradianceCacheOverture = OpenMaya.MObject()
    mIrradianceCacheQualityAdjustment = OpenMaya.MObject()
    mIrradianceCacheIndirectOnly = OpenMaya.MObject()
    mIrradianceCacheDebug = OpenMaya.MObject()

    # Multichannel variables
    mMultichannel = OpenMaya.MObject()
    mMultichannelPosition = OpenMaya.MObject()
    mMultichannelRelPosition = OpenMaya.MObject()
    mMultichannelDistance = OpenMaya.MObject()
    mMultichannelGeoNormal = OpenMaya.MObject()
    mMultichannelShadingNormal = OpenMaya.MObject()
    mMultichannelUV = OpenMaya.MObject()
    mMultichannelAlbedo = OpenMaya.MObject()
    mMultichannelShapeIndex = OpenMaya.MObject()
    mMultichannelPrimIndex = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # Invoked when the command is evaluated.
    def compute(self, plug, block):
        print "Render Settings evaluate!"
        return OpenMaya.kUnknownParameter

    @staticmethod
    def addBooleanAttribute(nAttr, attribute, longName, shortName, defaultBoolean=True):
        setattr(CyclesRenderSetting, attribute, nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kBoolean, defaultBoolean) )
        nAttr.setStorable(1)
        nAttr.setWritable(1)
 
    @staticmethod
    def addIntegerAttribute(nAttr, attribute, longName, shortName, defaultInt=0):
        setattr(CyclesRenderSetting, attribute, nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kInt, defaultInt) )
        nAttr.setStorable(1)
        nAttr.setWritable(1)

    @staticmethod
    def addFloatAttribute(nAttr, attribute, longName, shortName, defaultFloat=0.0):
        setattr(CyclesRenderSetting, attribute, nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kFloat, defaultFloat) )
        nAttr.setStorable(1)
        nAttr.setWritable(1)

    @staticmethod
    def addColorAttribute(nAttr, attribute, longName, shortName, defaultRGB):
        setattr(CyclesRenderSetting, attribute, nAttr.createColor(longName, shortName) )
        nAttr.setDefault(defaultRGB[0], defaultRGB[1], defaultRGB[2])
        nAttr.setStorable(1)
        nAttr.setWritable(1)

    @staticmethod
    def addStringAttribute(sAttr, attribute, longName, shortName, defaultString=""):
        stringFn = OpenMaya.MFnStringData()
        defaultText = stringFn.create(defaultString)
        setattr(CyclesRenderSetting, attribute, sAttr.create(longName, shortName, OpenMaya.MFnData.kString, defaultText) )
        sAttr.setStorable(1)
        sAttr.setWritable(1)

def nodeCreator():
    return CyclesRenderSetting()

def nodeInitializer():
    print "Render Settings initialize!"
    sAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    try:
        # Path to mitsuba executable
        defaultCyclesPath = os.getenv( "MITSUBA_PATH" )
        if not defaultCyclesPath:
            defaultCyclesPath = "cycles"
        CyclesRenderSetting.addStringAttribute(sAttr, "mCyclesPath", "mitsubaPath", "mp", defaultCyclesPath)

        # Path to oiiotool executable
        defaultOIIOToolPath = os.getenv( "OIIOTOOL_PATH" )
        if not defaultOIIOToolPath:
            defaultOIIOToolPath = ""
        CyclesRenderSetting.addStringAttribute(sAttr, "mOIIOToolPath", "oiiotoolPath", "oiiotp", defaultOIIOToolPath)

        # Integrator variables
        CyclesRenderSetting.addStringAttribute(sAttr,  "mIntegrator", "integrator", "ig", "Path Tracer")

        # Sampler variables
        CyclesRenderSetting.addStringAttribute(sAttr,  "mSampler", "sampler", "sm", "Independent Sampler")
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mSampleCount", "sampleCount", "sc", 8)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mSamplerDimension", "samplerDimension", "sd", 4)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mSamplerScramble", "samplerScramble", "ss", -1)

        # Reconstruction Filter variables
        CyclesRenderSetting.addStringAttribute(sAttr,  "mReconstructionFilter", "reconstructionFilter", "rf", "Box filter")

        # Overall controls
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mKeepTempFiles", "keepTempFiles", "kt", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mVerbose", "verbose", "vb", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mWritePartialResults", "writePartialResults", "wpr", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mWritePartialResultsInterval", "writePartialResultsInterval", "wpri", 15)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mBlockSize", "blockSize", "bs", 32)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mThreads", "threads", "th", 0)

        # Integrator - Path Tracer variables
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPathTracerUseInfiniteDepth", "iPathTracerUseInfiniteDepth", "iptuid", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPathTracerMaxDepth", "iPathTracerMaxDepth", "iptmd", -1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPathTracerRRDepth", "iPathTracerRRDepth", "iptrrd", 5)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPathTracerStrictNormals", "iPathTracerStrictNormals", "iptsn", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPathTracerHideEmitters", "iPathTracerHideEmitters", "ipthe", False)

        # Integrator - Bidirectional Path Tracer variables
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mBidrectionalPathTracerUseInfiniteDepth", "iBidrectionalPathTracerUseInfiniteDepth", "ibdptuid", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mBidrectionalPathTracerMaxDepth", "iBidrectionalPathTracerMaxDepth", "ibdptmd", -1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mBidrectionalPathTracerRRDepth", "iBidrectionalPathTracerRRDepth", "ibdptrrd", 5)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mBidrectionalPathTracerLightImage", "iBidrectionalPathTracerLightImage", "ibdptli", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mBidrectionalPathTracerSampleDirect", "iBidrectionalPathTracerSampleDirect", "ibdptsd", True)

        # Integrator - Ambient Occlusion variables
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mAmbientOcclusionShadingSamples", "iAmbientOcclusionShadingSamples", "iaoss", 1)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mAmbientOcclusionUseAutomaticRayLength", "iAmbientOcclusionUseAutomaticRayLength", "iaouarl", True)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mAmbientOcclusionRayLength", "iAmbientOcclusionRayLength", "iaorl", -1)

        # Integrator - Direct Illumination variables
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mDirectIlluminationShadingSamples", "iDirectIlluminationShadingSamples", "idiss", 1)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mDirectIlluminationUseEmitterAndBSDFSamples", "iDirectIlluminationUseEmitterAndBSDFSamples", "idiuebs", False)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mDirectIlluminationEmitterSamples", "iDirectIlluminationEmitterSamples", "idies", 1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mDirectIlluminationBSDFSamples", "iDirectIlluminationBSDFSamples", "idibs", 1)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mDirectIlluminationStrictNormals", "iDirectIlluminationStrictNormals", "idisn", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mDirectIlluminationHideEmitters", "iDirectIlluminationHideEmitters", "idihe", False)

        # Integrator - Simple Volumetric Path Tracer variables
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mSimpleVolumetricPathTracerUseInfiniteDepth", "iSimpleVolumetricPathTracerUseInfiniteDepth", "isvptuid", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mSimpleVolumetricPathTracerMaxDepth", "iSimpleVolumetricPathTracerMaxDepth", "isvptmd", -1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mSimpleVolumetricPathTracerRRDepth", "iSimpleVolumetricPathTracerRRDepth", "isvptrrd", 5)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mSimpleVolumetricPathTracerStrictNormals", "iSimpleVolumetricPathTracerStrictNormals", "isvptsn", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mSimpleVolumetricPathTracerHideEmitters", "iSimpleVolumetricPathTracerHideEmitters", "isvpthe", False)

        # Integrator - Volumetric Path Tracer variables
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mVolumetricPathTracerUseInfiniteDepth", "iVolumetricPathTracerUseInfiniteDepth", "ivptuid", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mVolumetricPathTracerMaxDepth", "iVolumetricPathTracerMaxDepth", "ivptmd", -1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mVolumetricPathTracerRRDepth", "iVolumetricPathTracerRRDepth", "ivptrrd", 5)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mVolumetricPathTracerStrictNormals", "iVolumetricPathTracerStrictNormals", "ivptsn", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mVolumetricPathTracerHideEmitters", "iVolumetricPathTracerHideEmitters", "ivpthe", False)

        # Integrator - Photon Map variables
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapDirectSamples", "iPhotonMapDirectSamples", "ipmds", 16)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapGlossySamples", "iPhotonMapGlossySamples", "ipmgs", 32)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPhotonMapUseInfiniteDepth", "iPhotonMapUseInfiniteDepth", "ipmuid", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapMaxDepth", "iPhotonMapMaxDepth", "ipmmd", -1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapGlobalPhotons", "iPhotonMapGlobalPhotons", "ipmgp", 250000)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapCausticPhotons", "iPhotonMapCausticPhotons", "ipmcp", 250000)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapVolumePhotons", "iPhotonMapVolumePhotons", "ipmvp", 250000)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mPhotonMapGlobalLookupRadius", "iPhotonMapGlobalLookupRadius", "ipmglr", 0.05)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mPhotonMapCausticLookupRadius", "iPhotonMapCausticLookupRadius", "ipmclr", 0.0125)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapLookupSize", "iPhotonMapLookupSize", "ipmls", 120)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapGranularity", "iPhotonMapGranularity", "ipmg", 0)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPhotonMapHideEmitters", "iPhotonMapHideEmitters", "ipmhe", False)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapRRDepth", "iPhotonMapRRDepth", "ipmrrd", 5)

        # Integrator - Progressive Photon Map variables
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mProgressivePhotonMapUseInfiniteDepth", "iProgressivePhotonMapUseInfiniteDepth", "ippmuid", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mProgressivePhotonMapMaxDepth", "iProgressivePhotonMapMaxDepth", "ippmmd", -1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mProgressivePhotonMapPhotonCount", "iProgressivePhotonMapPhotonCount", "ippmpc", 250000)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mProgressivePhotonMapInitialRadius", "iProgressivePhotonMapInitialRadius", "ippmir", 0)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mProgressivePhotonMapAlpha", "iProgressivePhotonMapAlpha", "ippma", 0.7)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mProgressivePhotonMapGranularity", "iProgressivePhotonMapGranularity", "ippmg", 0)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mProgressivePhotonMapRRDepth", "iProgressivePhotonMapRRDepth", "ippmrrd", 5)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mProgressivePhotonMapMaxPasses", "iProgressivePhotonMapMaxPasses", "ippmmp", 10)

        # Integrator - Stochastic Progressive Photon Map variables
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mStochasticProgressivePhotonMapUseInfiniteDepth", "iStochasticProgressivePhotonMapUseInfiniteDepth", "isppmuid", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mStochasticProgressivePhotonMapMaxDepth", "iStochasticProgressivePhotonMapMaxDepth", "isppmmd", -1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mStochasticProgressivePhotonMapPhotonCount", "iStochasticProgressivePhotonMapPhotonCount", "isppmpc", 250000)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mStochasticProgressivePhotonMapInitialRadius", "iStochasticProgressivePhotonMapInitialRadius", "isppmir", 0)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mStochasticProgressivePhotonMapAlpha", "iStochasticProgressivePhotonMapAlpha", "isppma", 0.7)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mStochasticProgressivePhotonMapGranularity", "iStochasticProgressivePhotonMapGranularity", "isppmg", 0)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mStochasticProgressivePhotonMapRRDepth", "iStochasticProgressivePhotonMapRRDepth", "isppmrrd", 5)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mStochasticProgressivePhotonMapMaxPasses", "iStochasticProgressivePhotonMapMaxPasses", "isppmmp", 10)

        # Integrator - Primary Sample Space Metropolis Light Transport variables
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportBidirectional", "iPrimarySampleSpaceMetropolisLightTransportBidirectional", "ipssmltb", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth", "iPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth", "ipssmltuid", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportMaxDepth", "iPrimarySampleSpaceMetropolisLightTransportMaxDepth", "ipssmltmd", -1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportDirectSamples", "iPrimarySampleSpaceMetropolisLightTransportDirectSamples", "ipssmltds", 16)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportRRDepth", "iPrimarySampleSpaceMetropolisLightTransportRRDepth", "ipssmltrrd", 5)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportLuminanceSamples", "iPrimarySampleSpaceMetropolisLightTransportLuminanceSamples", "ipssmltls", 100000)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportTwoStage", "iPrimarySampleSpaceMetropolisLightTransportTwoStage", "ipssmltts", False)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mPrimarySampleSpaceMetropolisLightTransportPLarge", "iPrimarySampleSpaceMetropolisLightTransportPLarge", "ipssmltpl", 0.3)

        # Integrator - Path Space Metropolis Light Transport variables
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportUseInfiniteDepth", "iPathSpaceMetropolisLightTransportUseInfiniteDepth", "ipsmlttuid", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPathSpaceMetropolisLightTransportMaxDepth", "iPathSpaceMetropolisLightTransportMaxDepth", "ipsmltmd", -1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPathSpaceMetropolisLightTransportDirectSamples", "iPathSpaceMetropolisLightTransportDirectSamples", "ipsmltds", 16)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mPathSpaceMetropolisLightTransportLuminanceSamples", "iPathSpaceMetropolisLightTransportLuminanceSamples", "ipsmltls", 100000)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportTwoStage", "iPathSpaceMetropolisLightTransportTwoStage", "ipsmltts", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportBidirectionalMutation", "iPathSpaceMetropolisLightTransportBidirectionalMutation", "ipsmltbm", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportLensPurturbation", "iPathSpaceMetropolisLightTransportLensPurturbation", "ipsmltlp", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportMultiChainPurturbation", "iPathSpaceMetropolisLightTransportMultiChainPurturbation", "ipsmltmcp", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportCausticPurturbation", "iPathSpaceMetropolisLightTransportCausticPurturbation", "ipsmltcp", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportManifoldPurturbation", "iPathSpaceMetropolisLightTransportManifoldPurturbation", "ipsmltmp", False)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mPathSpaceMetropolisLightTransportLambda", "iPathSpaceMetropolisLightTransportLambda", "ipsmltl", 50)

        # Integrator - Energy Redistribution Path Tracing variables
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mEnergyRedistributionPathTracingUseInfiniteDepth", "iEnergyRedistributionPathTracingUseInfiniteDepth", "ierptuid", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mEnergyRedistributionPathTracingMaxDepth", "iEnergyRedistributionPathTracingMaxDepth", "ierptmd", -1)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mEnergyRedistributionPathTracingNumChains", "iEnergyRedistributionPathTracingNumChains", "ierptnc", 1)
        CyclesRenderSetting.addIntegerAttribute(nAttr,   "mEnergyRedistributionPathTracingMaxChains", "iEnergyRedistributionPathTracingMaxChains", "ierptmc", 0)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mEnergyRedistributionPathTracingChainLength", "iEnergyRedistributionPathTracingChainLength", "ierptcl", 1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mEnergyRedistributionPathTracingDirectSamples", "iEnergyRedistributionPathTracingDirectSamples", "ierptds", 16)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mEnergyRedistributionPathTracingLensPerturbation", "iEnergyRedistributionPathTracingLensPerturbation", "ierptlp", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mEnergyRedistributionPathTracingMultiChainPerturbation", "iEnergyRedistributionPathTracingMultiChainPerturbation", "ierptmcp", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mEnergyRedistributionPathTracingCausticPerturbation", "iEnergyRedistributionPathTracingCausticPerturbation", "ierptcp", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mEnergyRedistributionPathTracingManifoldPerturbation", "iEnergyRedistributionPathTracingManifoldPerturbation", "ierptmp", False)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mEnergyRedistributionPathTracingLambda", "iEnergyRedistributionPathTracingLambda", "ierptl", 50)

        # Integrator - Adjoint Particle Tracer variables
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mAdjointParticleTracerUseInfiniteDepth", "iAdjointParticleTracerUseInfiniteDepth", "iaptuid", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mAdjointParticleTracerMaxDepth", "iAdjointParticleTracerMaxDepth", "iaptmd", -1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mAdjointParticleTracerRRDepth", "iAdjointParticleTracerRRDepth", "iaptrrd", 5)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mAdjointParticleTracerGranularity", "iAdjointParticleTracerGranularity", "iaptg", 200000)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mAdjointParticleTracerBruteForce", "iAdjointParticleTracerBruteForce", "iaptbf", False)

        # Integrator - Virtual Point Light variables
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mVirtualPointLightUseInfiniteDepth", "iVirtualPointLightUseInfiniteDepth", "ivpluid", True)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mVirtualPointLightMaxDepth", "iVirtualPointLightMaxDepth", "ivplmd", -1)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mVirtualPointLightShadowMapResolution", "iVirtualPointLightShadowMapResolution", "ivplsmr", 512)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mVirtualPointLightClamping", "iVirtualPointLightClamping", "ivplc", 0.1)

        # Sensor variables
        CyclesRenderSetting.addStringAttribute(sAttr,  "mSensorOverride", "sensorOverride", "so", "None")

        # Sensor - Perspective Rdist variables
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mPerspectiveRdistKc2", "sPerspectiveRdistKc2", "sprkc2", 0.0)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mPerspectiveRdistKc4", "sPerspectiveRdistKc4", "sprkc4", 0.0)

        # Film variables
        CyclesRenderSetting.addStringAttribute(sAttr,  "mFilm", "film", "fm", "HDR Film")

        # Film - HDR variables
        CyclesRenderSetting.addStringAttribute(sAttr,  "mHDRFilmFileFormat", "fHDRFilmFileFormat", "fhff", "OpenEXR (.exr)")
        CyclesRenderSetting.addStringAttribute(sAttr,  "mHDRFilmPixelFormat", "fHDRFilmPixelFormat", "fhpf", "RGBA")
        CyclesRenderSetting.addStringAttribute(sAttr,  "mHDRFilmComponentFormat", "fHDRFilmComponentFormat", "fhcf", "Float 16")
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mHDRFilmAttachLog", "fHDRFilmAttachLog", "fhal", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mHDRFilmBanner", "fHDRFilmBanner", "fhb", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mHDRFilmHighQualityEdges", "fHDRFilmHighQualityEdges", "fhhqe", False)

        # Film - Tiled HDR variables
        CyclesRenderSetting.addStringAttribute(sAttr,  "mTiledHDRFilmPixelFormat", "fTiledHDRFilmPixelFormat", "fthpf", "RGBA")
        CyclesRenderSetting.addStringAttribute(sAttr,  "mTiledHDRFilmComponentFormat", "fTiledHDRFilmComponentFormat", "fthcf", "Float 16")

        # Film - LDR variables
        CyclesRenderSetting.addStringAttribute(sAttr,  "mLDRFilmFileFormat", "fLDRFilmFileFormat", "flff", "PNG (.png)")
        CyclesRenderSetting.addStringAttribute(sAttr,  "mLDRFilmPixelFormat", "fLDRFilmPixelFormat", "flpf", "RGB")
        CyclesRenderSetting.addStringAttribute(sAttr,  "mLDRFilmTonemapMethod", "fLDRFilmTonemapMethod", "fltm", "Gamma")
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mLDRFilmGamma", "fLDRFilmGamma", "flg", -1)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mLDRFilmExposure", "fLDRFilmExposure", "fle", 0.0)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mLDRFilmKey", "fLDRFilmKey", "flk", 0.18)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mLDRFilmBurn", "fLDRFilmBurn", "flb", 0.0)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mLDRFilmBanner", "fLDRFilmBanner", "flbn", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mLDRFilmHighQualityEdges", "fLDRFilmHighQualityEdges", "flhqe", False)

        # Film - Math variables
        CyclesRenderSetting.addStringAttribute(sAttr,  "mMathFilmFileFormat", "fMathFilmFileFormat", "fmfm", "Matlab (.m)")
        CyclesRenderSetting.addStringAttribute(sAttr,  "mMathFilmPixelFormat", "fMathFilmPixelFormat", "fmpf", "RGB")
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mMathFilmDigits", "fMathFilmDigits", "fmd", 4)
        CyclesRenderSetting.addStringAttribute(sAttr,  "mMathFilmVariable", "fMathFilmVariable", "fmv", "data")
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mMathFilmHighQualityEdges", "fMathFilmHighQualityEdges", "fmhqe", False)

        # Meta-Integrator variables
        CyclesRenderSetting.addStringAttribute(sAttr,  "mMetaIntegrator", "metaIntegrator", "mi", "None")

        # Metaintegrator - Adaptive variables
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mAdaptiveMaxError", "miAdaptiveMaxError", "miame", 5.0)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mAdaptivePValue", "miAdaptivePValue", "miapv", 5.0)
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mAdaptiveMaxSampleFactor", "miAdaptiveMaxSampleFactor", "miamsf", 32)

        # Metaintegrator - Irradiance Cache variables
        CyclesRenderSetting.addIntegerAttribute(nAttr, "mIrradianceCacheResolution", "miIrradianceCacheResolution", "miicr", 14)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mIrradianceCacheQuality", "miIrradianceCacheQuality", "miicq", 1.0)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mIrradianceCacheGradients", "miIrradianceCacheGradients", "miicg", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mIrradianceCacheClampNeighbor", "miIrradianceCacheClampNeighbor" , "miiccn", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mIrradianceCacheClampScreen", "miIrradianceCacheClampScreen", "miiccs", True)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mIrradianceCacheOverture", "miIrradianceCacheOverture", "miico", True)
        CyclesRenderSetting.addFloatAttribute(nAttr,   "mIrradianceCacheQualityAdjustment", "miIrradianceCacheQualityAdjustment", "miicqa", 0.5)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mIrradianceCacheIndirectOnly", "miIrradianceCacheIndirectOnly", "miicio", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mIrradianceCacheDebug", "miIrradianceCacheDebug", "miicd", False)

        # Multichannel variables
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mMultichannel", "multichannel", "mc", False)

        CyclesRenderSetting.addBooleanAttribute(nAttr, "mMultichannelPosition", "multichannelPosition", "mcp", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mMultichannelRelPosition", "multichannelRelPosition", "mcrp", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mMultichannelDistance", "multichannelDistance", "mcd", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mMultichannelGeoNormal", "multichannelGeoNormal", "mcgn", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mMultichannelShadingNormal", "multichannelShadingNormal", "mcsn", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mMultichannelUV", "multichannelUV", "mcuv", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mMultichannelAlbedo", "multichannelAlbedo", "mca", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mMultichannelShapeIndex", "multichannelShapeIndex", "mcsi", False)
        CyclesRenderSetting.addBooleanAttribute(nAttr, "mMultichannelPrimIndex", "multichannelPrimIndex", "mcpi", False)

    except:
        sys.stderr.write("Failed to create and add attributes\n")
        raise

    try:
        # Path to executables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mCyclesPath)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mOIIOToolPath)

        # Integrator variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mIntegrator)

        # Sampler variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mSampler)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mSampleCount)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mSamplerDimension)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mSamplerScramble)

        # Reconstruction Filter variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mReconstructionFilter)

        # Overall controls
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mKeepTempFiles)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mVerbose)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mWritePartialResults)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mWritePartialResultsInterval)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mBlockSize)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mThreads)

        # Integrator - Path Tracer variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathTracerUseInfiniteDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathTracerMaxDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathTracerRRDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathTracerStrictNormals)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathTracerHideEmitters)

        # Integrator - Bidirectional Path Tracer variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mBidrectionalPathTracerUseInfiniteDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mBidrectionalPathTracerMaxDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mBidrectionalPathTracerRRDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mBidrectionalPathTracerLightImage)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mBidrectionalPathTracerSampleDirect)

        # Integrator - Ambient Occlusion variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mAmbientOcclusionShadingSamples)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mAmbientOcclusionUseAutomaticRayLength)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mAmbientOcclusionRayLength)

        # Integrator - Direct Illumination variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mDirectIlluminationShadingSamples)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mDirectIlluminationUseEmitterAndBSDFSamples)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mDirectIlluminationEmitterSamples)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mDirectIlluminationBSDFSamples)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mDirectIlluminationStrictNormals)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mDirectIlluminationHideEmitters)

        # Integrator - Simple Volumetric Path Tracer variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mSimpleVolumetricPathTracerUseInfiniteDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mSimpleVolumetricPathTracerMaxDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mSimpleVolumetricPathTracerRRDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mSimpleVolumetricPathTracerStrictNormals)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mSimpleVolumetricPathTracerHideEmitters)

        # Integrator - Volumetric Path Tracer variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mVolumetricPathTracerUseInfiniteDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mVolumetricPathTracerMaxDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mVolumetricPathTracerRRDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mVolumetricPathTracerStrictNormals)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mVolumetricPathTracerHideEmitters)

        # Integrator - Photon Map variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapDirectSamples)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapGlossySamples)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapUseInfiniteDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapMaxDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapGlobalPhotons)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapCausticPhotons)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapVolumePhotons)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapGlobalLookupRadius)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapCausticLookupRadius)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapLookupSize)        
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapGranularity)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapHideEmitters)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPhotonMapRRDepth)

        # Integrator - Progressive Photon Map variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mProgressivePhotonMapUseInfiniteDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mProgressivePhotonMapMaxDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mProgressivePhotonMapPhotonCount)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mProgressivePhotonMapInitialRadius)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mProgressivePhotonMapAlpha)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mProgressivePhotonMapGranularity)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mProgressivePhotonMapRRDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mProgressivePhotonMapMaxPasses)

        # Integrator - Stochastic Progressive Photon Map variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mStochasticProgressivePhotonMapUseInfiniteDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mStochasticProgressivePhotonMapMaxDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mStochasticProgressivePhotonMapPhotonCount)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mStochasticProgressivePhotonMapInitialRadius)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mStochasticProgressivePhotonMapAlpha)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mStochasticProgressivePhotonMapGranularity)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mStochasticProgressivePhotonMapRRDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mStochasticProgressivePhotonMapMaxPasses)

        # Integrator - Primary Sample Space Metropolis Light Transport variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPrimarySampleSpaceMetropolisLightTransportBidirectional)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPrimarySampleSpaceMetropolisLightTransportMaxDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPrimarySampleSpaceMetropolisLightTransportDirectSamples)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPrimarySampleSpaceMetropolisLightTransportRRDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPrimarySampleSpaceMetropolisLightTransportLuminanceSamples)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPrimarySampleSpaceMetropolisLightTransportTwoStage)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPrimarySampleSpaceMetropolisLightTransportPLarge)

        # Integrator - Path Space Metropolis Light Transport variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathSpaceMetropolisLightTransportUseInfiniteDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathSpaceMetropolisLightTransportMaxDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathSpaceMetropolisLightTransportDirectSamples)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathSpaceMetropolisLightTransportLuminanceSamples)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathSpaceMetropolisLightTransportTwoStage)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathSpaceMetropolisLightTransportBidirectionalMutation)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathSpaceMetropolisLightTransportLensPurturbation)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathSpaceMetropolisLightTransportMultiChainPurturbation)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathSpaceMetropolisLightTransportCausticPurturbation)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathSpaceMetropolisLightTransportManifoldPurturbation)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPathSpaceMetropolisLightTransportLambda)

        # Integrator - Energy Redistribution Path Tracing variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mEnergyRedistributionPathTracingUseInfiniteDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mEnergyRedistributionPathTracingMaxDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mEnergyRedistributionPathTracingNumChains)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mEnergyRedistributionPathTracingMaxChains)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mEnergyRedistributionPathTracingChainLength)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mEnergyRedistributionPathTracingDirectSamples)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mEnergyRedistributionPathTracingLensPerturbation)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mEnergyRedistributionPathTracingMultiChainPerturbation)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mEnergyRedistributionPathTracingCausticPerturbation)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mEnergyRedistributionPathTracingManifoldPerturbation)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mEnergyRedistributionPathTracingLambda)

        # Integrator - Adjoint Particle Tracer variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mAdjointParticleTracerUseInfiniteDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mAdjointParticleTracerMaxDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mAdjointParticleTracerRRDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mAdjointParticleTracerGranularity)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mAdjointParticleTracerBruteForce)

        # Integrator - Virtual Point Light variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mVirtualPointLightUseInfiniteDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mVirtualPointLightMaxDepth)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mVirtualPointLightShadowMapResolution)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mVirtualPointLightClamping)

        # Sensor variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mSensorOverride)

        # Sensor - Perspective Rdist variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPerspectiveRdistKc2)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mPerspectiveRdistKc4)

        # Film variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mFilm)

        # Film - HDR variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mHDRFilmFileFormat)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mHDRFilmPixelFormat)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mHDRFilmComponentFormat)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mHDRFilmAttachLog)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mHDRFilmBanner)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mHDRFilmHighQualityEdges)

        # Film - Tiled HDR variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mTiledHDRFilmPixelFormat)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mTiledHDRFilmComponentFormat)

        # Film - LDR variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mLDRFilmFileFormat)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mLDRFilmPixelFormat)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mLDRFilmTonemapMethod)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mLDRFilmGamma)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mLDRFilmExposure)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mLDRFilmKey)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mLDRFilmBurn)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mLDRFilmBanner)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mLDRFilmHighQualityEdges)

        # Film - Math variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMathFilmFileFormat)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMathFilmPixelFormat)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMathFilmDigits)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMathFilmVariable)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMathFilmHighQualityEdges)

        # Meta-Integrator variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMetaIntegrator)

        # Metaintegrator - Adaptive variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mAdaptiveMaxError)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mAdaptivePValue)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mAdaptiveMaxSampleFactor)

        # Metaintegrator - Irradiance Cache variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mIrradianceCacheResolution)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mIrradianceCacheQuality)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mIrradianceCacheGradients)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mIrradianceCacheClampNeighbor)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mIrradianceCacheClampScreen)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mIrradianceCacheOverture)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mIrradianceCacheQualityAdjustment)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mIrradianceCacheIndirectOnly)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mIrradianceCacheDebug)

        # Multichannel variables
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMultichannel)

        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMultichannelPosition)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMultichannelRelPosition)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMultichannelDistance)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMultichannelGeoNormal)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMultichannelShadingNormal)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMultichannelUV)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMultichannelAlbedo)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMultichannelShapeIndex)
        CyclesRenderSetting.addAttribute(CyclesRenderSetting.mMultichannelPrimIndex)

    except:
        sys.stderr.write("Failed to add attributes\n")
        raise
        
# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeName, 
                              kPluginNodeId, 
                              nodeCreator, 
                              nodeInitializer, 
                              OpenMayaMPx.MPxNode.kDependNode )
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
                
