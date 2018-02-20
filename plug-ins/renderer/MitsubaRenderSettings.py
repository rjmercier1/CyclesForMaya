import os
import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginNodeName = "MitsubaRenderSettings"
kPluginNodeId = OpenMaya.MTypeId(0x87021)

# Command
class MitsubaRenderSetting(OpenMayaMPx.MPxNode):
    # Class variables
    mMitsubaPath = OpenMaya.MObject()
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
        setattr(MitsubaRenderSetting, attribute, nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kBoolean, defaultBoolean) )
        nAttr.setStorable(1)
        nAttr.setWritable(1)
 
    @staticmethod
    def addIntegerAttribute(nAttr, attribute, longName, shortName, defaultInt=0):
        setattr(MitsubaRenderSetting, attribute, nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kInt, defaultInt) )
        nAttr.setStorable(1)
        nAttr.setWritable(1)

    @staticmethod
    def addFloatAttribute(nAttr, attribute, longName, shortName, defaultFloat=0.0):
        setattr(MitsubaRenderSetting, attribute, nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kFloat, defaultFloat) )
        nAttr.setStorable(1)
        nAttr.setWritable(1)

    @staticmethod
    def addColorAttribute(nAttr, attribute, longName, shortName, defaultRGB):
        setattr(MitsubaRenderSetting, attribute, nAttr.createColor(longName, shortName) )
        nAttr.setDefault(defaultRGB[0], defaultRGB[1], defaultRGB[2])
        nAttr.setStorable(1)
        nAttr.setWritable(1)

    @staticmethod
    def addStringAttribute(sAttr, attribute, longName, shortName, defaultString=""):
        stringFn = OpenMaya.MFnStringData()
        defaultText = stringFn.create(defaultString)
        setattr(MitsubaRenderSetting, attribute, sAttr.create(longName, shortName, OpenMaya.MFnData.kString, defaultText) )
        sAttr.setStorable(1)
        sAttr.setWritable(1)

def nodeCreator():
    return MitsubaRenderSetting()

