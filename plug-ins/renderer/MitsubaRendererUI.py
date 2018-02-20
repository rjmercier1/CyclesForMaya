import getpass
import inspect
import os
import re
import struct
import sys

import maya.cmds as cmds
import maya.mel as mel

##################################################

from MitsubaRenderer import createRenderSettingsNode, getRenderSettingsNode

global renderSettings

##################################################

#Main render settings window
global renderSettingsWindow
global renderWindow
global renderedImage
#Handle to the active integrator
global integrator
global integratorMenu
#List of possible integrators (stored as frameLayouts)
global integratorFrames

global sampler
global samplerMenu
global samplerFrames

global sampleCount

global filmFrames

global rfilter
global rfilterMenu

global sensorOverrideMenu
global sensorOverrideFrames

global metaIntegratorFrames

def createIntegratorFrameAmbientOcclusion():
    existingShadingSamples = cmds.getAttr( "%s.%s" % (renderSettings, "iAmbientOcclusionShadingSamples"))
    existingUseAutomaticRayLength = cmds.getAttr( "%s.%s" % (renderSettings, "iAmbientOcclusionUseAutomaticRayLength"))
    existingRayLength = cmds.getAttr( "%s.%s" % (renderSettings, "iAmbientOcclusionRayLength"))

    aoSettings = cmds.frameLayout(label="Ambient Occlusion", cll=True, visible=False)

    cmds.intFieldGrp(numberOfFields=1, label="Shading Samples", value1=existingShadingSamples,
        changeCommand=lambda (x): getIntFieldGroup(None, "iAmbientOcclusionShadingSamples", x))

    cmds.checkBox("Use Automatic Ray Length", value=existingUseAutomaticRayLength, 
        changeCommand=lambda (x): getCheckBox(None, "iAmbientOcclusionUseAutomaticRayLength", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Ray Length", value1=existingRayLength,
        changeCommand=lambda (x): getFloatFieldGroup(None, "iAmbientOcclusionRayLength", x))

    cmds.setParent('..')

    return aoSettings

def createIntegratorFrameDirectIllumination():
    iDirectIlluminationShadingSamples = cmds.getAttr("%s.%s" % (renderSettings, "iDirectIlluminationShadingSamples"))
    iDirectIlluminationUseEmitterAndBSDFSamples = cmds.getAttr("%s.%s" % (renderSettings, "iDirectIlluminationUseEmitterAndBSDFSamples"))
    iDirectIlluminationEmitterSamples = cmds.getAttr("%s.%s" % (renderSettings, "iDirectIlluminationEmitterSamples"))
    iDirectIlluminationBSDFSamples = cmds.getAttr("%s.%s" % (renderSettings, "iDirectIlluminationBSDFSamples"))
    iDirectIlluminationStrictNormals = cmds.getAttr("%s.%s" % (renderSettings, "iDirectIlluminationStrictNormals"))
    iDirectIlluminationHideEmitters = cmds.getAttr("%s.%s" % (renderSettings, "iDirectIlluminationHideEmitters"))

    diSettings = cmds.frameLayout(label="Direct Illumination", cll=True, visible=False)

    cmds.intFieldGrp(numberOfFields=1, label="Shading Samples", value1=iDirectIlluminationShadingSamples, 
        changeCommand=lambda (x): getIntFieldGroup(None, "iDirectIlluminationShadingSamples", x))

    cmds.checkBox(label = "Use Emitter and BSDF Samples", value=iDirectIlluminationUseEmitterAndBSDFSamples, 
        changeCommand=lambda (x): getCheckBox(None, "iDirectIlluminationUseEmitterAndBSDFSamples", x))

    cmds.intFieldGrp(numberOfFields=1, label="Emitter Samples", value1=iDirectIlluminationEmitterSamples, 
        changeCommand=lambda (x): getIntFieldGroup(None, "iDirectIlluminationEmitterSamples", x))

    cmds.intFieldGrp(numberOfFields=1, label="BSDF Samples", value1=iDirectIlluminationBSDFSamples, 
        changeCommand=lambda (x): getIntFieldGroup(None, "iDirectIlluminationBSDFSamples", x))

    cmds.checkBox(label = "Strict Normals", value=iDirectIlluminationStrictNormals, 
        changeCommand=lambda (x): getCheckBox(None, "iDirectIlluminationStrictNormals", x))

    cmds.checkBox(label = "Hide Visible Emitters", value=iDirectIlluminationStrictNormals, 
        changeCommand=lambda (x): getCheckBox(None, "iDirectIlluminationStrictNormals", x))    

    cmds.setParent('..')

    return diSettings

def createIntegratorFramePathTracer():
    existingUseInfiniteDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iPathTracerUseInfiniteDepth"))
    existingMaxDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iPathTracerMaxDepth"))
    existingRRDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iPathTracerRRDepth"))
    existingStrictNormals = cmds.getAttr( "%s.%s" % (renderSettings, "iPathTracerStrictNormals"))
    existingHideEmitters = cmds.getAttr( "%s.%s" % (renderSettings, "iPathTracerHideEmitters"))

    pSettings = cmds.frameLayout(label="Path Tracer", cll=True)

    cmds.checkBox("Use Infinite Depth", value=existingUseInfiniteDepth, 
        changeCommand=lambda (x): getCheckBox(None, "iPathTracerUseInfiniteDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Max Depth", value1=existingMaxDepth, 
        changeCommand=lambda (x): getIntFieldGroup(None, "iPathTracerMaxDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Russian Roulette Depth", value1=existingRRDepth, 
        changeCommand=lambda (x): getIntFieldGroup(None, "iPathTracerRRDepth", x))

    cmds.checkBox(label = "Strict Normals", value=existingStrictNormals, 
        changeCommand=lambda (x): getCheckBox(None, "iPathTracerStrictNormals", x))

    cmds.checkBox(label = "Hide Visible Emitters", value=existingHideEmitters, 
        changeCommand=lambda (x): getCheckBox(None, "iPathTracerHideEmitters", x))    

    cmds.setParent('..')

    return pSettings

def createIntegratorFrameSimpleVolumetricPathTracer():
    existingUseInfiniteDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iSimpleVolumetricPathTracerUseInfiniteDepth"))
    existingMaxDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iSimpleVolumetricPathTracerMaxDepth"))
    existingRRDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iSimpleVolumetricPathTracerRRDepth"))
    existingStrictNormals = cmds.getAttr( "%s.%s" % (renderSettings, "iSimpleVolumetricPathTracerStrictNormals"))
    existingHideEmitters = cmds.getAttr( "%s.%s" % (renderSettings, "iSimpleVolumetricPathTracerHideEmitters"))

    vpsSettings = cmds.frameLayout(label="Simple Volumetric Path Tracer", cll=True, visible=False)

    cmds.checkBox("Use Infinite Depth", value=existingUseInfiniteDepth, 
        changeCommand=lambda (x): getCheckBox(None, "iSimpleVolumetricPathTracerUseInfiniteDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Max Depth", value1=existingMaxDepth, 
        changeCommand=lambda (x): getIntFieldGroup(None, "iSimpleVolumetricPathTracerMaxDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Russian Roulette Depth", value1=existingRRDepth, 
        changeCommand=lambda (x): getIntFieldGroup(None, "iSimpleVolumetricPathTracerRRDepth", x))

    cmds.checkBox(label = "Strict Normals", value=existingStrictNormals, 
        changeCommand=lambda (x): getCheckBox(None, "iSimpleVolumetricPathTracerStrictNormals", x))

    cmds.checkBox(label = "Hide Visible Emitters", value=existingHideEmitters, 
        changeCommand=lambda (x): getCheckBox(None, "iSimpleVolumetricPathTracerHideEmitters", x))    

    cmds.setParent('..')

    return vpsSettings

def createIntegratorFrameVolumetricPathTracer():
    existingUseInfiniteDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iVolumetricPathTracerUseInfiniteDepth"))
    existingMaxDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iVolumetricPathTracerMaxDepth"))
    existingRRDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iVolumetricPathTracerRRDepth"))
    existingStrictNormals = cmds.getAttr( "%s.%s" % (renderSettings, "iVolumetricPathTracerStrictNormals"))
    existingHideEmitters = cmds.getAttr( "%s.%s" % (renderSettings, "iVolumetricPathTracerHideEmitters"))

    vpSettings = cmds.frameLayout(label="Volumetric Path Tracer", cll=True, visible=False)

    cmds.checkBox("Use Infinite Depth", value=existingUseInfiniteDepth, 
        changeCommand=lambda (x): getCheckBox(None, "iVolumetricPathTracerUseInfiniteDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Max Depth", value1=existingMaxDepth, 
        changeCommand=lambda (x): getIntFieldGroup(None, "iVolumetricPathTracerMaxDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Russian Roulette Depth", value1=existingRRDepth, 
        changeCommand=lambda (x): getIntFieldGroup(None, "iVolumetricPathTracerRRDepth", x))

    cmds.checkBox(label = "Strict Normals", value=existingStrictNormals, 
        changeCommand=lambda (x): getCheckBox(None, "iVolumetricPathTracerStrictNormals", x))

    cmds.checkBox(label = "Hide Visible Emitters", value=existingHideEmitters, 
        changeCommand=lambda (x): getCheckBox(None, "iVolumetricPathTracerHideEmitters", x))    

    cmds.setParent('..')

    return vpSettings

def createIntegratorFrameBidirectionalPathTracer():
    existingUseInfiniteDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iBidrectionalPathTracerUseInfiniteDepth"))
    existingMaxDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iBidrectionalPathTracerMaxDepth"))
    existingRRDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iBidrectionalPathTracerRRDepth"))
    existingLightImage = cmds.getAttr( "%s.%s" % (renderSettings, "iBidrectionalPathTracerLightImage"))
    existingSampleDirect = cmds.getAttr( "%s.%s" % (renderSettings, "iBidrectionalPathTracerSampleDirect"))

    bdptSettings = cmds.frameLayout(label="Bidirectional Path Tracer", cll=True, visible=False)

    cmds.checkBox("Use Infinite Depth", value=existingUseInfiniteDepth,
        changeCommand=lambda (x): getCheckBox(None, "iBidrectionalPathTracerUseInfiniteDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Max Depth", value1=existingMaxDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iBidrectionalPathTracerMaxDepth", x))

    cmds.checkBox(label = "Use Light Images", value=existingLightImage,
        changeCommand=lambda (x): getCheckBox(None, "iBidrectionalPathTracerLightImage", x))  

    cmds.checkBox(label = "Enable direct sampling strategies", value=existingSampleDirect,
        changeCommand=lambda (x): getCheckBox(None, "iBidrectionalPathTracerSampleDirect", x))   

    cmds.intFieldGrp(numberOfFields=1, label="Russian Roulette Depth", value1=existingRRDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iBidrectionalPathTracerRRDepth", x))

    cmds.setParent('..')

    return bdptSettings

def createIntegratorFramePhotonMap():
    iPhotonMapDirectSamples = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapDirectSamples"))
    iPhotonMapGlossySamples = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapGlossySamples"))
    iPhotonMapUseInfiniteDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapUseInfiniteDepth"))
    iPhotonMapMaxDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapMaxDepth"))
    iPhotonMapGlobalPhotons = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapGlobalPhotons"))
    iPhotonMapCausticPhotons = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapCausticPhotons"))
    iPhotonMapVolumePhotons = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapVolumePhotons"))
    iPhotonMapGlobalLookupRadius = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapGlobalLookupRadius"))
    iPhotonMapCausticLookupRadius = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapCausticLookupRadius"))
    iPhotonMapLookupSize = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapLookupSize"))
    iPhotonMapGranularity = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapGranularity"))
    iPhotonMapHideEmitters = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapHideEmitters"))
    iPhotonMapRRDepth = cmds.getAttr( "%s.%s" % (renderSettings, "iPhotonMapRRDepth"))

    pmSettings = cmds.frameLayout(label="Photon Map", cll=True, visible=False)

    cmds.intFieldGrp(numberOfFields=1, label="Direct Samples", value1=iPhotonMapDirectSamples,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPhotonMapDirectSamples", x))

    cmds.intFieldGrp(numberOfFields=1, label="Glossy Samples", value1=iPhotonMapGlossySamples,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPhotonMapGlossySamples", x))

    cmds.checkBox(label = "Use Infinite Depth", value=iPhotonMapUseInfiniteDepth,
        changeCommand=lambda (x): getCheckBox(None, "iPhotonMapUseInfiniteDepth", x))   

    cmds.intFieldGrp(numberOfFields=1, label="Max Depth", value1=iPhotonMapMaxDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPhotonMapMaxDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Global Photons", value1=iPhotonMapGlobalPhotons,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPhotonMapGlobalPhotons", x))

    cmds.intFieldGrp(numberOfFields=1, label="Caustic Photons", value1=iPhotonMapCausticPhotons,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPhotonMapCausticPhotons", x))

    cmds.intFieldGrp(numberOfFields=1, label="Volume Photons", value1=iPhotonMapVolumePhotons,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPhotonMapVolumePhotons", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Global Lookup Radius", value1=iPhotonMapGlobalLookupRadius,
        changeCommand=lambda (x): getFloatFieldGroup(None, "iPhotonMapGlobalLookupRadius", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Caustic Lookup Radius", value1=iPhotonMapCausticLookupRadius,
        changeCommand=lambda (x): getFloatFieldGroup(None, "iPhotonMapCausticLookupRadius", x))

    cmds.intFieldGrp(numberOfFields=1, label="Lookup Size", value1=iPhotonMapLookupSize,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPhotonMapLookupSize", x))

    cmds.intFieldGrp(numberOfFields=1, label="Granularity", value1=iPhotonMapGranularity,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPhotonMapGranularity", x))

    cmds.checkBox(label = "Hide Emitters", value=iPhotonMapHideEmitters,
        changeCommand=lambda (x): getCheckBox(None, "iPhotonMapHideEmitters", x))   

    cmds.intFieldGrp(numberOfFields=1, label="Russian Roulette Depth", value1=iPhotonMapRRDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPhotonMapRRDepth", x))

    cmds.setParent('..')

    return pmSettings

def createIntegratorFrameProgressivePhotonMap():
    iProgressivePhotonMapUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iProgressivePhotonMapUseInfiniteDepth"))
    iProgressivePhotonMapMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iProgressivePhotonMapMaxDepth"))
    iProgressivePhotonMapPhotonCount = cmds.getAttr("%s.%s" % (renderSettings, "iProgressivePhotonMapPhotonCount"))
    iProgressivePhotonMapInitialRadius = cmds.getAttr("%s.%s" % (renderSettings, "iProgressivePhotonMapInitialRadius"))
    iProgressivePhotonMapAlpha = cmds.getAttr("%s.%s" % (renderSettings, "iProgressivePhotonMapAlpha"))
    iProgressivePhotonMapGranularity = cmds.getAttr("%s.%s" % (renderSettings, "iProgressivePhotonMapGranularity"))
    iProgressivePhotonMapRRDepth = cmds.getAttr("%s.%s" % (renderSettings, "iProgressivePhotonMapRRDepth"))
    iProgressivePhotonMapMaxPasses = cmds.getAttr("%s.%s" % (renderSettings, "iProgressivePhotonMapMaxPasses"))

    ppmSettings = cmds.frameLayout(label="Progressive Photon Map", cll=True, visible=False)

    cmds.checkBox(label = "Use Infinite Depth", value=iProgressivePhotonMapUseInfiniteDepth,
        changeCommand=lambda (x): getCheckBox(None, "iProgressivePhotonMapUseInfiniteDepth", x))   

    cmds.intFieldGrp(numberOfFields=1, label="Max Depth", value1=iProgressivePhotonMapMaxDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iProgressivePhotonMapMaxDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Photon Count", value1=iProgressivePhotonMapPhotonCount,
        changeCommand=lambda (x): getIntFieldGroup(None, "iProgressivePhotonMapPhotonCount", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Initial Radius", value1=iProgressivePhotonMapInitialRadius,
        changeCommand=lambda (x): getFloatFieldGroup(None, "iProgressivePhotonMapInitialRadius", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Alpha", value1=iProgressivePhotonMapAlpha,
        changeCommand=lambda (x): getFloatFieldGroup(None, "iProgressivePhotonMapAlpha", x))

    cmds.intFieldGrp(numberOfFields=1, label="Granularity", value1=iProgressivePhotonMapGranularity,
        changeCommand=lambda (x): getIntFieldGroup(None, "iProgressivePhotonMapGranularity", x))

    cmds.intFieldGrp(numberOfFields=1, label="Russian Roulette Depth", value1=iProgressivePhotonMapRRDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iProgressivePhotonMapRRDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Max Passes", value1=iProgressivePhotonMapMaxPasses,
        changeCommand=lambda (x): getIntFieldGroup(None, "iProgressivePhotonMapMaxPasses", x))

    cmds.setParent('..')

    return ppmSettings

def createIntegratorFrameStochasticProgressivePhotonMap():
    iStochasticProgressivePhotonMapUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iStochasticProgressivePhotonMapUseInfiniteDepth"))
    iStochasticProgressivePhotonMapMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iStochasticProgressivePhotonMapMaxDepth"))
    iStochasticProgressivePhotonMapPhotonCount = cmds.getAttr("%s.%s" % (renderSettings, "iStochasticProgressivePhotonMapPhotonCount"))
    iStochasticProgressivePhotonMapInitialRadius = cmds.getAttr("%s.%s" % (renderSettings, "iStochasticProgressivePhotonMapInitialRadius"))
    iStochasticProgressivePhotonMapAlpha = cmds.getAttr("%s.%s" % (renderSettings, "iStochasticProgressivePhotonMapAlpha"))
    iStochasticProgressivePhotonMapGranularity = cmds.getAttr("%s.%s" % (renderSettings, "iStochasticProgressivePhotonMapGranularity"))
    iStochasticProgressivePhotonMapRRDepth = cmds.getAttr("%s.%s" % (renderSettings, "iStochasticProgressivePhotonMapRRDepth"))
    iStochasticProgressivePhotonMapMaxPasses = cmds.getAttr("%s.%s" % (renderSettings, "iStochasticProgressivePhotonMapMaxPasses"))

    sppmSettings = cmds.frameLayout(label="Stochastic Progressive Photon Map", cll=True, visible=False)

    cmds.checkBox(label = "Use Infinite Depth", value=iStochasticProgressivePhotonMapUseInfiniteDepth,
        changeCommand=lambda (x): getCheckBox(None, "iStochasticProgressivePhotonMapUseInfiniteDepth", x))   

    cmds.intFieldGrp(numberOfFields=1, label="Max Depth", value1=iStochasticProgressivePhotonMapMaxDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iStochasticProgressivePhotonMapMaxDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Photon Count", value1=iStochasticProgressivePhotonMapPhotonCount,
        changeCommand=lambda (x): getIntFieldGroup(None, "iStochasticProgressivePhotonMapPhotonCount", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Initial Radius", value1=iStochasticProgressivePhotonMapInitialRadius,
        changeCommand=lambda (x): getFloatFieldGroup(None, "iStochasticProgressivePhotonMapInitialRadius", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Alpha", value1=iStochasticProgressivePhotonMapAlpha,
        changeCommand=lambda (x): getFloatFieldGroup(None, "iStochasticProgressivePhotonMapAlpha", x))

    cmds.intFieldGrp(numberOfFields=1, label="Granularity", value1=iStochasticProgressivePhotonMapGranularity,
        changeCommand=lambda (x): getIntFieldGroup(None, "iStochasticProgressivePhotonMapGranularity", x))

    cmds.intFieldGrp(numberOfFields=1, label="Russian Roulette Depth", value1=iStochasticProgressivePhotonMapRRDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iStochasticProgressivePhotonMapRRDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Max Passes", value1=iStochasticProgressivePhotonMapMaxPasses,
        changeCommand=lambda (x): getIntFieldGroup(None, "iStochasticProgressivePhotonMapMaxPasses", x))

    cmds.setParent('..')

    return sppmSettings

def createIntegratorFramePrimarySampleSpaceMetropolisLightTransport():
    iPrimarySampleSpaceMetropolisLightTransportBidirectional = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportBidirectional"))
    iPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth"))
    iPrimarySampleSpaceMetropolisLightTransportMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportMaxDepth"))
    iPrimarySampleSpaceMetropolisLightTransportDirectSamples = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportDirectSamples"))
    iPrimarySampleSpaceMetropolisLightTransportRRDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportRRDepth"))
    iPrimarySampleSpaceMetropolisLightTransportLuminanceSamples = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportLuminanceSamples"))
    iPrimarySampleSpaceMetropolisLightTransportTwoStage = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportTwoStage"))
    iPrimarySampleSpaceMetropolisLightTransportPLarge = cmds.getAttr("%s.%s" % (renderSettings, "iPrimarySampleSpaceMetropolisLightTransportPLarge"))

    pssmltSettings = cmds.frameLayout(label="Primary Sample Space Metropolis Light Transport", cll=True, visible=False)

    cmds.checkBox(label = "Bidirectional", value=iPrimarySampleSpaceMetropolisLightTransportBidirectional,
        changeCommand=lambda (x): getCheckBox(None, "iPrimarySampleSpaceMetropolisLightTransportBidirectional", x))   

    cmds.checkBox(label = "Use Infinite Depth", value=iPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth,
        changeCommand=lambda (x): getCheckBox(None, "iPrimarySampleSpaceMetropolisLightTransportUseInfiniteDepth", x))   

    cmds.intFieldGrp(numberOfFields=1, label="Max Depth", value1=iPrimarySampleSpaceMetropolisLightTransportMaxDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPrimarySampleSpaceMetropolisLightTransportMaxDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Direct Samples", value1=iPrimarySampleSpaceMetropolisLightTransportDirectSamples,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPrimarySampleSpaceMetropolisLightTransportDirectSamples", x))

    cmds.intFieldGrp(numberOfFields=1, label="Russian Roulette Depth", value1=iPrimarySampleSpaceMetropolisLightTransportRRDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPrimarySampleSpaceMetropolisLightTransportRRDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Luminance Samples", value1=iPrimarySampleSpaceMetropolisLightTransportLuminanceSamples,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPrimarySampleSpaceMetropolisLightTransportLuminanceSamples", x))

    cmds.checkBox(label = "Two Stage", value=iPrimarySampleSpaceMetropolisLightTransportTwoStage,
        changeCommand=lambda (x): getCheckBox(None, "iPrimarySampleSpaceMetropolisLightTransportTwoStage", x))   

    cmds.floatFieldGrp(numberOfFields=1, label="P Large", value1=iPrimarySampleSpaceMetropolisLightTransportPLarge,
        changeCommand=lambda (x): getFloatFieldGroup(None, "iPrimarySampleSpaceMetropolisLightTransportPLarge", x))

    cmds.setParent('..')

    return pssmltSettings

def createIntegratorFramePathSpaceMetropolisLightTransport():
    iPathSpaceMetropolisLightTransportUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportUseInfiniteDepth"))
    iPathSpaceMetropolisLightTransportMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportMaxDepth"))
    iPathSpaceMetropolisLightTransportDirectSamples = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportDirectSamples"))
    iPathSpaceMetropolisLightTransportLuminanceSamples = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportLuminanceSamples"))
    iPathSpaceMetropolisLightTransportTwoStage = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportTwoStage"))
    iPathSpaceMetropolisLightTransportBidirectionalMutation = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportBidirectionalMutation"))
    iPathSpaceMetropolisLightTransportLensPurturbation = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportLensPurturbation"))
    iPathSpaceMetropolisLightTransportMultiChainPurturbation = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportMultiChainPurturbation"))
    iPathSpaceMetropolisLightTransportCausticPurturbation = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportCausticPurturbation"))
    iPathSpaceMetropolisLightTransportManifoldPurturbation = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportManifoldPurturbation"))
    iPathSpaceMetropolisLightTransportLambda = cmds.getAttr("%s.%s" % (renderSettings, "iPathSpaceMetropolisLightTransportLambda"))

    mltSettings = cmds.frameLayout(label="Path Space Metropolis Light Transport", cll=True, visible=False)

    cmds.checkBox(label = "Use Infinite Depth", value=iPathSpaceMetropolisLightTransportUseInfiniteDepth,
        changeCommand=lambda (x): getCheckBox(None, "iPathSpaceMetropolisLightTransportUseInfiniteDepth", x))   

    cmds.intFieldGrp(numberOfFields=1, label="Max Depth", value1=iPathSpaceMetropolisLightTransportMaxDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPathSpaceMetropolisLightTransportMaxDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Direct Samples", value1=iPathSpaceMetropolisLightTransportDirectSamples,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPathSpaceMetropolisLightTransportDirectSamples", x))

    cmds.intFieldGrp(numberOfFields=1, label="Luminance Samples", value1=iPathSpaceMetropolisLightTransportLuminanceSamples,
        changeCommand=lambda (x): getIntFieldGroup(None, "iPathSpaceMetropolisLightTransportLuminanceSamples", x))

    cmds.checkBox(label = "Two Stage", value=iPathSpaceMetropolisLightTransportTwoStage,
        changeCommand=lambda (x): getCheckBox(None, "iPathSpaceMetropolisLightTransportTwoStage", x))   

    cmds.checkBox(label = "Bidirectional Mutation", value=iPathSpaceMetropolisLightTransportBidirectionalMutation,
        changeCommand=lambda (x): getCheckBox(None, "iPathSpaceMetropolisLightTransportBidirectionalMutation", x))   

    cmds.checkBox(label = "Lens Purturbation", value=iPathSpaceMetropolisLightTransportLensPurturbation,
        changeCommand=lambda (x): getCheckBox(None, "iPathSpaceMetropolisLightTransportLensPurturbation", x))   

    cmds.checkBox(label = "MultiChain Perturbation", value=iPathSpaceMetropolisLightTransportMultiChainPurturbation,
        changeCommand=lambda (x): getCheckBox(None, "iPathSpaceMetropolisLightTransportMultiChainPurturbation", x))   

    cmds.checkBox(label = "Caustic Perturbation", value=iPathSpaceMetropolisLightTransportCausticPurturbation,
        changeCommand=lambda (x): getCheckBox(None, "iPathSpaceMetropolisLightTransportCausticPurturbation", x))   

    cmds.checkBox(label = "Manifold Perturbation", value=iPathSpaceMetropolisLightTransportManifoldPurturbation,
        changeCommand=lambda (x): getCheckBox(None, "iPathSpaceMetropolisLightTransportManifoldPurturbation", x))   

    cmds.floatFieldGrp(numberOfFields=1, label="Lambda", value1=iPathSpaceMetropolisLightTransportLambda,
        changeCommand=lambda (x): getFloatFieldGroup(None, "iPathSpaceMetropolisLightTransportLambda", x))

    cmds.setParent('..')

    return mltSettings

def createIntegratorFrameEnergyRedistributionPathTracing():
    iEnergyRedistributionPathTracingUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingUseInfiniteDepth"))
    iEnergyRedistributionPathTracingMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingMaxDepth"))
    iEnergyRedistributionPathTracingNumChains = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingNumChains"))
    iEnergyRedistributionPathTracingMaxChains = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingMaxChains"))
    iEnergyRedistributionPathTracingChainLength = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingChainLength"))
    iEnergyRedistributionPathTracingDirectSamples = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingDirectSamples"))
    iEnergyRedistributionPathTracingLensPerturbation = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingLensPerturbation"))
    iEnergyRedistributionPathTracingMultiChainPerturbation = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingMultiChainPerturbation"))
    iEnergyRedistributionPathTracingCausticPerturbation = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingCausticPerturbation"))
    iEnergyRedistributionPathTracingManifoldPerturbation = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingManifoldPerturbation"))
    iEnergyRedistributionPathTracingLambda = cmds.getAttr("%s.%s" % (renderSettings, "iEnergyRedistributionPathTracingLambda"))

    erptSettings = cmds.frameLayout(label="Energy Redistribution Path Tracer", cll=True, visible=False)

    cmds.checkBox(label = "Use Infinite Depth", value=iEnergyRedistributionPathTracingUseInfiniteDepth,
        changeCommand=lambda (x): getCheckBox(None, "iEnergyRedistributionPathTracingUseInfiniteDepth", x))   

    cmds.intFieldGrp(numberOfFields=1, label="Max Depth", value1=iEnergyRedistributionPathTracingMaxDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iEnergyRedistributionPathTracingMaxDepth", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Num Chains", value1=iEnergyRedistributionPathTracingNumChains,
        changeCommand=lambda (x): getFloatFieldGroup(None, "iEnergyRedistributionPathTracingNumChains", x))

    cmds.intFieldGrp(numberOfFields=1, label="Max Chains", value1=iEnergyRedistributionPathTracingMaxChains,
        changeCommand=lambda (x): getIntFieldGroup(None, "iEnergyRedistributionPathTracingMaxChains", x))

    cmds.intFieldGrp(numberOfFields=1, label="Chain Length", value1=iEnergyRedistributionPathTracingChainLength,
        changeCommand=lambda (x): getIntFieldGroup(None, "iEnergyRedistributionPathTracingChainLength", x))

    cmds.intFieldGrp(numberOfFields=1, label="Direct Samples", value1=iEnergyRedistributionPathTracingDirectSamples,
        changeCommand=lambda (x): getIntFieldGroup(None, "iEnergyRedistributionPathTracingDirectSamples", x))

    cmds.checkBox(label = "Lens Perturbation", value=iEnergyRedistributionPathTracingLensPerturbation,
        changeCommand=lambda (x): getCheckBox(None, "iEnergyRedistributionPathTracingLensPerturbation", x))   

    cmds.checkBox(label = "MultiChain Perturbation", value=iEnergyRedistributionPathTracingMultiChainPerturbation,
        changeCommand=lambda (x): getCheckBox(None, "iEnergyRedistributionPathTracingMultiChainPerturbation", x))   

    cmds.checkBox(label = "Caustic Perturbation", value=iEnergyRedistributionPathTracingCausticPerturbation,
        changeCommand=lambda (x): getCheckBox(None, "iEnergyRedistributionPathTracingCausticPerturbation", x))   

    cmds.checkBox(label = "Manifold Perturbation", value=iEnergyRedistributionPathTracingManifoldPerturbation,
        changeCommand=lambda (x): getCheckBox(None, "iEnergyRedistributionPathTracingManifoldPerturbation", x))   

    cmds.floatFieldGrp(numberOfFields=1, label="Lambda", value1=iEnergyRedistributionPathTracingLambda,
        changeCommand=lambda (x): getFloatFieldGroup(None, "iEnergyRedistributionPathTracingLambda", x))

    cmds.setParent('..')

    return erptSettings

def createIntegratorFrameAdjointParticleTracer():
    iAdjointParticleTracerUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iAdjointParticleTracerUseInfiniteDepth"))
    iAdjointParticleTracerMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iAdjointParticleTracerMaxDepth"))
    iAdjointParticleTracerRRDepth = cmds.getAttr("%s.%s" % (renderSettings, "iAdjointParticleTracerRRDepth"))
    iAdjointParticleTracerGranularity = cmds.getAttr("%s.%s" % (renderSettings, "iAdjointParticleTracerGranularity"))
    iAdjointParticleTracerBruteForce = cmds.getAttr("%s.%s" % (renderSettings, "iAdjointParticleTracerBruteForce"))

    ptrSettings = cmds.frameLayout(label="Adjoint Particle Tracer", cll=True, visible=False)

    cmds.checkBox(label = "Use Infinite Depth", value=iAdjointParticleTracerUseInfiniteDepth,
        changeCommand=lambda (x): getCheckBox(None, "iAdjointParticleTracerUseInfiniteDepth", x))   

    cmds.intFieldGrp(numberOfFields=1, label="Max Depth", value1=iAdjointParticleTracerMaxDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iAdjointParticleTracerMaxDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Russian Roulette Depth", value1=iAdjointParticleTracerRRDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iAdjointParticleTracerRRDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Granularity", value1=iAdjointParticleTracerGranularity,
        changeCommand=lambda (x): getIntFieldGroup(None, "iAdjointParticleTracerGranularity", x))

    cmds.checkBox(label = "Brute Force", value=iAdjointParticleTracerBruteForce,
        changeCommand=lambda (x): getCheckBox(None, "iAdjointParticleTracerBruteForce", x))   

    cmds.setParent('..')

    return ptrSettings

def createIntegratorFrameVirtualPointLights():
    iVirtualPointLightUseInfiniteDepth = cmds.getAttr("%s.%s" % (renderSettings, "iVirtualPointLightUseInfiniteDepth"))
    iVirtualPointLightMaxDepth = cmds.getAttr("%s.%s" % (renderSettings, "iVirtualPointLightMaxDepth"))
    iVirtualPointLightShadowMapResolution = cmds.getAttr("%s.%s" % (renderSettings, "iVirtualPointLightShadowMapResolution"))
    iVirtualPointLightClamping = cmds.getAttr("%s.%s" % (renderSettings, "iVirtualPointLightClamping"))

    vplSettings = cmds.frameLayout(label="Virtual Point Lights", cll=True, visible=False)

    cmds.checkBox(label = "Use Infinite Depth", value=iVirtualPointLightUseInfiniteDepth,
        changeCommand=lambda (x): getCheckBox(None, "iVirtualPointLightUseInfiniteDepth", x))   

    cmds.intFieldGrp(numberOfFields=1, label="Max Depth", value1=iVirtualPointLightMaxDepth,
        changeCommand=lambda (x): getIntFieldGroup(None, "iVirtualPointLightMaxDepth", x))

    cmds.intFieldGrp(numberOfFields=1, label="Shadow Map Resolution", value1=iVirtualPointLightShadowMapResolution,
        changeCommand=lambda (x): getIntFieldGroup(None, "iVirtualPointLightShadowMapResolution", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Clamping", value1=iVirtualPointLightClamping,
        changeCommand=lambda (x): getFloatFieldGroup(None, "iVirtualPointLightClamping", x))

    cmds.setParent('..')

    return vplSettings

def createSensorFramePerspectiveRdist():
    sPerspectiveRdistKc2 = cmds.getAttr( "%s.%s" % (renderSettings, "sPerspectiveRdistKc2"))
    sPerspectiveRdistKc4 = cmds.getAttr( "%s.%s" % (renderSettings, "sPerspectiveRdistKc4"))

    sPerspectiveRdistSettings = cmds.frameLayout(label="Perspective Pinhole Camera with Radial Distortion", cll=True, visible=False)

    cmds.floatFieldGrp(numberOfFields=1, label="Radial Distortion - Coeff 2", value1=sPerspectiveRdistKc2,
        changeCommand=lambda (x): getFloatFieldGroup(None, "sPerspectiveRdistKc2", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Radial Distortion - Coeff 4", value1=sPerspectiveRdistKc2,
        changeCommand=lambda (x): getFloatFieldGroup(None, "sPerspectiveRdistKc4", x))

    cmds.setParent('..')

    return sPerspectiveRdistSettings

def createIntegratorFrames():
    #Make the integrator specific settings
    global integratorFrames

    integratorFrames = []

    # Ambient Occlusion Settings
    aoSettings = createIntegratorFrameAmbientOcclusion()

    # Direct Illumination Settings
    diSettings = createIntegratorFrameDirectIllumination()

    # Path Tracer settings
    pSettings = createIntegratorFramePathTracer()

    # Simple Volumetric Path Tracer settings
    vpsSettings = createIntegratorFrameSimpleVolumetricPathTracer()

    # Volumetric Path Tracer settings
    vpSettings = createIntegratorFrameVolumetricPathTracer()

    # Bidirection Path Tracer Settings
    bdptSettings = createIntegratorFrameBidirectionalPathTracer()

    # Photon Map Settings
    pmSettings = createIntegratorFramePhotonMap()

    # Progressive Photon Map Settings
    ppmSettings = createIntegratorFrameProgressivePhotonMap()

    # Stochastic Progressive Photon Map Settings
    sppmSettings = createIntegratorFrameStochasticProgressivePhotonMap()

    # Primary Sample Space Metropolis Light Transport Settings
    pssmltSettings = createIntegratorFramePrimarySampleSpaceMetropolisLightTransport()

    # Path Space Metropolis Light Transport Settings
    mltSettings = createIntegratorFramePathSpaceMetropolisLightTransport()

    # Energy Redistribution Path Tracing Settings
    erptSettings = createIntegratorFrameEnergyRedistributionPathTracing()

    # Adjoint Particle Tracer Settings
    ptrSettings = createIntegratorFrameAdjointParticleTracer()

    # Virtual Point Lights Settings
    vplSettings = createIntegratorFrameVirtualPointLights()

    integratorFrames.append(aoSettings)
    integratorFrames.append(diSettings)
    integratorFrames.append(pSettings)
    integratorFrames.append(vpsSettings)
    integratorFrames.append(vpSettings)
    integratorFrames.append(bdptSettings)
    integratorFrames.append(pmSettings)
    integratorFrames.append(ppmSettings)
    integratorFrames.append(sppmSettings)
    integratorFrames.append(pssmltSettings)
    integratorFrames.append(mltSettings)
    integratorFrames.append(erptSettings)
    integratorFrames.append(ptrSettings)
    integratorFrames.append(vplSettings)

def createMetaIntegratorFramesAdaptive():
    miAdaptiveMaxError = cmds.getAttr("%s.%s" % (renderSettings, "miAdaptiveMaxError"))
    miAdaptivePValue = cmds.getAttr("%s.%s" % (renderSettings, "miAdaptivePValue"))
    miAdaptiveMaxSampleFactor = cmds.getAttr("%s.%s" % (renderSettings, "miAdaptiveMaxSampleFactor"))

    adaptiveSettings = cmds.frameLayout(label="Adaptive", cll=True, visible=False)

    cmds.floatFieldGrp(numberOfFields=1, label="Max Error", value1=miAdaptiveMaxError,
        changeCommand=lambda (x): getFloatFieldGroup(None, "miAdaptiveMaxError", x))

    cmds.floatFieldGrp(numberOfFields=1, label="P Value", value1=miAdaptivePValue,
        changeCommand=lambda (x): getFloatFieldGroup(None, "miAdaptivePValue", x))

    cmds.intFieldGrp(numberOfFields=1, label="Max Sample Factor", value1=miAdaptiveMaxSampleFactor,
        changeCommand=lambda (x): getIntFieldGroup(None, "miAdaptiveMaxSampleFactor", x))

    cmds.setParent('..')

    return adaptiveSettings

def createMetaIntegratorFramesIrradianceCache():
    miIrradianceCacheResolution = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheResolution"))
    miIrradianceCacheQuality = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheQuality"))
    miIrradianceCacheGradients = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheGradients"))
    miIrradianceCacheClampNeighbor = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheClampNeighbor"))
    miIrradianceCacheClampScreen = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheClampScreen"))
    miIrradianceCacheOverture = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheOverture"))
    miIrradianceCacheQualityAdjustment = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheQualityAdjustment"))
    miIrradianceCacheIndirectOnly = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheIndirectOnly"))
    miIrradianceCacheDebug = cmds.getAttr("%s.%s" % (renderSettings, "miIrradianceCacheDebug"))

    irracheSettings = cmds.frameLayout(label="Irradiance Cache", cll=True, visible=False)

    cmds.intFieldGrp(numberOfFields=1, label="Resolution", value1=miIrradianceCacheResolution,
        changeCommand=lambda (x): getFloatFieldGroup(None, "miIrradianceCacheResolution", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Quality", value1=miIrradianceCacheQuality,
        changeCommand=lambda (x): getFloatFieldGroup(None, "miIrradianceCacheQuality", x))

    cmds.checkBox(label = "Gradients", value=miIrradianceCacheGradients,
        changeCommand=lambda (x): getCheckBox(None, "miIrradianceCacheGradients", x))   

    cmds.checkBox(label = "Clamp Neighbor", value=miIrradianceCacheClampNeighbor,
        changeCommand=lambda (x): getCheckBox(None, "miIrradianceCacheClampNeighbor", x))   

    cmds.checkBox(label = "Clamp Screen", value=miIrradianceCacheClampScreen,
        changeCommand=lambda (x): getCheckBox(None, "miIrradianceCacheClampScreen", x))   

    cmds.checkBox(label = "Overture", value=miIrradianceCacheOverture,
        changeCommand=lambda (x): getCheckBox(None, "miIrradianceCacheOverture", x))   

    cmds.floatFieldGrp(numberOfFields=1, label="Quality Adjustment", value1=miIrradianceCacheQualityAdjustment,
        changeCommand=lambda (x): getFloatFieldGroup(None, "miIrradianceCacheQualityAdjustment", x))

    cmds.checkBox(label = "Indirect Only", value=miIrradianceCacheIndirectOnly,
        changeCommand=lambda (x): getCheckBox(None, "miIrradianceCacheIndirectOnly", x))   

    cmds.checkBox(label = "Debug", value=miIrradianceCacheDebug,
        changeCommand=lambda (x): getCheckBox(None, "miIrradianceCacheDebug", x))   

    cmds.setParent('..')

    return irracheSettings


def createMetaIntegratorFrames():
    #Make the integrator specific settings
    global metaIntegratorFrames
    metaIntegratorFrames = []

    # Adaptive Settings
    adaptiveSettings = createMetaIntegratorFramesAdaptive()

    # Irradiance Cache Settings
    irracheSettings = createMetaIntegratorFramesIrradianceCache()

    metaIntegratorFrames.append(adaptiveSettings)
    metaIntegratorFrames.append(irracheSettings)

def changeMenu(menu, attribute, renderSettings, value):
    #selected = cmds.optionMenu(menu, query=True, value=True)
    cmds.setAttr("%s.%s" % (renderSettings, attribute), value, type="string")

def createFilmFramesHDR(renderSettings):
    global filmFrames

    fHDRFilmFileFormat = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmFileFormat"))
    fHDRFilmPixelFormat = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmPixelFormat"))
    fHDRFilmComponentFormat = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmComponentFormat"))
    fHDRFilmAttachLog = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmAttachLog"))
    fHDRFilmBanner = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmBanner"))
    fHDRFilmHighQualityEdges = cmds.getAttr("%s.%s" % (renderSettings, "fHDRFilmHighQualityEdges"))

    hdrSettings = cmds.frameLayout(label="HDR Film", cll=True)

    fileFormatMenu = cmds.optionMenu(label="File Format")
    cmds.optionMenu(fileFormatMenu, edit=True,
        changeCommand=lambda (x): changeMenu(fileFormatMenu, "fHDRFilmFileFormat", renderSettings, x))
    cmds.menuItem('OpenEXR (.exr)')
    cmds.menuItem('RGBE (.hdr)')
    cmds.menuItem('Portable Float Map (.pfm)')

    if fHDRFilmFileFormat not in ["", None]:
        cmds.optionMenu(fileFormatMenu, edit=True, value=fHDRFilmFileFormat)

    pixelFormatMenu = cmds.optionMenu(label="Pixel Format")
    cmds.optionMenu(pixelFormatMenu, edit=True,
        changeCommand=lambda (x): changeMenu(pixelFormatMenu, "fHDRFilmPixelFormat", renderSettings, x))
    cmds.menuItem('Luminance')
    cmds.menuItem('Luminance Alpha')
    cmds.menuItem('RGB')
    cmds.menuItem('RGBA')
    cmds.menuItem('XYZ')
    cmds.menuItem('XYZA')
    cmds.menuItem('Spectrum')
    cmds.menuItem('Spectrum Alpha')

    if fHDRFilmPixelFormat not in ["", None]:
        cmds.optionMenu(pixelFormatMenu, edit=True, value=fHDRFilmPixelFormat)

    componentFormatMenu = cmds.optionMenu(label="Component Format")
    cmds.optionMenu(componentFormatMenu, edit=True,
        changeCommand=lambda (x): changeMenu(componentFormatMenu, "fHDRFilmComponentFormat", renderSettings, x))
    cmds.menuItem('Float 16')
    cmds.menuItem('Float 32')
    cmds.menuItem('UInt 32')

    if fHDRFilmComponentFormat not in ["", None]:
        cmds.optionMenu(componentFormatMenu, edit=True, value=fHDRFilmComponentFormat)

    cmds.checkBox(label = "Attach Log", value=fHDRFilmAttachLog,
        changeCommand=lambda (x): getCheckBox(None, "fHDRFilmAttachLog", x))   

    cmds.checkBox(label = "Banner", value=fHDRFilmBanner,
        changeCommand=lambda (x): getCheckBox(None, "fHDRFilmBanner", x))   

    cmds.checkBox(label = "High Quality Edges", value=fHDRFilmHighQualityEdges,
        changeCommand=lambda (x): getCheckBox(None, "fHDRFilmHighQualityEdges", x))   

    cmds.setParent('..')

    return hdrSettings


def createFilmFramesHDRTiled(renderSettings):
    fTiledHDRFilmPixelFormat = cmds.getAttr("%s.%s" % (renderSettings, "fTiledHDRFilmPixelFormat"))
    fTiledHDRFilmComponentFormat = cmds.getAttr("%s.%s" % (renderSettings, "fTiledHDRFilmComponentFormat"))

    hdrTiledSettings = cmds.frameLayout(label="HDR Film - Tiled", cll=True)

    pixelFormatMenu = cmds.optionMenu(label="Pixel Format")
    cmds.optionMenu(pixelFormatMenu, edit=True,
        changeCommand=lambda (x): changeMenu(pixelFormatMenu, "fTiledHDRFilmPixelFormat", renderSettings, x))
    cmds.menuItem('Luminance')
    cmds.menuItem('Luminance Alpha')
    cmds.menuItem('RGB')
    cmds.menuItem('RGBA')
    cmds.menuItem('XYZ')
    cmds.menuItem('XYZA')
    cmds.menuItem('Spectrum')
    cmds.menuItem('Spectrum Alpha')

    if fTiledHDRFilmPixelFormat not in ["", None]:
        cmds.optionMenu(pixelFormatMenu, edit=True, value=fTiledHDRFilmPixelFormat)

    componentFormatMenu = cmds.optionMenu(label="Component Format")
    cmds.optionMenu(componentFormatMenu, edit=True,
        changeCommand=lambda (x): changeMenu(componentFormatMenu, "fTiledHDRFilmComponentFormat", renderSettings, x))
    cmds.menuItem('Float 16')
    cmds.menuItem('Float 32')
    cmds.menuItem('UInt 32')

    if fTiledHDRFilmComponentFormat not in ["", None]:
        cmds.optionMenu(componentFormatMenu, edit=True, value=fTiledHDRFilmComponentFormat)

    cmds.setParent('..')

    return hdrTiledSettings


def createFilmFramesLDR(renderSettings):
    fLDRFilmFileFormat = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmFileFormat"))
    fLDRFilmPixelFormat = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmPixelFormat"))
    fLDRFilmTonemapMethod = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmTonemapMethod"))
    fLDRFilmGamma = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmGamma"))
    fLDRFilmExposure = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmExposure"))
    fLDRFilmKey = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmKey"))
    fLDRFilmBurn = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmBurn"))
    fLDRFilmBanner = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmBanner"))
    fLDRFilmHighQualityEdges = cmds.getAttr("%s.%s" % (renderSettings, "fLDRFilmHighQualityEdges"))

    ldrSettings = cmds.frameLayout(label="LDR Film", cll=True)

    fileFormatMenu = cmds.optionMenu(label="File Format")
    cmds.optionMenu(fileFormatMenu, edit=True,
        changeCommand=lambda (x): changeMenu(fileFormatMenu, "fLDRFilmFileFormat", renderSettings, x))
    cmds.menuItem('PNG (.png)')
    cmds.menuItem('JPEG (.jpg)')

    if fLDRFilmFileFormat not in ["", None]:
        cmds.optionMenu(fileFormatMenu, edit=True, value=fLDRFilmFileFormat)

    pixelFormatMenu = cmds.optionMenu(label="Pixel Format")
    cmds.optionMenu(pixelFormatMenu, edit=True,
        changeCommand=lambda (x): changeMenu(pixelFormatMenu, "fLDRFilmPixelFormat", renderSettings, x))
    cmds.menuItem('Luminance')
    cmds.menuItem('Luminance Alpha')
    cmds.menuItem('RGB')
    cmds.menuItem('RGBA')

    if fLDRFilmPixelFormat not in ["", None]:
        cmds.optionMenu(pixelFormatMenu, edit=True, value=fLDRFilmPixelFormat)

    tonemapMethodMenu = cmds.optionMenu(label="Tonemap Method")
    cmds.optionMenu(tonemapMethodMenu, edit=True,
        changeCommand=lambda (x): changeMenu(tonemapMethodMenu, "fLDRFilmTonemapMethod", renderSettings, x))
    cmds.menuItem('Gamma')
    cmds.menuItem('Reinhard')

    if fLDRFilmTonemapMethod not in ["", None]:
        cmds.optionMenu(tonemapMethodMenu, edit=True, value=fLDRFilmTonemapMethod)

    cmds.floatFieldGrp(numberOfFields=1, label="Gamma", value1=fLDRFilmGamma,
        changeCommand=lambda (x): getFloatFieldGroup(None, "fLDRFilmGamma", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Exposure", value1=fLDRFilmExposure,
        changeCommand=lambda (x): getFloatFieldGroup(None, "fLDRFilmExposure", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Key", value1=fLDRFilmKey,
        changeCommand=lambda (x): getFloatFieldGroup(None, "fLDRFilmKey", x))

    cmds.floatFieldGrp(numberOfFields=1, label="Burn", value1=fLDRFilmBurn,
        changeCommand=lambda (x): getFloatFieldGroup(None, "fLDRFilmBurn", x))

    cmds.checkBox(label = "Banner", value=fLDRFilmBanner,
        changeCommand=lambda (x): getCheckBox(None, "fLDRFilmBanner", x))   

    cmds.checkBox(label = "High Quality Edges", value=fLDRFilmHighQualityEdges,
        changeCommand=lambda (x): getCheckBox(None, "fLDRFilmHighQualityEdges", x))   

    cmds.setParent('..')

    return ldrSettings

def createFilmFramesMath(renderSettings):
    fMathFilmFileFormat = cmds.getAttr("%s.%s" % (renderSettings, "fMathFilmFileFormat"))
    fMathFilmPixelFormat = cmds.getAttr("%s.%s" % (renderSettings, "fMathFilmPixelFormat"))
    fMathFilmDigits = cmds.getAttr("%s.%s" % (renderSettings, "fMathFilmDigits"))
    fMathFilmVariable = cmds.getAttr("%s.%s" % (renderSettings, "fMathFilmVariable"))
    fMathFilmHighQualityEdges = cmds.getAttr("%s.%s" % (renderSettings, "fMathFilmHighQualityEdges"))

    mathSettings = cmds.frameLayout(label="Math Film", cll=True)

    fileFormatMenu = cmds.optionMenu(label="File Format")
    cmds.optionMenu(fileFormatMenu, edit=True,
        changeCommand=lambda (x): changeMenu(fileFormatMenu, "fMathFilmFileFormat", renderSettings, x))
    cmds.menuItem('Matlab (.m)')
    cmds.menuItem('Mathematica (.m)')
    cmds.menuItem('NumPy (.npy)')

    if fMathFilmFileFormat not in ["", None]:
        cmds.optionMenu(fileFormatMenu, edit=True, value=fMathFilmFileFormat)

    pixelFormatMenu = cmds.optionMenu(label="Pixel Format")
    cmds.optionMenu(pixelFormatMenu, edit=True,
        changeCommand=lambda (x): changeMenu(pixelFormatMenu, "fMathFilmPixelFormat", renderSettings, x))
    cmds.menuItem('Luminance')
    cmds.menuItem('Luminance Alpha')
    cmds.menuItem('RGB')
    cmds.menuItem('RGBA')
    cmds.menuItem('Spectrum')
    cmds.menuItem('Spectrum Alpha')

    if fMathFilmPixelFormat not in ["", None]:
        cmds.optionMenu(pixelFormatMenu, edit=True, value=fMathFilmPixelFormat)

    cmds.intFieldGrp(numberOfFields=1, label="Digits", value1=fMathFilmDigits,
        changeCommand=lambda (x): getIntFieldGroup(None, "fMathFilmDigits", x))

    cmds.textFieldGrp(label="Variable", text=fMathFilmVariable,
        changeCommand=lambda (x): getTextFieldGroup(None, "fMathFilmVariable", x))

    cmds.checkBox(label = "High Quality Edges", value=fMathFilmHighQualityEdges,
        changeCommand=lambda (x): getCheckBox(None, "fMathFilmHighQualityEdges", x))   

    cmds.setParent('..')

    return mathSettings

def createFilmFrames(renderSettings):
    global filmFrames
    filmFrames = []

    # HDR Settings
    hdrSettings = createFilmFramesHDR(renderSettings)

    # HDR Tiled Settings
    hdrTiledSettings = createFilmFramesHDRTiled(renderSettings)

    # LDR Settings
    ldrSettings = createFilmFramesLDR(renderSettings)

    # Math Settings
    mathSettings = createFilmFramesMath(renderSettings)

    filmFrames.append(hdrSettings)
    filmFrames.append(hdrTiledSettings)
    filmFrames.append(ldrSettings)
    filmFrames.append(mathSettings)


def createSamplerFrames():
    global samplerFrames

    samplerFrames = []

    existingSampleCount = cmds.getAttr( "%s.%s" % (renderSettings, "sampleCount"))
    existingSamplerDimension = cmds.getAttr( "%s.%s" % (renderSettings, "samplerDimension"))
    existingSamplerScramble = cmds.getAttr( "%s.%s" % (renderSettings, "samplerScramble"))

    changeSampleCount = lambda (x): getIntFieldGroup(None, "sampleCount", x)
    changeSamplerDimension = lambda (x): getIntFieldGroup(None, "samplerDimension", x)
    changeSamplerScramble = lambda (x): getIntFieldGroup(None, "samplerScramble", x)

    indSettings = cmds.frameLayout(label="Independent Sampler", cll=False, visible=True)
    cmds.setParent('..')

    stratSettings = cmds.frameLayout(label="Stratified Sampler", cll=True, visible=False)
    stratSamplerDimension = cmds.intFieldGrp(numberOfFields=1, label="dimension", value1=existingSamplerDimension)
    cmds.intFieldGrp(stratSamplerDimension, edit=1, changeCommand=changeSamplerDimension)    
    cmds.setParent('..')

    ldSettings = cmds.frameLayout(label="Low Discrepancy Sampler", cll=True, visible=False)
    ldSamplerDimension = cmds.intFieldGrp(numberOfFields=1, label="dimension", value1=existingSamplerDimension)
    cmds.intFieldGrp(ldSamplerDimension, edit=1, changeCommand=changeSamplerDimension)    
    cmds.setParent('..')

    halSettings = cmds.frameLayout(label="Halton QMC Sampler", cll=True, visible=False)
    halSamplerScramble = cmds.intFieldGrp(numberOfFields=1, label="scramble", value1=existingSamplerScramble)
    cmds.intFieldGrp(halSamplerScramble, edit=1, changeCommand=changeSamplerScramble)    
    cmds.setParent('..')

    hamSettings = cmds.frameLayout(label="Hammersley QMC Sampler", cll=True, visible=False)
    hamSamplerScramble = cmds.intFieldGrp(numberOfFields=1, label="scramble", value1=existingSamplerScramble)
    cmds.intFieldGrp(hamSamplerScramble, edit=1, changeCommand=changeSamplerScramble)    
    cmds.setParent('..')

    sobSettings = cmds.frameLayout(label="Sobol QMC Sampler", cll=True, visible=False)
    sobSamplerScramble = cmds.intFieldGrp(numberOfFields=1, label="scramble", value1=existingSamplerScramble)
    cmds.intFieldGrp(sobSamplerScramble, edit=1, changeCommand=changeSamplerScramble)    
    cmds.setParent('..')

    samplerFrames.append(indSettings)
    samplerFrames.append(stratSettings)
    samplerFrames.append(ldSettings)
    samplerFrames.append(halSettings)
    samplerFrames.append(hamSettings)
    samplerFrames.append(sobSettings)

def createSensorOverrideFrames():
    global sensorOverrideFrames
    sensorOverrideFrames = []

    perspectiveRdistSettings = createSensorFramePerspectiveRdist()

    sensorOverrideFrames.append(perspectiveRdistSettings)

def getRenderSettingsPath(name, renderSettingsAttribute=None):
    global renderSettings

    path = cmds.fileDialog2(fileMode=1, fileFilter="*")
    if path not in [None, []]:
        strPath = str(path[0])
        cmds.textFieldButtonGrp(name, e=1, text=strPath)
        if renderSettingsAttribute:
            cmds.setAttr("%s.%s" % (renderSettings, renderSettingsAttribute), strPath, type="string")

def getCheckBox(name, renderSettingsAttribute=None, value=None):
    global renderSettings

    if renderSettingsAttribute:
        attr = "%s.%s" % (renderSettings, renderSettingsAttribute)
        cmds.setAttr(attr, value)

def getIntFieldGroup(name, renderSettingsAttribute=None, value=None):
    global renderSettings

    if renderSettingsAttribute:
        attr = "%s.%s" % (renderSettings, renderSettingsAttribute)
        cmds.setAttr(attr, value)

def getFloatFieldGroup(name, renderSettingsAttribute=None, value=None):
    global renderSettings

    if renderSettingsAttribute:
        attr = "%s.%s" % (renderSettings, renderSettingsAttribute)
        cmds.setAttr(attr, value)

def getTextFieldGroup(name, renderSettingsAttribute=None, value=None):
    global renderSettings

    if renderSettingsAttribute:
        attr = "%s.%s" % (renderSettings, renderSettingsAttribute)
        cmds.setAttr(attr, value, type="string")

def getOptionMenu(name, renderSettingsAttribute=None, value=None):
    global renderSettings

    if renderSettingsAttribute:
        attr = "%s.%s" % (renderSettings, renderSettingsAttribute)
        cmds.setAttr(attr, value, type="string")

'''
This function creates the render settings window.
This includes the integrator, sample generator, image filter,
and film type.
'''
def createRenderSettingsUI():
    global renderSettings
    renderSettings = getRenderSettingsNode()

    global renderSettingsWindow
    global integrator
    global integratorMenu
    global sampler
    global samplerMenu
    global rfilter
    global rfilterMenu
    global sensorOverrideMenu

    print( "\n\n\nMitsuba Render Settings - Create UI - Python\n\n\n" )

    parentForm = cmds.setParent(query=True)

    mitsubaGlobalsScrollLayout = cmds.scrollLayout(horizontalScrollBarThickness=0)
    cmds.columnLayout(adjustableColumn=True)

    # Path to executable
    mitsubaPathGroup = cmds.textFieldButtonGrp(label="Mitsuba Path", 
        buttonLabel="Open", buttonCommand="browseFiles")
    # Get default
    existingMitsubaPath = cmds.getAttr( "%s.%s" % (renderSettings, "mitsubaPath"))
    if existingMitsubaPath not in ["", None]:
        cmds.textFieldButtonGrp(mitsubaPathGroup, e=1, text=existingMitsubaPath)
    cmds.textFieldButtonGrp(mitsubaPathGroup, e=1, 
        buttonCommand=lambda: getRenderSettingsPath(mitsubaPathGroup, "mitsubaPath"))

    # Path to executable
    oiiotoolPathGroup = cmds.textFieldButtonGrp(label="oiiotool Path", 
        buttonLabel="Open", buttonCommand="browseFiles")
    # Get default
    existingOIIOToolPath = cmds.getAttr( "%s.%s" % (renderSettings, "oiiotoolPath"))
    if existingOIIOToolPath not in ["", None]:
        cmds.textFieldButtonGrp(oiiotoolPathGroup, e=1, text=existingOIIOToolPath)
    cmds.textFieldButtonGrp(oiiotoolPathGroup, e=1, 
        buttonCommand=lambda: getRenderSettingsPath(oiiotoolPathGroup, "oiiotoolPath"))

    # Integrator controls
    cmds.frameLayout(label='Integrator', collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True)

    #Create integrator selection drop down menu
    existingIntegrator = cmds.getAttr( "%s.%s" % (renderSettings, "integrator"))
    #print( "Existing Integrator : %s" % existingIntegrator)

    integratorMenu = cmds.optionMenu(changeCommand=changeIntegrator)
    cmds.menuItem('Ambient Occlusion')
    cmds.menuItem('Direct Illumination')
    cmds.menuItem('Path Tracer')
    cmds.menuItem('Volumetric Path Tracer')
    cmds.menuItem('Simple Volumetric Path Tracer')
    cmds.menuItem('Bidirectional Path Tracer')
    cmds.menuItem('Photon Map')
    cmds.menuItem('Progressive Photon Map')
    cmds.menuItem('Stochastic Progressive Photon Map')
    cmds.menuItem('Primary Sample Space Metropolis Light Transport')
    cmds.menuItem('Path Space Metropolis Light Transport')
    cmds.menuItem('Energy Redistribution Path Tracer')
    cmds.menuItem('Adjoint Particle Tracer')
    cmds.menuItem('Virtual Point Lights')

    createIntegratorFrames()
    if existingIntegrator not in ["", None]:
        cmds.optionMenu(integratorMenu, edit=True, value=existingIntegrator)
        integrator = existingIntegrator
    else:
        cmds.optionMenu(integratorMenu, edit=True, select=3)
        integrator = "Path Tracer"

    changeIntegrator(integrator)

    cmds.setParent('..')
    cmds.setParent('..')

    # Meta Integrator controls
    cmds.frameLayout(label='Meta Integrator', collapsable=True, collapse=True)
    cmds.columnLayout(adjustableColumn=True)

    existingMetaIntegrator = cmds.getAttr( "%s.%s" % (renderSettings, "metaIntegrator"))

    metaIntegratorMenu = cmds.optionMenu(label="Meta Integrator", changeCommand=changeMetaIntegrator)
    cmds.menuItem('None')
    cmds.menuItem('Adaptive')
    cmds.menuItem('Irradiance Cache')

    createMetaIntegratorFrames()

    if existingMetaIntegrator not in ["", None]:
        cmds.optionMenu(metaIntegratorMenu, edit=True, value=existingMetaIntegrator)
    else:
        cmds.optionMenu(integratorMenu, edit=True, select=0)
        existingMetaIntegrator = "None"

    changeMetaIntegrator(existingMetaIntegrator)

    cmds.setParent('..')
    cmds.setParent('..')

    # Sampler controls
    cmds.frameLayout(label='Sampler', collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True)

    existingSampler = cmds.getAttr( "%s.%s" % (renderSettings, "sampler"))
    #print( "Existing Sampler : %s" % existingSampler)

    samplerMenu = cmds.optionMenu(label="Image Sampler", changeCommand=changeSampler)
    cmds.menuItem('Independent Sampler')
    cmds.menuItem('Stratified Sampler')
    cmds.menuItem('Low Discrepancy Sampler')
    cmds.menuItem('Halton QMC Sampler')
    cmds.menuItem('Hammersley QMC Sampler')
    cmds.menuItem('Sobol QMC Sampler')

    createSamplerFrames()
    if existingSampler not in ["", None]:
        cmds.optionMenu(samplerMenu, edit=True, value=existingSampler)
        sampler = existingSampler
    else:
        cmds.optionMenu(samplerMenu, edit=True, select=1)
        sampler = "Independent Sampler"

    changeSampler(sampler)

    existingSampleCount = cmds.getAttr( "%s.%s" % (renderSettings, "sampleCount"))
    changeSampleCount = lambda (x): getIntFieldGroup(None, "sampleCount", x)
    sampleCountGroup = cmds.intFieldGrp(numberOfFields=1, label="sampleCount", value1=existingSampleCount)
    cmds.intFieldGrp(sampleCountGroup, edit=1, changeCommand=changeSampleCount)    

    cmds.setParent('..')
    cmds.setParent('..')

    # Film controls
    cmds.frameLayout(label='Film', collapsable=True, collapse=True)
    cmds.columnLayout(adjustableColumn=True)

    existingFilm = cmds.getAttr( "%s.%s" % (renderSettings, "film"))

    filmMenu = cmds.optionMenu(label="Film", changeCommand=changeFilm)
    cmds.menuItem('HDR Film')
    cmds.menuItem('HDR Film - Tiled')
    cmds.menuItem('Math Film')
    cmds.menuItem('LDR Film')

    createFilmFrames(renderSettings)

    if existingFilm not in ["", None]:
        cmds.optionMenu(filmMenu, edit=True, value=existingFilm)
    else:
        cmds.optionMenu(filmMenu, edit=True, select=0)
        existingFilm = "HDR Film"

    changeFilm(existingFilm)

    #cmds.separator(style="none", height=10)

    cmds.setParent('..')
    cmds.setParent('..')

    # Reconstruction Filter controls
    cmds.frameLayout(label='Reconstruction Filter', collapsable=True, collapse=True)
    cmds.columnLayout(adjustableColumn=True)

    existingReconstructionFilter = cmds.getAttr( "%s.%s" % (renderSettings, "reconstructionFilter"))
    #print( "Existing Reconstruction Filter : %s" % existingReconstructionFilter)

    rfilterMenu = cmds.optionMenu(label="Film Reconstruction Filter", 
        changeCommand=lambda (x): getOptionMenu(None, "reconstructionFilter", x))
    cmds.menuItem("Box filter")
    cmds.menuItem("Tent filter")
    cmds.menuItem("Gaussian filter")
    cmds.menuItem("Mitchell-Netravali filter")
    cmds.menuItem("Catmull-Rom filter")
    cmds.menuItem("Lanczos filter")

    if existingReconstructionFilter not in ["", None]:
        cmds.optionMenu(rfilterMenu, edit=True, value=existingReconstructionFilter)
        rfilter = existingReconstructionFilter
    else:
        cmds.optionMenu(rfilterMenu, edit=True, select=1)
        rfilter = "Box filter"

    cmds.setParent('..')
    cmds.setParent('..')

    # Camera / Sensor controls
    cmds.frameLayout(label='Camera / Sensor', collapsable=True, collapse=True)
    cmds.columnLayout(adjustableColumn=True)

    existingSensorOverride = cmds.getAttr( "%s.%s" % (renderSettings, "sensorOverride"))

    sensorOverrideMenu = cmds.optionMenu(label="Sensor Override", changeCommand=changeSensorOverride)
    cmds.menuItem('None')
    cmds.menuItem('Telecentric')
    cmds.menuItem('Spherical')
    #cmds.menuItem('Irradiance Meter')
    cmds.menuItem('Radiance Meter')
    cmds.menuItem('Fluence Meter')
    cmds.menuItem('Perspective Pinhole Camera with Radial Distortion')

    createSensorOverrideFrames()

    if existingSensorOverride not in ["None", None]:
        cmds.optionMenu(sensorOverrideMenu, edit=True, value=existingSensorOverride)
        sensorOverride = existingSensorOverride
    else:
        cmds.optionMenu(sensorOverrideMenu, edit=True, select=1)
        sensorOverride = "None"

    changeSensorOverride(sensorOverride)

    cmds.setParent('..')
    cmds.setParent('..')

    # Multichannel controls
    cmds.frameLayout(label='Multichannel', collapsable=True, collapse=True)
    cmds.columnLayout(adjustableColumn=True)

    multichannel = cmds.getAttr( "%s.%s" % (renderSettings, "multichannel"))
    cmds.checkBox(label="Multichannel Rendering", value=multichannel,
        changeCommand=lambda (x): getCheckBox(None, "multichannel", x))

    multichannelPosition = cmds.getAttr( "%s.%s" % (renderSettings, "multichannelPosition"))
    cmds.checkBox(label="Position", value=multichannelPosition,
        changeCommand=lambda (x): getCheckBox(None, "multichannelPosition", x))

    multichannelRelPosition = cmds.getAttr( "%s.%s" % (renderSettings, "multichannelRelPosition"))
    cmds.checkBox(label="Relative Position", value=multichannelRelPosition,
        changeCommand=lambda (x): getCheckBox(None, "multichannelRelPosition", x))

    multichannelDistance = cmds.getAttr( "%s.%s" % (renderSettings, "multichannelDistance"))
    cmds.checkBox(label="Distance", value=multichannelDistance,
        changeCommand=lambda (x): getCheckBox(None, "multichannelDistance", x))

    multichannelGeoNormal = cmds.getAttr( "%s.%s" % (renderSettings, "multichannelGeoNormal"))
    cmds.checkBox(label="Geometric Normal", value=multichannelGeoNormal,
        changeCommand=lambda (x): getCheckBox(None, "multichannelGeoNormal", x))

    multichannelShadingNormal = cmds.getAttr( "%s.%s" % (renderSettings, "multichannelShadingNormal"))
    cmds.checkBox(label="Shading Normal", value=multichannelShadingNormal,
        changeCommand=lambda (x): getCheckBox(None, "multichannelShadingNormal", x))

    multichannelUV = cmds.getAttr( "%s.%s" % (renderSettings, "multichannelUV"))
    cmds.checkBox(label="UV", value=multichannelUV,
        changeCommand=lambda (x): getCheckBox(None, "multichannelUV", x))

    multichannelAlbedo = cmds.getAttr( "%s.%s" % (renderSettings, "multichannelAlbedo"))
    cmds.checkBox(label="Albedo", value=multichannelAlbedo,
        changeCommand=lambda (x): getCheckBox(None, "multichannelAlbedo", x))

    multichannelShapeIndex = cmds.getAttr( "%s.%s" % (renderSettings, "multichannelShapeIndex"))
    cmds.checkBox(label="Shape Index", value=multichannelShapeIndex,
        changeCommand=lambda (x): getCheckBox(None, "multichannelShapeIndex", x))

    multichannelPrimIndex = cmds.getAttr( "%s.%s" % (renderSettings, "multichannelPrimIndex"))
    cmds.checkBox(label="Primitive Index", value=multichannelPrimIndex,
        changeCommand=lambda (x): getCheckBox(None, "multichannelPrimIndex", x))

    cmds.setParent('..')
    cmds.setParent('..')

    # Overall controls
    cmds.frameLayout(label='Overall', collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True)

    existingKeepTempFiles = cmds.getAttr( "%s.%s" % (renderSettings, "keepTempFiles"))
    keepTempFiles = cmds.checkBox(label="keepTempFiles", value=existingKeepTempFiles)
    cmds.checkBox(keepTempFiles, edit=1,
        changeCommand=lambda (x): getCheckBox(keepTempFiles, "keepTempFiles", x))

    existingVerbose = cmds.getAttr( "%s.%s" % (renderSettings, "verbose"))
    verbose = cmds.checkBox(label="verbose", value=existingVerbose)
    cmds.checkBox(verbose, edit=1,
        changeCommand=lambda (x): getCheckBox(verbose, "verbose", x))

    existingWritePartialResults = cmds.getAttr( "%s.%s" % (renderSettings, "writePartialResults"))
    writePartialResults = cmds.checkBox(label="Write partial results", value=existingWritePartialResults)
    cmds.checkBox(writePartialResults, edit=1,
        changeCommand=lambda (x): getCheckBox(writePartialResults, "writePartialResults", x))

    existingWritePartialResultsInterval = cmds.getAttr( "%s.%s" % (renderSettings, "writePartialResultsInterval"))
    changeWritePartialResultsInterval = lambda (x): getIntFieldGroup(None, "writePartialResultsInterval", x)
    writePartialResultsIntervalGroup = cmds.intFieldGrp(numberOfFields=1, label="Partial results interval", value1=existingWritePartialResultsInterval)
    cmds.intFieldGrp(writePartialResultsIntervalGroup, edit=1, changeCommand=changeWritePartialResultsInterval)    

    existingThreads = cmds.getAttr( "%s.%s" % (renderSettings, "threads"))
    changeThreads = lambda (x): getIntFieldGroup(None, "threads", x)
    threadsGroup = cmds.intFieldGrp(numberOfFields=1, label="Threads", value1=existingThreads)
    cmds.intFieldGrp(threadsGroup, edit=1, changeCommand=changeThreads)    

    existingBlockSize = cmds.getAttr( "%s.%s" % (renderSettings, "blockSize"))
    changeBlockSize = lambda (x): getIntFieldGroup(None, "blockSize", x)
    blockSizeGroup = cmds.intFieldGrp(numberOfFields=1, label="Block size", value1=existingBlockSize)
    cmds.intFieldGrp(blockSizeGroup, edit=1, changeCommand=changeBlockSize)    

    cmds.setParent('..')
    cmds.setParent('..')


    af = []
    af.append((mitsubaGlobalsScrollLayout, 'top', 0))
    af.append((mitsubaGlobalsScrollLayout, 'bottom', 0))
    af.append((mitsubaGlobalsScrollLayout, 'left', 0))
    af.append((mitsubaGlobalsScrollLayout, 'right', 0))
    cmds.formLayout(parentForm, edit=True, attachForm=af)


def createRenderSettings():
    createRenderSettingsNode()
    createRenderSettingsUI()

def createRenderWindow():
    global renderWindow
    global renderedImage

    renderWindow = cmds.window("Mitsuba Rendered Image", retain=True, resizeToFitChildren=True)
    cmds.paneLayout()
    renderedImage = cmds.image()

#Make the render settings window visible
def showRenderSettings(self):
    global renderSettingsWindow

    cmds.showWindow(renderSettingsWindow)

def getRenderWindowPanel():
    renderPanels = cmds.getPanel(scriptType="renderWindowPanel")

    if renderPanels == []: 
        renderPanel = cmds.scriptedPanel(type="renderWindowPanel", unParent=True) 
        #cmds.scriptedPanel(e=True, label=`interToUI $renderPanel` $renderPanel; 
    else: 
        renderPanel = renderPanels[0] 

    return renderPanel

def showRender(fileName):
    renderWindowName = getRenderWindowPanel()
    cmds.renderWindowEditor(renderWindowName, edit=True, loadImage=fileName)

#Make the render window visible
def showRenderWindow(filename):
    global renderWindow

    imageWidth = cmds.getAttr("defaultResolution.width")
    imageHeight = cmds.getAttr("defaultResolution.height")
    cmds.window(renderWindow, edit=True, widthHeight=(imageWidth, imageHeight))
    cmds.showWindow(renderWindow)
    cmds.renderWindowEditor()

#Mel command to render with Mitsuba
def callMitsuba(self):
    cmds.mitsuba()

'''
Since we have a number of integrators that each have a number of properties,
we need to have a number of GUI widgets.  However we only want to show
the settings for the active integrator
'''
def changeIntegrator(selectedIntegrator):
    global integratorMenu
    global integratorFrames
    global integrator

    print( "selectedIntegrator : %s" % selectedIntegrator )

    #Query the integrator drop down menu to find the active integrator
    #selectedIntegrator = cmds.optionMenu(integratorMenu, query=True, value=True)

    #Set all other integrator frameLayout to be invisible
    for frame in integratorFrames:
        currentIntegrator = cmds.frameLayout(frame, query=True, label=True).replace("_", " ")
        if currentIntegrator == selectedIntegrator:
            cmds.frameLayout(frame, edit=True, visible=True)
        else:
            cmds.frameLayout(frame, edit=True, visible=False) 

    integrator = selectedIntegrator
    getOptionMenu(None, "integrator", selectedIntegrator)

def changeSampler(selectedSampler):
    global samplerMenu
    global samplerFrames
    global sample

    #print( "selectedSampler : %s" % selectedSampler )

    #Query the sampler drop down menu to find the active sampler
    selectedSampler = cmds.optionMenu(samplerMenu, query=True, value=True)
    #Set all other sampler frameLayout to be invisible
    for frame in samplerFrames:
        currentSampler = cmds.frameLayout(frame, query=True, label=True)
        currentSamplerUnderscore = currentSampler.replace(" ", "_")
        if currentSampler == selectedSampler or currentSamplerUnderscore == selectedSampler:
            cmds.frameLayout(frame, edit=True, visible=True)
        else:
            cmds.frameLayout(frame, edit=True, visible=False)

    sampler = selectedSampler
    getOptionMenu(None, "sampler", selectedSampler)

def changeSensorOverride(selectedSensorOverride):
    global sensorOverrideFrames

    #Set all other sensorOverride frameLayouts to be invisible
    for frame in sensorOverrideFrames:
        currentSensorOverride = cmds.frameLayout(frame, query=True, label=True)
        if currentSensorOverride == selectedSensorOverride:
            cmds.frameLayout(frame, edit=True, visible=True)
        else:
            cmds.frameLayout(frame, edit=True, visible=False)

    getOptionMenu(None, "sensorOverride", selectedSensorOverride)

def changeFilm(selectedFilm):
    global filmFrames

    #Set all other film frameLayouts to be invisible
    for frame in filmFrames:
        currentFilmFrame = cmds.frameLayout(frame, query=True, label=True)
        if currentFilmFrame == selectedFilm:
            cmds.frameLayout(frame, edit=True, visible=True)
        else:
            cmds.frameLayout(frame, edit=True, visible=False)

    getOptionMenu(None, "film", selectedFilm)

def changeMetaIntegrator(selectedMetaIntegrator):
    global metaIntegratorFrames

    #Set all other sensorOverride frameLayouts to be invisible
    for frame in metaIntegratorFrames:
        currentMetaIntegrator = cmds.frameLayout(frame, query=True, label=True)
        if currentMetaIntegrator == selectedMetaIntegrator:
            cmds.frameLayout(frame, edit=True, visible=True)
        else:
            cmds.frameLayout(frame, edit=True, visible=False)

    getOptionMenu(None, "metaIntegrator", selectedMetaIntegrator)