def nodeInitializer():
    print "Render Settings initialize!"
    sAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    try:
        # Path to mitsuba executable
        defaultMitsubaPath = os.getenv( "MITSUBA_PATH" )
        if not defaultMitsubaPath:
            defaultMitsubaPath = ""
        MitsubaRenderSetting.addStringAttribute(sAttr, "mMitsubaPath", "mitsubaPath", "mp", defaultMitsubaPath)

        # Path to oiiotool executable
        defaultOIIOToolPath = os.getenv( "OIIOTOOL_PATH" )
        if not defaultOIIOToolPath:
            defaultOIIOToolPath = ""
        MitsubaRenderSetting.addStringAttribute(sAttr, "mOIIOToolPath", "oiiotoolPath", "oiiotp", defaultOIIOToolPath)

        # Integrator variables
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mIntegrator", "integrator", "ig", "Path Tracer")

        # Sampler variables
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mSampler", "sampler", "sm", "Independent Sampler")
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mSampleCount", "sampleCount", "sc", 8)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mSamplerDimension", "samplerDimension", "sd", 4)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mSamplerScramble", "samplerScramble", "ss", -1)

        # Reconstruction Filter variables
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mReconstructionFilter", "reconstructionFilter", "rf", "Box filter")

        # Overall controls
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mKeepTempFiles", "keepTempFiles", "kt", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mVerbose", "verbose", "vb", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mWritePartialResults", "writePartialResults", "wpr", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mWritePartialResultsInterval", "writePartialResultsInterval", "wpri", 15)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mBlockSize", "blockSize", "bs", 32)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mThreads", "threads", "th", 0)

        # Integrator - Path Tracer variables
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPathTracerUseInfiniteDepth", "iPathTracerUseInfiniteDepth", "iptuid", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPathTracerMaxDepth", "iPathTracerMaxDepth", "iptmd", -1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPathTracerRRDepth", "iPathTracerRRDepth", "iptrrd", 5)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPathTracerStrictNormals", "iPathTracerStrictNormals", "iptsn", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPathTracerHideEmitters", "iPathTracerHideEmitters", "ipthe", False)

        # Integrator - Bidirectional Path Tracer variables
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mBidrectionalPathTracerUseInfiniteDepth", "iBidrectionalPathTracerUseInfiniteDepth", "ibdptuid", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mBidrectionalPathTracerMaxDepth", "iBidrectionalPathTracerMaxDepth", "ibdptmd", -1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mBidrectionalPathTracerRRDepth", "iBidrectionalPathTracerRRDepth", "ibdptrrd", 5)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mBidrectionalPathTracerLightImage", "iBidrectionalPathTracerLightImage", "ibdptli", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mBidrectionalPathTracerSampleDirect", "iBidrectionalPathTracerSampleDirect", "ibdptsd", True)

        # Integrator - Ambient Occlusion variables
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mAmbientOcclusionShadingSamples", "iAmbientOcclusionShadingSamples", "iaoss", 1)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mAmbientOcclusionUseAutomaticRayLength", "iAmbientOcclusionUseAutomaticRayLength", "iaouarl", True)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mAmbientOcclusionRayLength", "iAmbientOcclusionRayLength", "iaorl", -1)

        # Integrator - Direct Illumination variables
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mDirectIlluminationShadingSamples", "iDirectIlluminationShadingSamples", "idiss", 1)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mDirectIlluminationUseEmitterAndBSDFSamples", "iDirectIlluminationUseEmitterAndBSDFSamples", "idiuebs", False)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mDirectIlluminationEmitterSamples", "iDirectIlluminationEmitterSamples", "idies", 1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mDirectIlluminationBSDFSamples", "iDirectIlluminationBSDFSamples", "idibs", 1)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mDirectIlluminationStrictNormals", "iDirectIlluminationStrictNormals", "idisn", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mDirectIlluminationHideEmitters", "iDirectIlluminationHideEmitters", "idihe", False)

        # Integrator - Simple Volumetric Path Tracer variables
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mSimpleVolumetricPathTracerUseInfiniteDepth", "iSimpleVolumetricPathTracerUseInfiniteDepth", "isvptuid", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mSimpleVolumetricPathTracerMaxDepth", "iSimpleVolumetricPathTracerMaxDepth", "isvptmd", -1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mSimpleVolumetricPathTracerRRDepth", "iSimpleVolumetricPathTracerRRDepth", "isvptrrd", 5)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mSimpleVolumetricPathTracerStrictNormals", "iSimpleVolumetricPathTracerStrictNormals", "isvptsn", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mSimpleVolumetricPathTracerHideEmitters", "iSimpleVolumetricPathTracerHideEmitters", "isvpthe", False)

        # Integrator - Volumetric Path Tracer variables
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mVolumetricPathTracerUseInfiniteDepth", "iVolumetricPathTracerUseInfiniteDepth", "ivptuid", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mVolumetricPathTracerMaxDepth", "iVolumetricPathTracerMaxDepth", "ivptmd", -1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mVolumetricPathTracerRRDepth", "iVolumetricPathTracerRRDepth", "ivptrrd", 5)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mVolumetricPathTracerStrictNormals", "iVolumetricPathTracerStrictNormals", "ivptsn", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mVolumetricPathTracerHideEmitters", "iVolumetricPathTracerHideEmitters", "ivpthe", False)

        # Integrator - Photon Map variables
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapDirectSamples", "iPhotonMapDirectSamples", "ipmds", 16)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapGlossySamples", "iPhotonMapGlossySamples", "ipmgs", 32)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPhotonMapUseInfiniteDepth", "iPhotonMapUseInfiniteDepth", "ipmuid", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapMaxDepth", "iPhotonMapMaxDepth", "ipmmd", -1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapGlobalPhotons", "iPhotonMapGlobalPhotons", "ipmgp", 250000)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapCausticPhotons", "iPhotonMapCausticPhotons", "ipmcp", 250000)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapVolumePhotons", "iPhotonMapVolumePhotons", "ipmvp", 250000)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mPhotonMapGlobalLookupRadius", "iPhotonMapGlobalLookupRadius", "ipmglr", 0.05)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mPhotonMapCausticLookupRadius", "iPhotonMapCausticLookupRadius", "ipmclr", 0.0125)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapLookupSize", "iPhotonMapLookupSize", "ipmls", 120)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapGranularity", "iPhotonMapGranularity", "ipmg", 0)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPhotonMapHideEmitters", "iPhotonMapHideEmitters", "ipmhe", False)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPhotonMapRRDepth", "iPhotonMapRRDepth", "ipmrrd", 5)

        # Integrator - Progressive Photon Map variables
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mProgressivePhotonMapUseInfiniteDepth", "iProgressivePhotonMapUseInfiniteDepth", "ippmuid", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mProgressivePhotonMapMaxDepth", "iProgressivePhotonMapMaxDepth", "ippmmd", -1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mProgressivePhotonMapPhotonCount", "iProgressivePhotonMapPhotonCount", "ippmpc", 250000)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mProgressivePhotonMapInitialRadius", "iProgressivePhotonMapInitialRadius", "ippmir", 0)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mProgressivePhotonMapAlpha", "iProgressivePhotonMapAlpha", "ippma", 0.7)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mProgressivePhotonMapGranularity", "iProgressivePhotonMapGranularity", "ippmg", 0)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mProgressivePhotonMapRRDepth", "iProgressivePhotonMapRRDepth", "ippmrrd", 5)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mProgressivePhotonMapMaxPasses", "iProgressivePhotonMapMaxPasses", "ippmmp", 10)

        # Integrator - Stochastic Progressive Photon Map variables
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mStochasticProgressivePhotonMapUseInfiniteDepth", "iStochasticProgressivePhotonMapUseInfiniteDepth", "isppmuid", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mStochasticProgressivePhotonMapMaxDepth", "iStochasticProgressivePhotonMapMaxDepth", "isppmmd", -1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mStochasticProgressivePhotonMapPhotonCount", "iStochasticProgressivePhotonMapPhotonCount", "isppmpc", 250000)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mStochasticProgressivePhotonMapInitialRadius", "iStochasticProgressivePhotonMapInitialRadius", "isppmir", 0)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mStochasticProgressivePhotonMapAlpha", "iStochasticProgressivePhotonMapAlpha", "isppma", 0.7)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mStochasticProgressivePhotonMapGranularity", "iStochasticProgressivePhotonMapGranularity", "isppmg", 0)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mStochasticProgressivePhotonMapRRDepth", "iStochasticProgressivePhotonMapRRDepth", "isppmrrd", 5)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mStochasticProgressivePhotonMapMaxPasses", "iStochasticProgressivePhotonMapMaxPasses", "isppmmp", 10)

        # Integrator - Primary Sample Space Metropolis Light Transport variables
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportBidirectional", "iPrimarySampleSpaceMetropolisLightTransportBidirectional", "ipssmltb", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth", "iPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth", "ipssmltuid", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportMaxDepth", "iPrimarySampleSpaceMetropolisLightTransportMaxDepth", "ipssmltmd", -1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportDirectSamples", "iPrimarySampleSpaceMetropolisLightTransportDirectSamples", "ipssmltds", 16)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportRRDepth", "iPrimarySampleSpaceMetropolisLightTransportRRDepth", "ipssmltrrd", 5)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportLuminanceSamples", "iPrimarySampleSpaceMetropolisLightTransportLuminanceSamples", "ipssmltls", 100000)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPrimarySampleSpaceMetropolisLightTransportTwoStage", "iPrimarySampleSpaceMetropolisLightTransportTwoStage", "ipssmltts", False)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mPrimarySampleSpaceMetropolisLightTransportPLarge", "iPrimarySampleSpaceMetropolisLightTransportPLarge", "ipssmltpl", 0.3)

        # Integrator - Path Space Metropolis Light Transport variables
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportUseInfiniteDepth", "iPathSpaceMetropolisLightTransportUseInfiniteDepth", "ipsmlttuid", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPathSpaceMetropolisLightTransportMaxDepth", "iPathSpaceMetropolisLightTransportMaxDepth", "ipsmltmd", -1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPathSpaceMetropolisLightTransportDirectSamples", "iPathSpaceMetropolisLightTransportDirectSamples", "ipsmltds", 16)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mPathSpaceMetropolisLightTransportLuminanceSamples", "iPathSpaceMetropolisLightTransportLuminanceSamples", "ipsmltls", 100000)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportTwoStage", "iPathSpaceMetropolisLightTransportTwoStage", "ipsmltts", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportBidirectionalMutation", "iPathSpaceMetropolisLightTransportBidirectionalMutation", "ipsmltbm", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportLensPurturbation", "iPathSpaceMetropolisLightTransportLensPurturbation", "ipsmltlp", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportMultiChainPurturbation", "iPathSpaceMetropolisLightTransportMultiChainPurturbation", "ipsmltmcp", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportCausticPurturbation", "iPathSpaceMetropolisLightTransportCausticPurturbation", "ipsmltcp", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mPathSpaceMetropolisLightTransportManifoldPurturbation", "iPathSpaceMetropolisLightTransportManifoldPurturbation", "ipsmltmp", False)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mPathSpaceMetropolisLightTransportLambda", "iPathSpaceMetropolisLightTransportLambda", "ipsmltl", 50)

        # Integrator - Energy Redistribution Path Tracing variables
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mEnergyRedistributionPathTracingUseInfiniteDepth", "iEnergyRedistributionPathTracingUseInfiniteDepth", "ierptuid", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mEnergyRedistributionPathTracingMaxDepth", "iEnergyRedistributionPathTracingMaxDepth", "ierptmd", -1)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mEnergyRedistributionPathTracingNumChains", "iEnergyRedistributionPathTracingNumChains", "ierptnc", 1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr,   "mEnergyRedistributionPathTracingMaxChains", "iEnergyRedistributionPathTracingMaxChains", "ierptmc", 0)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mEnergyRedistributionPathTracingChainLength", "iEnergyRedistributionPathTracingChainLength", "ierptcl", 1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mEnergyRedistributionPathTracingDirectSamples", "iEnergyRedistributionPathTracingDirectSamples", "ierptds", 16)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mEnergyRedistributionPathTracingLensPerturbation", "iEnergyRedistributionPathTracingLensPerturbation", "ierptlp", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mEnergyRedistributionPathTracingMultiChainPerturbation", "iEnergyRedistributionPathTracingMultiChainPerturbation", "ierptmcp", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mEnergyRedistributionPathTracingCausticPerturbation", "iEnergyRedistributionPathTracingCausticPerturbation", "ierptcp", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mEnergyRedistributionPathTracingManifoldPerturbation", "iEnergyRedistributionPathTracingManifoldPerturbation", "ierptmp", False)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mEnergyRedistributionPathTracingLambda", "iEnergyRedistributionPathTracingLambda", "ierptl", 50)

        # Integrator - Adjoint Particle Tracer variables
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mAdjointParticleTracerUseInfiniteDepth", "iAdjointParticleTracerUseInfiniteDepth", "iaptuid", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mAdjointParticleTracerMaxDepth", "iAdjointParticleTracerMaxDepth", "iaptmd", -1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mAdjointParticleTracerRRDepth", "iAdjointParticleTracerRRDepth", "iaptrrd", 5)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mAdjointParticleTracerGranularity", "iAdjointParticleTracerGranularity", "iaptg", 200000)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mAdjointParticleTracerBruteForce", "iAdjointParticleTracerBruteForce", "iaptbf", False)

        # Integrator - Virtual Point Light variables
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mVirtualPointLightUseInfiniteDepth", "iVirtualPointLightUseInfiniteDepth", "ivpluid", True)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mVirtualPointLightMaxDepth", "iVirtualPointLightMaxDepth", "ivplmd", -1)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mVirtualPointLightShadowMapResolution", "iVirtualPointLightShadowMapResolution", "ivplsmr", 512)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mVirtualPointLightClamping", "iVirtualPointLightClamping", "ivplc", 0.1)

        # Sensor variables
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mSensorOverride", "sensorOverride", "so", "None")

        # Sensor - Perspective Rdist variables
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mPerspectiveRdistKc2", "sPerspectiveRdistKc2", "sprkc2", 0.0)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mPerspectiveRdistKc4", "sPerspectiveRdistKc4", "sprkc4", 0.0)

        # Film variables
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mFilm", "film", "fm", "HDR Film")

        # Film - HDR variables
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mHDRFilmFileFormat", "fHDRFilmFileFormat", "fhff", "OpenEXR (.exr)")
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mHDRFilmPixelFormat", "fHDRFilmPixelFormat", "fhpf", "RGBA")
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mHDRFilmComponentFormat", "fHDRFilmComponentFormat", "fhcf", "Float 16")
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mHDRFilmAttachLog", "fHDRFilmAttachLog", "fhal", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mHDRFilmBanner", "fHDRFilmBanner", "fhb", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mHDRFilmHighQualityEdges", "fHDRFilmHighQualityEdges", "fhhqe", False)

        # Film - Tiled HDR variables
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mTiledHDRFilmPixelFormat", "fTiledHDRFilmPixelFormat", "fthpf", "RGBA")
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mTiledHDRFilmComponentFormat", "fTiledHDRFilmComponentFormat", "fthcf", "Float 16")

        # Film - LDR variables
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mLDRFilmFileFormat", "fLDRFilmFileFormat", "flff", "PNG (.png)")
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mLDRFilmPixelFormat", "fLDRFilmPixelFormat", "flpf", "RGB")
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mLDRFilmTonemapMethod", "fLDRFilmTonemapMethod", "fltm", "Gamma")
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mLDRFilmGamma", "fLDRFilmGamma", "flg", -1)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mLDRFilmExposure", "fLDRFilmExposure", "fle", 0.0)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mLDRFilmKey", "fLDRFilmKey", "flk", 0.18)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mLDRFilmBurn", "fLDRFilmBurn", "flb", 0.0)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mLDRFilmBanner", "fLDRFilmBanner", "flbn", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mLDRFilmHighQualityEdges", "fLDRFilmHighQualityEdges", "flhqe", False)

        # Film - Math variables
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mMathFilmFileFormat", "fMathFilmFileFormat", "fmfm", "Matlab (.m)")
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mMathFilmPixelFormat", "fMathFilmPixelFormat", "fmpf", "RGB")
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mMathFilmDigits", "fMathFilmDigits", "fmd", 4)
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mMathFilmVariable", "fMathFilmVariable", "fmv", "data")
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mMathFilmHighQualityEdges", "fMathFilmHighQualityEdges", "fmhqe", False)

        # Meta-Integrator variables
        MitsubaRenderSetting.addStringAttribute(sAttr,  "mMetaIntegrator", "metaIntegrator", "mi", "None")

        # Metaintegrator - Adaptive variables
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mAdaptiveMaxError", "miAdaptiveMaxError", "miame", 5.0)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mAdaptivePValue", "miAdaptivePValue", "miapv", 5.0)
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mAdaptiveMaxSampleFactor", "miAdaptiveMaxSampleFactor", "miamsf", 32)

        # Metaintegrator - Irradiance Cache variables
        MitsubaRenderSetting.addIntegerAttribute(nAttr, "mIrradianceCacheResolution", "miIrradianceCacheResolution", "miicr", 14)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mIrradianceCacheQuality", "miIrradianceCacheQuality", "miicq", 1.0)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mIrradianceCacheGradients", "miIrradianceCacheGradients", "miicg", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mIrradianceCacheClampNeighbor", "miIrradianceCacheClampNeighbor" , "miiccn", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mIrradianceCacheClampScreen", "miIrradianceCacheClampScreen", "miiccs", True)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mIrradianceCacheOverture", "miIrradianceCacheOverture", "miico", True)
        MitsubaRenderSetting.addFloatAttribute(nAttr,   "mIrradianceCacheQualityAdjustment", "miIrradianceCacheQualityAdjustment", "miicqa", 0.5)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mIrradianceCacheIndirectOnly", "miIrradianceCacheIndirectOnly", "miicio", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mIrradianceCacheDebug", "miIrradianceCacheDebug", "miicd", False)

        # Multichannel variables
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mMultichannel", "multichannel", "mc", False)

        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mMultichannelPosition", "multichannelPosition", "mcp", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mMultichannelRelPosition", "multichannelRelPosition", "mcrp", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mMultichannelDistance", "multichannelDistance", "mcd", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mMultichannelGeoNormal", "multichannelGeoNormal", "mcgn", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mMultichannelShadingNormal", "multichannelShadingNormal", "mcsn", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mMultichannelUV", "multichannelUV", "mcuv", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mMultichannelAlbedo", "multichannelAlbedo", "mca", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mMultichannelShapeIndex", "multichannelShapeIndex", "mcsi", False)
        MitsubaRenderSetting.addBooleanAttribute(nAttr, "mMultichannelPrimIndex", "multichannelPrimIndex", "mcpi", False)

    except:
        sys.stderr.write("Failed to create and add attributes\n")
        raise

    try:
        # Path to executables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMitsubaPath)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mOIIOToolPath)

        # Integrator variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mIntegrator)

        # Sampler variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mSampler)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mSampleCount)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mSamplerDimension)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mSamplerScramble)

        # Reconstruction Filter variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mReconstructionFilter)

        # Overall controls
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mKeepTempFiles)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mVerbose)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mWritePartialResults)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mWritePartialResultsInterval)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mBlockSize)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mThreads)

        # Integrator - Path Tracer variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathTracerUseInfiniteDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathTracerMaxDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathTracerRRDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathTracerStrictNormals)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathTracerHideEmitters)

        # Integrator - Bidirectional Path Tracer variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mBidrectionalPathTracerUseInfiniteDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mBidrectionalPathTracerMaxDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mBidrectionalPathTracerRRDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mBidrectionalPathTracerLightImage)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mBidrectionalPathTracerSampleDirect)

        # Integrator - Ambient Occlusion variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mAmbientOcclusionShadingSamples)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mAmbientOcclusionUseAutomaticRayLength)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mAmbientOcclusionRayLength)

        # Integrator - Direct Illumination variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mDirectIlluminationShadingSamples)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mDirectIlluminationUseEmitterAndBSDFSamples)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mDirectIlluminationEmitterSamples)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mDirectIlluminationBSDFSamples)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mDirectIlluminationStrictNormals)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mDirectIlluminationHideEmitters)

        # Integrator - Simple Volumetric Path Tracer variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mSimpleVolumetricPathTracerUseInfiniteDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mSimpleVolumetricPathTracerMaxDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mSimpleVolumetricPathTracerRRDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mSimpleVolumetricPathTracerStrictNormals)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mSimpleVolumetricPathTracerHideEmitters)

        # Integrator - Volumetric Path Tracer variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mVolumetricPathTracerUseInfiniteDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mVolumetricPathTracerMaxDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mVolumetricPathTracerRRDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mVolumetricPathTracerStrictNormals)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mVolumetricPathTracerHideEmitters)

        # Integrator - Photon Map variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapDirectSamples)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapGlossySamples)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapUseInfiniteDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapMaxDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapGlobalPhotons)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapCausticPhotons)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapVolumePhotons)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapGlobalLookupRadius)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapCausticLookupRadius)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapLookupSize)        
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapGranularity)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapHideEmitters)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPhotonMapRRDepth)

        # Integrator - Progressive Photon Map variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mProgressivePhotonMapUseInfiniteDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mProgressivePhotonMapMaxDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mProgressivePhotonMapPhotonCount)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mProgressivePhotonMapInitialRadius)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mProgressivePhotonMapAlpha)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mProgressivePhotonMapGranularity)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mProgressivePhotonMapRRDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mProgressivePhotonMapMaxPasses)

        # Integrator - Stochastic Progressive Photon Map variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mStochasticProgressivePhotonMapUseInfiniteDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mStochasticProgressivePhotonMapMaxDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mStochasticProgressivePhotonMapPhotonCount)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mStochasticProgressivePhotonMapInitialRadius)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mStochasticProgressivePhotonMapAlpha)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mStochasticProgressivePhotonMapGranularity)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mStochasticProgressivePhotonMapRRDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mStochasticProgressivePhotonMapMaxPasses)

        # Integrator - Primary Sample Space Metropolis Light Transport variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPrimarySampleSpaceMetropolisLightTransportBidirectional)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPrimarySampleSpaceMetropolisLightTransportMaxDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPrimarySampleSpaceMetropolisLightTransportDirectSamples)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPrimarySampleSpaceMetropolisLightTransportRRDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPrimarySampleSpaceMetropolisLightTransportLuminanceSamples)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPrimarySampleSpaceMetropolisLightTransportTwoStage)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPrimarySampleSpaceMetropolisLightTransportPLarge)

        # Integrator - Path Space Metropolis Light Transport variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathSpaceMetropolisLightTransportUseInfiniteDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathSpaceMetropolisLightTransportMaxDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathSpaceMetropolisLightTransportDirectSamples)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathSpaceMetropolisLightTransportLuminanceSamples)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathSpaceMetropolisLightTransportTwoStage)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathSpaceMetropolisLightTransportBidirectionalMutation)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathSpaceMetropolisLightTransportLensPurturbation)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathSpaceMetropolisLightTransportMultiChainPurturbation)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathSpaceMetropolisLightTransportCausticPurturbation)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathSpaceMetropolisLightTransportManifoldPurturbation)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPathSpaceMetropolisLightTransportLambda)

        # Integrator - Energy Redistribution Path Tracing variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mEnergyRedistributionPathTracingUseInfiniteDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mEnergyRedistributionPathTracingMaxDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mEnergyRedistributionPathTracingNumChains)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mEnergyRedistributionPathTracingMaxChains)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mEnergyRedistributionPathTracingChainLength)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mEnergyRedistributionPathTracingDirectSamples)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mEnergyRedistributionPathTracingLensPerturbation)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mEnergyRedistributionPathTracingMultiChainPerturbation)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mEnergyRedistributionPathTracingCausticPerturbation)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mEnergyRedistributionPathTracingManifoldPerturbation)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mEnergyRedistributionPathTracingLambda)

        # Integrator - Adjoint Particle Tracer variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mAdjointParticleTracerUseInfiniteDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mAdjointParticleTracerMaxDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mAdjointParticleTracerRRDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mAdjointParticleTracerGranularity)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mAdjointParticleTracerBruteForce)

        # Integrator - Virtual Point Light variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mVirtualPointLightUseInfiniteDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mVirtualPointLightMaxDepth)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mVirtualPointLightShadowMapResolution)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mVirtualPointLightClamping)

        # Sensor variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mSensorOverride)

        # Sensor - Perspective Rdist variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPerspectiveRdistKc2)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mPerspectiveRdistKc4)

        # Film variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mFilm)

        # Film - HDR variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mHDRFilmFileFormat)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mHDRFilmPixelFormat)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mHDRFilmComponentFormat)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mHDRFilmAttachLog)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mHDRFilmBanner)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mHDRFilmHighQualityEdges)

        # Film - Tiled HDR variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mTiledHDRFilmPixelFormat)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mTiledHDRFilmComponentFormat)

        # Film - LDR variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mLDRFilmFileFormat)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mLDRFilmPixelFormat)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mLDRFilmTonemapMethod)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mLDRFilmGamma)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mLDRFilmExposure)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mLDRFilmKey)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mLDRFilmBurn)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mLDRFilmBanner)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mLDRFilmHighQualityEdges)

        # Film - Math variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMathFilmFileFormat)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMathFilmPixelFormat)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMathFilmDigits)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMathFilmVariable)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMathFilmHighQualityEdges)

        # Meta-Integrator variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMetaIntegrator)

        # Metaintegrator - Adaptive variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mAdaptiveMaxError)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mAdaptivePValue)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mAdaptiveMaxSampleFactor)

        # Metaintegrator - Irradiance Cache variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mIrradianceCacheResolution)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mIrradianceCacheQuality)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mIrradianceCacheGradients)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mIrradianceCacheClampNeighbor)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mIrradianceCacheClampScreen)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mIrradianceCacheOverture)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mIrradianceCacheQualityAdjustment)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mIrradianceCacheIndirectOnly)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mIrradianceCacheDebug)

        # Multichannel variables
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMultichannel)

        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMultichannelPosition)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMultichannelRelPosition)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMultichannelDistance)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMultichannelGeoNormal)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMultichannelShadingNormal)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMultichannelUV)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMultichannelAlbedo)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMultichannelShapeIndex)
        MitsubaRenderSetting.addAttribute(MitsubaRenderSetting.mMultichannelPrimIndex)

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
                
